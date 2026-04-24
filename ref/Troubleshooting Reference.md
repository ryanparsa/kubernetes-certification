# Kubernetes Troubleshooting Reference

Structured checklists and commands for diagnosing the most common cluster problems:
kubelet failures, pod crashes, node issues, static pods, etcd, event logging, and
certificate expiry.

---

## 1. Kubelet Failure Checklist

### Symptoms
- Node shows `NotReady`
- Pods stuck in `Pending` or never get assigned to the node
- `kubectl get nodes` shows the node with `STATUS=NotReady`

### Diagnosis steps

```bash
# 1. Check kubelet service status
systemctl status kubelet
journalctl -u kubelet -n 100 --no-pager

# 2. Check if kubelet is running at all
ps aux | grep kubelet

# 3. Common config file locations
cat /var/lib/kubelet/config.yaml          # kubelet runtime config
cat /etc/kubernetes/kubelet.conf          # kubeconfig kubelet uses to reach API server
cat /var/lib/kubelet/kubeadm-flags.env    # extra CLI flags from kubeadm

# 4. Check for typos in config files
kubelet --config /var/lib/kubelet/config.yaml --dry-run  # not available; parse errors shown on start

# 5. Reload and restart
systemctl daemon-reload
systemctl restart kubelet
systemctl enable kubelet      # ensure it starts on reboot

# 6. Verify after restart
systemctl status kubelet      # should show Active: active (running)
kubectl get node <node>       # should return to Ready
```

### Common kubelet failure causes

| Symptom in logs | Likely cause |
|---|---|
| `failed to run Kubelet: invalid kubeconfig` | Corrupted or wrong `kubelet.conf` path |
| `connection refused` to API server | API server not running, or wrong `--server` URL |
| `x509: certificate has expired` | Kubelet client cert expired — renew with `kubeadm certs renew all` |
| `no such file or directory` for config | Config path in `kubeadm-flags.env` is wrong |
| `failed to create containerd task` | Container runtime issue — check containerd/docker status |
| `node not found` | Node was deleted from API while kubelet was down — re-join the node |

---

## 2. Pod Crash-Loop Debugging

### Symptoms
- `CrashLoopBackOff`, `Error`, `OOMKilled`, `RunContainerError`

### Diagnosis steps

```bash
# 1. Get pod status and events
kubectl describe pod <pod> -n <ns>
# Look at: State, Last State, Exit Code, Restart Count, Events

# 2. Get current logs
kubectl logs <pod> -n <ns>

# 3. Get logs from the previous (crashed) container
kubectl logs <pod> -n <ns> --previous

# 4. For multi-container pods, specify container
kubectl logs <pod> -n <ns> -c <container>

# 5. Exec into a running container for live debugging
kubectl exec -it <pod> -n <ns> -- sh

# 6. If the image has no shell, use an ephemeral debug container
kubectl debug -it <pod> -n <ns> \
  --image=busybox:1.35 \
  --target=<main-container>

# 7. Check resource pressure (OOMKilled)
kubectl describe node <node> | grep -A 5 "Conditions:"
kubectl top pod <pod> -n <ns>
```

### Exit code reference

| Exit code | Meaning |
|---|---|
| 0 | Exited cleanly (expected) |
| 1 | Application error |
| 137 | OOMKilled (exit 128 + signal 9) |
| 139 | Segmentation fault (signal 11) |
| 143 | Graceful termination (SIGTERM, signal 15) |
| 255 | Entry point not found or exec error |

---

## 3. Node NotReady Diagnosis

```bash
# 1. Describe the node (look at Conditions and Events)
kubectl describe node <node>

# 2. Node Conditions to check
# Ready: False/Unknown → kubelet not reporting
# MemoryPressure: True → node is low on memory
# DiskPressure: True → node is low on disk
# PIDPressure: True → node has too many processes
# NetworkUnavailable: True → CNI plugin not configured

# 3. SSH to the node
ssh <node>

# 4. Check kubelet (see section 1)
systemctl status kubelet

# 5. Check container runtime
systemctl status containerd
crictl info

# 6. Check disk space (DiskPressure)
df -h
du -sh /var/lib/containerd/*

# 7. Check memory (MemoryPressure)
free -h
cat /proc/meminfo

# 8. Check CNI plugin (NetworkUnavailable)
ls /etc/cni/net.d/
ls /opt/cni/bin/
# CNI plugin pod (e.g. kindnet/flannel) must be Running on the node
kubectl -n kube-system get pods -o wide | grep <node>
```

---

## 4. Static Pod Debugging

Static pods are managed by kubelet directly from manifests in
`/etc/kubernetes/manifests/`. They don't appear as normal pod objects.

```bash
# List static pod manifests
ls /etc/kubernetes/manifests/
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

# Edit a static pod (kubelet auto-restarts it within seconds)
vim /etc/kubernetes/manifests/kube-apiserver.yaml

# Temporarily disable a static pod (move it out of the watched dir)
mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/

# Re-enable
mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/

# Watch kubelet pick up the change
journalctl -u kubelet -f

# Static pod logs (find the pod name first — it includes the node name)
kubectl -n kube-system get pod
kubectl -n kube-system logs kube-apiserver-<node>

# If API server is down, check logs directly
crictl ps -a | grep apiserver
crictl logs <container-id>
```

### Common static pod problems

| Problem | Check |
|---|---|
| API server not starting | Wrong `--etcd-servers` URL, bad cert path, port conflict |
| etcd not starting | Wrong data dir, corrupted data directory |
| Scheduler/controller not starting | Wrong kubeconfig path (`--kubeconfig` flag) |
| Static pod keeps restarting | Check manifest syntax; `kubelet` logs for errors |

---

## 5. etcd Health Check

```bash
# Find etcd pod and its certificates
kubectl -n kube-system describe pod etcd-<node>
# Look for: --cert-file, --key-file, --trusted-ca-file, --listen-client-urls

# Run etcdctl inside the etcd pod
kubectl -n kube-system exec -it etcd-<node> -- sh

# Inside etcd pod (or with ETCDCTL_API=3 set):
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# Output when healthy:
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.3ms

# Check cluster membership (HA clusters)
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  member list

# Quick backup
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/etcd-backup.db

# Verify backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table
```

---

## 6. Cluster Event Logging

```bash
# All events in a namespace (sorted by time)
kubectl get events -n <ns> --sort-by='.lastTimestamp'

# All events cluster-wide
kubectl get events -A --sort-by='.lastTimestamp'

# Watch events live
kubectl get events -n <ns> -w

# Only Warning events
kubectl get events -n <ns> --field-selector type=Warning

# Events for a specific object
kubectl get events -n <ns> \
  --field-selector involvedObject.name=<pod-name>

# Events for a specific kind (Pod, Node, etc.)
kubectl get events -A \
  --field-selector involvedObject.kind=Node

# Get reason from events
kubectl get events -n <ns> -o json | \
  jq '.items[] | {name:.involvedObject.name, reason:.reason, message:.message}'
```

### API server audit log

```bash
# Audit log location (if audit policy is configured)
# Check kube-apiserver.yaml for --audit-log-path
grep audit /etc/kubernetes/manifests/kube-apiserver.yaml

tail -f /var/log/kubernetes/audit.log | jq .
```

---

## 7. Checking Control Plane Component Health

```bash
# Check how components are running (static pods vs systemd services)
kubectl -n kube-system get pods | grep -E 'apiserver|scheduler|controller|etcd'

# For kubeadm clusters — all are static pods
# Check their logs
kubectl -n kube-system logs kube-apiserver-<node>
kubectl -n kube-system logs kube-scheduler-<node>
kubectl -n kube-system logs kube-controller-manager-<node>
kubectl -n kube-system logs etcd-<node>

# Component status (deprecated but still works for quick check)
kubectl get componentstatuses

# Check API server health endpoints
curl -k https://localhost:6443/healthz
curl -k https://localhost:6443/readyz
curl -k https://localhost:6443/livez
```

---

## 8. Certificate Expiry Checks

```bash
# Check all certificate expiry at once (kubeadm clusters)
kubeadm certs check-expiration

# Output example:
# CERTIFICATE                EXPIRES                  RESIDUAL TIME   ...
# admin.conf                 Dec 23, 2025 16:21 UTC   364d            ...
# apiserver                  Dec 23, 2025 16:21 UTC   364d            ...
# etcd-ca                    Dec 21, 2033 16:21 UTC   9y              ...

# Renew all certificates
kubeadm certs renew all

# After renewal, restart static pods (they embed the certs)
# Move manifests out and back in:
cd /etc/kubernetes/manifests
mv kube-apiserver.yaml /tmp/
mv kube-controller-manager.yaml /tmp/
mv kube-scheduler.yaml /tmp/

# Wait for pods to stop
watch crictl ps

# Move back
mv /tmp/kube-apiserver.yaml .
mv /tmp/kube-controller-manager.yaml .
mv /tmp/kube-scheduler.yaml .

# Update local kubeconfig
cp /etc/kubernetes/admin.conf ~/.kube/config

# Check kubelet client cert (auto-rotated — just verify it's current)
ls -la /var/lib/kubelet/pki/
# kubelet-client-current.pem should point to a recent dated file
openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem \
  -noout -dates

# Inspect any certificate
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | \
  grep -E 'Subject:|Not After|DNS:|IP Address'
```

---

## 9. Common Troubleshooting Commands

```bash
# Find all non-Running pods cluster-wide
kubectl get pods -A --field-selector 'status.phase!=Running'

# Find pods with high restart counts
kubectl get pods -A | awk '$5 > 5'   # 5th column is RESTARTS

# Describe any resource to see events
kubectl describe <resource> <name> -n <ns>

# Check available resources on all nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Tail kubelet logs in real time
journalctl -u kubelet -f

# Check container runtime status
systemctl status containerd
crictl ps -a
crictl logs <container-id>

# List images on a node
crictl images

# Remove unused images
crictl rmi --prune
```

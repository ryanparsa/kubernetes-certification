# Kubernetes Commands Reference

[← Back to index](../README.md)

---

## Part 3: kubelet

The node agent. Runs on every node (control plane and workers). Not managed by the API server
— it is a systemd service that **manages** pods on the node.

---

### 3.1 — What kubelet Does

- Watches API server for `Pod` objects assigned to this node (`spec.nodeName` set)
- Also watches the `staticPodPath` directory for static pod manifests (used by control plane)
- Calls the CRI (containerd via `/run/containerd/containerd.sock`) to create/start/stop containers
- Reports pod and node status back to the API server
- Serves health and metrics endpoints on port 10250 (TLS, requires authn/authz)
- Manages volume mounts, secret injection, projected service account tokens
- Runs liveness, readiness, and startup probes
- Manages certificate rotation: client cert (CSR API), server cert (`serverTLSBootstrap`)

---

### 3.2 — Configuration

kubelet is configured via a `KubeletConfiguration` file (flags are deprecated):

```
/var/lib/kubelet/config.yaml          # KubeletConfiguration object
/var/lib/kubelet/kubeadm-flags.env    # remaining CLI flags set by kubeadm
```

**Key `KubeletConfiguration` fields:**

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDNS:
  - 10.96.0.10                        # CoreDNS ClusterIP
clusterDomain: cluster.local
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
staticPodPath: /etc/kubernetes/manifests   # control plane nodes only
authentication:
  anonymous:
    enabled: false                    # must be false (security hardening)
  webhook:
    enabled: true                     # delegates authn to API server
authorization:
  mode: Webhook                       # delegates authz to API server (Node authorizer)
serverTLSBootstrap: true             # kubelet requests its own serving cert via CSR
rotateCertificates: true             # automatically rotates client cert before expiry
evictionHard:
  memory.available: "100Mi"          # evict pods when node has < 100Mi free memory
  nodefs.available: "10%"            # evict when node disk < 10%
  imagefs.available: "15%"
cpuManagerPolicy: static             # CPU pinning for Guaranteed QoS pods
topologyManagerPolicy: none
cgroupDriver: systemd                # must match containerd cgroupDriver
```

---

### 3.3 — Key Endpoints

| Endpoint                  | Purpose                                              |
|---------------------------|------------------------------------------------------|
| `:10250/healthz`          | kubelet health (requires valid client cert)          |
| `:10250/pods`             | JSON list of all pods on this node                   |
| `:10250/stats/summary`    | CPU/memory resource usage stats                      |
| `:10250/logs/<logfile>`   | read node log files                                  |
| `:10248/healthz`          | local-only health check (no TLS, no auth)            |

The `:10248` endpoint is used by `kubeadm` preflight to check kubelet is running.

---

### 3.4 — Systemd Unit and Debugging

```bash
systemctl status kubelet               # show current state, last log lines
systemctl start kubelet
systemctl stop kubelet
systemctl restart kubelet
systemctl daemon-reload                # reload unit files after editing service file

journalctl -u kubelet -f               # follow kubelet logs (most useful debug source)
journalctl -u kubelet --since "5 min ago"
journalctl -u kubelet -n 100           # last 100 lines
```

**Common kubelet failure modes:**

| Symptom                        | Likely cause                                              |
|--------------------------------|-----------------------------------------------------------|
| kubelet fails to start         | wrong cgroupDriver (must match containerd)                |
| Pod stuck in `ContainerCreating`| CRI socket path wrong; containerd not running            |
| Node shows `NotReady`          | kubelet not running, or can't reach API server            |
| `Failed to pull image`         | imagePullPolicy, registry auth, or network issue          |
| `Evicted` pods                 | eviction thresholds hit — check `kubectl describe node`   |

---

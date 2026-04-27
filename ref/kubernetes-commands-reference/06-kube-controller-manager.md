# Kubernetes Commands Reference — Part 6: kube-controller-manager

> Part of [Kubernetes Commands Reference](../Kubernetes Commands Reference.md)


Runs all built-in Kubernetes control loops in a single process. Each controller watches
resources via the API server and reconciles actual state toward desired state.

---

### 6.1 — What It Does

Key controllers included:

| Controller                      | Responsibility                                                   |
|---------------------------------|------------------------------------------------------------------|
| Node controller                 | marks nodes `NotReady`, evicts pods when node unreachable        |
| Deployment controller           | creates/updates ReplicaSets to match desired spec                |
| ReplicaSet controller           | creates/deletes pods to match replica count                      |
| StatefulSet controller          | manages ordered pod creation and persistent volumes              |
| Job controller                  | creates pods for batch Jobs, tracks completions/failures         |
| CronJob controller              | creates Jobs on a schedule                                       |
| ServiceAccount controller       | creates default ServiceAccount + token for new namespaces        |
| Namespace controller            | handles namespace deletion (processes finalizers)                |
| EndpointSlice controller        | keeps EndpointSlices in sync with pod IP addresses               |
| CertificateSigningRequest ctrl  | auto-approves kubelet bootstrap CSRs                             |
| Token controller                | signs ServiceAccount JWT tokens using `sa.key`                   |
| PersistentVolume controller     | binds PVCs to PVs; provisions dynamic PVs via StorageClass       |

---

### 6.2 — Run Mode

Static pod: `/etc/kubernetes/manifests/kube-controller-manager.yaml`

---

### 6.3 — Key Flags

```
--kubeconfig=/etc/kubernetes/controller-manager.conf
--service-account-private-key-file=/etc/kubernetes/pki/sa.key    # signs SA JWT tokens
--root-ca-file=/etc/kubernetes/pki/ca.crt
--cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt           # signs kubelet CSRs
--cluster-signing-key-file=/etc/kubernetes/pki/ca.key
--leader-elect=true
--profiling=false                                                  # CKS: disable
--node-monitor-grace-period=40s        # time before node marked Unreachable
--node-monitor-period=5s               # how often node status is checked
--pod-eviction-timeout=5m0s            # time after Unreachable before pods are evicted
--controllers=*,bootstrapsigner,tokencleaner   # * = all built-in + named extras
--use-service-account-credentials=true         # each controller uses its own SA token
```

**Identity:** CN = `system:kube-controller-manager`.
Maps to built-in `system:kube-controller-manager` ClusterRole.

**What breaks:**
- Wrong `sa.key` path → ServiceAccount tokens cannot be signed → pods using SAs get auth errors
- Controller-manager not running → Deployments/ReplicaSets not reconciled → pods not created
- `--cluster-signing-*` wrong → kubelet bootstrap CSRs not signed → worker nodes cannot join

---


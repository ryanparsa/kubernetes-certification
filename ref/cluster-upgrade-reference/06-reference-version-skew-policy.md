# Kubernetes Cluster Upgrade Reference — 6. Reference — Version Skew Policy

> Part of [Kubernetes Cluster Upgrade Reference](../Cluster Upgrade Reference.md)


| Component | Allowed skew from API server version |
|---|---|
| kubelet | Up to 3 minor versions behind API server |
| kubectl | ±1 minor version from API server |
| kube-controller-manager, kube-scheduler | Must not be newer than API server |
| kubeadm | Same minor version as the target Kubernetes version |

> **Rule of thumb:** upgrade the control-plane first, then workers. Never run a worker
> kubelet on a *newer* version than the API server.

---


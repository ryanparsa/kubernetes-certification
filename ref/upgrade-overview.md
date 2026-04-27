# Upgrade Overview

Kubernetes supports upgrading **one minor version at a time** (e.g. 1.29 → 1.30).
Skipping minor versions is not supported.

```
1. Upgrade kubeadm on the control-plane node
2. Run kubeadm upgrade plan   → review what will change
3. Run kubeadm upgrade apply  → upgrade control-plane components
4. Upgrade kubelet + kubectl on the control-plane node
5. Repeat steps 1, 3–4 on each additional control-plane node (HA clusters)
6. For each worker node: drain → upgrade kubeadm/kubelet/kubectl → uncordon
```

---


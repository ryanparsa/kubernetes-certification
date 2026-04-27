# Kubernetes Cluster Upgrade Reference

[← Back to index](../README.md)

---

## 2. Pre-flight Checks

```bash
# Check current versions
kubectl version --short
kubeadm version
kubelet --version

# Verify all nodes are Ready before starting
kubectl get nodes

# Confirm which version you can upgrade to
apt-cache madison kubeadm          # Debian/Ubuntu
yum list --showduplicates kubeadm  # RHEL/CentOS
```

---

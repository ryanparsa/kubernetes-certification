# Useful Commands

```bash
# List available kubeadm versions (Debian/Ubuntu)
apt-cache madison kubeadm | head -20

# Hold all Kubernetes packages (prevent accidental upgrades)
apt-mark hold kubeadm kubelet kubectl

# Unhold before intentional upgrade
apt-mark unhold kubeadm kubelet kubectl

# Check kubelet service status after upgrade
systemctl status kubelet

# Watch all nodes come back Ready after upgrade
kubectl get nodes -w
```

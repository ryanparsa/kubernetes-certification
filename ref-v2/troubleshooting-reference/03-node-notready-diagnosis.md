# Kubernetes Troubleshooting Reference

[← Back to index](../README.md)

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

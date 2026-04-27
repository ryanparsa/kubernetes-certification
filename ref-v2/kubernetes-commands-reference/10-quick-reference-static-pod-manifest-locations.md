# Kubernetes Commands Reference

[← Back to index](../README.md)

---

## Quick Reference: Static Pod Manifest Locations

All control plane components run as static pods on control plane nodes:

```
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml
/etc/kubernetes/manifests/etcd.yaml
```

Editing any of these files triggers kubelet to automatically restart the pod.
kubelet watches the directory specified in `staticPodPath` (default `/etc/kubernetes/manifests`).

---

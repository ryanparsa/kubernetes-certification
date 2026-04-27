# Question 8

> **Solve this question on:** the "cka-lab-8" kind cluster

Your coworker notified you that node `cka-lab-8-worker` is running an older Kubernetes version and is not even part of the cluster yet.

1. Update the node's Kubernetes to the exact version of the controlplane
2. Add the node to the cluster using kubeadm

> ⚠️ **Kind limitation:** In this local kind lab both nodes already run the same Kubernetes version and the worker is already joined. You can still practise generating a join token (`kubeadm token create --print-join-command`) and exploring the kubeadm upgrade workflow.

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

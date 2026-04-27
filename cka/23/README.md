# Question 6

> **Solve this question on:** the "cka-lab-23" kind cluster

There seems to be an issue with the kubelet on controlplane node `cka-lab-23-control-plane`, it's not running.

Fix the kubelet and confirm that the node is available in `Ready` state.

Create a *Pod* called `success` in `default` *Namespace* of image `nginx:1-alpine`.

> [!NOTE]
> The node has no taints and can schedule *Pods* without additional tolerations

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

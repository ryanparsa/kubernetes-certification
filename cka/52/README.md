# Question 52

> **Solve this question on:** `cka-lab-52`

Create a deployment named `app-scheduling` with `3` replicas using the `nginx` image in the `scheduling` namespace that must only run on node `k3d-cluster-agent-1` using node affinity (not node selector).

Requirements:

- Use `requiredDuringSchedulingIgnoredDuringExecution`
- Match the node by its hostname
- Label the target node with `disk=ssd` before creating the deployment

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 71

> **Solve this question on:** `cka-lab-71`

Ensure a single instance of an `nginx` pod is running on **every node** of the cluster.

Create a *DaemonSet* named `nginx-ds` using the `nginx` image that:

- Does **not** override any existing taints on nodes.
- Runs a pod on every schedulable node.

Verify that the DaemonSet pods are distributed across all nodes.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

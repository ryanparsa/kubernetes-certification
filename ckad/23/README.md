# Question 23

> **Solve this question on:** `ckad-lab-23`

The operations team has reported performance degradation in the cluster.

Pod `logging-pod` in namespace `troubleshooting` is consuming excessive CPU resources, affecting other workloads in the cluster.

Your task is to:

1. Identify which container within the pod is causing the high CPU usage

2. Configure appropriate CPU limits of `100m` and memory limits of `50Mi` for that container to prevent resource abuse while ensuring the application can still function

3. Implement your solution by modifying the pod specification with the necessary resource constraints

Ensure that the pod continues to run successfully after your changes, but with its CPU usage kept within reasonable bounds as defined by the limits you set.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

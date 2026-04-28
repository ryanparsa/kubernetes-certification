# Question 38

> **Solve this question on:** `ckad-lab-38`

Create a Pod named `multi-container-pod` in the `multi-container` namespace with two containers:

1. Container 1 — Name: `main-container`, Image: `nginx`
2. Container 2 — Name: `sidecar-container`, Image: `busybox`, Command: `['sh', '-c', 'while true; do echo $(date) >> /var/log/app.log; sleep 5; done']`

Create a shared volume named `log-volume` that both containers can access. Mount this volume at `/var/log` in both containers.

Ensure the namespace exists before creating the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

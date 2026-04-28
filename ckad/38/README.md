# Question 38

> **Solve this question on:** the "ckad-lab-38" *Kind* cluster

Create a *Pod* named `multi-container-pod` in the `multi-container` *Namespace* with two *Containers*:

1. *Container* 1 — Name: `main-container`, Image: `nginx`
2. *Container* 2 — Name: `sidecar-container`, Image: `busybox`, Command: `['sh', '-c', 'while true; do echo $(date) >> /var/log/app.log; sleep 5; done']`

Create a shared *Volume* named `log-volume` that both *Containers* can access. Mount this *Volume* at `/var/log` in both *Containers*.

Ensure the *Namespace* exists before creating the *Pod*.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

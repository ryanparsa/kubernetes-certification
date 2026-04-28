# Question 21

> **Solve this question on:** `ckad-lab-21`

The DevOps team needs a specialized pod to help with monitoring and logging.

Create a multi-container pod named `sidecar-pod` in the `troubleshooting` namespace with the following specifications:

1. Main container:
   - Image: `nginx`
   - Container name: `nginx`
   - Purpose: Serve web content

2. Sidecar container:
   - Image: `busybox`
   - Container name: `sidecar`
   - Command: `["sh", "-c", "while true; do date >> /var/my-log/date.log; sleep 10; done"]`

3. Shared volume configuration:
   - Volume name: `log-volume`
   - Mount path: `/var/my-log` in both containers

This demonstrates the sidecar container pattern for extending application functionality.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

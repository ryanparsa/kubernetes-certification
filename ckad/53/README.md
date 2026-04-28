# Question 53

> **Solve this question on:** `ckad-lab-53`

Create a Pod named `lifecycle-pod` in the `pod-lifecycle` namespace with the following specifications:

1. Use image `nginx`
2. Add a postStart hook that creates a file `/usr/share/nginx/html/welcome.txt` with content `Welcome to the pod!`
3. Add a preStop hook that waits for `10` seconds
4. Set termination grace period to `30` seconds

Ensure the namespace exists before creating the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

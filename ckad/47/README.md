# Question 47

> **Solve this question on:** `ckad-lab-47`

Create a Pod named `secure-app` in the `security` namespace with the following security configurations:

1. Run as non-root user (UID: `1000`)
2. Set security context to drop all capabilities
3. Set `readOnlyRootFilesystem` to `true`
4. Add a security context to the container to run as non-root
5. Use the `nginx:alpine` image

Ensure the namespace exists before creating the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

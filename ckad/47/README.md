# Question 47

> **Solve this question on:** the "ckad-lab-47" *Kind* cluster

Create a *Pod* named `secure-app` in the `security` *Namespace* with the following security configurations:

1. Run as non-root user (UID: `1000`)
2. Set security context to drop all capabilities
3. Set `readOnlyRootFilesystem` to `true`
4. Add a security context to the *Container* to run as non-root
5. Use the `nginx:alpine` image
6. The container should run the command `sleep 3600`

Ensure the *Namespace* exists before creating the *Pod*.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

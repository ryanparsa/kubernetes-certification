# Question 80

> **Solve this question on:** `ckad-lab-80`

Create a namespace `backend`.

Create a multi-container Pod named `app-stack` in namespace `backend` with the following containers:

- **Init container** named `init-db` using image `busybox` that runs: `sleep 2`
- **Main container** named `app` using image `nginx:1.25`
- **Sidecar container** named `cache` using image `redis:7`

All containers must have a CPU request of `50m` and a memory request of `64Mi`.

The Pod must only move to `Running` after the init container completes successfully.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

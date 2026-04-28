# Question 74

> **Solve this question on:** `ckad-lab-74`

1. Create a *Pod* named `secured` that uses the image `nginx` for a single container.

2. Mount an `emptyDir` volume to the directory `/data/app` inside the container.

3. Set a *security context* on the **Pod** so that all files created on the volume use filesystem group ID `3000`.

4. Shell into the running container, create a file named `logs.txt` in `/data/app`, and confirm that the file is owned by group `3000`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

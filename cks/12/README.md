# Question 12

> **Solve this question on:** `cks-lab-12`

Create a Secret named `db-creds` in the `secrets-management` namespace with the following data:
- username: `admin`
- password: `SecretP@ssw0rd`

Deploy a pod named `secure-app` that mounts this secret as files at `/etc/db-creds`.

Additionally, deploy a second pod named `env-app` that exposes the secret data as environment variables with names `DB_USER` and `DB_PASS`.

Both pods should use the `busybox` image and run the command `sleep 3600`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

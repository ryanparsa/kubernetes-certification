# Question 81

> **Solve this question on:** `ckad-lab-81`

Create a namespace `config-test`.

1. Create a ConfigMap named `app-config` in namespace `config-test` with the following key-value pairs:
   - `DATABASE_HOST=postgres.default.svc.cluster.local`
   - `DATABASE_PORT=5432`
   - `LOG_LEVEL=debug`

2. Create a Pod named `config-pod` in namespace `config-test` using image `alpine` with command `sleep 3600`. Inject **all** keys from the ConfigMap as environment variables into the container using `envFrom`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

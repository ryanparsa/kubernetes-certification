# Question 56

> **Solve this question on:** `ckad-lab-56`

Create a Pod named `config-pod` in the `pod-configuration` namespace with the following specifications:

1. Use image `nginx`
2. Add direct environment variables: `APP_ENV=production`, `DEBUG=false`
3. Add environment variables from ConfigMap `app-config` with keys `DB_HOST` and `DB_PORT`
4. Mount ConfigMap `app-config` as a volume at `/etc/app-config`
5. Add environment variables from Secret `app-secret` with keys `API_KEY` and `API_SECRET`

First create:
- ConfigMap `app-config` with data: `DB_HOST=db.example.com`, `DB_PORT=5432`
- Secret `app-secret` with data: `API_KEY=my-api-key`, `API_SECRET=my-api-secret`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 67

> **Solve this question on:** `ckad-lab-67`

Create a *ConfigMap* named `db-config` in the `default` namespace with the following key-value pairs:

- `DB_HOST=db.example.com`
- `DB_USER=development`
- `DB_PASSWD=password`

Then create a *Pod* named `nginx-config` using the `nginx` image that:

1. Injects **all** keys from `db-config` as environment variables using `envFrom`.
2. Mounts `db-config` as a *Volume* named `db-config-vol` at the path `/config` (read-only).

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

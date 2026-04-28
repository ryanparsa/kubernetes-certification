# Question 68

> **Solve this question on:** `ckad-lab-68`

Create a *Secret* named `db-secret` in the `default` namespace with the following key-value pairs:

- `DB_HOST=db.example.com`
- `DB_USER=development`
- `DB_PASSWD=password`

Then create two *Pods*:

1. **`nginx-secret-env`** using the `nginx` image — inject **all** keys from `db-secret` as environment variables using `envFrom`.
2. **`nginx-secret-vol`** using the `nginx` image — mount `db-secret` as a *Volume* named `db-secret-vol` at the path `/secret` (read-only).

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

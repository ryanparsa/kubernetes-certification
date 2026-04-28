# Question 82

> **Solve this question on:** `ckad-lab-82`

Create a namespace `secrets-ns`.

1. Create a Secret named `db-secret` in namespace `secrets-ns` with the following literal values:
   - `username=admin`
   - `password=SuperSecret123`

2. Create a Pod named `secret-pod` in namespace `secrets-ns` using image `alpine` with command `sleep 3600`. Mount the Secret as a volume at path `/etc/secrets` inside the container.

3. Verify the Secret files are present in the container:

```bash
kubectl exec secret-pod -n secrets-ns -- ls /etc/secrets/
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

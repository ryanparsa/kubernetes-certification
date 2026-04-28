# Question 84

> **Solve this question on:** `ckad-lab-84`

Create a namespace `dev`.

1. Create a ServiceAccount named `developer` in namespace `dev`.
2. Create a Role named `pod-reader` in namespace `dev` that grants `get`, `list`, and `watch` permissions on Pods.
3. Create a RoleBinding named `developer-read-pods` in namespace `dev` that binds the Role `pod-reader` to the ServiceAccount `developer`.

4. Verify the ServiceAccount has the expected permissions:

```bash
kubectl auth can-i list pods -n dev --as=system:serviceaccount:dev:developer
```

The command must output `yes`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

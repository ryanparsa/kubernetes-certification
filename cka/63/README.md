# Question 63

> **Solve this question on:** `cka-lab-63`

Perform the following cluster administration tasks in the `cluster-admin` namespace:

1. Create a ServiceAccount named `app-admin`
2. Create a Role that allows:
   - `list`, `get`, `watch` operations on `pods` and `deployments`
   - `create` and `delete` operations on `configmaps`
   - `update` operations on `deployments`
3. Bind the Role to the ServiceAccount
4. Create a test Pod named `admin-pod` that uses this ServiceAccount with:
   - Image: `bitnami/kubectl:latest`
   - Command: `sleep 3600`

Verify the pod can perform the allowed operations but cannot perform other operations (e.g. creating pods).

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

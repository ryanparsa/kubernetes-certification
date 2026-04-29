# Question 68

> **Solve this question on:** the "cka-lab-68" kind cluster

Perform the following steps in the `ci` namespace (create it if it does not exist):

1. Create a *ServiceAccount* named `cicd-sa`.
2. Create a *Role* named `deployment-manager` that allows `create`, `update`, and `delete` actions on `deployments` resources.
3. Create a *RoleBinding* named `cicd-sa-deployment-manager` that binds the *Role* `deployment-manager` to the *ServiceAccount* `cicd-sa`.
4. Verify that `cicd-sa` can `create` deployments but **cannot** `get` pods in the `ci` namespace.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

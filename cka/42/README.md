# Question 42

> **Solve this question on:** `cka-lab-42`

Create a *ServiceAccount* named `app-sa` in the `default` namespace.

Create a *Role* named `pod-reader` that allows listing and getting pods.

Create a *RoleBinding* named `read-pods` that binds the `pod-reader` Role to the `app-sa` ServiceAccount.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

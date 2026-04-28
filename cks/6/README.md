# Question 6

> **Solve this question on:** `cks-lab-6`

Create a Role and RoleBinding in the `rbac-minimize` namespace to provide a ServiceAccount named `app-reader` with minimal permissions required to read pods, services, and deployments, but not secrets or configmaps.

The Role should be named `app-reader-role` and the RoleBinding should be named `app-reader-binding`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 28

> **Solve this question on:** `ckad-lab-28`

In the `cluster-admin` namespace, implement proper access control and security segmentation in the cluster by configuring RBAC resources.

First, create a ClusterRole named `pod-reader` that defines a set of permissions for pod operations. This role should specifically allow three operations on pods: `get` (view individual pods), `watch` (receive notifications about pod changes), and `list` (view collections of pods).

Next, create a ClusterRoleBinding named `read-pods` that associates this role with the user `jane` in the namespace `cluster-admin`.

This binding will grant user `jane` read-only access to pod resources across all namespaces in the cluster, following the principle of least privilege while allowing her to perform her monitoring duties.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 3

> **Solve this question on:** `cks-lab-3`

Enhance the security of the Kubernetes API server by configuring a Pod Security Standard (PSS):

1. Create a namespace named `api-security`

2. Apply a label to the namespace to enforce the `baseline` Pod Security Standard: `pod-security.kubernetes.io/enforce=baseline`

3. Create a pod named `secure-pod` using the `nginx` image that complies with the baseline Pod Security Standard.

4. Create a Role and RoleBinding that allow a ServiceAccount named `pss-viewer` (which has already been created) to view the pod security standards applied to namespaces.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

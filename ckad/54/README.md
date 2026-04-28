# Question 54

> **Solve this question on:** `ckad-lab-54`

Create a Custom Resource Definition (CRD) for a simple application:

1. Create a CRD named `applications.training.ckad.io` with:
   - Group: `training.ckad.io`
   - Version: `v1`
   - Kind: `Application`
   - Scope: `Namespaced`
   - Required fields: `spec.image` (string) and `spec.replicas` (integer, minimum 1)

2. After creating the CRD, create a custom resource in the `crd-demo` namespace named `my-app` with:
   - Image: `nginx:1.19.0`
   - Replicas: `3`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

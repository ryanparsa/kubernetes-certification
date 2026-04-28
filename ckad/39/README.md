# Question 39

> **Solve this question on:** `ckad-lab-39`

Create a Deployment in the `pod-design` namespace with the following specifications:

- Name: `frontend`
- Replicas: `3`
- Image: `nginx:1.19.0`
- Labels: `app=frontend, tier=frontend`
- Pod Labels: same as deployment labels

Then create a service `frontend-svc` that exposes the deployment on port `80`, targeting container port `80`, and is of type `ClusterIP`.

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

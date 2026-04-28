# Question 39

> **Solve this question on:** the "ckad-lab-39" *Kubernetes* cluster

Create a *Deployment* in the `pod-design` *Namespace* with the following specifications:

- Name: `frontend`
- Replicas: `3`
- Image: `nginx:1.19.0`
- Labels: `app=frontend, tier=frontend`
- *Pod* Labels: same as *Deployment* labels

Then create a *Service* `frontend-svc` that exposes the *Deployment* on port `80`, targeting container port `80`, and is of type *ClusterIP*.

Ensure the *Namespace* exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

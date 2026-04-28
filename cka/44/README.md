# Question 44

> **Solve this question on:** `cka-lab-44`

Create a *Deployment* named `web-app` in the `default` namespace with `3` replicas using the `nginx:1.19` image.

Create a *NodePort* service named `web-service` that exposes the deployment on port `80`.

Ensure the pods are distributed across multiple nodes using an appropriate pod anti-affinity rule.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

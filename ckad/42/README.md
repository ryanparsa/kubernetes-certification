# Question 42

> **Solve this question on:** `ckad-lab-42`

Create a Deployment named `web-app` in the `services` namespace with 3 replicas using the image `nginx:alpine`. Label the pods with `app=web`.

Expose the deployment with three different services:

1. A ClusterIP service named `web-svc-cluster` on port `80`
2. A NodePort service named `web-svc-nodeport` on port `80`, using nodePort `30080`
3. A LoadBalancer service named `web-svc-lb` on port `80`

Ensure the namespace exists before creating the resources.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

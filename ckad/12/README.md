# Question 12

> **Solve this question on:** `ckad-lab-12`

Perform the following networking tasks:

1. Create a Deployment named `frontend` with image `nginx`, `2` replicas, and container port `80`. Expose it as a **ClusterIP** Service named `frontend-svc` on port `80` targeting port `80`.

2. Change the service type of `frontend-svc` from `ClusterIP` to `NodePort`.

3. Create a NetworkPolicy named `allow-labeled` in namespace `default` that allows **ingress** traffic to pods with label `app=frontend` only from pods that have label `access=granted`.

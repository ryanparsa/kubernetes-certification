# Question 69

> **Solve this question on:** `ckad-lab-69`

1. Create a *Pod* named `nginx-clusterip` with the `nginx` image and expose it as a *ClusterIP* service named `nginx-clusterip` on port `80`.

2. Create a *Deployment* named `nginx-deployment` with the `nginx` image and `3` replicas. Expose it as a *NodePort* service named `nginx-deployment-svc` on port `80`, with `nodePort: 30080`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 60

> **Solve this question on:** `ckad-lab-60`

Create a namespace called `deployment-namespace`.

Create a Deployment called `my-deployment` inside the namespace with the following specifications:
- Image: `nginx`
- Replicas: `3`
- Container name: `my-container`
- Expose container port `80`
- Memory request: `25Mi`
- Memory limit: `100Mi`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

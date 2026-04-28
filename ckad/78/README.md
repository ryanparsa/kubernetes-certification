# Question 78

> **Solve this question on:** `ckad-lab-78`

1. Create a *Deployment* named `deploy` with **3 replicas**. The *Pods* should use the image `nginx` and the container name `nginx`. The *Deployment* should carry the label `tier=backend` and the *Pod* template should use the label `app=v1`.

2. Update the container image to `nginx:latest` and verify the rollout reaches all replicas.

3. Scale the *Deployment* to **5 replicas**.

4. Inspect the rollout history and then roll the *Deployment* back to **revision 1**.

5. Confirm that the *Pods* are now using the original `nginx` image.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 16

> **Solve this question on:** `ckad-lab-16`

In this task, you need to set up a basic web application deployment.

Create a deployment called `nginx-deployment` in the namespace `dev` with `3` replicas using the image `nginx:latest`.

Ensure that the namespace exists before creating the deployment. The deployment should maintain exactly 3 pods running at all times, and all pods should be using the specified nginx image version.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

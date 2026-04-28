# Question 4

> **Solve this question on:** `ckad-lab-4`

Perform the following tasks with Deployments:

1. Create a Deployment named `webapp` with image `nginx:1.20`, `3` replicas, and container port `80`.
2. Update the image to `nginx:1.21` and observe the rolling update.
3. Roll back the deployment to the previous revision and confirm the image returns to `nginx:1.20`.
4. Scale the deployment to `5` replicas.
5. Configure the rolling update strategy to use `maxSurge: 1` and `maxUnavailable: 0`.

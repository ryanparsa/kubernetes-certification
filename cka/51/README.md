# Question 51

> **Solve this question on:** `cka-lab-51`

Create a Deployment named `scaling-app` in the `scaling` namespace with the following specifications:

- Image: `nginx`
- Initial replicas: `2`
- Resource requests: CPU: `200m`, Memory: `256Mi`
- Resource limits: CPU: `500m`, Memory: `512Mi`

Then create a `HorizontalPodAutoscaler` for this deployment:

- Use apiVersion: `autoscaling/v1`
- Min replicas: `2`
- Max replicas: `5`
- Target CPU utilization: `70%`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

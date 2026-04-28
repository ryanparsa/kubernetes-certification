# Question 62

> **Solve this question on:** `cka-lab-62`

Create a deployment named `resource-consumer` in the `monitoring` namespace with `3` replicas that:

1. Uses the image `gcr.io/kubernetes-e2e-test-images/resource-consumer:1.5`
2. Sets resource requests: CPU `100m`, Memory `128Mi`
3. Sets resource limits: CPU `200m`, Memory `256Mi`

Then create a `HorizontalPodAutoscaler` for this deployment:

- Min replicas: `3`
- Max replicas: `6`
- Target CPU utilization: `50%`

Note: metrics-server is already installed in the cluster.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

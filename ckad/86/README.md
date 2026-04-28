# Question 86

> **Solve this question on:** `ckad-lab-86`

Create a namespace `monitoring`.

Create a Pod named `health-check` in namespace `monitoring` using image `nginx:1.25` with the following probes configured:

- **Liveness probe**: HTTP GET on port `80`, path `/`, `initialDelaySeconds: 10`, `periodSeconds: 5`
- **Readiness probe**: HTTP GET on port `80`, path `/`, `initialDelaySeconds: 5`, `periodSeconds: 3`

Verify the probes are configured:

```bash
kubectl describe pod health-check -n monitoring | grep -A 5 "Liveness\|Readiness"
```

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

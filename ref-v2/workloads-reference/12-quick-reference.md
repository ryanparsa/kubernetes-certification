# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 12. Quick Reference

| Field | Default | Notes |
|---|---|---|
| `restartPolicy` | `Always` | Jobs/CronJobs must use `Never` or `OnFailure` |
| `terminationGracePeriodSeconds` | 30s | How long kubelet waits after SIGTERM before SIGKILL |
| `spec.replicas` | 1 | Remove from Deployment spec when using HPA |
| `maxUnavailable` | 25% | RollingUpdate: can be absolute number or % |
| `maxSurge` | 25% | RollingUpdate: extra pods above desired count |

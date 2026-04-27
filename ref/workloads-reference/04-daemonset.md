# Kubernetes Workloads Reference — 4. DaemonSet

> Part of [Kubernetes Workloads Reference](../Workloads Reference.md)


Runs exactly one pod on every (matching) node. Common for log collectors, monitoring
agents, network plugins.

See the **Scheduling Reference** for scheduling details (taints, nodeSelector).

```bash
# Check DaemonSet status
kubectl -n kube-system get daemonset

# Restart all DaemonSet pods (triggers rolling update)
kubectl -n kube-system rollout restart daemonset fluentd

# Check rollout status
kubectl -n kube-system rollout status daemonset fluentd
```

---


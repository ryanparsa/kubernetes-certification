# Kubernetes Commands Reference

[← Back to index](../README.md)

---

## Part 5: kube-scheduler

Assigns unscheduled pods to nodes. It runs the scheduling algorithm (filter → score → bind)
and writes the chosen node name back to `pod.spec.nodeName` via the API server.

---

### 5.1 — What It Does

- **Watches** for pods with no `.spec.nodeName` (unscheduled pods)
- **Filters** candidate nodes using predicates (resource fit, taints, affinity, topology spread)
- **Scores** remaining nodes using priority functions (balanced resource, affinity preference)
- **Binds** the pod to the best node (writes `pod.spec.nodeName` via API server `bind` subresource)

Never communicates directly with kubelets or containerd — only with the API server.

---

### 5.2 — Run Mode

Static pod: `/etc/kubernetes/manifests/kube-scheduler.yaml`

---

### 5.3 — Key Flags

```
--config=/etc/kubernetes/scheduler.conf       # kubeconfig for auth to API server
--leader-elect=true                           # HA: only one scheduler instance is active
--profiling=false                             # CKS: disable profiling endpoint
```

For custom scheduling profiles (multiple schedulers, plugins):
```yaml
# KubeSchedulerConfiguration
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
    plugins:
      score:
        disabled:
          - name: NodeResourcesBalancedAllocation
```

**Identity:** CN = `system:kube-scheduler`, no Organization.
Maps to the built-in `system:kube-scheduler` ClusterRole.

**What breaks:**
- Scheduler not running → new pods stay in `Pending` with no `Events` (no scheduling events)
- Incorrect kubeconfig cert → scheduler cannot watch pods → no scheduling happens

---

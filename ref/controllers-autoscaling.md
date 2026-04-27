# Autoscaling

| Controller | Main File | What It Does |
| --- | --- | --- |
| **HorizontalPodAutoscaler** | `pkg/controller/podautoscaler/horizontal.go` | `HorizontalController` · `Run()` ticks every 15s and calls `reconcileAutoscaler()`. `computeReplicasForMetrics()` fetches current values via `metrics.go` and calculates desired replica count, then patches `.spec.replicas` on the target workload |

---


# Availability & Scheduling Support

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Disruption** | `pkg/controller/disruption/disruption.go` | `DisruptionController` · `sync()` counts disrupted Pods and blocks voluntary evictions that would violate `minAvailable`/`maxUnavailable` in the `PodDisruptionBudget`. `syncDisruptedPods()` cleans up stale disruption records |
| **PodGroupProtection** | `pkg/controller/scheduling/podgroupprotection/` | Adds finalizers to `PodGroup` objects to prevent deletion while member Pods are running (gang scheduling) |

---


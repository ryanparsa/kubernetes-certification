# Kubernetes Controllers Reference — Resource Management Controllers

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


| Controller | Main File | What It Does |
| --- | --- | --- |
| **ResourceQuota** | `pkg/controller/resourcequota/resource_quota_controller.go` | `Controller` · `syncResourceQuota()` recalculates namespace resource usage and updates `status.used`. Rejects requests that would exceed limits |
| **ResourceClaim** | `pkg/controller/resourceclaim/controller.go` | DRA: `Controller` · `syncClaim()` allocates devices (GPUs, FPGAs) to Pods via `ResourceClaim` objects |
| **ResourcePoolStatusRequest** | `pkg/controller/resourcepoolstatusrequest/` | DRA: allows device drivers to report resource pool capacity and health back to the API server |

---


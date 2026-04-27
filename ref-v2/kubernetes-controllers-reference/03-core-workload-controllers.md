# Kubernetes Controllers Reference

[← Back to index](../README.md)

---

## Core Workload Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Deployment** | `pkg/controller/deployment/deployment_controller.go` | `DeploymentController` · `syncDeployment()` drives rolling updates via `rolloutRolling()` / `rolloutRecreate()`, tracks revision history, handles rollbacks |
| **ReplicaSet** | `pkg/controller/replicaset/replica_set.go` | `ReplicaSetController` · `syncReplicaSet()` calls `manageReplicas()` to create/delete Pods until count matches `.spec.replicas` |
| **ReplicationController** | `pkg/controller/replication/replication_controller.go` | `ReplicationManager` · `syncReplicationController()` — legacy equivalent of ReplicaSet, kept for backwards compatibility |
| **StatefulSet** | `pkg/controller/statefulset/stateful_set.go` | `StatefulSetController` · `sync()` delegates to `defaultStatefulSetControl.UpdateStatefulSet()` in `stateful_set_control.go` for ordered Pod creation, per-Pod PVCs, and rolling updates |
| **DaemonSet** | `pkg/controller/daemon/daemon_controller.go` | `DaemonSetsController` · `syncDaemonSet()` calls `podsShouldBeOnNode()` to decide which Nodes need a Pod, then creates or deletes Pods accordingly |
| **Job** | `pkg/controller/job/job_controller.go` | `Controller` · `syncJob()` calls `manageJob()` to create/delete Pods toward completion. Tracks success/failure counts, retries, parallelism, indexed jobs |
| **CronJob** | `pkg/controller/cronjob/cronjob_controller.go` | `ControllerV2` · `Run()` ticks every ~10s and calls `syncAll()` → `sync()` per CronJob. `getNextScheduleTime()` parses the cron expression and compares against `status.lastScheduleTime` in etcd — no external event fires at schedule time |

---

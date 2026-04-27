# Kubernetes Controllers Reference

[← Back to index](../README.md)

---

## Pod Lifecycle & Garbage Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **PodGC** | `pkg/controller/podgc/gc_controller.go` | `PodGCController` · `gc()` deletes terminated Pods above `--terminated-pod-gc-threshold`. `gcOrphaned()` removes Pods bound to non-existent Nodes |
| **TTL** | `pkg/controller/ttl/ttl_controller.go` | `Controller` · `sync()` sets TTL annotations on Nodes so the API server knows how long to cache them — reduces etcd load |
| **TTLAfterFinished** | `pkg/controller/ttlafterfinished/ttlafterfinished_controller.go` | `Controller` · `sync()` is timer-driven — checks elapsed time since `status.completionTime` against `spec.ttlSecondsAfterFinished` and deletes the Job and its Pods when expired |
| **GarbageCollector** | `pkg/controller/garbagecollector/garbage_collector.go` | `GarbageCollector` · `GraphBuilder` in `graph.go` maintains an in-memory `uidToNode` ownership graph. `runAttemptToDeleteWorker()` calls `attemptToDeleteItem()` for orphaned objects. Runs a periodic full resync independently of events |

---

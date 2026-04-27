# Kubernetes Controllers Reference — Admission Policy Status

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


| Controller | Main File | What It Does |
| --- | --- | --- |
| **ValidatingAdmissionPolicyStatus** | `pkg/controller/validatingadmissionpolicystatus/controller.go` | `Controller` · `reconcile()` runs CEL type-checking against current CRD schemas and writes results into `ValidatingAdmissionPolicy.status.typeChecking` |

---

# LAYER 3 — cloud-controller-manager

A **separate binary** that decouples cloud-provider logic from the core Kubernetes binaries. Each cloud provider ships its own implementation.

> Interface definitions: `staging/src/k8s.io/cloud-provider/` in kubernetes/kubernetes
Implementations: separate repos per provider
> 

| Controller | Interface Path | What It Does |
| --- | --- | --- |
| **Node (Cloud)** | `staging/src/k8s.io/cloud-provider/controllers/node/` | Syncs cloud instance metadata (zone, region, instance type) onto Node objects. Deletes Node objects when the cloud VM is terminated |
| **NodeLifecycle (Cloud)** | `staging/src/k8s.io/cloud-provider/controllers/nodelifecycle/` | Monitors cloud APIs for instance health; taints or deletes Nodes for cloud-side failures |
| **Service (LoadBalancer)** | `staging/src/k8s.io/cloud-provider/controllers/service/` | Creates/updates/deletes cloud load balancers (AWS ELB, GCP LB, Azure LB) when a `Service` of type `LoadBalancer` is created |
| **Route** | `staging/src/k8s.io/cloud-provider/controllers/route/` | Programs cloud network routes so the Pod CIDR on each Node is routable within the VPC |

### Provider Repos

| Provider | Repo |
| --- | --- |
| AWS | `github.com/kubernetes/cloud-provider-aws` |
| GCP | `github.com/kubernetes/cloud-provider-gcp` |
| Azure | `github.com/kubernetes/cloud-provider-azure` |
| OpenStack | `github.com/kubernetes/cloud-provider-openstack` |

---

# LAYER 4 — kubelet (node-level control loops)

The **kubelet** runs on every Node and is itself a collection of control loops — just scoped to a single node rather than the whole cluster.

> Source root: `pkg/kubelet/` in kubernetes/kubernetes
> 

> Kubelet main struct: `Kubelet` in `pkg/kubelet/kubelet.go` · Top-level loop: `syncLoop()` → `syncLoopIteration()`
> 

| Loop | Main File | What It Does |
| --- | --- | --- |
| **Pod Manager** | `pkg/kubelet/pod/pod_manager.go` | `Manager` interface / `basicManager` · Syncs desired Pod spec (from API server) with running containers via the CRI. `HandlePodAdditions()`, `HandlePodUpdates()` in `kubelet.go` drive this |
| **PLEG** (Pod Lifecycle Event Generator) | `pkg/kubelet/pleg/generic.go` | `GenericPLEG` · `relist()` polls the container runtime on a 1s ticker, diffs against the previous state, and emits `PodLifecycleEvent` structs that feed into `syncLoop()` |
| **Volume Manager** | `pkg/kubelet/volumemanager/volume_manager.go` | `VolumeManager` interface / `volumeManager` · `reconciler.go` runs a loop to attach, mount, and unmount volumes. Blocks Pod start until volumes are ready |
| **Image Manager** | `pkg/kubelet/images/image_manager.go` | `ImageManager` · `EnsureImageExists()` pulls images, respects `imagePullPolicy`. Backed by `imageBackOff` for retry limiting |
| **Image GC** | `pkg/kubelet/images/image_gc_manager.go` | `realImageGCManager` · `GarbageCollect()` evicts unused images when disk usage exceeds `--image-gc-high-threshold` |
| **Container GC** | `pkg/kubelet/container/container_gc.go` | `ContainerGC` · `GarbageCollect()` removes dead containers, keeping at most `--maximum-dead-containers-per-container` per Pod |
| **Node Status Manager** | `pkg/kubelet/nodestatus/setters.go` | Collection of setter funcs composed by `Kubelet.setNodeStatus()` in `kubelet_node_status.go`. Periodically patches `Node.status` (conditions, capacity, allocatable, addresses) |
| **Certificate Manager** | `pkg/kubelet/certificate/certificate_manager.go` | `manager` · `rotateCerts()` watches certificate expiry and requests a new CSR via the `certificates.k8s.io` API before the current cert expires |
| **Eviction Manager** | `pkg/kubelet/eviction/eviction_manager.go` | `managerImpl` · `synchronize()` runs on a timer checking cgroup memory/disk/PID thresholds and evicts Pods in priority order |
| **OOM Watcher** | `pkg/kubelet/oom/oom_watcher_linux.go` | `realOOMWatcher` · Watches `/dev/kmsg` for OOM kill events and records them as Kubernetes `Event` objects on the affected Pod |
| **Resource Analyzer** | `pkg/kubelet/server/stats/provider.go` | `Provider` · `GetCgroupStats()` collects cgroup-level CPU/memory/disk stats exposed via `/stats/summary` (consumed by metrics-server) |
| **Plugin Manager** | `pkg/kubelet/pluginmanager/plugin_manager.go` | `PluginManager` · Watches the plugin registration socket directory and calls `RegisterPlugin()` / `DeRegisterPlugin()` for device plugins and CSI drivers |
| **Probe Manager** | `pkg/kubelet/prober/prober_manager.go` | `Manager` interface / `manager` · `AddPod()` starts per-container goroutines that run liveness, readiness, and startup probes and update `Pod.status.conditions` |

---

# Custom Controllers / Operators (outside the main repo)

Any controller you build yourself using the standard Kubernetes controller pattern. Runs as a Deployment in the cluster.

| Framework | Repo | Used By |
| --- | --- | --- |
| **controller-runtime** | `github.com/kubernetes-sigs/controller-runtime` | Kubebuilder, Operator SDK, most modern operators |
| **client-go** (informer + workqueue) | `github.com/kubernetes/client-go` | Kubernetes itself internally; low-level custom controllers |

At the Go level, every controller is one or more **goroutines** running a `for {}` loop inside a single binary. The kube-controller-manager binary starts all its controllers as goroutines at boot and they run concurrently for the lifetime of the process.

```go
// cmd/kube-controller-manager/app/controllermanager.go
// Each controller is started as a goroutine via startController()
go deploymentController.Run(ctx, workers)   // DeploymentController.Run()
go replicaSetController.Run(ctx, workers)   // ReplicaSetController.Run()
go cronJobController.Run(ctx, workers)      // ControllerV2.Run()
// ... all others registered in app/apps.go, app/batch.go, app/core.go
```

Each `Run()` looks like one of two patterns depending on the controller:

**Event-driven** — uses a `workqueue.RateLimitingQueue` from `k8s.io/client-go/util/workqueue`. An informer (`cache.SharedIndexInformer` from `k8s.io/client-go/tools/cache`) pushes keys on API events; a worker goroutine blocks on `queue.Get()`:

```go
// typical worker loop (e.g. ReplicaSetController.worker())
func (c *ReplicaSetController) worker(ctx context.Context) {
    for {
        key, quit := c.queue.Get()   // workqueue.RateLimitingQueue — blocks until event
        if quit { return }
        c.syncReplicaSet(ctx, key.(string))
        c.queue.Done(key)
    }
}
```

**Timer-driven** — uses `select` over a `time.Ticker` channel; never waits for an API event:

```go
// CronJob: ControllerV2.Run() in cronjob_controller.go
for {
    select {
    case <-time.After(jitteredSleepDuration):   // ~10s
        c.syncAll(ctx)   // getNextScheduleTime() → create Job if due
    case <-ctx.Done():
        return
    }
}
```

Most controllers combine both: a `workqueue.RateLimitingQueue` for API events + a `resyncPeriod` on the `SharedIndexInformer` that re-enqueues all cached objects periodically as a safety net. Pure timer-driven controllers — CronJob (~10s), HPA (~15s), NodeLifecycle (heartbeat age check), TTLAfterFinished (elapsed time check), GarbageCollector (full graph resync) — skip the work queue entirely or use it only as secondary.

The general reconcile steps are the same regardless of what woke the goroutine:
1. **List+Watch** — informer caches objects and feeds change events into the queue
2. **Enqueue** — push the object key into a work queue (from an API event or a timer tick)
3. **Reconcile** — dequeue, read current state, compare to desired state, act


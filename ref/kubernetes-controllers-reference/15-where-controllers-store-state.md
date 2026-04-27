# Kubernetes Controllers Reference — Where controllers store state

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


Controllers are **stateless processes** — they can crash, restart, and fully reconstruct themselves. All durable state lives outside the goroutine. Where it lives depends on what kind of state it is:

| State type | Storage | Go type / Example |
| --- | --- | --- |
| Desired state | etcd via `.spec` on API objects | `deployment.spec.replicas = 3` |
| Observed / current state | etcd via `.status` on API objects | `deployment.status.readyReplicas = 2` |
| Ownership / relationships | etcd via `ownerReferences` on objects | `metav1.OwnerReference` — ReplicaSet points back to its Deployment |
| Deletion protection | etcd via `finalizers` on objects | `metadata.finalizers` — PVC has `kubernetes.io/pvc-protection` |
| Controller revision history | etcd via `ControllerRevision` objects | `apps/v1.ControllerRevision` — StatefulSet and DaemonSet rollback snapshots, managed via `pkg/controller/history/controller_history.go` |
| Leader election lock | etcd via `Lease` objects in `kube-system` | `coordination/v1.Lease` — `LeaseLock` in `k8s.io/client-go/tools/leaderelection/resourcelock`. Only one kube-controller-manager instance is active in HA |
| Sensitive state | etcd via `Secret` objects | `v1.Secret` — ServiceAccount tokens, bootstrap tokens |
| Config state | etcd via `ConfigMap` objects | `v1.ConfigMap` — some controllers store non-sensitive state here |
| External / cloud state | Cloud provider APIs (AWS, GCP, Azure) | cloud-controller-manager calls EC2 / Compute APIs and writes results back to `Node.status` |
| Fast local cache | In-memory `cache.ThreadSafeStore` (ephemeral) | `k8s.io/client-go/tools/cache` — `SharedIndexInformer` rebuilds from etcd via list+watch on every restart, never the source of truth |

The split between `.spec` and `.status` is the core pattern:

```
User writes → .spec  (desired state)     stored in etcd
Controller writes → .status (observed state)  stored in etcd
Controller's job = make .status match .spec
```

Because all durable state is in etcd, a controller goroutine that crashes loses nothing — on restart it does a full list+watch, rebuilds its in-memory cache, and picks up exactly where it left off. The in-memory informer cache is always treated as a disposable read-through layer over etcd, never as the authoritative record.

---

# Summary: Where Each Layer Lives

```
kubernetes/kubernetes (monorepo)
│
├── cmd/kube-controller-manager/
│   ├── main.go                          ← binary entry point
│   └── app/
│       ├── controllermanager.go         ← NewControllerManagerCommand(), Run()
│       ├── apps.go                      ← registers Deployment, StatefulSet, DaemonSet, ReplicaSet
│       ├── batch.go                     ← registers Job, CronJob
│       └── core.go                      ← registers Namespace, GC, Node, Endpoints, ...
│
├── plugin/pkg/admission/                ← LAYER 1: Admission controllers
│   ├── serviceaccount/
│   ├── limitranger/
│   ├── resourcequota/
│   ├── podsecurity/
│   ├── noderestriction/
│   ├── webhook/mutating/                ← MutatingAdmissionWebhook
│   ├── webhook/validating/              ← ValidatingAdmissionWebhook
│   └── validatingadmissionpolicy/       ← CEL-based in-process validation
│
├── pkg/controller/                      ← LAYER 2: kube-controller-manager loops
│   ├── deployment/deployment_controller.go       (DeploymentController)
│   ├── replicaset/replica_set.go                 (ReplicaSetController)
│   ├── statefulset/stateful_set.go               (StatefulSetController)
│   ├── daemon/daemon_controller.go               (DaemonSetsController)
│   ├── job/job_controller.go                     (Controller)
│   ├── cronjob/cronjob_controller.go             (ControllerV2)
│   ├── nodelifecycle/node_lifecycle_controller.go
│   ├── garbagecollector/garbage_collector.go     (GarbageCollector)
│   ├── garbagecollector/graph.go                 (GraphBuilder)
│   ├── podautoscaler/horizontal.go               (HorizontalController)
│   ├── namespace/namespace_controller.go         (NamespaceController)
│   ├── disruption/disruption.go                  (DisruptionController)
│   ├── history/controller_history.go             (realHistory)
│   ├── volume/persistentvolume/controller.go     (PersistentVolumeController)
│   └── ... (all others above)
│
├── staging/src/k8s.io/
│   ├── cloud-provider/controllers/      ← LAYER 3: cloud-controller-manager interface
│   │   ├── node/
│   │   ├── service/
│   │   └── route/
│   └── client-go/
│       ├── tools/cache/                 ← SharedIndexInformer, ThreadSafeStore
│       ├── util/workqueue/              ← RateLimitingQueue
│       └── tools/leaderelection/        ← LeaderElector, LeaseLock
│
└── pkg/kubelet/                         ← LAYER 4: kubelet node-level loops
    ├── kubelet.go                       ← Kubelet struct, syncLoop()
    ├── pleg/generic.go                  ← GenericPLEG, relist()
    ├── pod/pod_manager.go               ← basicManager
    ├── volumemanager/volume_manager.go
    ├── eviction/eviction_manager.go     ← managerImpl
    ├── images/image_gc_manager.go       ← realImageGCManager
    ├── prober/prober_manager.go         ← manager
    └── certificate/certificate_manager.go

External repos
├── kubernetes/cloud-provider-aws        ← cloud-controller-manager (AWS)
├── kubernetes/cloud-provider-gcp        ← cloud-controller-manager (GCP)
├── kubernetes/cloud-provider-azure
├── kubernetes-sigs/controller-runtime  ← operator framework (Reconciler interface)
└── kubernetes/client-go                ← informer + workqueue building blocks
```
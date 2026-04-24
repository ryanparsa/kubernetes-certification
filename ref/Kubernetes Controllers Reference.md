# Kubernetes Controllers Reference

Kubernetes controllers live in **four different layers**. Each layer has a different role and lives in a different part of the repository.

```
┌─────────────────────────────────────────────────────────┐
│  API Request arrives at kube-apiserver                  │
│                                                         │
│  LAYER 1 ── Admission Controllers  (plugin/pkg/admission)
│             intercept & mutate/validate BEFORE persist  │
│                                                         │
│  Object is written to etcd                              │
│                                                         │
│  LAYER 2 ── kube-controller-manager (pkg/controller/)   │
│             reconcile cluster state AFTER persist       │
│                                                         │
│  LAYER 3 ── cloud-controller-manager                    │
│             reconcile cloud-provider resources          │
│                                                         │
│  LAYER 4 ── kubelet  (pkg/kubelet/)                     │
│             reconcile node-local state per Node         │
└─────────────────────────────────────────────────────────┘
```

---

# LAYER 1 — Admission Controllers

Admission controllers run **inside the kube-apiserver process** and intercept every write request (CREATE / UPDATE / DELETE) before the object is persisted to etcd. They are **not** separate processes.

- **Mutating** controllers can modify the object (e.g. inject a sidecar, set a default).
- **Validating** controllers can only approve or reject — they cannot change the object.
- Many controllers are **both** (mutate first, then validate).

> Source root: `plugin/pkg/admission/` in kubernetes/kubernetes
> 

---

## Mutating Admission Controllers

| Controller | Repo Path | What It Does |
| --- | --- | --- |
| **DefaultStorageClass** | `plugin/pkg/admission/storage/storageclass/setdefault/` | Sets `.spec.storageClassName` on a PVC if none is specified, using the StorageClass marked as default |
| **DefaultIngressClass** | `plugin/pkg/admission/network/defaultingressclass/` | Sets `.spec.ingressClassName` on an Ingress if none is specified, using the IngressClass marked as default |
| **DefaultTolerationSeconds** | `plugin/pkg/admission/pod/defaulttolerationseconds/` | Injects default `tolerationSeconds` for `node.kubernetes.io/not-ready` and `node.kubernetes.io/unreachable` taints if not already set |
| **ExtendedResourceToleration** | `plugin/pkg/admission/extendedresourcetoleration/` | Automatically adds tolerations to Pods that request extended resources (GPU, FPGA, etc.) so they schedule on nodes with those resources tainted |
| **LimitRanger** | `plugin/pkg/admission/limitranger/` | Applies defaults from `LimitRange` objects (default CPU/memory requests and limits) to Pods and Containers in the namespace |
| **MutatingAdmissionWebhook** | `plugin/pkg/admission/webhook/mutating/` | Calls out to external webhooks registered via `MutatingWebhookConfiguration`. The webhook can modify the object and return a JSON patch |
| **NamespaceAutoProvision** | `plugin/pkg/admission/namespace/autoprovision/` | Automatically creates a Namespace if it doesn’t exist when a resource is created in it (disabled by default) |
| **PersistentVolumeLabel** | `plugin/pkg/admission/storage/persistentvolume/label/` | Adds cloud-provider zone/region labels to PersistentVolumes (legacy; mostly replaced by cloud-controller-manager) |
| **Priority** | `plugin/pkg/admission/priority/` | Resolves the `.spec.priorityClassName` of a Pod to an integer `.spec.priority` by looking up the `PriorityClass` object |
| **RuntimeClass** | `plugin/pkg/admission/runtimeclass/` | Sets the Pod’s scheduling overhead (`spec.overhead`) from the referenced `RuntimeClass` object |
| **ServiceAccount** | `plugin/pkg/admission/serviceaccount/` | Injects `default` ServiceAccount if none specified, mounts the service account token secret, and validates image pull secrets |
| **StorageObjectInUseProtection** | `plugin/pkg/admission/storage/persistentvolume/inuseprotection/` | Adds the `kubernetes.io/pvc-protection` and `kubernetes.io/pv-protection` finalizers to PVCs and PVs so they can’t be deleted while in use |
| **TaintNodesByCondition** | `plugin/pkg/admission/nodetaint/` | Adds `NoSchedule` taints to Nodes based on their conditions (e.g. `NotReady`, `MemoryPressure`) so that new Pods don’t schedule on unhealthy nodes |

---

## Validating Admission Controllers

| Controller | Repo Path | What It Does |
| --- | --- | --- |
| **AlwaysAdmit** | `plugin/pkg/admission/alwaysadmit/` | Admits every request unconditionally. Used for testing; never enable in production |
| **AlwaysDeny** | `plugin/pkg/admission/alwaysdeny/` | Rejects every request unconditionally. Used for testing only |
| **AlwaysPullImages** | `plugin/pkg/admission/alwayspullimages/` | Forces `imagePullPolicy: Always` on every container so nodes always re-authenticate with the registry before running an image |
| **CertificateApproval** | `plugin/pkg/admission/certificates/approval/` | Restricts who can approve `CertificateSigningRequest` objects based on the signer name |
| **CertificateSigning** | `plugin/pkg/admission/certificates/signing/` | Restricts who can sign CSRs for a given signer name |
| **CertificateSubjectRestriction** | `plugin/pkg/admission/certificates/subjectrestriction/` | Rejects CSRs for the `kubernetes.io/kube-apiserver-client` signer if the requested subject has the `system:masters` group (privilege escalation prevention) |
| **ClusterTrustBundleAttest** | `plugin/pkg/admission/certificates/ctbattest/` | Validates that the signer field in a `ClusterTrustBundle` matches the requesting user’s permissions |
| **DenyServiceExternalIPs** | `plugin/pkg/admission/network/deny/` | Rejects Services that set `.spec.externalIPs` (mitigates a known traffic interception attack vector) |
| **EventRateLimit** | `plugin/pkg/admission/eventratelimit/` | Rate-limits Event creation per user, namespace, or source to prevent event floods from overwhelming the API server |
| **ImagePolicyWebhook** | `plugin/pkg/admission/imagepolicy/` | Calls an external webhook to approve or reject a Pod based on its container images (supply chain security gate) |
| **LimitPodHardAntiAffinityTopology** | `plugin/pkg/admission/antiaffinity/` | Rejects Pods that use `requiredDuringSchedulingIgnoredDuringExecution` anti-affinity with a topology key other than `kubernetes.io/hostname` |
| **NamespaceExists** | `plugin/pkg/admission/namespace/exists/` | Rejects requests to create resources in a Namespace that doesn’t exist |
| **NamespaceLifecycle** | `plugin/pkg/admission/namespace/lifecycle/` | Rejects creation of new objects in a `Terminating` namespace; protects `default`, `kube-system`, `kube-public` from deletion |
| **NodeRestriction** | `plugin/pkg/admission/noderestriction/` | Limits what a kubelet (Node identity) can modify — it can only update its own Node object and Pods bound to itself. Prevents node compromise from spreading |
| **OwnerReferencesPermissionEnforcement** | `plugin/pkg/admission/gc/` | Prevents users from setting `ownerReferences` that point to objects they don’t have delete permission on (prevents privilege escalation via GC) |
| **PersistentVolumeClaimResize** | `plugin/pkg/admission/storage/persistentvolumeclaim/resize/` | Validates that a PVC resize request only increases size (not decrease) and that the StorageClass allows expansion |
| **PodNodeSelector** | `plugin/pkg/admission/podnodeselector/` | Forces Pods in a namespace to use specific node selectors defined in a namespace annotation. Prevents Pods from scheduling outside their allowed node pool |
| **PodSecurity** | `plugin/pkg/admission/security/podsecurity/` | Enforces the Pod Security Standards (`privileged`, `baseline`, `restricted`) defined on the namespace via labels |
| **PodTolerationRestriction** | `plugin/pkg/admission/podtolerationrestriction/` | Merges default tolerations onto Pods and rejects Pods with tolerations not allowed by namespace-level policy |
| **ResourceQuota** | `plugin/pkg/admission/resourcequota/` | Rejects requests that would exceed a `ResourceQuota` in the namespace. Works in tandem with the ResourceQuota controller in kube-controller-manager |
| **ValidatingAdmissionPolicy** | `plugin/pkg/admission/validatingadmissionpolicy/` | Evaluates CEL (Common Expression Language) rules defined in `ValidatingAdmissionPolicy` objects directly in-process — no webhook roundtrip needed |
| **ValidatingAdmissionWebhook** | `plugin/pkg/admission/webhook/validating/` | Calls external webhooks registered via `ValidatingWebhookConfiguration`. The webhook returns allow/deny with an optional reason |

---

### Key Difference: Webhooks vs In-Tree Controllers

```
In-tree admission controller          External admission webhook
(compiled into kube-apiserver)        (your own HTTP server)
        │                                       │
plugin/pkg/admission/xxx/             registered via:
        │                               MutatingWebhookConfiguration
runs in apiserver process               ValidatingWebhookConfiguration
no network hop                                  │
                                       apiserver calls your endpoint
                                       over HTTPS (network hop)
```

---

# LAYER 2 — kube-controller-manager

A **single binary** running control loops that watch the API server and reconcile cluster state. Runs as a static Pod on control plane nodes.

> Source root: `pkg/controller/` in kubernetes/kubernetes
Binary entry: `cmd/kube-controller-manager/main.go`
Bootstrap & registration: `cmd/kube-controller-manager/app/controllermanager.go` — `NewControllerManagerCommand()`, `Run()`
Controller registration by group: `app/apps.go` (Deployment, StatefulSet, DaemonSet, ReplicaSet), `app/batch.go` (Job, CronJob), `app/core.go` (Namespace, GC, Node, Endpoints…)
> 

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

## Pod Lifecycle & Garbage Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **PodGC** | `pkg/controller/podgc/gc_controller.go` | `PodGCController` · `gc()` deletes terminated Pods above `--terminated-pod-gc-threshold`. `gcOrphaned()` removes Pods bound to non-existent Nodes |
| **TTL** | `pkg/controller/ttl/ttl_controller.go` | `Controller` · `sync()` sets TTL annotations on Nodes so the API server knows how long to cache them — reduces etcd load |
| **TTLAfterFinished** | `pkg/controller/ttlafterfinished/ttlafterfinished_controller.go` | `Controller` · `sync()` is timer-driven — checks elapsed time since `status.completionTime` against `spec.ttlSecondsAfterFinished` and deletes the Job and its Pods when expired |
| **GarbageCollector** | `pkg/controller/garbagecollector/garbage_collector.go` | `GarbageCollector` · `GraphBuilder` in `graph.go` maintains an in-memory `uidToNode` ownership graph. `runAttemptToDeleteWorker()` calls `attemptToDeleteItem()` for orphaned objects. Runs a periodic full resync independently of events |

---

## Node Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **NodeLifecycle** | `pkg/controller/nodelifecycle/node_lifecycle_controller.go` | `Controller` · `monitorNodeHealth()` runs on a timer checking heartbeat age per Node. `doNoScheduleTaintingPass()` adds taints, `doEvictionPass()` evicts Pods — failure is inferred from elapsed time, no “node went bad” event exists |
| **NodeIPAM** | `pkg/controller/nodeipam/nodeipam_controller.go` | `Controller` · `syncNodeCIDR()` allocates a Pod CIDR subnet to each Node. CIDR allocation strategies live in `pkg/controller/nodeipam/ipam/` |
| **TaintEviction** | `pkg/controller/tainteviction/taint_eviction.go` | `Controller` · `processPodOnNode()` evicts Pods from Nodes carrying `NoExecute` taints, respecting each Pod’s `tolerationSeconds` |
| **DeviceTaintEviction** | `pkg/controller/devicetainteviction/` | Evicts Pods when a DRA device they rely on becomes tainted (part of Dynamic Resource Allocation) |

---

## Endpoint & Service Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Endpoint** | `pkg/controller/endpoint/endpoints_controller.go` | `Controller` · `syncEndpoints()` queries Pods matching the Service selector and writes their IPs into the `Endpoints` object |
| **EndpointSlice** | `pkg/controller/endpointslice/endpointslice_controller.go` | `Controller` · `syncEndpointSlices()` splits Pod IPs across `EndpointSlice` objects (max 100 each). Diff logic lives in `reconciler.go` |
| **EndpointSliceMirroring** | `pkg/controller/endpointslicemirroring/endpointslicemirroring_controller.go` | `Controller` · Mirrors hand-crafted `Endpoints` into `EndpointSlice` objects for Services without pod selectors |
| **ServiceCIDRs** | `pkg/controller/servicecidrs/` | Manages `ServiceCIDR` objects that define IP ranges for ClusterIP services |

---

## RBAC & Security Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **ClusterRoleAggregation** | `pkg/controller/clusterroleaggregation/clusterroleaggregation_controller.go` | `ClusterRoleAggregationController` · `syncClusterRole()` merges rules from matching ClusterRoles into aggregate roles (e.g. `admin` includes `edit` and `view`) |
| **ServiceAccount** | `pkg/controller/serviceaccount/serviceaccounts_controller.go` | `ServiceAccountsController` · `syncServiceAccount()` creates the `default` ServiceAccount in every new Namespace |
| **Certificates** | `pkg/controller/certificates/` | `CertificateController` · `approver/` handles auto-approval, `signer/` handles signing of well-known CSR types (Node client certs, kubelet serving certs) |

---

## Resource Management Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **ResourceQuota** | `pkg/controller/resourcequota/resource_quota_controller.go` | `Controller` · `syncResourceQuota()` recalculates namespace resource usage and updates `status.used`. Rejects requests that would exceed limits |
| **ResourceClaim** | `pkg/controller/resourceclaim/controller.go` | DRA: `Controller` · `syncClaim()` allocates devices (GPUs, FPGAs) to Pods via `ResourceClaim` objects |
| **ResourcePoolStatusRequest** | `pkg/controller/resourcepoolstatusrequest/` | DRA: allows device drivers to report resource pool capacity and health back to the API server |

---

## Namespace Controller

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Namespace** | `pkg/controller/namespace/namespace_controller.go` | `NamespaceController` · `syncNamespaceFromKey()` delegates to `NamespacedResourcesDeleter` in `deletion/namespaced_resources_deleter.go` — deletes all objects inside a `Terminating` namespace then removes the finalizer |

---

## Availability & Scheduling Support

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Disruption** | `pkg/controller/disruption/disruption.go` | `DisruptionController` · `sync()` counts disrupted Pods and blocks voluntary evictions that would violate `minAvailable`/`maxUnavailable` in the `PodDisruptionBudget`. `syncDisruptedPods()` cleans up stale disruption records |
| **PodGroupProtection** | `pkg/controller/scheduling/podgroupprotection/` | Adds finalizers to `PodGroup` objects to prevent deletion while member Pods are running (gang scheduling) |

---

## Autoscaling

| Controller | Main File | What It Does |
| --- | --- | --- |
| **HorizontalPodAutoscaler** | `pkg/controller/podautoscaler/horizontal.go` | `HorizontalController` · `Run()` ticks every 15s and calls `reconcileAutoscaler()`. `computeReplicasForMetrics()` fetches current values via `metrics.go` and calculates desired replica count, then patches `.spec.replicas` on the target workload |

---

## Storage & Version Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Volume** | `pkg/controller/volume/` | Four sub-controllers: `persistentvolume/controller.go` (`PersistentVolumeController`, `syncVolume()`, `syncClaim()`) · `attachdetach/attach_detach_controller.go` (`AttachDetachController`) · `expand/expand_controller.go` (`ExpandController`) · `ephemeral/controller.go` (`ephemeralController`) |
| **StorageVersionGC** | `pkg/controller/storageversiongc/gc_controller.go` | `StorageVersionGCController` · Removes stale `StorageVersion` objects for API types that no longer exist in the cluster |
| **StorageVersionMigrator** | `pkg/controller/storageversionmigrator/storageversionmigrator.go` | `StaleVersionMigrator` · Rewrites objects in etcd to the latest storage version of their API type after an API server upgrade |

---

## History & Bootstrap

| Controller | Main File | What It Does |
| --- | --- | --- |
| **History** | `pkg/controller/history/controller_history.go` | `Interface` / `realHistory` · `CreateControllerRevision()` and `DeleteControllerRevision()` manage `ControllerRevision` snapshots for StatefulSet and DaemonSet rollbacks |
| **Bootstrap** | `pkg/controller/bootstrap/bootstrap_signer.go` | `BootstrapSigner` · Signs bootstrap tokens. `token_cleaner.go` runs `TokenCleaner` which deletes expired tokens from `kube-system` |

---

## Admission Policy Status

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

## Where controllers store state

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
# Node Controllers

| Controller | Main File | What It Does |
| --- | --- | --- |
| **NodeLifecycle** | `pkg/controller/nodelifecycle/node_lifecycle_controller.go` | `Controller` · `monitorNodeHealth()` runs on a timer checking heartbeat age per Node. `doNoScheduleTaintingPass()` adds taints, `doEvictionPass()` evicts Pods — failure is inferred from elapsed time, no “node went bad” event exists |
| **NodeIPAM** | `pkg/controller/nodeipam/nodeipam_controller.go` | `Controller` · `syncNodeCIDR()` allocates a Pod CIDR subnet to each Node. CIDR allocation strategies live in `pkg/controller/nodeipam/ipam/` |
| **TaintEviction** | `pkg/controller/tainteviction/taint_eviction.go` | `Controller` · `processPodOnNode()` evicts Pods from Nodes carrying `NoExecute` taints, respecting each Pod’s `tolerationSeconds` |
| **DeviceTaintEviction** | `pkg/controller/devicetainteviction/` | Evicts Pods when a DRA device they rely on becomes tainted (part of Dynamic Resource Allocation) |

---


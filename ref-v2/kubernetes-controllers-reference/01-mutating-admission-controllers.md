# Kubernetes Controllers Reference

[← Back to index](../README.md)

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

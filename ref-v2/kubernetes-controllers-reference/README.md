# Kubernetes Controllers Reference

[← Back to index](../README.md)

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

## Sections

- [Mutating Admission Controllers](01-mutating-admission-controllers.md)
- [Validating Admission Controllers](02-validating-admission-controllers.md)
- [Core Workload Controllers](03-core-workload-controllers.md)
- [Pod Lifecycle & Garbage Controllers](04-pod-lifecycle-garbage-controllers.md)
- [Node Controllers](05-node-controllers.md)
- [Endpoint & Service Controllers](06-endpoint-service-controllers.md)
- [RBAC & Security Controllers](07-rbac-security-controllers.md)
- [Resource Management Controllers](08-resource-management-controllers.md)
- [Namespace Controller](09-namespace-controller.md)
- [Availability & Scheduling Support](10-availability-scheduling-support.md)
- [Autoscaling](11-autoscaling.md)
- [Storage & Version Controllers](12-storage-version-controllers.md)
- [History & Bootstrap](13-history-bootstrap.md)
- [Admission Policy Status](14-admission-policy-status.md)
- [Where controllers store state](15-where-controllers-store-state.md)

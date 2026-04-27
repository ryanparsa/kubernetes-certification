# Kubernetes Controllers Reference

[← Back to index](../README.md)

---

## Namespace Controller

| Controller | Main File | What It Does |
| --- | --- | --- |
| **Namespace** | `pkg/controller/namespace/namespace_controller.go` | `NamespaceController` · `syncNamespaceFromKey()` delegates to `NamespacedResourcesDeleter` in `deletion/namespaced_resources_deleter.go` — deletes all objects inside a `Terminating` namespace then removes the finalizer |

---

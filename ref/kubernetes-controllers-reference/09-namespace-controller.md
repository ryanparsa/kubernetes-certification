# Kubernetes Controllers Reference — Namespace Controller

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


| Controller | Main File | What It Does |
| --- | --- | --- |
| **Namespace** | `pkg/controller/namespace/namespace_controller.go` | `NamespaceController` · `syncNamespaceFromKey()` delegates to `NamespacedResourcesDeleter` in `deletion/namespaced_resources_deleter.go` — deletes all objects inside a `Terminating` namespace then removes the finalizer |

---


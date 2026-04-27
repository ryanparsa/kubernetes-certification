# Kubernetes Controllers Reference — Storage & Version Controllers

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


| Controller | Main File | What It Does |
| --- | --- | --- |
| **Volume** | `pkg/controller/volume/` | Four sub-controllers: `persistentvolume/controller.go` (`PersistentVolumeController`, `syncVolume()`, `syncClaim()`) · `attachdetach/attach_detach_controller.go` (`AttachDetachController`) · `expand/expand_controller.go` (`ExpandController`) · `ephemeral/controller.go` (`ephemeralController`) |
| **StorageVersionGC** | `pkg/controller/storageversiongc/gc_controller.go` | `StorageVersionGCController` · Removes stale `StorageVersion` objects for API types that no longer exist in the cluster |
| **StorageVersionMigrator** | `pkg/controller/storageversionmigrator/storageversionmigrator.go` | `StaleVersionMigrator` · Rewrites objects in etcd to the latest storage version of their API type after an API server upgrade |

---


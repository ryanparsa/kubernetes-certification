# Kubernetes Controllers Reference — History & Bootstrap

> Part of [Kubernetes Controllers Reference](../Kubernetes Controllers Reference.md)


| Controller | Main File | What It Does |
| --- | --- | --- |
| **History** | `pkg/controller/history/controller_history.go` | `Interface` / `realHistory` · `CreateControllerRevision()` and `DeleteControllerRevision()` manage `ControllerRevision` snapshots for StatefulSet and DaemonSet rollbacks |
| **Bootstrap** | `pkg/controller/bootstrap/bootstrap_signer.go` | `BootstrapSigner` · Signs bootstrap tokens. `token_cleaner.go` runs `TokenCleaner` which deletes expired tokens from `kube-system` |

---


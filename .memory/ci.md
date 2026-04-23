# CI Memory

Every lab needs a workflow at `.github/workflows/<exam>-lab-<N>.yml`.
Use `helm/kind-action@v1` for cluster creation — do NOT manually install kind or kubectl.
The `cluster_name` in the workflow must match the `name` field in `kind-config.yaml`.
The tear-down step must always set `if: always()` so the cluster is deleted even when checks fail.
Workflow triggers on `push` and `pull_request` scoped to `['<exam>/<N>/**', '.github/workflows/<exam>-lab-<N>.yml']`.
Workflow job order: checkout → create cluster → apply solution (`fix.sh`) → run checks (`check.sh`) → tear down (`down.sh`).

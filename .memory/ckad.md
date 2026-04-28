# CKAD Lab Memory

## Known Labs

- ckad/23: kind-based lab — multi-container pod `logging-pod` in namespace `troubleshooting`; task = identify high-CPU container (`log-processor`) and set CPU limit `100m` / memory limit `50Mi`. Complete with full assets and CI workflow.

## Conventions

- After `kubectl create namespace <ns>`, always poll for the default service account before creating pods:
  ```bash
  until kubectl get serviceaccount default -n <ns> --no-headers 2>/dev/null | grep -q default; do sleep 1; done
  ```
  Omitting this causes `pods is forbidden: error looking up service account <ns>/default: serviceaccount "default" not found`.
- CI workflows (`ckad-lab-<N>.yml`) must include `permissions: contents: read` to satisfy the `actions/missing-workflow-permissions` CodeQL rule.
- In CI, `fix.sh` runs without `lab/kubeconfig.yaml` (no setup.sh is executed). Use the kubeconfig fallback pattern and `--ignore-not-found` for delete commands so fix.sh is safe in both local dev and CI contexts.

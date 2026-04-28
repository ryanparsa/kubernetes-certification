# CKA Lab Memory

## Known Labs

- cka/8: lima-based lab — worker node not joined, older K8s version; task = upgrade worker to match CP version + join via kubeadm. Complete with full assets.

## Duplicate Detection Notes

- Any lab asking to "join a worker node running an older Kubernetes version to the cluster using kubeadm" duplicates cka/8.
  - cka/87 was deleted (2026-04-28) as a duplicate of cka/8: identical task, no assets, answer.md was "TODO".
  - cka/189 was deleted as a duplicate of cka/10: identical task (RBAC processor in project-hamster), no assets, answer.md was "TODO".

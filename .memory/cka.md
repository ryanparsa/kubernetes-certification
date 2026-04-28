# CKA Lab Memory

## Known Labs

- cka/8: lima-based lab — worker node not joined, older K8s version; task = upgrade worker to match CP version + join via kubeadm. Complete with full assets.

## Duplicate Detection Notes

- Any lab asking to "join a worker node running an older Kubernetes version to the cluster using kubeadm" duplicates cka/8.
  - cka/87 was deleted (2026-04-28) as a duplicate of cka/8: identical task, no assets, answer.md was "TODO".
- Any lab asking to "change the Service CIDR to 11.96.0.0/12" duplicates cka/37.
  - cka/199 was deleted (2026-04-28) as a duplicate of cka/37: identical task, no assets, answer.md was "TODO".

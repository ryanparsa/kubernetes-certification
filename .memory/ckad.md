# CKAD Lab Memory

## Known Labs

- ckad/78: kind-based lab -- deployment rollout and rollback; task = create deploy with labels, update image, scale, rollback. Complete with full assets + CI.

## Duplicate Detection Notes

- ckad/65 covers rolling back a pre-existing broken deployment. ckad/78 covers the full lifecycle (create -> image update -> scale -> rollback) and is not a duplicate.

## Patterns

- Single control-plane kind cluster is sufficient for pure API-level deployment tasks (no node affinity/taints involved).
- After rollback with `--to-revision=1`, the original ReplicaSet is reused; check for `nginx:latest` in ReplicaSets to verify the image update step occurred.
# CKAD Lab Memory

## Known Labs

- ckad/28: kind-based lab — RBAC task: create ClusterRole `pod-reader` (get/watch/list pods) + ClusterRoleBinding `read-pods` (user jane). Complete with full assets and CI workflow.

## Duplicate Detection Notes

- ckad/124 covers ServiceAccount + ClusterRoleBinding to an *existing* ClusterRole (different from ckad/28 which creates both the ClusterRole and ClusterRoleBinding from scratch).

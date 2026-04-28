# Question 65

> **Solve this question on:** `ckad-lab-65`

A deployment called `my-revision-deployment` with revision history exists in namespace `revision-namespace`. The latest image update introduced a broken image tag.

1. Check the rollout status and revision history of `my-revision-deployment`.
2. Undo the deployment to the previous working revision.
3. Then roll back further to revision `2`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

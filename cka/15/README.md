# Question 15

> **Solve this question on:** the `cka-lab-15` kind cluster

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend Pod.

To prevent this create a NetworkPolicy called `np-backend` in Namespace `project-snake`. It should allow the `backend-*` Pods only to:

- Connect to `db1-*` Pods on port 1111
- Connect to `db2-*` Pods on port 2222

Use the `app` Pod labels in your policy.

> [!NOTE]
> All Pods in the Namespace run plain Nginx images. This allows simple connectivity tests like: `kubectl -n project-snake exec POD_NAME -- curl POD_IP:PORT`

> [!NOTE]
> For example, connections from `backend-*` Pods to `vault-*` Pods on port 3333 should no longer work

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

# Question 123

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend *Pod*. To prevent this create a *NetworkPolicy* called `np-backend` in *Namespace* `project-snake`. It should allow the backend *Pods* only to:

- connect to `db1` *Pods* on port `1111`
- connect to `db2` *Pods* on port `2222`

Use the `app` label of *Pods* in your policy.

After implementation, connections from backend *Pods* to `db1` *Pods* on port `3333` should no longer work.

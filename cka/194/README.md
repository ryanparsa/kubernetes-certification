# Question 194

> **Solve this question on:** `ssh cka4774`

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend *Pod*. To prevent this create a *NetworkPolicy* called `np-backend` in *Namespace* `project-snake`. It should allow the `backend-*` *Pods* only to:

- Connect to `db1-*` *Pods* on port `1111`
- Connect to `db2-*` *Pods* on port `2222`

Use the `app` *Pod* labels in your policy.

> [i] All Pods in the Namespace run plain Nginx images, allowing simple connectivity tests: exec into a Pod and `curl POD_IP:PORT`.

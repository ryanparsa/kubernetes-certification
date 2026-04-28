# Question 94

> **Solve this question on:** the `cka-lab` kind cluster

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend *Pod*.

To prevent this, create a *NetworkPolicy* named `np-backend` in *Namespace* `project-snake`. It should:

- Only allow backend *Pods* (label `app=backend`) to communicate with `db-service` in the same namespace on port `5432`
- Deny all other ingress and egress for backend *Pods*

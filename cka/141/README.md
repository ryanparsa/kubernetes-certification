# Question 141

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Use *Namespace* `project-tiger` for the following. Create a *Deployment* named `deploy-important` with `3` replicas. The *Deployment* and its *Pods* should have label `id=very-important`. The *Pods* should contain two containers:
- First named `container1` with image `nginx:1.17.6-alpine`
- Second named `container2` with image `google/pause`

There should be only **one** *Pod* of that *Deployment* running on **one** worker node. Because the *Deployment* has three replicas, one *Pod* should run on each worker node and the third won't be scheduled on the controlplane.

> [i] This simulates the behaviour of a *DaemonSet* but using a *Deployment* with a fixed number of replicas.

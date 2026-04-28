# Question 191

> **Solve this question on:** `ssh cka2506`

Implement the following in *Namespace* `project-tiger`:

- Create a *Deployment* named `deploy-important` with `3` replicas
- The *Deployment* and its *Pods* should have label `id=very-important`
- First container named `container1` with image `nginx:1.3-alpine`
- Second container named `container2` with image `google/pause`
- There should only ever be **one** *Pod* of that *Deployment* running on **one** worker node, use `topologyKey: kubernetes.io/hostname` for this

> [i] Because there are two worker nodes and the *Deployment* has three replicas the third *Pod* won't be scheduled. This simulates the behaviour of a *DaemonSet* but using a *Deployment* with a fixed number of replicas.

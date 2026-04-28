# Question 12

> **Solve this question on:** the `cka-lab-12` kind cluster

Implement the following in *Namespace* `project-tiger`:

- Create a *Deployment* named `deploy-important` with `3` replicas
- The *Deployment* and its *Pods* should have label `id=very-important`
- First container named `container1` with image `nginx:1-alpine`
- Second container named `container2` with image `registry.k8s.io/pause:3.9`
- There should only ever be **one** *Pod* of that *Deployment* running on **one** worker node, use `topologyKey: kubernetes.io/hostname` for this

> [i] Because there are two worker nodes and the *Deployment* has three replicas the result should be that the third *Pod* won't be scheduled. In a way this scenario simulates the behaviour of a *DaemonSet*, but using a *Deployment* with a fixed number of replicas

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

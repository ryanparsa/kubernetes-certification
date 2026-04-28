# Question 198

> **Solve this question on:** `ssh cka2506`

You're asked to confirm that `kube-proxy` is running correctly. Perform the following in *Namespace* `project-master`:

1. Create *Pod* `p2-pod` with image `nginx:1.5-alpine` and label `id=p2-pod`

1. Create *Service* `p2-service` which exposes the *Pod* internally in the cluster on port `3000→80`

1. Write the iptables rules of node `cka2506` belonging to the created *Service* `p2-service` into file `/opt/course/p2/iptables.txt`

1. Delete the *Service* and confirm that the iptables rules are gone again

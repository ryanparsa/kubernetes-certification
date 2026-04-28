# Question 141

> **Solve this question on:** `ckad-lab-22`

There is existing *Namespace* named `nemo`. Create a new *Pod* named `nemo-0` in *Namespace* `nemo` using image `nginx:1.14.2`.

The *Pod* should expose port 9090 on the container and set the `protocol` to `TCP`. Also add the label `id: nemo-0`.

Additionally, you should add a second *Pod* named `nemo-1` in the same *Namespace* using image `nginx:1.14.2`. Put it on the same node as `nemo-0` by using a `nodeSelector`. Write the name of the node to `/opt/course/22/node.txt`.

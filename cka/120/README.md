# Question 120

> **Solve this question on:** `kubectl config use-context k8s-c3-CCC`

Create a *Static Pod* named `my-static-pod` in *Namespace* `default` on `cluster1-master1`. It should be of image `nginx:1.16-alpine` and have resource requests for `10m` CPU and `20Mi` memory.

Then create a *NodePort* *Service* named `static-pod-service` which exposes that static pod on port `80` and check if it has *Endpoints* and if it's reachable through the cluster-internal IP address.

# Question 2

> **Solve this question on:** the `cka-lab` kind cluster

Create a *Static Pod* named `my-static-pod` in *Namespace* `default` on the *Node* `cka-lab-control-plane`. It should be of image `nginx:1-alpine` and have resource requests for `10m` CPU and `20Mi` memory.

Create a *NodePort Service* named `static-pod-service` which exposes that *Static Pod* on port `80`.

> [!NOTE]
> [i] For verification check if the new *Service* has one *Endpoint*. In the kind lab you can access the *Node* `cka-lab-control-plane` with `docker exec -it cka-lab-control-plane bash`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

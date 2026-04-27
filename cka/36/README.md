# Question 36

> **Solve this question on:** the "cka-lab-36" kind cluster

You're asked to confirm that kube-proxy is running correctly. For this perform the following in *Namespace* `project-hamster`:

1.  Create *Pod* `p2-pod` with image `nginx:1-alpine`
2.  Create *Service* `p2-service` which exposes the *Pod* internally in the cluster on port `3000->80`
3.  Write the iptables rules of the control-plane node belonging to the created *Service* `p2-service` into file `cka/36/lab/iptables.txt`
4.  Delete the *Service* and confirm that the iptables rules are gone again

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

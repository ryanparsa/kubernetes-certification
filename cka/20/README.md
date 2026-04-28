# Question 3

> **Solve this question on:** the `cka-lab` kind cluster

*Node* `cka-lab-worker` has been added to the cluster using kubeadm and TLS bootstrapping.

Find the *Issuer* and *Extended Key Usage* values on `cka-lab-worker` for:

1. Kubelet Client Certificate, the one used for outgoing connections to the kube-apiserver
2. Kubelet Server Certificate, the one used for incoming connections from the kube-apiserver

Write the information into file `cka/20/lab/certificate-info.txt`.

> [!NOTE]
> [i] You can connect to the worker node using `docker exec -it cka-lab-worker bash`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

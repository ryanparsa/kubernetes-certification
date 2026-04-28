# Question 14

Perform some tasks on cluster certificates:

> **Solve this question on:** `docker exec -it cka-lab-14-control-plane bash`

1. Check how long the kube-apiserver server certificate is valid using openssl or cfssl. Write the expiration date into `cka/14/lab/expiration`. Run the `kubeadm` command to list the expiration dates and confirm both methods show the same one
2. Write the `kubeadm` command that would renew the kube-apiserver certificate into `cka/14/lab/kubeadm-renew-certs.sh`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 193

> **Solve this question on:** `ssh cka412`

Perform some tasks on cluster certificates:

1. Check how long the `kube-apiserver` server certificate is valid using `openssl` or `cfssl`. Write the expiration date into `/opt/course/14/expiration.txt`. Also run the `kubeadm` command to list expiration dates and confirm both methods show the same date.

1. Write the `kubeadm` command that would renew the kube-apiserver certificate into `/opt/course/14/kubeadm-renew-certs.sh`

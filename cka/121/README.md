# Question 121

> **Solve this question on:** `ssh cluster1-master1`

Check how long the `kube-apiserver` server certificate is valid on `cluster1-master1`. Do this with `openssl` or `cfssl`. Write the expiration date into `/opt/course/22/expiration`.

Also run the correct `kubeadm` command to list the expiration dates and confirm both methods show the same date.

Write the correct `kubeadm` command that would renew the apiserver server certificate into `/opt/course/22/kubeadm-renew-certs.sh`.

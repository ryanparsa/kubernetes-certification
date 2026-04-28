# Question 152

> **Solve this question on:** `kubectl config use-context k8s-c2-AC`

Node `cluster2-worker1` has been added to the cluster using `kubeadm` and TLS bootstrapping.

Find the **Issuer** and **Extended Key Usage** values of the `cluster2-worker1`:

1. `kubelet` **client** certificate — the one used for outgoing connections to the `kube-apiserver`
2. `kubelet` **server** certificate — the one used for incoming connections from the `kube-apiserver`

Write the information into `/opt/course/23/certificate-info.txt`.

Compare the "Issuer" and "Extended Key Usage" fields of both certificates and make sense of these.

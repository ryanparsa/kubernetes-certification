# Question 14 | Check how long certificates are valid

Solve this question on: `ssh cka9412`

Perform some tasks on cluster certificates:

1. Check how long the kube-apiserver server certificate is valid using openssl or cfssl. Write the expiration date into `/opt/course/14/expiration`. Run the `kubeadm` command to list the expiration dates and confirm both methods show the same one
2. Write the `kubeadm` command that would renew the kube-apiserver certificate into `/opt/course/14/kubeadm-renew-certs.sh`

## Answer

First let's find that certificate:

```bash
➜ ssh cka9412

➜ candidate@cka9412:~$ sudo -i

➜ root@cka9412:~# find /etc/kubernetes/pki | grep apiserver
/etc/kubernetes/pki/apiserver-etcd-client.key
/etc/kubernetes/pki/apiserver-kubelet-client.key
/etc/kubernetes/pki/apiserver-etcd-client.crt
/etc/kubernetes/pki/apiserver.key
/etc/kubernetes/pki/apiserver-kubelet-client.crt
/etc/kubernetes/pki/apiserver.crt
```

Next we use openssl to find out the expiration date:

```bash
➜ root@cka9412:~# openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2
        Validity
            Not Before: Oct 29 14:14:27 2024 GMT
            Not After : Oct 29 14:19:27 2025 GMT
```

There we have it, so we write it in the required location:

```yaml
# cka9412:/opt/course/14/expiration
Oct 29 14:19:27 2025 GMT
```

And we use kubeadm to get the expiration to compare:

```bash
➜ root@cka9412:~# kubeadm certs check-expiration | grep apiserver
apiserver                  Oct 29, 2025 14:19 UTC   356d    ca         no      
apiserver-etcd-client      Oct 29, 2025 14:19 UTC   356d    etcd-ca    no      
apiserver-kubelet-client   Oct 29, 2025 14:19 UTC   356d    ca         no 
```

Looking good, both are the same.

And finally we write the command that would renew the kube-apiserver certificate into the requested location:

```bash
# cka9412:/opt/course/14/kubeadm-renew-certs.sh
kubeadm certs renew apiserver
```

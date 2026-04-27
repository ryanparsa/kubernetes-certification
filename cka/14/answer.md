## Answer

> **Local lab note:** The Kubernetes PKI certificates live inside the kind control-plane container. Exec into it first:
> ```bash
> docker exec -it cka-lab-14-control-plane bash
> ```
> All commands below are run inside that container.

First let's find that certificate:

```bash
find /etc/kubernetes/pki | grep apiserver
/etc/kubernetes/pki/apiserver-etcd-client.key
/etc/kubernetes/pki/apiserver-kubelet-client.key
/etc/kubernetes/pki/apiserver-etcd-client.crt
/etc/kubernetes/pki/apiserver.key
/etc/kubernetes/pki/apiserver-kubelet-client.crt
/etc/kubernetes/pki/apiserver.crt
```

Next we use openssl to find out the expiration date:

```bash
openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2
        Validity
            Not Before: Oct 29 14:14:27 2024 GMT
            Not After : Oct 29 14:19:27 2025 GMT
```

There we have it, so we write it in the required location:

```yaml
# cka/14/lab/expiration
Oct 29 14:19:27 2025 GMT
```

And we use kubeadm to get the expiration to compare:

```bash
kubeadm certs check-expiration | grep apiserver
apiserver                  Oct 29, 2025 14:19 UTC   356d    ca         no      
apiserver-etcd-client      Oct 29, 2025 14:19 UTC   356d    etcd-ca    no      
apiserver-kubelet-client   Oct 29, 2025 14:19 UTC   356d    ca         no 
```

Looking good, both are the same.

And finally we write the command that would renew the kube-apiserver certificate into the requested location:

```bash
# cka/14/lab/kubeadm-renew-certs.sh
kubeadm certs renew apiserver
```

## Killer.sh Checklist (Score: 0/4)

- [ ] File `cka/14/lab/expiration` exists and contains the apiserver certificate expiration date
- [ ] Expiration date in the file matches the `kubeadm certs check-expiration` output for `apiserver`
- [ ] File `cka/14/lab/kubeadm-renew-certs.sh` exists
- [ ] File contains the command `kubeadm certs renew apiserver`

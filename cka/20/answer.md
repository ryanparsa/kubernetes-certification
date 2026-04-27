## Answer

First we check the kubelet client certificate:

```bash
# Access the worker node
docker exec -it cka-lab-worker bash

find /var/lib/kubelet/pki
/var/lib/kubelet/pki
/var/lib/kubelet/pki/kubelet-client-2024-10-29-14-24-14.pem
/var/lib/kubelet/pki/kubelet.crt
/var/lib/kubelet/pki/kubelet.key
/var/lib/kubelet/pki/kubelet-client-current.pem

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep Issuer
        Issuer: CN = kubernetes

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep "Extended Key Usage" -A1
            X509v3 Extended Key Usage: 
                TLS Web Client Authentication
```

Next we check the kubelet server certificate:

```bash
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt | grep Issuer
        Issuer: CN = cka-lab-worker-ca@1730211854

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt | grep "Extended Key Usage" -A1
            X509v3 Extended Key Usage: 
                TLS Web Server Authentication
```

We see that the server certificate was generated on the worker node itself and the client certificate was issued by the Kubernetes api. The *Extended Key Usage* also shows if it's for client or server authentication.

The solution file should look something like this:

```
# cka/20/lab/certificate-info.txt
Issuer: CN = kubernetes
X509v3 Extended Key Usage: TLS Web Client Authentication
Issuer: CN = cka-lab-worker-ca@1730211854
X509v3 Extended Key Usage: TLS Web Server Authentication
```


## Killer.sh Checklist (Score: 4/4)

- [ ] Kubelet Client Certificate Issuer is correct
- [ ] Kubelet Client Certificate Extended Key Usage is correct
- [ ] Kubelet Server Certificate Issuer is correct
- [ ] Kubelet Server Certificate Extended Key Usage is correct

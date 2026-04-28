## Answer

**Reference:** <https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/>

> **Local lab note:** The Kubernetes PKI certificates live inside the kind control-plane container. Exec into it first:
> ```bash
> docker exec -it cka-lab-93-control-plane bash
> ```
> All commands below are run inside that container.

### 1. Find the API server certificate

```bash
find /etc/kubernetes/pki | grep apiserver
# /etc/kubernetes/pki/apiserver-etcd-client.key
# /etc/kubernetes/pki/apiserver-kubelet-client.key
# /etc/kubernetes/pki/apiserver-etcd-client.crt
# /etc/kubernetes/pki/apiserver.key
# /etc/kubernetes/pki/apiserver-kubelet-client.crt
# /etc/kubernetes/pki/apiserver.crt
```

### 2. Check the expiration date with openssl

```bash
openssl x509 -noout -enddate -in /etc/kubernetes/pki/apiserver.crt
# notAfter=Apr 27 06:12:47 2026 GMT
```

Reformat the date and write it to the required file:

```bash
mkdir -p /opt/course/14
openssl x509 -noout -enddate -in /etc/kubernetes/pki/apiserver.crt \
  | cut -d= -f2 \
  | xargs -I{} date -d "{}" "+%m/%d/%Y" \
  > /opt/course/14/expiration

cat /opt/course/14/expiration
# 04/27/2026
```

You can also confirm the same date with `kubeadm`:

```bash
kubeadm certs check-expiration | grep apiserver
# apiserver           Apr 27, 2026 06:12 UTC   364d  ca  no
```

### 3. Write the kubeadm renewal command

```bash
echo "kubeadm certs renew apiserver" > /opt/course/14/kubeadm-renew-certs.txt
```

## Checklist (Score: 0/4)

- [ ] File `/opt/course/14/expiration` exists inside the control-plane container
- [ ] The file contains the apiserver certificate expiration date in `mm/dd/YYYY` format
- [ ] File `/opt/course/14/kubeadm-renew-certs.txt` exists inside the control-plane container
- [ ] The file contains the command `kubeadm certs renew apiserver`

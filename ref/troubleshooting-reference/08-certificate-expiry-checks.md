# Kubernetes Troubleshooting Reference — 8. Certificate Expiry Checks

> Part of [Kubernetes Troubleshooting Reference](../Troubleshooting Reference.md)


```bash
# Check all certificate expiry at once (kubeadm clusters)
kubeadm certs check-expiration

# Output example:
# CERTIFICATE                EXPIRES                  RESIDUAL TIME   ...
# admin.conf                 Dec 23, 2025 16:21 UTC   364d            ...
# apiserver                  Dec 23, 2025 16:21 UTC   364d            ...
# etcd-ca                    Dec 21, 2033 16:21 UTC   9y              ...

# Renew all certificates
kubeadm certs renew all

# After renewal, restart static pods (they embed the certs)
# Move manifests out and back in:
cd /etc/kubernetes/manifests
mv kube-apiserver.yaml /tmp/
mv kube-controller-manager.yaml /tmp/
mv kube-scheduler.yaml /tmp/

# Wait for pods to stop
watch crictl ps

# Move back
mv /tmp/kube-apiserver.yaml .
mv /tmp/kube-controller-manager.yaml .
mv /tmp/kube-scheduler.yaml .

# Update local kubeconfig
cp /etc/kubernetes/admin.conf ~/.kube/config

# Check kubelet client cert (auto-rotated — just verify it's current)
ls -la /var/lib/kubelet/pki/
# kubelet-client-current.pem should point to a recent dated file
openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem \
  -noout -dates

# Inspect any certificate
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | \
  grep -E 'Subject:|Not After|DNS:|IP Address'
```

---


# Diagnostic Commands

### Inspect a certificate with openssl

```bash
# View full certificate details
openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt

# Check expiration date only
openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2

# Check issuer (who signed the cert)
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep Issuer

# Check Extended Key Usage (client vs. server auth)
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep "Extended Key Usage" -A1
```

**Extended Key Usage values:**

| Value | Meaning |
|---|---|
| `TLS Web Client Authentication` | Client cert — used for outgoing connections (e.g. kubelet → API Server) |
| `TLS Web Server Authentication` | Server cert — used for incoming connections (e.g. API Server → kubelet) |

**Issuer patterns:**

| Issuer CN | What it means |
|---|---|
| `kubernetes` | Signed by the cluster CA (`/etc/kubernetes/pki/ca.crt`) — standard for kubeadm-bootstrapped certs |
| `<node>-ca@<timestamp>` | Self-signed by the kubelet on that node — typical for kubelet serving certs when `serverTLSBootstrap` is not enabled |

### Check all cert expiry with kubeadm

```bash
# List expiry dates for all control-plane certs and kubeconfigs
kubeadm certs check-expiration

# Filter to a specific cert
kubeadm certs check-expiration | grep apiserver
```

Sample output:

```
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Oct 29, 2025 14:19 UTC   356d            ca                      no
apiserver                  Oct 29, 2025 14:19 UTC   356d            ca                      no
apiserver-etcd-client      Oct 29, 2025 14:19 UTC   356d            etcd-ca                 no
apiserver-kubelet-client   Oct 29, 2025 14:19 UTC   356d            ca                      no
controller-manager.conf    Oct 29, 2025 14:19 UTC   356d            ca                      no
etcd-healthcheck-client    Oct 29, 2025 14:19 UTC   356d            etcd-ca                 no
etcd-peer                  Oct 29, 2025 14:19 UTC   356d            etcd-ca                 no
etcd-server                Oct 29, 2025 14:19 UTC   356d            etcd-ca                 no
front-proxy-client         Oct 29, 2025 14:19 UTC   356d            front-proxy-ca          no
scheduler.conf             Oct 29, 2025 14:19 UTC   356d            ca                      no
```

### Renew a single certificate

```bash
# Renew only the apiserver cert (instead of all)
kubeadm certs renew apiserver
```

> Use `kubeadm certs renew <name>` when only one cert is expiring to minimise disruption. Run `kubeadm certs check-expiration` first to see the cert name.

---


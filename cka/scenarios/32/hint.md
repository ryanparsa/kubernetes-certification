# Hints — Task 32

## Hint 1
Check the controller manager logs:
```bash
kubectl logs -n kube-system kube-controller-manager-controlplane
# or
tail /var/log/containers/kube-controller-manager-controlplane_kube-system_*.log
```
What file is it failing to find?

## Hint 2
`ll /etc/kubernetes/pki/` — is `ca.crt` present?
Compare what's there against what a healthy cluster has.

## Hint 3
`ca.crt` is missing but `ca.key` exists.
`kubeadm` can regenerate the certificate from the existing key.

## Solution

```bash
kubeadm init phase certs ca

ll /etc/kubernetes/pki/ca*
# ca.crt should now exist

kubectl -n kube-system get pod kube-controller-manager-controlplane
# Static pod restarts automatically within ~30s — Expected: 1/1 Running
```

**⚠️ Watch Out:** `kubeadm init phase certs ca` only regenerates `ca.crt` if `ca.key`
is present. If both are missing, recovery is more involved (requires a full PKI rebuild).

**Reflex:** Control plane CrashLoopBackOff → check logs → missing cert/file →
look in `/etc/kubernetes/pki/` → regenerate with `kubeadm init phase certs <cert-name>`.

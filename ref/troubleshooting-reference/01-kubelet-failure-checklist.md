# Kubernetes Troubleshooting Reference — 1. Kubelet Failure Checklist

> Part of [Kubernetes Troubleshooting Reference](../Troubleshooting Reference.md)


### Symptoms
- Node shows `NotReady`
- Pods stuck in `Pending` or never get assigned to the node
- `kubectl get nodes` shows the node with `STATUS=NotReady`

### Diagnosis steps

```bash
# 1. Check kubelet service status
systemctl status kubelet
journalctl -u kubelet -n 100 --no-pager

# 2. Check if kubelet is running at all
ps aux | grep kubelet

# 3. Common config file locations
cat /var/lib/kubelet/config.yaml          # kubelet runtime config
cat /etc/kubernetes/kubelet.conf          # kubeconfig kubelet uses to reach API server
cat /var/lib/kubelet/kubeadm-flags.env    # extra CLI flags from kubeadm

# 4. Check for typos in config files
kubelet --config /var/lib/kubelet/config.yaml --dry-run  # not available; parse errors shown on start

# 5. Reload and restart
systemctl daemon-reload
systemctl restart kubelet
systemctl enable kubelet      # ensure it starts on reboot

# 6. Verify after restart
systemctl status kubelet      # should show Active: active (running)
kubectl get node <node>       # should return to Ready
```

### Common kubelet failure causes

| Symptom in logs | Likely cause |
|---|---|
| `failed to run Kubelet: invalid kubeconfig` | Corrupted or wrong `kubelet.conf` path |
| `connection refused` to API server | API server not running, or wrong `--server` URL |
| `x509: certificate has expired` | Kubelet client cert expired — renew with `kubeadm certs renew all` |
| `no such file or directory` for config | Config path in `kubeadm-flags.env` is wrong |
| `failed to create containerd task` | Container runtime issue — check containerd/docker status |
| `node not found` | Node was deleted from API while kubelet was down — re-join the node |

---


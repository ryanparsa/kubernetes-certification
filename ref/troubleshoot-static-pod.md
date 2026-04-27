# Static Pod Debugging

Static pods are managed by kubelet directly from manifests in
`/etc/kubernetes/manifests/`. They don't appear as normal pod objects.

```bash
# List static pod manifests
ls /etc/kubernetes/manifests/
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

# Edit a static pod (kubelet auto-restarts it within seconds)
vim /etc/kubernetes/manifests/kube-apiserver.yaml

# Temporarily disable a static pod (move it out of the watched dir)
mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/

# Re-enable
mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/

# Watch kubelet pick up the change
journalctl -u kubelet -f

# Static pod logs (find the pod name first — it includes the node name)
kubectl -n kube-system get pod
kubectl -n kube-system logs kube-apiserver-<node>

# If API server is down, check logs directly
crictl ps -a | grep apiserver
crictl logs <container-id>
```

### Common static pod problems

| Problem | Check |
|---|---|
| API server not starting | Wrong `--etcd-servers` URL, bad cert path, port conflict |
| etcd not starting | Wrong data dir, corrupted data directory |
| Scheduler/controller not starting | Wrong kubeconfig path (`--kubeconfig` flag) |
| Static pod keeps restarting | Check manifest syntax; `kubelet` logs for errors |

---


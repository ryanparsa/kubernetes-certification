# Checking Control Plane Component Health

```bash
# Check how components are running (static pods vs systemd services)
kubectl -n kube-system get pods | grep -E 'apiserver|scheduler|controller|etcd'

# For kubeadm clusters — all are static pods
# Check their logs
kubectl -n kube-system logs kube-apiserver-<node>
kubectl -n kube-system logs kube-scheduler-<node>
kubectl -n kube-system logs kube-controller-manager-<node>
kubectl -n kube-system logs etcd-<node>

# Component status (deprecated but still works for quick check)
kubectl get componentstatuses

# Check API server health endpoints
curl -k https://localhost:6443/healthz
curl -k https://localhost:6443/readyz
curl -k https://localhost:6443/livez
```

---


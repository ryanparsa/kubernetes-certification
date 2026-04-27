# Kubernetes Scheduling Reference

[← Back to index](../README.md)

---

## 7. Manual Scheduling (when kube-scheduler is stopped)

When the scheduler is down, pods remain `Pending`. Assign them manually:

```bash
# Stop the scheduler (move manifest out of watched dir)
mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/kube-scheduler.yaml

# Manually schedule a pod by setting nodeName via a Binding object
kubectl apply -f - <<EOF
apiVersion: v1
kind: Binding
metadata:
  name: my-pod
  namespace: default
target:
  apiVersion: v1
  kind: Node
  name: worker-1
EOF

# Or: patch the pod's nodeName directly
kubectl patch pod my-pod -p '{"spec":{"nodeName":"worker-1"}}'

# Restart the scheduler
mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/kube-scheduler.yaml
```

---

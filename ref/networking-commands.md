# Useful Commands

```bash
# List all Services with ClusterIP and ports
kubectl get svc -A

# Describe a Service (see Endpoints)
kubectl describe svc my-service -n my-app

# Check endpoints for a Service
kubectl get endpoints my-service -n my-app

# Test connectivity from a debug pod
kubectl run -it --rm test --image=busybox:1.35 -- \
  wget -qO- http://my-service.my-app.svc.cluster.local

# List NetworkPolicies
kubectl get networkpolicies -A

# Describe a NetworkPolicy
kubectl describe networkpolicy np-backend -n project-snake

# Check which pods match a NetworkPolicy selector
kubectl -n my-app get pods -l app=backend
```

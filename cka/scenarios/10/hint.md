# Hints — Task 10

## Hint 1
```bash
kubectl -n kube-system get deployment coredns
```
What's the replica count?

## Solution

```bash
kubectl -n kube-system scale deployment coredns --replicas=2
kubectl -n kube-system rollout status deployment/coredns
# verify
kubectl run dnstest --rm -i --restart=Never --image=busybox:1.36 -- \
  nslookup web.probe.svc.cluster.local
```

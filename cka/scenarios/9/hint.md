# Hints — Task 9

## Hint 1
```bash
kubectl describe node cka-task-9-worker | grep -i 'condition\|reason' -A2
```
The conditions will say `Kubelet stopped posting node status`.

## Hint 2
Get into the worker and check the kubelet service:
```bash
docker exec -it cka-task-9-worker bash
systemctl status kubelet
journalctl -u kubelet -n 30 --no-pager
```

## Solution

```bash
docker exec cka-task-9-worker systemctl start kubelet
# Wait ~30s, then verify
kubectl get nodes
kubectl rollout status deployment/hello
```

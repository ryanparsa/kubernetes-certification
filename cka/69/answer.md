## Answer

**Reference:** <https://kubernetes.io/docs/concepts/services-networking/network-policies/>

### Create pods and services

```bash
kubectl run consumer --image=nginx --labels="run=consumer"
kubectl expose pod consumer --port=80

kubectl run producer --image=nginx --labels="run=producer"
kubectl expose pod producer --port=80

kubectl run web --image=nginx --labels="run=web"
kubectl expose pod web --port=80
```

### Verify communication before the policy

```bash
kubectl exec producer -- curl -s --max-time 5 http://consumer  # success
kubectl exec web -- curl -s --max-time 5 http://consumer        # success (should fail after policy)
```

### Create the NetworkPolicy

```yaml
# lab/limit-consumer.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: limit-consumer
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: consumer
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: producer
```

```bash
kubectl apply -f lab/limit-consumer.yaml
```

### Verify communication after the policy

```bash
kubectl exec producer -- curl -s --max-time 5 http://consumer  # success
kubectl exec web -- curl -s --max-time 5 http://consumer        # timeout / connection refused
```

## Checklist (Score: 0/5)

- [ ] Pods `consumer`, `producer`, and `web` are running
- [ ] Services `consumer`, `producer`, and `web` exist on port `80`
- [ ] NetworkPolicy `limit-consumer` selects pods with label `run=consumer`
- [ ] NetworkPolicy allows ingress only from pods with label `run=producer`
- [ ] Pod `web` cannot reach `consumer`; pod `producer` can reach `consumer`

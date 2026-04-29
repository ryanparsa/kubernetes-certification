## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create deployment and ClusterIP service

```bash
kubectl create deployment frontend --image=nginx --replicas=2 --port=80
kubectl expose deployment frontend --name=frontend-svc --port=80 --target-port=80 --type=ClusterIP
kubectl get svc frontend-svc
```

### Change service type to NodePort

```bash
kubectl patch svc frontend-svc -p '{"spec":{"type":"NodePort"}}'
kubectl get svc frontend-svc
```

The service will now have a `NodePort` assigned (in the 30000--32767 range).

### Create NetworkPolicy allow-labeled

```yaml
# lab/allow-labeled.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-labeled
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: granted
```

```bash
kubectl apply -f lab/allow-labeled.yaml
kubectl get networkpolicy allow-labeled
kubectl describe networkpolicy allow-labeled
```

### Verify

```bash
# Confirm service type
kubectl get svc frontend-svc -o jsonpath='{.spec.type}'

# Confirm NetworkPolicy targets correct pods
kubectl get networkpolicy allow-labeled -o jsonpath='{.spec.podSelector}'
kubectl get networkpolicy allow-labeled -o jsonpath='{.spec.ingress[0].from[0].podSelector}'
```

## Checklist (Score: 0/3)

- [ ] Deployment `frontend` running with 2 replicas and Service `frontend-svc` created as ClusterIP
- [ ] Service `frontend-svc` changed to type `NodePort`
- [ ] NetworkPolicy `allow-labeled` allows ingress to `app=frontend` pods only from `access=granted` pods

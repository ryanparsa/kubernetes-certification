# Hints — Task 30

## Hint 1
`kubectl -n prod get endpoints` — is `backend` showing an IP or `<none>`?
`<none>` means the Service selector matches zero pods.

## Hint 2
`kubectl -n prod get svc backend -o yaml` — check `spec.selector`.
`kubectl -n prod get deployment backend -o yaml` — check `spec.template.metadata.labels`.
Compare them.

## Hint 3
The Service selector is `app: backend-svc` but the pod label is `app: backend`.
Change the Service selector to match the pod label.

## Solution

```bash
kubectl -n prod patch service backend --type=json \
  -p='[{"op":"replace","path":"/spec/selector/app","value":"backend"}]'

kubectl -n prod get endpoints backend
# Expected: 10.244.x.x:8080
```

**Reflex:** Service not routing? Check endpoints first.
`<none>` = selector mismatch — diff `svc.spec.selector` against pod labels.

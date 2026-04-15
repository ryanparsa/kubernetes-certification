# Hints — Task 4

## Hint 1
Imperative generation works for all three:
```bash
kubectl -n dev create serviceaccount dev-reader
kubectl -n dev create role pod-reader --verb=get,list,watch --resource=pods
kubectl -n dev create rolebinding dev-reader-binding \
  --role=pod-reader --serviceaccount=dev:dev-reader
```

## Hint 2
Verify with `kubectl auth can-i`:
```bash
kubectl auth can-i list pods   --as=system:serviceaccount:dev:dev-reader -n dev   # yes
kubectl auth can-i list pods   --as=system:serviceaccount:dev:dev-reader -n prod  # no
kubectl auth can-i delete pods --as=system:serviceaccount:dev:dev-reader -n dev   # no
```

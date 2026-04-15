# Hints — Task 6

## Hint 1
```bash
kubectl -n shop get endpoints broken-svc
```
Empty endpoints means the Service's `selector` doesn't match any pod labels.

## Hint 2
Compare:
```bash
kubectl -n shop get svc broken-svc -o jsonpath='{.spec.selector}'
kubectl -n shop get pods --show-labels
```
The Service selects `app=webapp` but the pods carry `app=web`.

## Solution

```bash
kubectl -n shop patch svc broken-svc --type=merge -p '{"spec":{"selector":{"app":"web"}}}'
kubectl -n shop get endpoints broken-svc
```

# Hints — Task 18

## Hint 1
Patch the deployment to add resources:
```bash
kubectl -n web patch deployment shop --type=json -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/resources","value":{"requests":{"cpu":"200m"},"limits":{"cpu":"500m"}}}
]'
```

## Hint 2
Imperative HPA creation supports v2:
```bash
kubectl -n web autoscale deployment shop --min=2 --max=6 --cpu-percent=60
```
This creates an `autoscaling/v2` HPA targeting `averageUtilization: 60`.

## Solution

```bash
kubectl -n web patch deployment shop --type=json -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/resources","value":{"requests":{"cpu":"200m"},"limits":{"cpu":"500m"}}}
]'
kubectl -n web autoscale deployment shop --name=shop-hpa --min=2 --max=6 --cpu-percent=60
kubectl -n web get hpa shop-hpa
```

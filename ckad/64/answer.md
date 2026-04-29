## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/jsonpath/

### Create the namespace and pod

```bash
kubectl create namespace json-namespace
kubectl run json-pod --image=nginx -n json-namespace
kubectl wait pod/json-pod -n json-namespace --for=condition=Ready --timeout=60s
```

### Retrieve the hostIP using JSONPath

```bash
kubectl get pod json-pod -n json-namespace -o jsonpath='{.status.hostIP}'
```

Alternative (recursive search):

```bash
kubectl get pod json-pod -n json-namespace -o jsonpath='{..hostIP}'
```

### Understanding the path

```bash
# Inspect pod status fields
kubectl explain pod.status | grep hostIP
```

The field path is: `pod -> .status -> .hostIP`

## Checklist (Score: 0/2)

- [ ] Pod `json-pod` exists in `json-namespace` and is `Running`
- [ ] `hostIP` extracted using `jsonpath={.status.hostIP}`

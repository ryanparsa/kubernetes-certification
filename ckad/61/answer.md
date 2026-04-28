## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/service/

### Create the namespace

```bash
kubectl create namespace service-namespace
```

### Create the Pod

```bash
kubectl run service-pod --image=nginx --port=80 --labels="tier=web" -n service-namespace
kubectl wait pod/service-pod -n service-namespace --for=condition=Ready --timeout=60s
```

### Create the Service

```bash
kubectl expose pod service-pod --port=8080 --target-port=80 --name=my-service -n service-namespace
```

### Verify

```bash
kubectl get service my-service -n service-namespace
kubectl get endpoints my-service -n service-namespace
```

Expected output shows `ClusterIP` type and `8080/TCP` port with the pod IP as endpoint.

## Checklist (Score: 0/3)

- [ ] Pod `service-pod` exists in `service-namespace` with label `tier=web` and is `Running`
- [ ] Service `my-service` exists in `service-namespace` of type `ClusterIP`
- [ ] Service `my-service` exposes port `8080` and forwards to pod port `80`

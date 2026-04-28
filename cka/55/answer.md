## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

### Create the namespace

```bash
kubectl create namespace stateful
```

### Create the headless Service and StatefulSet

```yaml
# lab/55-statefulset.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-svc
  namespace: stateful
spec:
  clusterIP: None
  selector:
    app: web
  ports:
  - port: 80
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
  namespace: stateful
spec:
  serviceName: web-svc
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: cold
      resources:
        requests:
          storage: 1Gi
```

```bash
kubectl apply -f lab/55-statefulset.yaml
kubectl wait statefulset web -n stateful --for=jsonpath='{.status.readyReplicas}'=3 --timeout=120s
```

### Verify

```bash
kubectl get statefulset web -n stateful
kubectl get pods -n stateful
kubectl get svc web-svc -n stateful
# Pods are accessible as web-0.web-svc, web-1.web-svc, web-2.web-svc
```

## Checklist (Score: 0/7)

- [ ] Service `web-svc` is headless (`clusterIP: None`) in `stateful` namespace
- [ ] StatefulSet `web` exists in `stateful` namespace
- [ ] StatefulSet has `3` replicas using `nginx` image
- [ ] StatefulSet references `web-svc` as its serviceName
- [ ] Volumes are mounted at `/usr/share/nginx/html`
- [ ] VolumeClaimTemplate uses StorageClass `cold` with `1Gi`
- [ ] All 3 pods are `Running`

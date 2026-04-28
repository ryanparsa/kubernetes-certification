## Answer

**Reference:** https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/

### Create the directory structure

```bash
mkdir -p /tmp/exam/kustomize/base
mkdir -p /tmp/exam/kustomize/overlays/production
```

### Create base files

```yaml
# /tmp/exam/kustomize/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: nginx-index
          mountPath: /usr/share/nginx/html/
      volumes:
      - name: nginx-index
        configMap:
          name: nginx-config
```

```yaml
# /tmp/exam/kustomize/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
```

### Create overlay files

```yaml
# /tmp/exam/kustomize/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: kustomize
bases:
- ../../base
patches:
- patch: |
    - op: replace
      path: /spec/replicas
      value: 3
  target:
    kind: Deployment
    name: nginx
commonLabels:
  environment: production
configMapGenerator:
- name: nginx-config
  literals:
  - index.html=Welcome to Production
```

### Apply the overlay

```bash
kubectl create namespace kustomize
kubectl apply -k /tmp/exam/kustomize/overlays/production/
```

### Verify

```bash
kubectl get deployments -n kustomize
kubectl get configmaps -n kustomize
kubectl get pods -n kustomize
```

## Checklist (Score: 0/6)

- [ ] Base deployment `nginx` exists with `2` replicas
- [ ] Overlay increases replicas to `3`
- [ ] Overlay adds label `environment=production`
- [ ] ConfigMap `nginx-config` has key `index.html` with value `Welcome to Production`
- [ ] ConfigMap is mounted as volume `nginx-index` at `/usr/share/nginx/html/`
- [ ] Resources are deployed in the `kustomize` namespace

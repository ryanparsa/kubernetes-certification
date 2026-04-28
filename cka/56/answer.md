## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/

### Create the namespace

```bash
kubectl create namespace dns-debug
```

### Create the Deployment, Service, Pod, and ConfigMap

```yaml
# lab/56-dns-debug.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: dns-debug
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc
  namespace: dns-debug
spec:
  selector:
    app: web-app
  ports:
  - port: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: dns-test
  namespace: dns-debug
spec:
  containers:
  - name: busybox
    image: busybox
    command:
    - sh
    - -c
    - "wget -qO- http://web-svc && wget -qO- http://web-svc.dns-debug.svc.cluster.local && sleep 36000"
  dnsConfig:
    searches:
    - dns-debug.svc.cluster.local
    - svc.cluster.local
    - cluster.local
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: dns-config
  namespace: dns-debug
data:
  search-domains: |
    search dns-debug.svc.cluster.local svc.cluster.local cluster.local
```

```bash
kubectl apply -f lab/56-dns-debug.yaml
kubectl wait deployment web-app -n dns-debug --for=condition=Available --timeout=60s
```

### Verify

```bash
kubectl get deployment web-app -n dns-debug
kubectl get svc web-svc -n dns-debug
kubectl get pod dns-test -n dns-debug
kubectl logs dns-test -n dns-debug
```

## Checklist (Score: 0/6)

- [ ] Deployment `web-app` has `3` replicas in `dns-debug` namespace
- [ ] Service `web-svc` exposes `web-app` on port `80`
- [ ] Pod `dns-test` exists in `dns-debug` namespace
- [ ] Pod resolves `web-svc` short name via custom dnsConfig searches
- [ ] Pod resolves FQDN `web-svc.dns-debug.svc.cluster.local`
- [ ] ConfigMap `dns-config` exists with custom search domains

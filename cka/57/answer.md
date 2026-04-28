## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/

### Create the namespace

```bash
kubectl create namespace dns-config
```

### Create the Deployment, Service, and DNS tester Pod

```yaml
# lab/57-dns-config.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dns-app
  namespace: dns-config
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dns-app
  template:
    metadata:
      labels:
        app: dns-app
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: dns-svc
  namespace: dns-config
spec:
  selector:
    app: dns-app
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: dns-tester
  namespace: dns-config
spec:
  containers:
  - name: dns-tester
    image: infoblox/dnstools
    command:
    - sh
    - -c
    - |
      nslookup dns-svc > /tmp/dns-test.txt
      nslookup dns-svc.dns-config.svc.cluster.local >> /tmp/dns-test.txt
      sleep 3600
```

```bash
kubectl apply -f lab/57-dns-config.yaml
kubectl wait deployment dns-app -n dns-config --for=condition=Available --timeout=60s
kubectl wait pod dns-tester -n dns-config --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec -n dns-config dns-tester -- cat /tmp/dns-test.txt
kubectl get svc dns-svc -n dns-config
kubectl get endpoints dns-svc -n dns-config
```

## Checklist (Score: 0/5)

- [ ] Deployment `dns-app` has `2` replicas in `dns-config` namespace
- [ ] Service `dns-svc` exposes `dns-app` on port `80`
- [ ] Pod `dns-tester` exists in `dns-config` namespace using `infoblox/dnstools`
- [ ] Pod resolves short DNS `dns-svc` and FQDN `dns-svc.dns-config.svc.cluster.local`
- [ ] Results are stored in `/tmp/dns-test.txt` inside the pod

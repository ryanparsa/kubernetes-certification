# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 3. StatefulSet

Manages stateful applications where each pod needs:
- A stable, unique network identity
- Stable persistent storage
- Ordered, graceful deployment and scaling

### Key characteristics

- Pods are named `<name>-0`, `<name>-1`, `<name>-2`, etc.
- Scale-up is sequential (0 → 1 → 2); scale-down is reverse (2 → 1 → 0)
- Each pod gets its own PVC from `volumeClaimTemplates`
- Requires a **Headless Service** for stable DNS names

### StatefulSet + Headless Service

```yaml
# Headless Service — required for stable pod DNS names
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: my-db
spec:
  clusterIP: None            # headless
  selector:
    app: mysql
  ports:
  - port: 3306
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  namespace: my-db
spec:
  serviceName: mysql          # must match the Headless Service name
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      storageClassName: fast
      resources:
        requests:
          storage: 10Gi
```

### Stable DNS names

```
mysql-0.mysql.my-db.svc.cluster.local
mysql-1.mysql.my-db.svc.cluster.local
mysql-2.mysql.my-db.svc.cluster.local
```

```bash
# Scale down StatefulSet (wait for ordered termination)
kubectl scale statefulset mysql --replicas=1 -n my-db
kubectl rollout status statefulset/mysql -n my-db
```

---

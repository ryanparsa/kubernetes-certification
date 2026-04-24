# Kubernetes Workloads Reference

Reference for all workload types: Pod QoS, Deployments, StatefulSets, DaemonSets,
Jobs, CronJobs, HPA, and init/sidecar containers.

---

## 1. Pod QoS Classes

Kubernetes assigns a QoS class to each pod based on resource requests and limits.
This determines eviction order when a node is under memory pressure.

### QoS classes

| Class | Condition | Eviction priority |
|---|---|---|
| `Guaranteed` | Every container has equal `requests` and `limits` for CPU and memory | Last to be evicted |
| `Burstable` | At least one container has a request or limit set, but not Guaranteed | Middle |
| `BestEffort` | No container has any requests or limits | First to be evicted |

### Examples

```yaml
# Guaranteed — requests == limits for ALL containers
resources:
  requests:
    cpu: "500m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

```yaml
# Burstable — requests set but not matching limits
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

```yaml
# BestEffort — nothing set
resources: {}
```

```bash
# Check QoS class
kubectl get pod my-pod -o jsonpath='{.status.qosClass}'

# List pods sorted by QoS (BestEffort first)
kubectl get pods -A -o custom-columns=\
NAME:.metadata.name,QOS:.status.qosClass,NS:.metadata.namespace
```

> Pods in the `Guaranteed` class also get dedicated CPU (no throttling) when the CPU
> manager policy is set to `static`.

---

## 2. Deployments

Manages a ReplicaSet and provides rolling updates and rollbacks.

### Deployment strategies

| Strategy | Effect |
|---|---|
| `RollingUpdate` (default) | Gradually replaces old pods; zero downtime if configured correctly |
| `Recreate` | Terminates ALL old pods before creating new ones; causes downtime |

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1     # max pods that can be unavailable during rollout
      maxSurge: 1           # max extra pods created above desired replica count
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: app
        image: my-image:v2
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
```

```yaml
strategy:
  type: Recreate            # simpler; all old pods killed before new ones start
```

### Rollout commands

```bash
# Check rollout status
kubectl rollout status deployment/api-gateway -n my-app

# View rollout history
kubectl rollout history deployment/api-gateway -n my-app

# Rollback to previous version
kubectl rollout undo deployment/api-gateway -n my-app

# Rollback to a specific revision
kubectl rollout undo deployment/api-gateway --to-revision=2 -n my-app

# Pause a rollout
kubectl rollout pause deployment/api-gateway -n my-app

# Resume a rollout
kubectl rollout resume deployment/api-gateway -n my-app

# Scale
kubectl scale deployment api-gateway --replicas=5 -n my-app
```

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

## 4. DaemonSet

Runs exactly one pod on every (matching) node. Common for log collectors, monitoring
agents, network plugins.

See the **Scheduling Reference** for scheduling details (taints, nodeSelector).

```bash
# Check DaemonSet status
kubectl -n kube-system get daemonset

# Restart all DaemonSet pods (triggers rolling update)
kubectl -n kube-system rollout restart daemonset fluentd

# Check rollout status
kubectl -n kube-system rollout status daemonset fluentd
```

---

## 5. Jobs

A Job runs one or more pods to completion (exit code 0).

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  completions: 1          # total pods that must succeed
  parallelism: 1          # pods running in parallel
  backoffLimit: 4         # retry limit before marking Job as failed
  activeDeadlineSeconds: 600
  template:
    spec:
      restartPolicy: Never   # Never or OnFailure (not Always)
      containers:
      - name: migrate
        image: my-migrator:latest
        command: ["python", "migrate.py"]
```

```bash
# Check Job status
kubectl get job db-migrate
kubectl describe job db-migrate

# Get logs from a completed Job pod
kubectl logs -l job-name=db-migrate
```

---

## 6. CronJobs

Runs a Job on a schedule (cron syntax).

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"            # every day at 02:00
  timeZone: "UTC"
  concurrencyPolicy: Forbid        # Allow | Forbid | Replace
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 300     # how late a missed run can start
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["/backup.sh"]
```

| `concurrencyPolicy` | Effect |
|---|---|
| `Allow` | Multiple Job runs can overlap |
| `Forbid` | Skip new run if previous is still running |
| `Replace` | Cancel previous run and start new one |

---

## 7. Horizontal Pod Autoscaler (HPA)

Scales a Deployment (or StatefulSet/ReplicaSet) based on metrics.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
  namespace: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50    # target 50% of CPU requests across all pods
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 200Mi
```

```bash
# Create HPA imperatively
kubectl autoscale deployment api-gateway \
  --cpu-percent=50 --min=2 --max=10 -n my-app

# Check HPA status
kubectl get hpa -n my-app
kubectl describe hpa api-gateway -n my-app

# HPA requires metrics-server to be installed
kubectl top pods -n my-app
```

> If the Deployment also has `spec.replicas` set, the HPA will immediately override it
> to `minReplicas`. Remove `replicas:` from the Deployment spec to avoid conflicts.

---

## 8. Init Containers

Run to completion **before** any app containers start. Used for setup tasks (wait for DB,
fetch secrets, populate volumes, etc.).

```yaml
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.35
    command: ['sh', '-c',
      'until nc -z mysql.my-db.svc.cluster.local 3306; do sleep 2; done']
  - name: db-migrate
    image: my-migrator:latest
    command: ["python", "migrate.py"]
  containers:
  - name: app
    image: my-app:v1
```

- Init containers run sequentially (in order)
- Each must exit 0 before the next starts
- If an init container fails, the pod restarts it (respecting `restartPolicy`)
- App containers don't start until all init containers succeed

---

## 9. Sidecar Containers

A sidecar runs **alongside** the main container throughout the pod lifetime. In
Kubernetes 1.29+ there is a native sidecar container type (`initContainers` with
`restartPolicy: Always`) that starts before app containers and stops after them.

### Classic sidecar (just an extra container)

```yaml
spec:
  containers:
  - name: app
    image: my-app:v1
  - name: log-shipper
    image: fluentbit:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
```

### Native sidecar (Kubernetes 1.29+)

```yaml
spec:
  initContainers:
  - name: log-shipper
    image: fluentbit:latest
    restartPolicy: Always       # marks this as a sidecar — starts before app containers
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  containers:
  - name: app
    image: my-app:v1
```

> Native sidecars are included in HPA scaling decisions and are properly ordered during
> pod start/stop, unlike classic sidecars.

---

## 10. Pod Lifecycle Events

```
Pending → (init containers) → Running → Succeeded / Failed
                                ↑
                           (CrashLoopBackOff if container keeps failing)
```

```bash
# Watch pod lifecycle
kubectl get pod my-pod -w

# Pod ready conditions
kubectl get pod my-pod -o jsonpath='{.status.conditions}'

# Container statuses
kubectl get pod my-pod -o jsonpath='{.status.containerStatuses[*].state}'
```

---

## 11. Quick Reference

| Field | Default | Notes |
|---|---|---|
| `restartPolicy` | `Always` | Jobs/CronJobs must use `Never` or `OnFailure` |
| `terminationGracePeriodSeconds` | 30s | How long kubelet waits after SIGTERM before SIGKILL |
| `spec.replicas` | 1 | Remove from Deployment spec when using HPA |
| `maxUnavailable` | 25% | RollingUpdate: can be absolute number or % |
| `maxSurge` | 25% | RollingUpdate: extra pods above desired count |

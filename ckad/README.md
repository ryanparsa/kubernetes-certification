# CKAD — Certified Kubernetes Application Developer

## Exam Overview

| | |
|---|---|
| **Format** | Performance-based (hands-on CLI tasks) |
| **Duration** | 2 hours |
| **Passing score** | 66% |
| **Cost** | $395 USD (includes one free retake) |
| **Validity** | 3 years |
| **Allowed docs** | kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs, github.com/kubernetes |
| **Official curriculum** | https://github.com/cncf/curriculum |

## Domains & Weights

| Domain | Weight |
|---|---|
| Application Design and Build | 20% |
| Application Deployment | 20% |
| Application Observability and Maintenance | 15% |
| Application Environment, Configuration and Security | 25% |
| Services and Networking | 20% |

## Domain Topics

### Application Design and Build (20%)
- Choosing the right workload: Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob
- Job: `completions`, `parallelism`, `backoffLimit`, `activeDeadlineSeconds`, `restartPolicy: Never/OnFailure`
- CronJob: schedule syntax, `concurrencyPolicy`, `startingDeadlineSeconds`, `successfulJobsHistoryLimit`
- Multi-container pod patterns:
  - Sidecar: shared volume, log shipping, proxy injection
  - Init container: sequencing, dependency checks, one-time setup
  - Ambassador: outbound proxy pattern
  - Adapter: transforming output for a monitoring system
- Container image build: multi-stage builds, non-root USER, minimal base image
- Dockerfile best practices: layer caching, `.dockerignore`, avoiding secrets in layers

### Application Deployment (20%)
- Rolling update: `maxSurge`, `maxUnavailable`
- `kubectl rollout`: status, undo, `history --revision`, pause, resume
- Canary deployment: two Deployments sharing one Service, traffic split by replica ratio
- Blue/green deployment: label swap on Service selector
- Helm: `install`, `upgrade`, `rollback`, `uninstall`
- `helm template --values` / `--set`; difference between `--set` and `-f values.yaml`
- `helm repo add / update / search repo`; `helm show values / chart`

### Application Observability and Maintenance (15%)
- Liveness probe: restarts unhealthy containers; exec, httpGet, tcpSocket
- Readiness probe: gates traffic; removes pod from Service endpoints when failing
- Startup probe: for slow-starting apps; disables liveness/readiness until it passes
- Probe fields: `initialDelaySeconds`, `periodSeconds`, `failureThreshold`, `successThreshold`
- `kubectl top pod / node` (requires metrics-server)
- `kubectl describe` events as first debugging step
- Logging: `kubectl logs`, `-f`, `--previous`, `-c <container>`
- Debugging: `kubectl exec -it`, ephemeral containers (`kubectl debug`)
- Deprecation handling: `kubectl explain`, API version migration

### Application Environment, Configuration and Security (25%)
- ConfigMap: `--from-file`, `--from-literal`, `envFrom`, volume mount
- Secret: `--from-literal`, base64 encoding, volume mount vs env injection
- Immutable ConfigMap / Secret
- ServiceAccount: `automountServiceAccountToken`, projected volumes
- ResourceQuota: limits total CPU/memory/object counts per namespace
- LimitRange: sets default requests/limits per container or pod
- SecurityContext (pod level vs container level):
  - `runAsUser`, `runAsGroup`, `fsGroup`
  - `runAsNonRoot: true`
  - `allowPrivilegeEscalation: false`
  - `readOnlyRootFilesystem: true`
  - `capabilities: add / drop`
- Custom Resources: `kubectl get crd`, `kubectl explain <cr>.<field>`, treating CRs like native objects
- Admission controllers concept: validating vs mutating webhooks

### Services and Networking (20%)
- Services: ClusterIP, NodePort, LoadBalancer, ExternalName — `spec.selector`, `targetPort` int vs string
- Ingress: rules, TLS, `pathType` (`Exact` / `Prefix` / `ImplementationSpecific`), `ingressClassName`
- NetworkPolicy: `podSelector`, `namespaceSelector`, `ipBlock`, ingress/egress rules, `ports[].protocol` uppercase
- DNS: `<service>.<namespace>.svc.cluster.local`; pod DNS policy (`ClusterFirst`, `None`)
- Service discovery via environment variables vs DNS

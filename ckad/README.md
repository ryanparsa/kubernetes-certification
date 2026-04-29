# CKAD -- Certified Kubernetes Application Developer

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
- Services: ClusterIP, NodePort, LoadBalancer, ExternalName -- `spec.selector`, `targetPort` int vs string
- Ingress: rules, TLS, `pathType` (`Exact` / `Prefix` / `ImplementationSpecific`), `ingressClassName`
- NetworkPolicy: `podSelector`, `namespaceSelector`, `ipBlock`, ingress/egress rules, `ports[].protocol` uppercase
- DNS: `<service>.<namespace>.svc.cluster.local`; pod DNS policy (`ClusterFirst`, `None`)
- Service discovery via environment variables vs DNS

---

## Labs Mapping
| Lab | Topics |
|---|---|
| [1](1/README.md) | Namespace, Pod, image, kubectl |
| [2](2/README.md) | Init Container, Pod, Volume, emptyDir, image, kubectl |
| [3](3/README.md) | Labels, Pod, Selector, describe, image, kubectl, nodeSelector |
| [4](4/README.md) | Deployment, Labels, Selector, image, kubectl |
| [5](5/README.md) | Job, describe, image, kubectl |
| [6](6/README.md) | CronJob, Job, image, kubectl |
| [7](7/README.md) | Pod, Volume, describe, image, kubectl |
| [8](8/README.md) | Pod, Secret, Volume, image, kubectl |
| [9](9/README.md) | Capabilities, Namespace, Pod, SecurityContext, ServiceAccount, allowPrivilegeEscalation, context, image, kubectl |
| [10](10/README.md) | CPU, LimitRange, Limits, Memory, Namespace, Pod, Requests, ResourceQuota, Resources, describe, image, kubectl |
| [11](11/README.md) | Events, Pod, Probes, describe, image, kubectl |
| [12](12/README.md) | ClusterIP, Deployment, Ingress, Namespace, NetworkPolicy, NodePort, Service, describe, image, ingress, kubectl |
| [13](13/README.md) | PV, PVC, Pod, Requests, Resources, Volume, hostPath, image, kubectl |
| [14](14/README.md) | Deployment, Namespace, Upgrade, helm, kubectl |
| [15](15/README.md) | Namespace, Resources, kubectl |
| [16](16/README.md) | Deployment, Namespace, image, kubectl |
| [17](17/README.md) | Node, PV, Resources, describe, hostPath, kubectl |
| [18](18/README.md) | PVC, Pod, Provisioner, Resources, StorageClass, Volume, VolumeBindingMode, describe, kubectl |
| [19](19/README.md) | Namespace, PVC, Requests, Resources, StorageClass, describe, kubectl |
| [20](20/README.md) | CPU, Debug, Deployment, Fix, Limits, Memory, Namespace, Pod, Resources, describe, image, kubectl |
| [21](21/README.md) | Log, Multi-container, Namespace, Pod, Sidecar, Volume, emptyDir, image, kubectl |
| [22](22/README.md) | Fix, Labels, Namespace, Pod, Selector, Service, kubectl |
| [23](23/README.md) | CPU, Limits, Memory, Namespace, Pod, Resources, describe, kubectl, top |
| [24](24/README.md) | CPU, Limits, Memory, Namespace, Pod, Requests, Resources, image, kubectl |
| [25](25/README.md) | Namespace, Pod, Secret, image, kubectl |
| [26](26/README.md) | CronJob, Job, Log, Namespace, describe, image, kubectl |
| [27](27/README.md) | Namespace, Pod, Probes, Service, describe, image, kubectl |
| [28](28/README.md) | ClusterRole, ClusterRoleBinding, Namespace, Pod, RBAC, Resources, Role, kubectl |
| [29](29/README.md) | Deployment, Namespace, Service, helm, kubectl |
| [30](30/README.md) | Backup, Resources, describe, kubectl |
| [31](31/README.md) | Ingress, Namespace, NetworkPolicy, describe, ingress, kubectl |
| [32](32/README.md) | ClusterIP, Labels, Namespace, Pod, Selector, Service, describe, kubectl |
| [33](33/README.md) | Deployment, Namespace, Node, NodePort, Selector, Service, describe, kubectl |
| [34](34/README.md) | Ingress, Namespace, Service, describe, ingress, kubectl |
| [35](35/README.md) | Job, Namespace, Pod, image, kubectl |
| [36](36/README.md) | OCI, docker, image |
| [37](37/README.md) | Labels, Namespace, Pod, image, kubectl |
| [38](38/README.md) | Log, Multi-container, Namespace, Pod, Sidecar, Volume, describe, emptyDir, image, kubectl |
| [39](39/README.md) | ClusterIP, Deployment, Labels, Namespace, Pod, Resources, Selector, Service, image, kubectl |
| [40](40/README.md) | Namespace, Pod, Resources, Secret, Volume, image, kubectl |
| [41](41/README.md) | CPU, Limits, Memory, Namespace, Pod, Probes, Requests, Resources, describe, image, kubectl |
| [42](42/README.md) | ClusterIP, Deployment, Labels, LoadBalancer, Namespace, NodePort, Resources, Selector, Service, image, kubectl |
| [43](43/README.md) | Namespace, PV, PVC, Pod, Requests, Resources, hostPath, image, kubectl |
| [44](44/README.md) | Backup, CronJob, Job, Namespace, Pod, describe, image, kubectl |
| [45](45/README.md) | CPU, Debug, Deployment, Fix, Limits, Memory, Namespace, NetworkPolicy, Pod, Requests, Resources, describe, image, kubectl |
| [46](46/README.md) | Ingress, Labels, Namespace, NetworkPolicy, Pod, Resources, Role, describe, egress, image, ingress, kubectl |
| [47](47/README.md) | Capabilities, Namespace, Pod, SecurityContext, context, describe, image, kubectl, readOnlyRootFilesystem, runAsNonRoot |
| [48](48/README.md) | Dockerfile, docker, image |
| [49](49/README.md) | Job, Namespace, describe, image, kubectl |
| [50](50/README.md) | Init Container, Log, Namespace, Pod, Resources, Selector, Service, Sidecar, Volume, describe, emptyDir, image, kubectl |
| [51](51/README.md) | Namespace, helm, kubectl |
| [52](52/README.md) | Namespace, Pod, Probes, describe, image, kubectl |
| [53](53/README.md) | Namespace, Pod, describe, image, kubectl |
| [54](54/README.md) | Namespace, Resources, image, kubectl |
| [55](55/README.md) | Multi-container, Namespace, Pod, image, kubectl |
| [56](56/README.md) | Debug, Namespace, Pod, Resources, Secret, Volume, image, kubectl |
| [57](57/README.md) | Labels, Namespace, Pod, image, kubectl |
| [58](58/README.md) | Namespace, PV, PVC, Pod, Requests, Resources, StorageClass, Volume, describe, hostPath, image, kubectl |
| [59](59/README.md) | CPU, LimitRange, Limits, Memory, Namespace, Pod, ResourceQuota, Resources, describe, kubectl |
| [60](60/README.md) | Deployment, Labels, Limits, Memory, Namespace, Requests, Resources, Selector, describe, image, kubectl |
| [61](61/README.md) | ClusterIP, Endpoint, Labels, Namespace, Pod, Service, image, kubectl |
| [62](62/README.md) | Ingress, Labels, Namespace, NetworkPolicy, Pod, describe, egress, image, ingress, kubectl |
| [63](63/README.md) | Log, Namespace, Pod, image, kubectl |
| [64](64/README.md) | Namespace, Pod, image, kubectl |
| [65](65/README.md) | Deployment, Namespace, describe, image, kubectl |
| [66](66/README.md) | Deployment, Namespace, describe, kubectl |
| [67](67/README.md) | Namespace, Pod, Volume, describe, image, kubectl |
| [68](68/README.md) | Namespace, Pod, Secret, Volume, describe, image, kubectl |
| [69](69/README.md) | ClusterIP, Deployment, NodePort, Pod, Selector, Service, image, kubectl |
| [70](70/README.md) | Pod, Probes, describe, image, kubectl |
| [71](71/README.md) | CronJob, Job, image, kubectl |
| [72](72/README.md) | Labels, Namespace, Pod, Resources, image, kubectl |
| [73](73/README.md) | Labels, Namespace, Pod, Resources, Secret, image, kubectl |
| [74](74/README.md) | Labels, Pod, Resources, SecurityContext, Volume, context, emptyDir, image, kubectl |
| [75](75/README.md) | Adapter, Log, Pod, Volume, emptyDir, image, kubectl |
| [76](76/README.md) | Ingress, Labels, Namespace, NetworkPolicy, Pod, Selector, image, ingress, kubectl |
| [77](77/README.md) | Events, PV, PVC, Pod, Requests, Resources, StorageClass, Volume, describe, hostPath, image, kubectl |
| [78](78/README.md) | Deployment, Labels, Pod, Resources, Selector, image, kubectl |
| [79](79/README.md) | CPU, Labels, Limits, Memory, Namespace, Pod, Requests, Resources, describe, image, kubectl |
| [80](80/README.md) | CPU, Init Container, Memory, Multi-container, Namespace, Pod, Requests, Resources, Sidecar, describe, image, kubectl |
| [81](81/README.md) | Debug, Namespace, Pod, image, kubectl |
| [82](82/README.md) | Namespace, Pod, Secret, Volume, image, kubectl |
| [83](83/README.md) | DNS, Ingress, Namespace, NetworkPolicy, Pod, Role, Service, describe, egress, image, ingress, kubectl |
| [84](84/README.md) | Namespace, Pod, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl |
| [85](85/README.md) | Capabilities, Namespace, Pod, SecurityContext, Volume, allowPrivilegeEscalation, context, image, kubectl, readOnlyRootFilesystem |
| [86](86/README.md) | Namespace, Pod, Probes, describe, image, kubectl |
| [87](87/README.md) | Backup, CronJob, Job, Namespace, describe, image, kubectl |
| [88](88/README.md) | CPU, DaemonSet, Labels, Memory, Namespace, Node, Pod, Requests, Resources, Role, Selector, Toleration, image, kubectl, nodeSelector |
| [89](89/README.md) | Namespace, Pod, Volume, emptyDir, image, kubectl |
| [120](120/README.md) | kubectl |
| [121](121/README.md) | Namespace, NodePort, Pod, Service, image, kubectl |
| [122](122/README.md) | Job, Namespace, Pod, image, kubectl |
| [123](123/README.md) | Debug, Namespace, Node, crictl, docker, image |
| [124](124/README.md) | ClusterRole, Namespace, RBAC, RoleBinding, Secret, ServiceAccount, kubectl |
| [126](126/README.md) | Deployment, Namespace, Service, kubectl |
| [127](127/README.md) | Deployment, Namespace, image, kubectl |
| [128](128/README.md) | Deployment, Log, Namespace, Sidecar, Volume, docker, emptyDir, image, kubectl |
| [129](129/README.md) | ClusterIP, Namespace, Pod, Service, image, kubectl |
| [130](130/README.md) | Dockerfile, Log, docker, image |
| [131](131/README.md) | Deployment, Labels, Namespace, PV, PVC, Requests, Resources, Selector, Volume, hostPath, image, kubectl |
| [132](132/README.md) | Namespace, Pod, Probes, Service, describe, image, kubectl |
| [133](133/README.md) | Deployment, Fix, Namespace, Pod, Secret, describe, docker, image, kubectl |
| [134](134/README.md) | Deployment, Pod, Volume, kubectl |
| [135](135/README.md) | Deployment, Log, Namespace, Pod, Sidecar, Volume, emptyDir, image, kubectl, top |
| [136](136/README.md) | Deployment, Log, Namespace, Pod, Volume, image, kubectl |
| [137](137/README.md) | Debug, Deployment, Fix, Namespace, Pod, Requests, Service, describe, image, kubectl |
| [138](138/README.md) | Deployment, Namespace, Node, Pod, Service, image, kubectl |
| [139](139/README.md) | Deployment, Labels, Namespace, kubectl |
| [140](140/README.md) | Deployment, Namespace, Replica, Selector, kubectl |
| [141](141/README.md) | Labels, Namespace, Node, Pod, image, kubectl, nodeSelector |

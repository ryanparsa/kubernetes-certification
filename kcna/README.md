# Kubernetes and Cloud Native Associate (KCNA)

## Exam Overview

| | |
|---|---|
| **Format** | 60 multiple-choice questions, remotely proctored |
| **Duration** | 90 minutes |
| **Passing score** | 75% |
| **Cost** | $250 USD (includes one free retake) |
| **Validity** | 24 months |
| **Official curriculum** | https://github.com/cncf/curriculum |

## Domains & Weights

| Domain | Weight |
|---|---|
| Kubernetes Fundamentals | 44%–46% |
| Container Orchestration | 22%–28% |
| Cloud Native Architecture (incl. Observability) | 12%–16% |
| Cloud Native Application Delivery | 8%–16% |

> **Note:** The standalone "Cloud Native Observability" domain was merged into "Cloud Native Architecture" starting in 2025.

## Domain Topics

### Kubernetes Fundamentals (44%–46%)
- Cluster architecture: control plane (API server, etcd, scheduler, controller-manager) and worker nodes (kubelet, kube-proxy)
- Pod lifecycle: Pending → Running → Succeeded / Failed / Unknown
- Workloads: Deployment, ReplicaSet, StatefulSet, DaemonSet, Job, CronJob
- Services: ClusterIP, NodePort, LoadBalancer, ExternalName, Headless
- Namespaces, Labels, Annotations, Label Selectors
- Resource model: requests vs limits, LimitRange, ResourceQuota
- Probes: liveness, readiness, startup — exec, httpGet, tcpSocket
- ConfigMap and Secret: creation, env injection, volume mount
- RBAC: Role, RoleBinding, ClusterRole, ClusterRoleBinding, ServiceAccount
- Taints, tolerations, node affinity, pod affinity/anti-affinity
- Storage: PersistentVolume, PersistentVolumeClaim, StorageClass, access modes
- Custom Resource Definitions (CRD) and Operators
- `kubeconfig` structure; `kubectl config use-context`
- Static pods, init containers, ephemeral containers
- Declarative vs imperative model; reconciliation loop

### Container Orchestration (22%–28%)
- Container runtime: containerd, CRI-O, OCI spec
- Container vs VM: namespaces, cgroups, image layers
- Multi-container pod patterns: sidecar, init, ambassador, adapter
- Container networking: CNI, pod-to-pod, pod-to-service, DNS
- Container storage: volumes, bind mounts, tmpfs
- Image registries, image pull policies, digest vs tag pinning
- Health checks and restart policies
- Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA) concepts
- Cluster autoscaling concepts

### Cloud Native Architecture (incl. Observability) (12%–16%)
- Cloud native principles: microservices, 12-factor app, loose coupling
- Service mesh concepts: mTLS, traffic management, observability (Istio, Linkerd)
- Serverless concepts: FaaS, event-driven, Knative
- GitOps principles: declarative config, reconciliation, Flux/Argo CD
- Observability pillars: metrics (Prometheus), logs (Loki/Fluentd), traces (Jaeger/OpenTelemetry)
- `kubectl top pod / node`; metrics-server dependency
- Alerting, dashboards (Grafana)
- Cloud native storage: object storage, block storage, CSI drivers

### Cloud Native Application Delivery (8%–16%)
- Helm: install, upgrade, rollback, uninstall; `helm repo add/update`; `values.yaml` vs `--set`
- CI/CD pipeline concepts: build, test, deploy stages
- GitOps workflow: PR-based deployments, drift detection
- Kustomize: `kustomization.yaml`, overlays, patches
- Container image build best practices: minimal base, non-root USER, multi-stage builds
- Artifact registries and image promotion strategies

---

## Repository Contents

| File | Description |
|---|---|
| [kcna-assessment-bank.md](kcna-assessment-bank.md) | 200 practice questions with answers, explanations, difficulty, and frequency |
| [kcna-exam-checklist.md](kcna-exam-checklist.md) | Domain-by-domain preparation checklist |
| [resources.md](resources.md) | Curated learning resources |

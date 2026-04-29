# CKA & CKAD Curriculum Comparison (2025/2026, Kubernetes v1.34/v1.35)

This report consolidates the **official, currently-published exam domains, weightings, and competencies** for the
Certified Kubernetes Administrator (CKA) and Certified Kubernetes Application Developer (CKAD) exams, as listed on the
Linux Foundation Training & Certification site and the CNCF open-source curriculum repository (
`github.com/cncf/curriculum`) as of April 2026. It then provides a granular, side-by-side mapping of shared topics,
CKA-only topics, and CKAD-only topics, plus notes on what changed in the 2024–2026 curriculum overhaul.

A note on Kubernetes version: as of April 2026 the **CKA exam is administered against Kubernetes v1.34**, and the **CKAD
exam is administered against Kubernetes v1.35** (the linked CNCF curriculum PDFs are titled `CKA_Curriculum_v1.35.pdf`
and `CKAD_Curriculum_v1.35.pdf`). The Linux Foundation aligns the live exam environment to the most recent Kubernetes
minor release within roughly 4–8 weeks of that release, so the exam version increments quarterly. There is no "v1.35"
curriculum that is materially different in domains/weights from the v1.31, v1.32, v1.33, or v1.34 versions — the domain
list and weighting have been stable since the major **February 2024 curriculum reset**, which is the version still in
force for 2025/2026.

---

## 1. CKA — Official Domains & Weights (2025/2026)

The CKA exam consists of five domains. The percentages match exactly what is published in
`cncf/curriculum/cka/README.md` and on the Linux Foundation CKA product page.

| # | Domain                                             | Weight  |
|---|----------------------------------------------------|---------|
| 1 | Cluster Architecture, Installation & Configuration | **25%** |
| 2 | Workloads & Scheduling                             | **15%** |
| 3 | Services & Networking                              | **20%** |
| 4 | Storage                                            | **10%** |
| 5 | Troubleshooting                                    | **30%** |

### 1.1 Cluster Architecture, Installation & Configuration — 25%

Verbatim competencies (per Linux Foundation):

- Manage role-based access control (RBAC)
- Prepare underlying infrastructure for installing a Kubernetes cluster
- Create and manage Kubernetes clusters using `kubeadm`
- Manage the lifecycle of Kubernetes clusters
- Implement and configure a highly-available control plane
- Use **Helm** and **Kustomize** to install cluster components
- Understand extension interfaces (**CNI, CSI, CRI**, etc.)
- Understand **CRDs**, install and configure **operators**

Granular sub-topics implied/expected:

- RBAC primitives: `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding`, `ServiceAccount` bindings, aggregated
  ClusterRoles, `kubectl auth can-i`
- Underlying infrastructure: container runtime (containerd/CRI-O), `systemd` cgroup driver, swap, kernel modules (
  `br_netfilter`, `overlay`), sysctls, firewalld/iptables, `/etc/hosts`, kubelet prerequisites
- `kubeadm init` / `kubeadm join` / `kubeadm reset` / `kubeadm token` / `kubeadm certs renew` /
  `kubeadm upgrade plan|apply|node`
- Cluster lifecycle: minor-version upgrades of control plane and worker nodes, draining nodes (`kubectl drain`,
  `kubectl cordon`/`uncordon`), backup & restore of **etcd** (`etcdctl snapshot save/restore`)
- Highly-available control plane: stacked vs. external etcd topologies, load balancer in front of `kube-apiserver`,
  multiple `kube-controller-manager` and `kube-scheduler` replicas with leader election
- Helm: `helm repo add/update`, `helm install`, `helm upgrade`, `helm rollback`, `helm template`, `helm uninstall`,
  values files
- Kustomize: `kustomization.yaml`, bases/overlays, strategic-merge and JSON patches, `kubectl apply -k`
- Extension interfaces: CNI plugins (Calico, Cilium, Flannel, Weave), CSI drivers, CRI sockets (containerd, CRI-O)
- CRDs and operators: `CustomResourceDefinition` v1, controller pattern, installing operators via Helm or operator
  manifests

### 1.2 Workloads & Scheduling — 15%

Verbatim competencies:

- Understand application Deployments and how to perform rolling updates and rollbacks
- Use **ConfigMaps** and **Secrets** to configure applications
- Configure **workload autoscaling**
- Understand the primitives used to create robust, self-healing application deployments
- Configure **Pod admission and scheduling** (limits, node affinity, etc.)

Granular sub-topics:

- `Deployment` rollout strategies (`RollingUpdate`, `Recreate`), `maxSurge`, `maxUnavailable`,
  `kubectl rollout status|history|undo|restart`, `revisionHistoryLimit`
- `ConfigMap` and `Secret` consumption: env vars, `envFrom`, projected volumes, file mounts, immutable
  ConfigMaps/Secrets, base64 encoding for Secrets
- Autoscaling: **HorizontalPodAutoscaler (HPA)** v2 with CPU/memory/custom metrics, **VerticalPodAutoscaler (VPA)**, *
  *Cluster Autoscaler** (conceptual)
- Self-healing primitives: `ReplicaSet`, `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`,
  liveness/readiness/startup probes, `restartPolicy`, PodDisruptionBudgets
- Scheduling: `nodeSelector`, **node affinity / anti-affinity** (required vs. preferred), **pod affinity / anti-affinity
  **, **taints and tolerations**, `topologySpreadConstraints`, `priorityClassName` and `PriorityClass`,
  `resources.requests/limits` (CPU, memory, ephemeral-storage), `LimitRange`, `ResourceQuota`, `nodeName`, manual
  scheduling, scheduler profiles

### 1.3 Services & Networking — 20%

Verbatim competencies:

- Understand connectivity between Pods
- Define and enforce **NetworkPolicies**
- Use **ClusterIP**, **NodePort**, **LoadBalancer** service types and endpoints
- Use the **Gateway API** to manage Ingress traffic
- Know how to use **Ingress controllers** and **Ingress resources**
- Understand and use **CoreDNS**

Granular sub-topics:

- Pod-to-Pod connectivity model, the CNI plugin's role, kube-proxy modes (iptables, IPVS, nftables)
- `NetworkPolicy` ingress/egress rules, `podSelector`, `namespaceSelector`, default-deny patterns
- `Service` types: `ClusterIP`, `NodePort`, `LoadBalancer`, `ExternalName`, headless services (`clusterIP: None`);
  `Endpoints` and `EndpointSlice`; `kubectl expose`
- **Gateway API** resources: `GatewayClass`, `Gateway`, `HTTPRoute`, `TCPRoute`, `TLSRoute`, `ReferenceGrant` (this
  replaced/supplemented Ingress emphasis in the 2024 curriculum reset)
- `Ingress` resources, ingressClassName, path types (`Prefix`, `Exact`), TLS termination, common controllers (NGINX,
  Traefik)
- CoreDNS: ConfigMap (`Corefile`), service discovery names (`<svc>.<ns>.svc.cluster.local`), pod DNS, `dnsPolicy`,
  `dnsConfig`

### 1.4 Storage — 10%

Verbatim competencies:

- Implement storage classes and dynamic volume provisioning
- Configure volume types, access modes and reclaim policies
- Manage persistent volumes and persistent volume claims

Granular sub-topics:

- `StorageClass` with provisioner, parameters, `volumeBindingMode` (`Immediate`, `WaitForFirstConsumer`), default
  StorageClass annotation
- Volume types: `emptyDir`, `hostPath`, `configMap`, `secret`, `downwardAPI`, `projected`, `nfs`, `iscsi`, CSI-backed
  volumes
- Access modes: `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod`
- Reclaim policies: `Retain`, `Delete`, (`Recycle` deprecated)
- `PersistentVolume` (PV) and `PersistentVolumeClaim` (PVC) lifecycle, binding, expansion, snapshots (CSI),
  `VolumeMode` (Filesystem vs. Block)

### 1.5 Troubleshooting — 30% (largest single domain on CKA)

Verbatim competencies:

- Troubleshoot clusters and nodes
- Troubleshoot cluster components
- Monitor cluster and application resource usage
- Manage and evaluate container output streams
- Troubleshoot services and networking

Granular sub-topics:

- Cluster/node troubleshooting: `kubectl get nodes`, `NotReady` diagnosis, `journalctl -u kubelet`,
  `crictl ps|logs|inspect`, container runtime troubleshooting, certificate expiration, `kubelet`/`kube-proxy` config
  under `/var/lib/kubelet`
- Control-plane component troubleshooting: static-pod manifests in `/etc/kubernetes/manifests/`, `kube-apiserver`,
  `etcd`, `kube-controller-manager`, `kube-scheduler` logs, control-plane failure scenarios
- Resource monitoring: `metrics-server`, `kubectl top nodes`, `kubectl top pods`, events (
  `kubectl get events --sort-by=...`, `kubectl describe`)
- Logs and output streams: `kubectl logs`, `--previous`, `-c <container>`, `--since`, `--tail`, multi-container pods,
  sidecar logging
- Service/networking troubleshooting: DNS resolution inside Pods, `nslookup`/`dig`, NetworkPolicy debugging,
  `kubectl port-forward`, `kubectl exec`, endpoint-to-service mismatch, kube-proxy iptables rules

---

## 2. CKAD — Official Domains & Weights (2025/2026)

The CKAD exam consists of five domains. Numbers and competencies are taken verbatim from the Linux Foundation CKAD
product page and the `cncf/curriculum/ckad` README.

| # | Domain                                              | Weight  |
|---|-----------------------------------------------------|---------|
| 1 | Application Design and Build                        | **20%** |
| 2 | Application Deployment                              | **20%** |
| 3 | Application Observability and Maintenance           | **15%** |
| 4 | Application Environment, Configuration and Security | **25%** |
| 5 | Services and Networking                             | **20%** |

### 2.1 Application Design and Build — 20%

Verbatim competencies:

- Define, build and modify container images
- Choose and use the right workload resource (Deployment, DaemonSet, CronJob, etc.)
- Understand multi-container Pod design patterns (e.g. **sidecar**, **init**, and others)
- Utilize **persistent and ephemeral volumes**

Granular sub-topics:

- Container images: writing `Dockerfile`s, multi-stage builds, image tags vs. digests, OCI compliance,
  `imagePullPolicy`, `imagePullSecrets`, private registries
- Choosing workload resources: `Pod`, `Deployment`, `ReplicaSet`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`, when to
  use each
- Multi-container patterns: **init containers**, **sidecar containers** (including the new restartable native sidecar
  pattern with `restartPolicy: Always` on init containers, GA in v1.29+), **ambassador** pattern, **adapter** pattern
- Volumes: `emptyDir` (ephemeral), `configMap`/`secret`/`downwardAPI`/`projected` (ephemeral), `persistentVolumeClaim`,
  generic ephemeral volumes, `volumeMounts`, `subPath`

### 2.2 Application Deployment — 20%

Verbatim competencies:

- Use Kubernetes primitives to implement common deployment strategies (e.g. **blue/green** or **canary**)
- Understand Deployments and how to perform **rolling updates**
- Use the **Helm** package manager to deploy existing packages
- **Kustomize**

Granular sub-topics:

- Deployment strategies built from primitives: blue/green using two Deployments + Service selector swap; canary using
  two Deployments with shared labels and replica ratios; rolling update with `maxSurge`/`maxUnavailable`
- `kubectl rollout status|history|undo|pause|resume|restart`, `revisionHistoryLimit`
- Helm: installing existing charts, `helm install/upgrade/rollback/uninstall/list/status`, `--values`, `--set`,
  repository management
- Kustomize: `kustomization.yaml`, bases and overlays (dev/stage/prod), `commonLabels`, `commonAnnotations`,
  `namePrefix`, `nameSuffix`, `images:` transformer, `configMapGenerator`, `secretGenerator`, strategic-merge and
  JSON-6902 patches, `kubectl apply -k`

### 2.3 Application Observability and Maintenance — 15%

Verbatim competencies:

- Understand **API deprecations**
- Implement **probes and health checks**
- Use built-in CLI tools to **monitor** Kubernetes applications
- Utilize container **logs**
- **Debugging** in Kubernetes

Granular sub-topics:

- API deprecations: identifying `apiVersion` versions (e.g., `apps/v1beta1` → `apps/v1`), `kubectl convert`, deprecation
  warnings, `kubectl api-resources`, `kubectl api-versions`, `kubectl explain`
- Probes: `livenessProbe`, `readinessProbe`, `startupProbe`; probe types `httpGet`, `tcpSocket`, `exec`, `grpc`;
  tunables (`initialDelaySeconds`, `periodSeconds`, `failureThreshold`, etc.)
- Monitoring CLI: `kubectl top pod/node` (requires metrics-server), `kubectl get`, `kubectl describe`
- Logs: `kubectl logs`, `-c`, `--previous`, `-f`, `--since`, `--tail`, `--all-containers`
- Debugging: `kubectl describe`, `kubectl events`, `kubectl exec -it`, `kubectl port-forward`, `kubectl cp`, **ephemeral
  debug containers** via `kubectl debug` (pod, node, copy modes)

### 2.4 Application Environment, Configuration and Security — 25% (largest CKAD domain)

Verbatim competencies:

- Discover and use resources that extend Kubernetes (**CRD, Operators**)
- Understand **authentication, authorization and admission control**
- Understand **requests, limits, quotas**
- Understand **ConfigMaps**
- Define **resource requirements**
- Create & consume **Secrets**
- Understand **ServiceAccounts**
- Understand Application Security (**SecurityContexts, Capabilities**, etc.)

Granular sub-topics:

- CRDs/Operators: `kubectl get crd`, discovering custom resources, consuming them as a developer
- AuthN/AuthZ/Admission: token-based auth, certificates, RBAC consumption (Role/RoleBinding from a developer
  perspective), admission controllers conceptually (LimitRanger, ResourceQuota, PodSecurity), **Pod Security Admission**
  with labels `pod-security.kubernetes.io/enforce|audit|warn` set to `privileged|baseline|restricted`
- Requests, limits, quotas: container `resources.requests` and `resources.limits` (CPU, memory, ephemeral-storage),
  `LimitRange`, `ResourceQuota` (object counts + compute)
- ConfigMaps: creation (`--from-literal`, `--from-file`, `--from-env-file`), mounting as env (`env`, `envFrom`), as
  files (volume), immutable ConfigMaps
- Secrets: types (`Opaque`, `kubernetes.io/dockerconfigjson`, `kubernetes.io/tls`,
  `kubernetes.io/service-account-token`, `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth`), consuming as env vars or
  files, immutable secrets
- ServiceAccounts: creating SAs, binding to Roles, mounting tokens, projected token volumes,
  `automountServiceAccountToken`
- Security: `securityContext` at pod and container level (`runAsUser`, `runAsGroup`, `fsGroup`, `runAsNonRoot`,
  `readOnlyRootFilesystem`, `allowPrivilegeEscalation`), Linux **capabilities** (`add`/`drop`), seccomp profiles,
  AppArmor (conceptual)

### 2.5 Services and Networking — 20%

Verbatim competencies:

- Demonstrate basic understanding of **NetworkPolicies**
- Provide and troubleshoot access to applications via **Services**
- Use **Ingress** rules to expose applications

Granular sub-topics:

- NetworkPolicy: ingress/egress rules, `podSelector`, `namespaceSelector`, port/protocol selectors, default-deny
  patterns, label-based pod targeting (often the trick is to relabel pods to fit a policy rather than edit the policy)
- Services: `ClusterIP`, `NodePort`, `LoadBalancer`, `ExternalName`, headless services, label selectors matching pod
  labels, `targetPort` vs. `port`, `kubectl expose`, troubleshooting via `Endpoints`/`EndpointSlice`
- Ingress: `Ingress` resource, `ingressClassName`, host- and path-based routing, `pathType` (`Prefix`, `Exact`,
  `ImplementationSpecific`), TLS via Secret, basic Ingress troubleshooting (404, backend service mismatch)

---

## 3. Shared Topics — Appear in BOTH CKA and CKAD

These are the topic areas where the two curricula explicitly overlap. CKA tests them from a **cluster-operator**
perspective (configure, troubleshoot at scale, install); CKAD tests them from a **workload-author** perspective (define
them in YAML, use them inside an app).

| Shared Topic Area                                                                                        | CKA framing                                         | CKAD framing                                        |
|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------|
| **Deployments & rolling updates / rollbacks**                                                            | Workloads & Scheduling                              | Application Deployment                              |
| **ConfigMaps**                                                                                           | Workloads & Scheduling                              | Application Environment, Configuration and Security |
| **Secrets**                                                                                              | Workloads & Scheduling                              | Application Environment, Configuration and Security |
| **Resource requests, limits, quotas, LimitRange, ResourceQuota**                                         | Workloads & Scheduling                              | Application Environment, Configuration and Security |
| **Helm (deploy existing packages)**                                                                      | Cluster Architecture (install cluster components)   | Application Deployment                              |
| **Kustomize**                                                                                            | Cluster Architecture (install cluster components)   | Application Deployment                              |
| **CRDs and Operators**                                                                                   | Cluster Arch. (install/configure operators)         | App. Env. (discover/use CRDs as a developer)        |
| **NetworkPolicies**                                                                                      | Services & Networking (define and enforce)          | Services and Networking (basic understanding)       |
| **Services (ClusterIP / NodePort / LoadBalancer / ExternalName) and Endpoints/EndpointSlice**            | Services & Networking                               | Services and Networking                             |
| **Ingress resources & Ingress controllers**                                                              | Services & Networking                               | Services and Networking                             |
| **Persistent and ephemeral volumes** (PVC consumption, emptyDir, configMap/secret/downwardAPI/projected) | Storage                                             | App. Design and Build                               |
| **Probes & health checks** (liveness/readiness/startup)                                                  | Implicit in Workloads/Troubleshooting               | App. Observability and Maintenance                  |
| **Logs (`kubectl logs`) & container output streams**                                                     | Troubleshooting                                     | App. Observability and Maintenance                  |
| **Debugging applications: `kubectl describe`, `exec`, `port-forward`, events, `kubectl debug`**          | Troubleshooting                                     | App. Observability and Maintenance                  |
| **`kubectl top` / metrics-server-based monitoring**                                                      | Troubleshooting                                     | App. Observability and Maintenance                  |
| **ServiceAccounts**                                                                                      | Implicit in RBAC (CKA)                              | App. Env. (explicit)                                |
| **SecurityContext, capabilities, runAsNonRoot, etc.**                                                    | Implicit (admission/cluster security)               | App. Env. (explicit)                                |
| **Authentication, authorization, admission control**                                                     | Cluster Arch. (RBAC primary, admission as operator) | App. Env. (consumer-side understanding)             |
| **Workload resources: Deployment, DaemonSet, CronJob, Job, StatefulSet, ReplicaSet, Pod**                | Workloads & Scheduling                              | App. Design and Build                               |

---

## 4. CKA-Only Topics (Not on CKAD)

These items appear in the CKA curriculum but **do not** appear in the CKAD curriculum. They are predominantly
cluster-build, cluster-lifecycle, and infrastructure-troubleshooting topics.

- **`kubeadm`-based cluster install/join/upgrade/reset** and preparation of underlying infrastructure (container runtime
  install, kernel modules, sysctls, swap)
- **Highly-available control plane** (multi-master, stacked vs. external etcd, load-balancer fronting `kube-apiserver`)
- **Cluster lifecycle management**: minor-version upgrades of control plane and worker nodes, `kubectl drain`/`cordon`/
  `uncordon`
- **etcd backup and restore** (`etcdctl snapshot save/restore`)
- **Designing and managing RBAC** (Role, ClusterRole, RoleBinding, ClusterRoleBinding) — CKA explicitly tests
  creation/management; CKAD only requires consumer-side awareness
- **Extension interfaces**: CNI, CSI, CRI plugin selection and configuration
- **Operators**: install and configure (versus just discover/use)
- **StorageClass design and dynamic volume provisioning** (provisioner, parameters, `volumeBindingMode`, default
  class) — CKAD does not require creating StorageClasses
- **PersistentVolume** lifecycle from the admin side: access modes, reclaim policies (`Retain`/`Delete`), binding,
  expansion
- **Workload autoscaling configuration**: HPA, VPA, Cluster Autoscaler
- **Pod admission and advanced scheduling**: node affinity/anti-affinity, pod affinity/anti-affinity,
  taints/tolerations, topology spread constraints, PriorityClass, scheduler profiles, manual scheduling
- **Gateway API** (`GatewayClass`, `Gateway`, `HTTPRoute`, etc.) — CKAD lists Ingress only
- **CoreDNS configuration and service discovery internals**
- **kube-proxy modes** (iptables / IPVS / nftables)
- **Cluster- and node-level troubleshooting**: kubelet logs (`journalctl -u kubelet`), `crictl`, certificate expiration,
  NotReady nodes, container runtime failures
- **Control-plane component troubleshooting**: static pod manifests in `/etc/kubernetes/manifests/`, troubleshooting
  `kube-apiserver`, `etcd`, `kube-controller-manager`, `kube-scheduler`
- **Cluster-wide service & networking troubleshooting** (kube-proxy rules, CNI plugin issues)

---

## 5. CKAD-Only Topics (Not on CKA)

These items appear in the CKAD curriculum but **do not** appear (or are not emphasized) in the CKA curriculum.

- **Defining, building, and modifying container images** (writing `Dockerfile`s, multi-stage builds, OCI image
  semantics, `imagePullPolicy`, `imagePullSecrets`, private registries) — CKA assumes images already exist
- **Multi-container Pod design patterns**: explicit emphasis on **init containers**, **sidecar containers** (including
  the native sidecar pattern with `restartPolicy: Always` on init containers), **ambassador**, and **adapter** patterns
- **Implementing common deployment strategies from primitives**: explicit blue/green and canary using Services, label
  selectors, and parallel Deployments — CKA covers rolling updates but not blue/green or canary recipes
- **API deprecations** as a developer concern: identifying outdated `apiVersion`s, fixing manifests (e.g.,
  `extensions/v1beta1` → `apps/v1`), using `kubectl explain`, `kubectl convert`, and `kubectl api-versions` to remediate
  broken manifests
- **Probes and health checks** as an explicit, weighted competency (liveness/readiness/startup, with
  httpGet/tcpSocket/exec/grpc handlers and timing tunables) — on CKA this is implicit
- **SecurityContext, Linux capabilities, runAsNonRoot, readOnlyRootFilesystem** as an explicit, weighted developer
  competency
- **Pod Security Admission** profile selection (privileged/baseline/restricted) as an application-author concern
- **Generic ephemeral volumes** and **`subPath`** mounting as a build-time concern
- **Discovering and using CRDs as a consumer** (versus installing them as an operator on CKA)
- **Helm chart consumption as an app deployer** (versus using Helm to install cluster components on CKA)

---

## 6. 2024–2026 Curriculum Changes (vs. older versions)

A major curriculum reset took effect in **February 2024** for both exams. This is the curriculum still in force
throughout 2025 and 2026 (only the underlying Kubernetes minor version has incremented quarterly: v1.29 → v1.30 →
v1.31 → v1.32 → v1.33 → v1.34 → v1.35).

**CKA — what changed in the 2024 reset (still current in 2026):**

- Troubleshooting was **increased from 30% to 30% but reweighted** as the largest single domain (it was the largest
  before too, but the new exam is much heavier on cluster-component and node-level troubleshooting).
- "Workloads & Scheduling" was **reduced from ~15%** and several scheduling concepts shifted toward more advanced
  affinity/topology constraints.
- **Gateway API** was added as a first-class topic (alongside Ingress) — this is the most visible
  Kubernetes-feature-driven change.
- **Helm** and **Kustomize** were added explicitly under "Cluster Architecture, Installation & Configuration" (
  previously only implicit).
- **CRDs and operators** were elevated to explicit competencies under Cluster Architecture.
- **CNI/CSI/CRI** extension interfaces were called out explicitly.
- **etcd backup/restore** remains in the curriculum but is folded into the broader "manage the lifecycle of Kubernetes
  clusters" wording rather than being its own bullet.

**CKAD — what changed in the 2024 reset (still current in 2026):**

- The old curriculum had **seven domain headings** (Core Concepts, Configuration, Multi-Container Pods, Observability,
  Pod Design, Services & Networking, State Persistence). These were **consolidated to five** that mirror the application
  lifecycle: Design and Build / Deployment / Observability and Maintenance / Environment, Configuration and Security /
  Services and Networking.
- **Application Environment, Configuration and Security** was promoted to the largest domain at **25%**, reflecting
  heavier emphasis on Secrets, ServiceAccounts, SecurityContexts, capabilities, and Pod Security Admission.
- **CRDs and Operators** were added (developers now expected to consume custom resources).
- **Helm and Kustomize** were added explicitly under Application Deployment.
- **Blue/green and canary deployment strategies** (built from primitives) were called out explicitly.
- **API deprecations** became an explicit, weighted observability/maintenance competency.
- **Sidecar containers** in the curriculum now reflect the native restartable-sidecar pattern (Kubernetes feature
  graduated to GA in v1.29 and stable in v1.33+).

**Cosmetic / version-only changes 2025 → 2026:**
The published domain list and percentages are **identical** between the v1.31, v1.32, v1.33, v1.34, and v1.35 curriculum
PDFs in `cncf/curriculum`. The only differences across these PDFs are the Kubernetes version banner and minor wording
cleanups. No domain has been added, removed, or reweighted since the February 2024 reset.

---

## 7. Quick Reference Summary Table

| Aspect                     | CKA                                                | CKAD                                                |
|----------------------------|----------------------------------------------------|-----------------------------------------------------|
| Domains                    | 5                                                  | 5                                                   |
| Largest domain             | Troubleshooting (30%)                              | App. Env., Config & Security (25%)                  |
| Smallest domain            | Storage (10%)                                      | App. Observability & Maintenance (15%)              |
| Duration                   | 2 hours                                            | 2 hours                                             |
| Format                     | Performance-based, live cluster                    | Performance-based, live cluster                     |
| Cost (April 2026)          | $445 USD                                           | $445 USD                                            |
| Validity                   | 2 years                                            | 2 years                                             |
| Retakes                    | 1 free retake                                      | 1 free retake                                       |
| Killer.sh simulator        | 2 sessions                                         | 2 sessions                                          |
| K8s version (April 2026)   | v1.34                                              | v1.35                                               |
| Curriculum source of truth | `github.com/cncf/curriculum/cka` + LF product page | `github.com/cncf/curriculum/ckad` + LF product page |

The unifying theme: **CKA** tests you as the person who **builds and operates** the cluster (kubeadm, etcd, HA control
plane, RBAC design, StorageClasses, CNI/CSI/CRI, Gateway API, scheduling, troubleshooting nodes and components). **CKAD
** tests you as the person who **builds and ships applications onto** an existing cluster (Dockerfiles, multi-container
patterns, probes, ConfigMaps/Secrets, SecurityContexts, deployment strategies, debugging your own apps). The overlap —
Deployments, Services, Ingress, NetworkPolicies, ConfigMaps/Secrets, RBAC concepts, volumes, observability — is real but
is approached from opposite sides of the cluster boundary.
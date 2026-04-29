# CKAD — Certified Kubernetes Application Developer

## Exam Overview

| | |
|---|---|
| **Format** | Performance-based (hands-on CLI tasks in a live cluster) |
| **Duration** | 2 hours |
| **Passing score** | 66% |
| **Cost** | $445 USD (includes one free retake) |
| **Validity** | 2 years |
| **K8s version** | v1.35 (as of April 2026) |
| **Simulator** | 2 Killer.sh sessions included |
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

---

## Domain Topics

### Application Design and Build (20%)

**Container Images**
- Write `Dockerfile`s: `FROM`, `RUN`, `COPY`, `WORKDIR`, `EXPOSE`, `USER`, `ENTRYPOINT`/`CMD`
- Multi-stage builds to reduce final image size; minimal base images; `.dockerignore`
- Non-root `USER` in Dockerfile as a security best practice
- Image tags vs. digests; `imagePullPolicy` (`Always`, `IfNotPresent`, `Never`)
- `imagePullSecrets` for private registries; `docker.io/library/*` OCI compliance

**Workload Resources — Choosing the Right One**
- `Deployment`: long-running, stateless, rolling updates
- `StatefulSet`: ordered identity, stable network names, persistent storage per replica
- `DaemonSet`: one pod per node (log agents, monitoring collectors)
- `Job`: run-to-completion; `completions`, `parallelism`, `backoffLimit`, `activeDeadlineSeconds`, `restartPolicy: Never|OnFailure`
- `CronJob`: schedule (cron syntax), `concurrencyPolicy` (`Allow`/`Forbid`/`Replace`), `startingDeadlineSeconds`, `successfulJobsHistoryLimit`, `failedJobsHistoryLimit`

**Multi-Container Pod Patterns**
- **Init containers**: sequential dependency checks, one-time setup; block main container until complete
- **Sidecar containers** (native, GA in v1.29+): set `restartPolicy: Always` inside `initContainers` — runs for the full pod lifetime alongside main container; log shipping, proxy injection
- **Ambassador**: outbound proxy pattern (route traffic to external services through a local proxy)
- **Adapter**: transform or normalise output for a monitoring/logging system

**Volumes**
- Ephemeral: `emptyDir` (shared scratch space between containers in a pod), `hostPath`
- Projected: `configMap`, `secret`, `downwardAPI`, `projected` (combine multiple sources)
- Persistent: `persistentVolumeClaim`; `volumeMounts`, `subPath`
- Generic ephemeral volumes (`ephemeral:` block in pod spec)

---

### Application Deployment (20%)

**Rolling Updates & Rollbacks**
- `strategy.type: RollingUpdate` (default) vs. `Recreate`
- `maxSurge`, `maxUnavailable` — control pace and availability during rollout
- `kubectl rollout status|history|undo|pause|resume|restart`
- `--to-revision=<N>` to target a specific history entry; `revisionHistoryLimit`

**Deployment Strategies (from primitives)**
- **Canary**: two Deployments sharing one Service (matching label); control traffic split by replica count ratio
- **Blue/Green**: two Deployments; swap Service selector (`kubectl set selector`) to cut over traffic instantly

**Helm**
- `helm repo add / update / list / search repo`
- `helm install <release> <chart>`, `helm upgrade`, `helm rollback`, `helm uninstall`
- `helm list`, `helm status <release>`, `helm show values <chart>`
- Override values: `--set key=value` (inline) vs. `-f values.yaml` (file); understand precedence
- `helm template <release> <chart>` to render manifests without installing
- `helm get manifest <release>` to inspect what is running

**Kustomize**
- `kustomization.yaml`: `resources:`, `namespace:`, `commonLabels:`, `commonAnnotations:`, `namePrefix:`, `nameSuffix:`
- `images:` transformer to change image tags without editing base manifests
- `configMapGenerator:` and `secretGenerator:` with `--from-literal` / `--from-file` / `--from-env-file`
- Bases and overlays (`dev` / `staging` / `prod`): `resources:` pointing to a base path
- Patches: `patchesStrategicMerge:` (YAML merge) and `patches:` with JSON-6902 (`op: replace/add/remove`)
- Apply: `kubectl apply -k <dir>`

---

### Application Observability and Maintenance (15%)

**Health Probes**
- `livenessProbe`: restarts container when it fails; use for deadlock/crash detection
- `readinessProbe`: removes pod from Service endpoints until it passes; use for warm-up gates
- `startupProbe`: disables liveness/readiness checks until it passes; use for slow-starting apps
- Probe handlers: `httpGet` (path, port), `tcpSocket` (port), `exec` (command), `grpc` (port, service)
- Timing tunables: `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`

**Monitoring**
- `kubectl top pod|node` (requires `metrics-server`)
- `kubectl get events --sort-by=.lastTimestamp`
- `kubectl describe <resource>` — first debugging step; check `Events:` section

**Logs**
- `kubectl logs <pod> -c <container>`, `--previous`, `-f`, `--since`, `--tail`, `--all-containers`
- Multi-container pods: always specify `-c <container>` when more than one container is present

**Debugging**
- `kubectl describe pod` — image pull failures, OOMKilled, probe failures
- `kubectl exec -it <pod> -- /bin/sh` — interactive shell inside running container
- `kubectl debug <pod> --image=busybox --copy-to=<new-pod>` — copy pod with debug container
- Ephemeral debug containers: `kubectl debug -it <pod> --image=busybox --target=<container>` (distroless-safe)
- `kubectl debug node/<node> --image=busybox` — attach a container in host namespaces
- `kubectl port-forward pod/<pod> <local>:<remote>` — forward traffic for local testing
- `kubectl cp <pod>:<path> <local>` — copy files out of a container

**API Deprecations**
- Identify outdated `apiVersion` (e.g., `extensions/v1beta1` → `apps/v1`)
- `kubectl explain <resource>.<field>` — check current schema and apiVersion
- `kubectl api-resources`, `kubectl api-versions` — list available APIs
- `kubectl convert -f <manifest> --output-version <group/version>` (requires `kubectl-convert` plugin)

---

### Application Environment, Configuration and Security (25%)

**ConfigMaps**
- Create: `kubectl create configmap <name> --from-literal=key=val --from-file=path --from-env-file=.env`
- Consume as env vars: `env[].valueFrom.configMapKeyRef` or `envFrom[].configMapRef`
- Consume as volume: mounts each key as a file; `subPath` to mount a single key
- Immutable ConfigMaps: `immutable: true` (changes rejected; reduces API server load)

**Secrets**
- Types: `Opaque` (default), `kubernetes.io/dockerconfigjson`, `kubernetes.io/tls`, `kubernetes.io/service-account-token`, `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth`
- Create: `kubectl create secret generic <name> --from-literal=key=val`
- Base64 encoding: `echo -n 'value' | base64` / `echo 'b64' | base64 -d`
- Consume: same as ConfigMaps (env vars or volume mount)
- Immutable Secrets: `immutable: true`

**ServiceAccounts**
- Create: `kubectl create serviceaccount <name>`
- Attach to pod: `spec.serviceAccountName`
- Disable auto-mount: `automountServiceAccountToken: false` (pod or SA level)
- Projected token volumes: short-lived, audience-scoped tokens via `serviceAccountToken` projected volume source

**Resource Management**
- Container `resources.requests` (scheduling guarantee) vs. `resources.limits` (enforcement ceiling)
- Units: CPU in millicores (`500m` = 0.5 CPU), memory in bytes (`256Mi`, `1Gi`)
- `LimitRange`: sets default `requests`/`limits` per container or pod within a namespace
- `ResourceQuota`: caps total CPU, memory, and object counts per namespace; triggers `403 Forbidden` on violation
- **In-place Pod Resource Resize** (GA in v1.35): change container `requests`/`limits` without pod restart using `kubectl patch pod <name> --subresource resize --patch '{...}'`; `resizePolicy` field per resource (`NotRequired` vs. `RestartContainer`)

**CRDs & Operators**
- `kubectl get crd` — list installed Custom Resource Definitions
- `kubectl explain <cr>.<field>` — inspect schema of a custom resource
- Create/update/delete custom resource instances like native objects
- Discover what operators manage (via ownerReferences, controller logs)

**Authentication, Authorization & Admission**
- RBAC (consumer perspective): `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding`
- `kubectl auth can-i <verb> <resource> --as=<user>` — check effective permissions
- Pod Security Admission labels on namespaces:
  - `pod-security.kubernetes.io/enforce: restricted|baseline|privileged`
  - `pod-security.kubernetes.io/audit: restricted|baseline|privileged`
  - `pod-security.kubernetes.io/warn: restricted|baseline|privileged`
- Admission controllers (conceptual): `LimitRanger`, `ResourceQuota`, `PodSecurity`, mutating vs. validating webhooks
- **CEL-based ValidatingAdmissionPolicy** (GA in v1.35): inline CEL expressions validated server-side without external webhook; bind with `ValidatingAdmissionPolicyBinding`

**SecurityContext**
- Pod level: `runAsUser`, `runAsGroup`, `fsGroup`, `runAsNonRoot`, `supplementalGroups`
- Container level: `runAsUser`, `runAsNonRoot`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`
- Linux capabilities: `capabilities.add: [NET_ADMIN]`, `capabilities.drop: [ALL]`
- Seccomp profiles: `seccompProfile.type: RuntimeDefault|Localhost`
- **User Namespaces** (`hostUsers: false` in pod spec, default-enabled in v1.35): UID/GID inside container mapped to unprivileged IDs on host — mitigates privilege escalation
- **Pod Certificates** (`podCertificate` projected volume, beta in v1.35): kubelet auto-issues and rotates X.509 certs for workloads; set `signerName` and `keyType` (e.g., `ED25519`)

---

### Services and Networking (20%)

**Services**
- `ClusterIP` (default): cluster-internal VIP; set `clusterIP: None` for headless service (DNS returns pod IPs directly)
- `NodePort`: exposes on every node at a static port (30000–32767)
- `LoadBalancer`: provisions external LB (cloud); `externalTrafficPolicy`
- `ExternalName`: CNAME alias to an external DNS name
- `spec.selector` must match pod labels; `targetPort` (container port, int or named string) vs. `port` (service port)
- `kubectl expose deployment <name> --port=80 --target-port=8080 --type=ClusterIP`
- Troubleshoot via `Endpoints` / `EndpointSlice`: `kubectl get endpoints <svc>`

**Ingress**
- `Ingress` resource: `rules[].host`, `rules[].http.paths[].path`, `pathType` (`Exact`/`Prefix`/`ImplementationSpecific`)
- `ingressClassName` field (replaces deprecated `kubernetes.io/ingress.class` annotation)
- TLS termination: reference a `kubernetes.io/tls` Secret in `spec.tls`
- Common troubleshooting: 404 (path mismatch or wrong `pathType`), 503 (backend service selector mismatch)

**Gateway API** (explicit in v1.35 curriculum)
- `GatewayClass`: defines the controller type (cluster-scoped, set by admin)
- `Gateway`: declares listeners (port, protocol, TLS) — cluster or namespace-scoped
- `HTTPRoute`: developer-facing; attach to a `Gateway` via `parentRefs`
  - Path matching: `matches[].path.type: PathPrefix|Exact`
  - Header-based routing: `matches[].headers`
  - Traffic splitting (canary): `backendRefs[].weight` — e.g., 90% v1, 10% v2
- `ReferenceGrant`: allows cross-namespace references (e.g., HTTPRoute → Service in another namespace)

**NetworkPolicies**
- Default: all traffic allowed; first NetworkPolicy creates implicit deny for selected pods
- Default-deny pattern: empty `podSelector: {}` + empty `ingress: []` or `egress: []`
- Selectors: `podSelector`, `namespaceSelector`, `ipBlock` (CIDR + `except`)
- `ports[].port` and `ports[].protocol` (must be uppercase: `TCP`, `UDP`, `SCTP`)
- Ingress and egress rules are independent; both directions must be explicitly allowed for bidirectional traffic

**DNS**
- Service DNS: `<svc>.<namespace>.svc.cluster.local`
- Pod DNS: `<pod-ip-dashes>.<namespace>.pod.cluster.local`
- `dnsPolicy`: `ClusterFirst` (default), `ClusterFirstWithHostNet`, `Default`, `None`
- `dnsConfig` for custom nameservers and search domains
- Service discovery: prefer DNS over env vars (env vars only set at pod start time)

---

## CKAD-Only Topics (Not on CKA)

These subjects appear in the CKAD curriculum but are omitted from CKA:

- **Defining, building, and modifying container images** — writing `Dockerfile`s, multi-stage builds, OCI image semantics, `imagePullPolicy`, `imagePullSecrets`, private registries (CKA assumes images already exist)
- **Multi-container Pod design patterns** — explicit emphasis on **init containers**, **sidecar containers** (native restartable sidecar with `restartPolicy: Always`), **ambassador**, and **adapter** patterns
- **Common deployment strategies from primitives** — explicit **blue/green** (Service selector swap) and **canary** (parallel Deployments + label ratio) recipes; CKA covers rolling updates but not these patterns
- **API deprecations** as a developer concern — identifying outdated `apiVersion`s, fixing manifests (`extensions/v1beta1` → `apps/v1`), `kubectl convert`, `kubectl api-versions`
- **Probes and health checks** as an explicit, weighted competency — liveness/readiness/startup with `httpGet`/`tcpSocket`/`exec`/`grpc` handlers and timing tunables
- **SecurityContext, Linux capabilities, `runAsNonRoot`, `readOnlyRootFilesystem`** as explicit, weighted developer competencies
- **Pod Security Admission** profile selection (`privileged` / `baseline` / `restricted`) as an application-author concern
- **Generic ephemeral volumes** and `subPath` volume mounting as a build-time concern
- **Discovering and using CRDs as a consumer** — `kubectl get crd`, creating/updating custom resource instances (versus installing CRDs as an operator on CKA)
- **Helm chart consumption as an app deployer** — `helm repo add`, `helm install`, `helm upgrade`, `--set` / `-f` overrides (versus using Helm to install cluster components on CKA)

---

## 2024–2026 Curriculum Changes

A major curriculum reset took effect in **February 2024** and remains current for 2025/2026. Key CKAD updates:
- Seven old domain headings **consolidated to five** mirroring the application lifecycle.
- **Application Environment, Configuration and Security** promoted to the largest domain at **25%**, reflecting heavier emphasis on Secrets, ServiceAccounts, SecurityContexts, capabilities, and Pod Security Admission.
- **CRDs and Operators** added — developers now expected to consume custom resources.
- **Helm and Kustomize** added explicitly under Application Deployment.
- **Blue/green and canary deployment strategies** (built from primitives) called out explicitly.
- **API deprecations** became an explicit, weighted observability/maintenance competency.
- **Native sidecar containers** (`restartPolicy: Always` on init containers) reflect the GA sidecar pattern (GA in v1.29+, stable in v1.33+).
- **Gateway API** (`HTTPRoute`, `GatewayClass`, `Gateway`) added as a first-class topic in v1.35.
- **In-place Pod Resource Resize** now a required skill (GA in v1.35) — `kubectl patch pod --subresource resize`.
- **User Namespaces** (`hostUsers: false`, default-enabled in v1.35) and **Pod Certificates** (`podCertificate` projected volume, beta in v1.35) added as developer-level security competencies.
- **CEL-based ValidatingAdmissionPolicy** (GA in v1.35) — developers must understand namespace-level admission policies that affect their workloads.

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

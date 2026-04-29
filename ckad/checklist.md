# CKAD Exam Checklist
**Kubernetes v1.35 · 2026 · Performance-based · 2 hours · 66% passing score**

Domain weights: App Environment, Config & Security 25% · App Design & Build 20% · App Deployment 20% · Services & Networking 20% · App Observability & Maintenance 15%

Items marked **[S]** are shared with CKA but tested here from the application-developer perspective.

---

# Domain 1 — Application Design and Build (20%)

## Container Images & Dockerfiles

- [ ] D-001. Write a `Dockerfile` with `FROM`, `RUN`, `COPY`, `ADD`, `WORKDIR`, `EXPOSE`, `ENV`, `ARG`, `CMD`, and `ENTRYPOINT` instructions and understand the layering model.
- [ ] D-002. Explain the difference between `CMD` and `ENTRYPOINT` in a Dockerfile and how they interact (exec vs. shell form, override behavior).
- [ ] D-003. Use a multi-stage `Dockerfile` to separate the build environment from the final runtime image, reducing the final image size significantly.
- [ ] D-004. Understand how `COPY --from=<stage>` works in a multi-stage build to selectively copy artifacts between stages.
- [ ] D-005. Override a Docker image's `CMD` from the Kubernetes Pod spec using `spec.containers[].args`.
- [ ] D-006. Override a Docker image's `ENTRYPOINT` from the Kubernetes Pod spec using `spec.containers[].command`.
- [ ] D-007. Set the `imagePullPolicy` to `Always`, `IfNotPresent`, or `Never` and explain when each is appropriate (especially `Always` for `latest` tag).
- [ ] D-008. Reference a private registry image in a Pod spec and attach an `imagePullSecrets` entry pointing to a Docker registry Secret.
- [ ] D-009. Understand image digest pinning (`image: repo/name@sha256:<hash>`) versus tag-based references and the immutability advantage of digests.

---

## Workload Resources **[S]**

- [ ] S-001. Explain the role of a `ReplicaSet` and how its label selector continuously reconciles the desired number of running Pods.
- [ ] S-002. Describe how a `Deployment` wraps a `ReplicaSet` to enable declarative updates, rollbacks, and scaling without downtime.
- [ ] S-003. Create a `Deployment` imperatively with `kubectl create deployment` and declaratively via a YAML manifest specifying `replicas`, `selector.matchLabels`, and `template`.
- [ ] S-004. Perform a rolling update on a `Deployment` by changing the container image, and monitor its progress with `kubectl rollout status`.
- [ ] S-005. Configure `maxSurge` and `maxUnavailable` under `strategy.rollingUpdate` to control how many Pods are added or removed during a rolling update.
- [ ] S-006. Roll back a `Deployment` to its previous revision using `kubectl rollout undo` and to a specific revision using `--to-revision=<n>`.
- [ ] S-007. Inspect `Deployment` revision history with `kubectl rollout history` and understand how `revisionHistoryLimit` controls the number of stored `ReplicaSets`.
- [ ] S-008. Pause and resume a `Deployment` rollout using `kubectl rollout pause` and `kubectl rollout resume` to batch multiple changes into a single rollout.
- [ ] S-009. Force a restart of all Pods in a `Deployment` without changing the spec using `kubectl rollout restart`.
- [ ] S-010. Explain when to use a `StatefulSet` (stable network identity, stable storage, ordered deployment and scaling) versus a `Deployment`.
- [ ] S-011. Describe how `StatefulSet` names Pods with a predictable ordinal index and creates `PersistentVolumeClaims` per Pod via `volumeClaimTemplates`.
- [ ] S-012. Explain the use case of a `DaemonSet` — running exactly one Pod per matching node — and give three real-world examples (log collector, monitoring agent, CNI plugin).
- [ ] S-013. Create a `Job` that runs a task to completion and configure `completions`, `parallelism`, `backoffLimit`, and `activeDeadlineSeconds`.
- [ ] S-014. Distinguish between `Job` completion modes: `NonIndexed` (default) versus `Indexed` (each Pod gets a unique completion index via `JOB_COMPLETION_INDEX`).
- [ ] S-015. Create a `CronJob` with a valid cron schedule expression, and explain `successfulJobsHistoryLimit`, `failedJobsHistoryLimit`, and `concurrencyPolicy` (`Allow`, `Forbid`, `Replace`).
- [ ] S-016. Identify and fix a `CronJob` that has missed its schedule due to `startingDeadlineSeconds` being exceeded.

---

## StatefulSet & DaemonSet Update Strategies **[S]**

- [ ] S-104. Configure a `StatefulSet` with `updateStrategy.type: RollingUpdate` and understand that Pods are updated in reverse ordinal order (highest index first).
- [ ] S-105. Set `updateStrategy.type: OnDelete` on a `StatefulSet` to require manual deletion of each Pod before the updated template is applied to it; use this when you need full control over the upgrade sequence.
- [ ] S-106. Use `updateStrategy.rollingUpdate.partition` on a `StatefulSet` to perform a canary-style staged rollout: only Pods with an ordinal index ≥ the partition value are updated, leaving lower-indexed Pods on the old version.
- [ ] S-107. Configure a `DaemonSet` update strategy with `rollingUpdate.maxUnavailable` to control how many nodes' Pods are taken down simultaneously during a DaemonSet rolling update.
- [ ] S-108. Understand that `kubectl rollout undo` is **not supported** for `StatefulSet` — to roll back a StatefulSet, manually set `spec.template.spec.containers[].image` back to the previous version and let the rolling update strategy apply the change.

---

## Job & CronJob Advanced **[S]**

- [ ] S-109. Set `spec.ttlSecondsAfterFinished` on a `Job` to automatically delete it (and its Pods) a fixed number of seconds after it reaches a terminal state (`Complete` or `Failed`), preventing accumulation of finished Jobs.
- [ ] S-110. Suspend a `CronJob` by setting `spec.suspend: true` (e.g., `kubectl patch cronjob <name> -p '{"spec":{"suspend":true}}'`) and resume it by setting it back to `false`; understand that all scheduled runs are skipped while suspended.

---

## Multi-Container Pod Patterns

- [ ] D-010. Explain why containers in the same Pod share a network namespace (same IP, same port space) and can communicate via `localhost`.
- [ ] D-011. Explain why containers in the same Pod can share storage by mounting the same `emptyDir` volume to exchange data at runtime.
- [ ] D-012. Write an **init container** that runs to completion before the main container starts and use it to pre-populate a shared `emptyDir` volume.
- [ ] D-013. Use an init container to wait for a dependency (e.g., a database Service) to be available before the main application starts.
- [ ] D-014. Write a **sidecar container** that runs alongside the main container to handle a cross-cutting concern (e.g., log shipper, proxy, metrics exporter).
- [ ] D-015. Implement the native restartable sidecar pattern (Kubernetes v1.29+ GA): place the sidecar as an init container with `restartPolicy: Always` so it starts before app containers and outlives them.
- [ ] D-016. Implement the **ambassador** pattern: a proxy sidecar that intercepts outbound traffic from the main container (e.g., routing to a local proxy).
- [ ] D-017. Implement the **adapter** pattern: a sidecar that transforms output from the main container into a standard format (e.g., normalizing log format for a centralized logging system).
- [ ] D-018. Write a Pod spec with multiple containers each having their own `resources`, `env`, `volumeMounts`, and `readinessProbe`.

---

## Pod Lifecycle Hooks **[S]**

- [ ] S-101. Configure a `lifecycle.postStart` exec handler that runs a command immediately after a container starts, and understand that it blocks the container from reaching `Running` state until the handler completes or times out.
- [ ] S-102. Configure a `lifecycle.preStop` exec or sleep handler to delay SIGTERM and enable graceful shutdown (e.g., `preStop: exec: command: ["sleep","10"]`); this is essential for zero-downtime deployments behind a load balancer.
- [ ] S-103. Explain how `terminationGracePeriodSeconds` interacts with `preStop`: the kubelet waits up to `terminationGracePeriodSeconds` for both the `preStop` handler and the main process to exit before sending SIGKILL; the `preStop` duration counts against this budget.

---

## Volumes (Developer Perspective)

- [ ] S-073. Distinguish between the admin role (creates `PersistentVolume` or `StorageClass`) and the developer role (creates `PersistentVolumeClaim` to consume storage).
- [ ] S-074. Write a `PersistentVolumeClaim` manifest specifying `storageClassName`, `accessModes`, and `resources.requests.storage`.
- [ ] S-075. Mount a `PersistentVolumeClaim` in a Pod by adding it to `volumes` and referencing it in `volumeMounts` with a `mountPath`.
- [ ] S-076. Explain the four access modes — `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod` — and which volume backends support each.
- [ ] S-077. Explain the PVC lifecycle: Pending → Bound, and what causes a PVC to remain `Pending` (no matching PV, StorageClass provisioner unavailable).
- [ ] S-078. Use `emptyDir` for ephemeral shared storage between containers in the same Pod and understand that data is lost when the Pod is deleted.
- [ ] D-056. Use an `emptyDir` volume shared between an init container and the main container to pre-seed configuration or data files at startup.
- [ ] D-057. Use a `downwardAPI` volume to expose Pod labels and annotations as files inside the container for consumption by the application.
- [ ] D-058. Use a `projected` volume to combine multiple sources (ConfigMap, Secret, downwardAPI, ServiceAccount token) into a single unified mount point.
- [ ] D-059. Request ephemeral storage with `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` to protect against disk-hungry containers evicting other Pods.
- [ ] D-060. Use `subPathExpr` in a `volumeMount` to dynamically set the subpath using a Pod environment variable expansion.
- [ ] D-072. Define a generic ephemeral volume inline in a Pod spec using the `ephemeral:` volume type with an embedded `volumeClaimTemplate`; a PVC is automatically provisioned when the Pod starts and deleted when the Pod is deleted — unlike `emptyDir`, this uses a `StorageClass` and survives container restarts within the same Pod.

---

# Domain 2 — Application Deployment (20%)

## Application Deployment Strategies

- [ ] D-028. Implement a **blue/green** deployment using two `Deployment` objects (one active, one idle) and switch live traffic by changing the `Service` `selector` label.
- [ ] D-029. Implement a **canary** deployment by running two `Deployment` objects with shared labels and splitting traffic proportionally through replica counts.
- [ ] D-030. Explain the trade-offs between blue/green (instant switch, double resources) and canary (gradual rollout, partial risk exposure, incremental validation).
- [ ] D-031. Configure a `Deployment` with `strategy.type: Recreate` to terminate all existing Pods before creating new ones (accepts downtime, avoids mixed-version state).
- [ ] D-032. Write the full rollout workflow for a failed deployment: push bad image → observe failure → `kubectl rollout undo` → verify rollback with `kubectl rollout status`.

---

## Helm **[S]**

- [ ] S-036. Add a Helm repository with `helm repo add`, update the cache with `helm repo update`, and search for available charts with `helm search repo`.
- [ ] S-037. Install a chart with `helm install <release> <chart>` and override values using `--set key=value` and `--values values.yaml`.
- [ ] S-038. List all deployed Helm releases in a namespace with `helm list` and across all namespaces with `helm list -A`.
- [ ] S-039. Upgrade an existing release with `helm upgrade` and roll back to a previous revision with `helm rollback <release> <revision>`.
- [ ] S-040. Uninstall a release with `helm uninstall` and verify that all managed resources have been removed.
- [ ] S-041. Render Helm templates locally without installing them using `helm template` to inspect the generated Kubernetes manifests.
- [ ] S-042. Inspect the values available in a chart with `helm show values <chart>` and understand how to override defaults.

---

## Kustomize **[S]**

- [ ] S-043. Write a minimal `kustomization.yaml` that references a list of `resources` (YAML files) and apply it with `kubectl apply -k`.
- [ ] S-044. Add `commonLabels` and `commonAnnotations` in `kustomization.yaml` to patch all managed resources simultaneously.
- [ ] S-045. Use `namePrefix` and `nameSuffix` in `kustomization.yaml` to rename all resources without touching individual files.
- [ ] S-046. Build a base-overlay Kustomize structure: a `base/` directory with a `kustomization.yaml` and one or more `overlays/` (dev, staging, prod) that extend it.
- [ ] S-047. Apply a strategic-merge patch in an overlay to override specific fields (e.g., replica count or image tag) without duplicating the entire manifest.
- [ ] S-048. Apply a JSON-6902 patch (`patchesJson6902`) in an overlay to add, remove, or replace specific fields using JSON patch operations.
- [ ] S-049. Use the `images:` transformer in `kustomization.yaml` to override a container image name or tag across all resources.
- [ ] S-050. Generate a `ConfigMap` or `Secret` inline with `configMapGenerator` and `secretGenerator` inside `kustomization.yaml`.

---

# Domain 3 — Application Observability and Maintenance (15%)

## Probes & Health Checks

- [ ] D-019. Configure a `livenessProbe` using `httpGet` on a specific path and port and explain what happens when it fails (container restart, subject to `restartPolicy`).
- [ ] D-020. Configure a `livenessProbe` using `exec` to run a command inside the container and explain how exit code 0 means healthy.
- [ ] D-021. Configure a `livenessProbe` using `tcpSocket` to check if a specific port is accepting connections.
- [ ] D-022. Configure a `livenessProbe` using `grpc` to call a gRPC Health Checking Protocol endpoint.
- [ ] D-023. Configure a `readinessProbe` and explain how it controls whether a Pod's IP is added to the Service `Endpoints` — it does not cause restarts.
- [ ] D-024. Configure a `startupProbe` to give slow-starting containers time to initialize before liveness and readiness probes begin evaluating.
- [ ] D-025. Tune probe parameters: `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `successThreshold`, and `failureThreshold` and explain each field's effect.
- [ ] D-026. Diagnose a Pod that is repeatedly being restarted by identifying a misconfigured `livenessProbe` from `kubectl describe pod` events.
- [ ] D-027. Diagnose a Pod that never receives traffic by identifying a `readinessProbe` that is permanently failing.

---

## API Deprecations & Discovery

- [ ] D-033. Identify deprecated API versions in a manifest (e.g., `extensions/v1beta1`) by running `kubectl apply --dry-run=server` and reading the deprecation warning.
- [ ] D-034. Use `kubectl api-resources` to list all resource types, their short names, API groups, and whether they are namespaced.
- [ ] D-035. Use `kubectl api-versions` to list all API groups and their available versions currently served by the cluster.
- [ ] D-036. Use `kubectl explain <resource>.<field>` to interactively explore the API schema and find the correct field names for any resource.
- [ ] D-037. Use `kubectl explain --recursive <resource>` to get the full field tree for a resource for quick YAML authoring in the exam.
- [ ] D-038. Fix a manifest that uses a deprecated API version by editing `apiVersion` and updating any removed or renamed fields to match the current API.
- [ ] D-065. Use the `kubectl-convert` plugin (`kubectl convert -f <manifest.yaml> --output-version <group/version>`) to automatically rewrite a manifest from a deprecated API version to a supported one; install the plugin separately from the kubectl binary.

---

## Observability: Logs, Events, Top, Debug **[S]**

- [ ] S-085. Stream logs from a running container using `kubectl logs -f <pod> -c <container>` and retrieve terminated container logs with `--previous`.
- [ ] S-086. Filter logs by time window using `--since=1h` or `--since-time=<RFC3339>` and limit output with `--tail=50`.
- [ ] S-087. Retrieve logs from all containers in a Pod simultaneously with `kubectl logs <pod> --all-containers=true`.
- [ ] S-088. View cluster events sorted by timestamp using `kubectl get events --sort-by='.lastTimestamp'` to diagnose recent failures.
- [ ] S-089. Check node and Pod resource usage with `kubectl top nodes` and `kubectl top pods --sort-by=memory` using the metrics-server.
- [ ] S-090. Use `kubectl describe pod <name>` to read the `Events` section and diagnose issues like `ImagePullBackOff`, `OOMKilled`, and `CrashLoopBackOff`.
- [ ] S-091. Launch an ephemeral debug container into a running Pod with `kubectl debug -it <pod> --image=busybox --target=<container>`.
- [ ] S-092. Create a debugging copy of a Pod with a different image using `kubectl debug <pod> -it --copy-to=<debug-pod> --set-image=<container>=busybox`.
- [ ] S-093. Debug a node directly by launching a privileged Pod on it with `kubectl debug node/<node> -it --image=ubuntu`.
- [ ] S-094. Copy files to and from a running container with `kubectl cp <pod>:<remote-path> <local-path>` and vice versa.
- [ ] S-095. Use `kubectl port-forward pod/<name> 8080:80` to test a container's HTTP endpoint locally without exposing it via a Service.
- [ ] S-096. Use `kubectl exec -it <pod> -- sh` to get a shell into a running container for live troubleshooting.

---

# Domain 4 — Application Environment, Configuration and Security (25%)

## ConfigMaps **[S]**

- [ ] S-017. Create a `ConfigMap` from literal values (`--from-literal`), from a file (`--from-file`), and from an env file (`--from-env-file`), and inspect its data with `kubectl describe`.
- [ ] S-018. Inject all keys from a `ConfigMap` into a container as environment variables using `envFrom.configMapRef`.
- [ ] S-019. Inject a single key from a `ConfigMap` into an environment variable using `env.valueFrom.configMapKeyRef`.
- [ ] S-020. Mount a `ConfigMap` as a volume so each key becomes a file inside a directory in the container filesystem.
- [ ] S-021. Use `subPath` to mount a single key from a `ConfigMap` volume to a specific file path without replacing the entire directory.
- [ ] S-022. Create an immutable `ConfigMap` by setting `immutable: true` and explain why this improves performance at scale.

---

## Advanced ConfigMap & Secret Usage

- [ ] D-049. Use `configMapGenerator` in a Kustomize `kustomization.yaml` to auto-generate a ConfigMap from files with a hash suffix to trigger rolling updates on change.
- [ ] D-050. Use `secretGenerator` in a Kustomize `kustomization.yaml` to generate a Secret from literal values in an overlay.
- [ ] D-051. Understand that updating a ConfigMap mounted as a volume eventually updates the file inside a running container (kubelet refresh delay ~60s), unlike env vars which require a Pod restart.
- [ ] D-052. Pass Pod metadata into a container using `downwardAPI` volumes or env vars to expose `metadata.name`, `metadata.namespace`, `status.podIP`, and resource field values.
- [ ] D-073. Understand that a ConfigMap or Secret mounted via `subPath` does **not** automatically refresh inside a running container when the source data changes — only a full directory mount (without `subPath`) benefits from the kubelet's periodic refresh (~60 s); applications using `subPath` mounts require a Pod restart (e.g., `kubectl rollout restart deployment/<name>`) to pick up changes.

---

## Secrets **[S]**

- [ ] S-023. Create an `Opaque` `Secret` from literal values and understand that values are base64-encoded (not encrypted) at rest by default.
- [ ] S-024. Decode a `Secret` value in the shell using `kubectl get secret <name> -o jsonpath='{.data.<key>}' | base64 -d`.
- [ ] S-025. Inject `Secret` data into a container as environment variables via `envFrom.secretRef` and `env.valueFrom.secretKeyRef`.
- [ ] S-026. Mount a `Secret` as a volume, understanding that each key becomes a file and the value is the decoded content.
- [ ] S-027. Create a `kubernetes.io/tls` Secret from a certificate and key file using `kubectl create secret tls`.
- [ ] S-028. Create a `kubernetes.io/dockerconfigjson` Secret for authenticating to a private container registry and reference it in a Pod via `imagePullSecrets`.
- [ ] S-029. Create an immutable `Secret` with `immutable: true` and explain the kubelet caching benefit.

---

## Additional Secret Types

- [ ] D-066. Recognize the `kubernetes.io/basic-auth` Secret type (required data keys: `username` and `password`) and the `kubernetes.io/ssh-auth` type (required key: `ssh-privatekey`); create them with `kubectl create secret` or a YAML manifest specifying `type:`.
- [ ] D-067. Recognize the `kubernetes.io/service-account-token` Secret type as the legacy mechanism for manually creating long-lived SA tokens; in Kubernetes v1.24+ tokens are no longer auto-created as Secrets — prefer `kubectl create token <sa-name>` for short-lived tokens or a projected `serviceAccountToken` volume.

---

## Resource Requests, Limits, LimitRange, ResourceQuota **[S]**

- [ ] S-030. Define `resources.requests.cpu` and `resources.requests.memory` on a container and explain how the scheduler uses requests for node selection.
- [ ] S-031. Define `resources.limits.cpu` and `resources.limits.memory` and explain how the kubelet enforces them (CPU throttling via cgroups; OOMKill for memory).
- [ ] S-032. Explain the three QoS classes — `Guaranteed`, `Burstable`, `BestEffort` — and the conditions that place a Pod into each class.
- [ ] S-033. Create a `LimitRange` that sets default requests and limits for containers, and a maximum and minimum range for CPU and memory.
- [ ] S-034. Create a `ResourceQuota` that limits the total CPU, memory, and object counts (Pods, Services, PVCs) within a namespace.
- [ ] S-035. Demonstrate what happens when a Pod spec violates a `LimitRange` or a `ResourceQuota` (admission rejection with descriptive error).
- [ ] S-111. Define `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` on a container to protect against disk-hungry containers; when the limit is exceeded the kubelet evicts the Pod from the node.

---

## ServiceAccounts **[S]**

- [ ] S-079. Explain how every Pod is automatically associated with a `ServiceAccount` (default is `default` in the namespace) and what token is auto-mounted.
- [ ] S-080. Create a named `ServiceAccount` with `kubectl create serviceaccount` and associate it with a Pod via `spec.serviceAccountName`.
- [ ] S-081. Disable the automatic mounting of the service account token in a Pod by setting `automountServiceAccountToken: false`.
- [ ] S-082. Explain the components of RBAC: `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding` and which scope (namespace vs. cluster) each applies to.
- [ ] S-083. Create a `Role` that grants `get`, `list`, and `watch` on `pods` within a namespace, and bind it to a `ServiceAccount` via a `RoleBinding`.
- [ ] S-084. Test what a `ServiceAccount` or user is allowed to do using `kubectl auth can-i <verb> <resource> --as=<user> -n <namespace>`.
- [ ] D-053. Create a `ServiceAccount`, bind it to a `Role` that allows specific API operations, and reference it in a Pod to give the application Kubernetes API access.
- [ ] D-054. Mount a projected `ServiceAccount` token with a custom audience and expiry using the `projected` volume with a `serviceAccountToken` source.
- [ ] D-055. Explain why `automountServiceAccountToken: false` is a security best practice for Pods that do not need to call the Kubernetes API.

---

## SecurityContexts & Application Security

- [ ] D-039. Set a `securityContext` at the **Pod level** to define `runAsUser`, `runAsGroup`, `fsGroup`, and `supplementalGroups` that apply to all containers in the Pod.
- [ ] D-040. Set a `securityContext` at the **container level** to override Pod-level settings for specific containers (e.g., different `runAsUser`, `readOnlyRootFilesystem`).
- [ ] D-041. Set `runAsNonRoot: true` at the Pod or container level and understand that Kubernetes rejects containers whose image runs as UID 0.
- [ ] D-042. Set `readOnlyRootFilesystem: true` for a container and add a writable `emptyDir` volume mounted at paths that the application needs to write to.
- [ ] D-043. Set `allowPrivilegeEscalation: false` to prevent a process inside a container from gaining more privileges than its parent process.
- [ ] D-044. Drop all Linux capabilities with `securityContext.capabilities.drop: ["ALL"]` and selectively add back only what is needed (e.g., `NET_BIND_SERVICE`).
- [ ] D-045. Add a Linux capability with `securityContext.capabilities.add` and explain what each capability grants (e.g., `NET_ADMIN`, `SYS_TIME`, `SYS_PTRACE`).
- [ ] D-046. Apply a **Pod Security Admission** profile to a namespace by setting the label `pod-security.kubernetes.io/enforce: restricted` and understand the three profiles: `privileged`, `baseline`, `restricted`.
- [ ] D-047. Understand what the `restricted` PSA profile requires: no privileged containers, no host namespaces, drop `ALL` capabilities, `runAsNonRoot`, `readOnlyRootFilesystem`, no privilege escalation.
- [ ] D-048. Set a **seccomp** profile on a container using `securityContext.seccompProfile.type: RuntimeDefault` or `Localhost` with a profile path.
- [ ] D-070. Apply an AppArmor profile to a container by setting `securityContext.appArmorProfile.type: RuntimeDefault` (node's default profile) or `Localhost` with `localhostProfile: <profile-name>`; `Unconfined` disables AppArmor enforcement. This field is GA from Kubernetes v1.30.

---

## Pod-Level Host Namespaces

- [ ] D-068. Set `spec.hostNetwork: true` on a Pod to make it share the node's network namespace (the Pod uses the node's IP and ports directly) and explain why the `restricted` Pod Security Admission profile forbids this.
- [ ] D-069. Set `spec.hostPID: true` or `spec.hostIPC: true` on a Pod to share the node's PID or IPC namespace; understand the security implications (visibility of all node processes / IPC resources) and that both PSA `baseline` and `restricted` profiles block these fields.

---

## CRDs and Operators **[S]**

- [ ] S-097. Explain what a `CustomResourceDefinition` (CRD) is and how it extends the Kubernetes API with new resource types.
- [ ] S-098. List all CRDs installed in a cluster with `kubectl get crds` and discover their short names and API groups.
- [ ] S-099. Create instances of a custom resource (CR) from a YAML manifest and interact with them using standard `kubectl` commands.
- [ ] S-100. Explain the operator pattern: a controller that watches CRs and reconciles real-world state to match the CR spec.

---

## PodDisruptionBudget (Developer Perspective)

- [ ] D-071. Read a `PodDisruptionBudget` status with `kubectl get pdb -n <ns>` to understand `ALLOWED` (how many Pods may currently be disrupted) versus `DISRUPTIONS` (how many are currently disrupted), and explain how a PDB protects your application from simultaneous evictions during node drains or cluster upgrades.

---

# Domain 5 — Services and Networking (20%)

## Services & Endpoints **[S]**

- [ ] S-051. Explain how a `Service` uses a `selector` to dynamically match Pods by label and create `Endpoints` / `EndpointSlice` objects.
- [ ] S-052. Create a `ClusterIP` Service with `kubectl expose` and from a YAML manifest; verify it resolves inside the cluster.
- [ ] S-053. Create a `NodePort` Service and explain the port/targetPort/nodePort relationship and the default NodePort range (30000–32767).
- [ ] S-054. Describe when to use a `LoadBalancer` Service (cloud provider or MetalLB) and how it builds on top of `NodePort` and `ClusterIP`.
- [ ] S-055. Create an `ExternalName` Service that provides a CNAME alias to an external DNS name without proxying traffic.
- [ ] S-056. Create a headless Service (`clusterIP: None`) and explain how it enables direct Pod DNS records for StatefulSets.
- [ ] S-057. Troubleshoot a Service that has no endpoints: check that Pod labels match the Service selector, Pods are Running, and the correct port is exposed.
- [ ] S-058. Inspect `EndpointSlice` objects to see which Pod IPs are backing a Service using `kubectl get endpointslices`.

---

## NetworkPolicies **[S]**

- [ ] S-059. Explain the default-allow behavior of Kubernetes networking and why explicit `NetworkPolicy` is required to enforce isolation.
- [ ] S-060. Write a `NetworkPolicy` that creates a default-deny-all-ingress policy for all Pods in a namespace by leaving `podSelector: {}` and `ingress: []`.
- [ ] S-061. Write a `NetworkPolicy` that allows ingress to a Pod on a specific port only from Pods with a specific label using `podSelector` under `ingress.from`.
- [ ] S-062. Write a `NetworkPolicy` that allows ingress from Pods in a specific namespace using `namespaceSelector` under `ingress.from`.
- [ ] S-063. Write a `NetworkPolicy` with an egress rule that restricts outbound traffic from selected Pods to only a specific IP block and port.
- [ ] S-064. Combine `podSelector` and `namespaceSelector` in the same `from` entry (AND logic) versus in separate entries (OR logic) and explain the difference.
- [ ] S-065. Verify `NetworkPolicy` enforcement by using `kubectl exec` to run `curl` or `nc` between Pods and confirming allowed vs. blocked paths.
- [ ] D-063. Write a `NetworkPolicy` from the perspective of a developer to isolate application Pods and permit only traffic from a specific frontend tier label.

---

## Ingress **[S]**

- [ ] S-066. Explain the role of an Ingress controller (NGINX, Traefik, etc.) versus the `Ingress` resource object, and why both are required.
- [ ] S-067. Write an `Ingress` manifest that routes traffic to two different Services based on the HTTP path (`/api` → service-a, `/web` → service-b).
- [ ] S-068. Write an `Ingress` manifest that routes traffic based on the HTTP `Host` header to route multiple virtual hosts through a single IP.
- [ ] S-069. Configure TLS termination on an `Ingress` by referencing a `kubernetes.io/tls` Secret and adding a `tls:` block.
- [ ] S-070. Set `pathType` correctly (`Prefix` vs. `Exact` vs. `ImplementationSpecific`) and explain the routing differences.
- [ ] S-071. Set the `ingressClassName` field (or annotation) to select a specific Ingress controller when multiple controllers are installed.
- [ ] S-072. Troubleshoot an Ingress returning 404 or 502 by checking the controller logs, backend Service existence, endpoint readiness, and path/host match.

---

## Services & Networking (Developer Perspective)

- [ ] D-061. Troubleshoot an application that cannot reach a Service by checking DNS resolution, Service selector label matching, and endpoint readiness from within a debug Pod.
- [ ] D-062. Configure an application to discover Service endpoints via environment variables (`<SVC_NAME>_SERVICE_HOST`, `<SVC_NAME>_SERVICE_PORT`) injected automatically by Kubernetes.
- [ ] D-064. Use `kubectl port-forward svc/<name> 8080:80` to forward traffic to a Service (not just a Pod) for local testing without a NodePort or LoadBalancer.

---

*Total CKAD items: all D-001–D-073 + shared S-* items relevant to CKAD*
*Source: CNCF official curriculum (github.com/cncf/curriculum), Linux Foundation exam pages — April 2026*

# CKA Exam Checklist
**Kubernetes v1.34 · 2026 · Performance-based · 2 hours · 66% passing score**

Domain weights: Troubleshooting 30% · Cluster Architecture 25% · Services & Networking 20% · Workloads & Scheduling 15% · Storage 10%

Items marked **[S]** are shared with CKAD but tested here from the cluster-operator perspective.

---

# Domain 1 — Cluster Architecture, Installation & Configuration (25%)

## Control Plane Components

- [ ] C-001. Describe the exact function of `kube-apiserver` as the single entry point for all REST operations, authentication, authorization, and admission control.
- [ ] C-002. Explain how `etcd` stores all cluster state as key-value pairs and why it is the single source of truth for the Kubernetes control plane.
- [ ] C-003. Describe the role of `kube-controller-manager` and list five built-in controllers it runs (Node, Replication, Endpoints, ServiceAccount, Job).
- [ ] C-004. Explain how `kube-scheduler` selects a node for an unscheduled Pod through filtering (predicates) and scoring (priorities).
- [ ] C-005. Describe what `kubelet` does on every worker node: registers the node, pulls images, starts containers via CRI, reports status, and runs probes.
- [ ] C-006. Explain the role of `kube-proxy` in maintaining network rules (iptables/IPVS) on every node to implement `Service` virtual IPs.
- [ ] C-007. Locate and read static Pod manifests in `/etc/kubernetes/manifests/` and understand how the kubelet self-hosts control-plane components.
- [ ] C-008. Identify the key configuration flags for `kube-apiserver` (e.g., `--etcd-servers`, `--service-cluster-ip-range`, `--authorization-mode`, `--enable-admission-plugins`).
- [ ] C-009. Identify the key configuration flags for `kubelet` in `/var/lib/kubelet/config.yaml` and `/etc/kubernetes/kubelet.conf`.

---

## kubeadm — Cluster Installation & Lifecycle

- [ ] C-010. Install the required prerequisites for `kubeadm`: disable swap, load `br_netfilter` and `overlay` kernel modules, set `net.ipv4.ip_forward=1`, and install a container runtime.
- [ ] C-011. Install specific versions of `kubeadm`, `kubelet`, and `kubectl` using the package manager and hold them to prevent unintended upgrades.
- [ ] C-012. Initialize a cluster with `kubeadm init --pod-network-cidr=<cidr> --apiserver-advertise-address=<ip>` and save the join command and certificate key.
- [ ] C-013. Configure `kubectl` for the new cluster by copying `/etc/kubernetes/admin.conf` to `~/.kube/config`.
- [ ] C-014. Install a CNI plugin (e.g., Calico or Flannel) after `kubeadm init` using the plugin's official manifest URL.
- [ ] C-015. Join a worker node to the cluster using `kubeadm join <control-plane-host>:<port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>`.
- [ ] C-016. Generate a new bootstrap token for joining nodes with `kubeadm token create --print-join-command`.
- [ ] C-017. Renew all control-plane certificates with `kubeadm certs renew all` and verify expiry dates with `kubeadm certs check-expiration`.
- [ ] C-018. Reset a node cleanly with `kubeadm reset` before rejoining it or repurposing it.
- [ ] C-019. Use `kubeadm config print init-defaults` to understand the default initialization configuration and how to customize it via a `kubeadm-config.yaml` file.
- [ ] C-109. Pre-pull all required control-plane container images before running `kubeadm init` using `kubeadm config images pull [--kubernetes-version v1.X.Y]`; useful on air-gapped or slow-network nodes to verify image availability before starting cluster initialization.

---

## Cluster Upgrades

- [ ] C-020. Describe the Kubernetes version skew policy and which components must be upgraded first (control plane before worker nodes).
- [ ] C-021. Upgrade `kubeadm` to the target version before upgrading any cluster component.
- [ ] C-022. Plan the upgrade by running `kubeadm upgrade plan` and reading its output to identify the target version and required steps.
- [ ] C-023. Apply the upgrade to the control plane with `kubeadm upgrade apply v1.X.Y` and verify control-plane component versions afterwards.
- [ ] C-024. Upgrade `kubelet` and `kubectl` on the control-plane node after running `kubeadm upgrade apply`.
- [ ] C-025. Drain a worker node with `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data` before upgrading it.
- [ ] C-026. Upgrade `kubeadm`, then `kubelet` and `kubectl` on the worker node, and run `kubeadm upgrade node`.
- [ ] C-027. Uncordon the worker node with `kubectl uncordon <node>` and verify it is `Ready` and running the new kubelet version.

---

## Highly Available Control Plane

- [ ] C-035. Explain the difference between stacked etcd topology (etcd runs on the same nodes as control-plane components) and external etcd topology.
- [ ] C-036. Describe how to initialize an HA control plane with `kubeadm init --control-plane-endpoint=<lb-dns>:<port> --upload-certs`.
- [ ] C-037. Join additional control-plane nodes with `kubeadm join --control-plane --certificate-key <key>`.
- [ ] C-038. Explain the role of a load balancer (HAProxy, Keepalived, cloud LB) in front of multiple `kube-apiserver` instances.
- [ ] C-039. Understand how `kube-controller-manager` and `kube-scheduler` use leader election to avoid split-brain when running on multiple control-plane nodes.

---

## RBAC (Admin/Operator Perspective)

- [ ] C-040. Create a `ClusterRole` that grants read-only access to all resources in a specific API group across all namespaces.
- [ ] C-041. Create a `ClusterRoleBinding` to bind a `ClusterRole` to a user, group, or `ServiceAccount`.
- [ ] C-042. Create a namespace-scoped `Role` and `RoleBinding` to grant a service account access to specific verbs on specific resources.
- [ ] C-043. Use aggregated `ClusterRoles` by adding the `rbac.authorization.k8s.io/aggregate-to-<role>: "true"` label to extend built-in roles.
- [ ] C-044. Verify a user's permissions with `kubectl auth can-i --list --as=<user>` and `kubectl auth can-i <verb> <resource> --as=<user> -n <ns>`.
- [ ] C-045. Identify and fix over-permissive RBAC configurations — e.g., remove wildcard verbs (`*`) or resources that grant excessive access.

---

## Extension Interfaces (CNI, CSI, CRI)

- [ ] C-046. Explain what CNI (Container Network Interface) does: provisions a network interface inside a Pod sandbox and configures routing on the node.
- [ ] C-047. Identify which CNI plugin is installed by inspecting files under `/etc/cni/net.d/` and `/opt/cni/bin/`.
- [ ] C-048. Explain what CRI (Container Runtime Interface) does and identify the active runtime socket (e.g., `/run/containerd/containerd.sock`) with `crictl info`.
- [ ] C-049. Use `crictl ps`, `crictl logs`, and `crictl inspect` to inspect containers at the CRI level when `kubectl` cannot reach a Pod.
- [ ] C-050. Explain what CSI (Container Storage Interface) does: allows external storage drivers to be installed and managed independently of Kubernetes core.

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

## CRDs and Operators **[S]**

- [ ] S-097. Explain what a `CustomResourceDefinition` (CRD) is and how it extends the Kubernetes API with new resource types.
- [ ] S-098. List all CRDs installed in a cluster with `kubectl get crds` and discover their short names and API groups.
- [ ] S-099. Create instances of a custom resource (CR) from a YAML manifest and interact with them using standard `kubectl` commands.
- [ ] S-100. Explain the operator pattern: a controller that watches CRs and reconciles real-world state to match the CR spec.

---

## Admission Controllers & Webhooks

- [ ] C-106. Explain the admission control pipeline: after authentication and authorization, requests pass through mutating admission plugins (including `MutatingAdmissionWebhook`) and then validating admission plugins (including `ValidatingAdmissionWebhook`) before the object is persisted to etcd.
- [ ] C-107. Diagnose a resource rejected by an admission webhook: read the rejection reason from the `kubectl apply` error output, identify the responsible webhook with `kubectl get validatingwebhookconfigurations` or `kubectl get mutatingwebhookconfigurations`, and check its `failurePolicy` (`Fail` blocks the request; `Ignore` allows it through on webhook error).

---

# Domain 2 — Workloads & Scheduling (15%)

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

## Pod Lifecycle Hooks **[S]**

- [ ] S-101. Configure a `lifecycle.postStart` exec handler that runs a command immediately after a container starts, and understand that it blocks the container from reaching `Running` state until the handler completes or times out.
- [ ] S-102. Configure a `lifecycle.preStop` exec or sleep handler to delay SIGTERM and enable graceful shutdown (e.g., `preStop: exec: command: ["sleep","10"]`); this is essential for zero-downtime deployments behind a load balancer.
- [ ] S-103. Explain how `terminationGracePeriodSeconds` interacts with `preStop`: the kubelet waits up to `terminationGracePeriodSeconds` for both the `preStop` handler and the main process to exit before sending SIGKILL; the `preStop` duration counts against this budget.

---

## ConfigMaps **[S]**

- [ ] S-017. Create a `ConfigMap` from literal values (`--from-literal`), from a file (`--from-file`), and from an env file (`--from-env-file`), and inspect its data with `kubectl describe`.
- [ ] S-018. Inject all keys from a `ConfigMap` into a container as environment variables using `envFrom.configMapRef`.
- [ ] S-019. Inject a single key from a `ConfigMap` into an environment variable using `env.valueFrom.configMapKeyRef`.
- [ ] S-020. Mount a `ConfigMap` as a volume so each key becomes a file inside a directory in the container filesystem.
- [ ] S-021. Use `subPath` to mount a single key from a `ConfigMap` volume to a specific file path without replacing the entire directory.
- [ ] S-022. Create an immutable `ConfigMap` by setting `immutable: true` and explain why this improves performance at scale.

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

## Resource Requests, Limits, LimitRange, ResourceQuota **[S]**

- [ ] S-030. Define `resources.requests.cpu` and `resources.requests.memory` on a container and explain how the scheduler uses requests for node selection.
- [ ] S-031. Define `resources.limits.cpu` and `resources.limits.memory` and explain how the kubelet enforces them (CPU throttling via cgroups; OOMKill for memory).
- [ ] S-032. Explain the three QoS classes — `Guaranteed`, `Burstable`, `BestEffort` — and the conditions that place a Pod into each class.
- [ ] S-033. Create a `LimitRange` that sets default requests and limits for containers, and a maximum and minimum range for CPU and memory.
- [ ] S-034. Create a `ResourceQuota` that limits the total CPU, memory, and object counts (Pods, Services, PVCs) within a namespace.
- [ ] S-035. Demonstrate what happens when a Pod spec violates a `LimitRange` or a `ResourceQuota` (admission rejection with descriptive error).
- [ ] S-111. Define `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` on a container to protect against disk-hungry containers; when the limit is exceeded the kubelet evicts the Pod from the node.

---

## Scheduling (Admin Perspective)

- [ ] C-051. Schedule a Pod on a specific node using `spec.nodeName` (bypasses the scheduler entirely).
- [ ] C-052. Use `nodeSelector` to constrain a Pod to nodes with a specific label (e.g., `disktype: ssd`).
- [ ] C-053. Write a `requiredDuringSchedulingIgnoredDuringExecution` node affinity rule that prevents a Pod from being scheduled on non-matching nodes.
- [ ] C-054. Write a `preferredDuringSchedulingIgnoredDuringExecution` node affinity rule with a weight to softly prefer certain nodes.
- [ ] C-055. Add a taint to a node with `kubectl taint nodes <node> key=value:NoSchedule` and add a matching toleration to a Pod spec.
- [ ] C-056. Use `NoExecute` taint effect to evict existing Pods from a node and add `tolerationSeconds` to a toleration to allow a grace period before eviction.
- [ ] C-057. Write pod affinity rules to co-locate Pods with a specific topology key (e.g., `kubernetes.io/hostname`) and pod anti-affinity to spread Pods across nodes.
- [ ] C-058. Write a `topologySpreadConstraint` to spread Pods evenly across zones using `maxSkew`, `topologyKey`, and `whenUnsatisfiable`.
- [ ] C-059. Create a `PriorityClass` object and assign it to a Pod via `spec.priorityClassName` to control preemption order.
- [ ] C-060. Identify why a Pod is stuck in `Pending` due to scheduling constraints using `kubectl describe pod` and reading the `Events` section.

---

## Node Management

- [ ] C-108. Label a node with `kubectl label nodes <node-name> <key>=<value>`, verify with `kubectl get node <name> --show-labels`, and remove a label with `kubectl label nodes <node-name> <key>-`; node labels are the foundation for `nodeSelector` and node affinity rules.

---

## Scheduler Profiles

- [ ] C-104. Assign a Pod to a non-default scheduler or scheduler profile by setting `spec.schedulerName: <profile-name>` in the Pod spec; Pods referencing an unknown scheduler name remain `Pending` indefinitely.
- [ ] C-105. Explain how multiple scheduler profiles are defined in the `KubeSchedulerConfiguration` file under `profiles:`, each with a distinct `schedulerName` and its own plugin configuration, allowing different scheduling behaviour without running separate scheduler processes.

---

## Workload Autoscaling

- [ ] C-061. Create a `HorizontalPodAutoscaler` (HPA) v2 that scales a `Deployment` based on CPU utilization using `kubectl autoscale` and verify with `kubectl get hpa`.
- [ ] C-062. Write an HPA manifest with a `metrics` block targeting average CPU utilization (as a percentage of request) and set `minReplicas` and `maxReplicas`.
- [ ] C-063. Explain the role of `metrics-server` as the source of real-time resource metrics for HPA and how to verify it is running.
- [ ] C-064. Describe conceptually what `VerticalPodAutoscaler` (VPA) does and its three update modes: `Off`, `Initial`, `Auto`.
- [ ] C-065. Explain what `Cluster Autoscaler` does (adds/removes nodes) and how it interacts with unschedulable Pods.
- [ ] C-066. Create a `PodDisruptionBudget` (PDB) specifying `minAvailable` or `maxUnavailable` to protect an application during voluntary disruptions like node drains.

---

## ServiceAccounts & RBAC (Consumer Perspective) **[S]**

- [ ] S-079. Explain how every Pod is automatically associated with a `ServiceAccount` (default is `default` in the namespace) and what token is auto-mounted.
- [ ] S-080. Create a named `ServiceAccount` with `kubectl create serviceaccount` and associate it with a Pod via `spec.serviceAccountName`.
- [ ] S-081. Disable the automatic mounting of the service account token in a Pod by setting `automountServiceAccountToken: false`.
- [ ] S-082. Explain the components of RBAC: `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding` and which scope (namespace vs. cluster) each applies to.
- [ ] S-083. Create a `Role` that grants `get`, `list`, and `watch` on `pods` within a namespace, and bind it to a `ServiceAccount` via a `RoleBinding`.
- [ ] S-084. Test what a `ServiceAccount` or user is allowed to do using `kubectl auth can-i <verb> <resource> --as=<user> -n <namespace>`.

---

# Domain 3 — Services & Networking (20%)

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

## Gateway API

- [ ] C-073. Explain the three kube-proxy modes — `iptables`, `IPVS`, and `nftables` — and the key differences in performance and rule management.
- [ ] C-074. Inspect iptables rules on a node with `iptables -t nat -L KUBE-SERVICES` to trace how a `ClusterIP` is translated to a Pod IP.
- [ ] C-075. Configure CoreDNS by editing its `ConfigMap` (`coredns` in `kube-system`) and understand the structure of the `Corefile`.
- [ ] C-076. Explain Kubernetes DNS naming: `<svc>.<ns>.svc.cluster.local` for Services and `<pod-ip-dashes>.<ns>.pod.cluster.local` for Pods.
- [ ] C-077. Configure Pod DNS settings with `spec.dnsPolicy` (values: `ClusterFirst`, `Default`, `None`, `ClusterFirstWithHostNet`) and custom `spec.dnsConfig`.
- [ ] C-078. Install and use the **Gateway API** resources: `GatewayClass`, `Gateway`, and `HTTPRoute` to route HTTP traffic with more expressiveness than `Ingress`.
- [ ] C-079. Write an `HTTPRoute` that routes traffic to different backends based on HTTP path prefixes and understand how it references a `Gateway`.
- [ ] C-080. Explain `ReferenceGrant` in the Gateway API and why it is required when an `HTTPRoute` in one namespace references a Service in another namespace.

---

## CoreDNS Advanced

- [ ] C-110. Add a stub zone to the CoreDNS `Corefile` ConfigMap (in `kube-system`) so that DNS queries for a specific internal domain (e.g., `corp.internal`) are forwarded to a designated upstream resolver IP, then restart the CoreDNS Pods to apply the change.

---

# Domain 4 — Storage (10%)

## Persistent Volumes and Persistent Volume Claims **[S]**

- [ ] S-073. Distinguish between the admin role (creates `PersistentVolume` or `StorageClass`) and the developer role (creates `PersistentVolumeClaim` to consume storage).
- [ ] S-074. Write a `PersistentVolumeClaim` manifest specifying `storageClassName`, `accessModes`, and `resources.requests.storage`.
- [ ] S-075. Mount a `PersistentVolumeClaim` in a Pod by adding it to `volumes` and referencing it in `volumeMounts` with a `mountPath`.
- [ ] S-076. Explain the four access modes — `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod` — and which volume backends support each.
- [ ] S-077. Explain the PVC lifecycle: Pending → Bound, and what causes a PVC to remain `Pending` (no matching PV, StorageClass provisioner unavailable).
- [ ] S-078. Use `emptyDir` for ephemeral shared storage between containers in the same Pod and understand that data is lost when the Pod is deleted.

---

## Storage (Admin Perspective)

- [ ] C-067. Create a `StorageClass` with a specific provisioner, parameters, `reclaimPolicy`, and `volumeBindingMode` (`Immediate` vs. `WaitForFirstConsumer`).
- [ ] C-068. Annotate a `StorageClass` as the cluster default using `storageclass.kubernetes.io/is-default-class: "true"`.
- [ ] C-069. Create a `PersistentVolume` manually with a specific `capacity`, `accessModes`, `persistentVolumeReclaimPolicy`, and a `hostPath` or `nfs` source.
- [ ] C-070. Understand PV reclaim policies: `Retain` (keeps data, must be manually reclaimed) vs. `Delete` (deletes the underlying storage asset).
- [ ] C-071. Expand a `PersistentVolumeClaim` by editing its `spec.resources.requests.storage` and ensure the `StorageClass` has `allowVolumeExpansion: true`.
- [ ] C-072. Explain VolumeMode `Filesystem` (default, mounted as a directory) versus `Block` (raw block device, no filesystem layer).

---

## Volume Snapshots (CSI)

- [ ] C-101. Explain the three VolumeSnapshot API objects: `VolumeSnapshotClass` (defines the CSI driver and deletion policy), `VolumeSnapshot` (the user's snapshot request, analogous to a PVC), and `VolumeSnapshotContent` (the actual snapshot resource, analogous to a PV).
- [ ] C-102. Create a `VolumeSnapshot` from an existing PVC by writing a manifest with `spec.source.persistentVolumeClaimName` and `spec.volumeSnapshotClassName`, then verify it is `readyToUse: true`.
- [ ] C-103. Restore data from a `VolumeSnapshot` by creating a new PVC with `spec.dataSource.kind: VolumeSnapshot` and `spec.dataSource.name` pointing to the snapshot name.

---

## Storage Troubleshooting

- [ ] C-112. Diagnose a PVC expansion stuck in `FileSystemResizePending` status: understand that the filesystem resize happens inside the running container and only completes after the Pod mounting the PVC is restarted; delete and recreate the Pod (or trigger a rollout restart) to allow the kubelet to expand the filesystem.

---

# Domain 5 — Troubleshooting (30%)

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

## etcd Backup & Restore

- [ ] C-028. Identify the `etcd` endpoint, CA certificate, client certificate, and client key required to authenticate `etcdctl` commands.
- [ ] C-029. Set the `ETCDCTL_API=3` environment variable before using `etcdctl` commands to target the v3 API.
- [ ] C-030. Create an etcd snapshot with `etcdctl snapshot save <path> --endpoints=<url> --cacert=<ca> --cert=<cert> --key=<key>`.
- [ ] C-031. Verify the integrity of an etcd snapshot file with `etcdctl snapshot status <path> --write-out=table`.
- [ ] C-032. Restore an etcd snapshot with `etcdctl snapshot restore <path> --data-dir=<new-dir>` and update the etcd static Pod manifest to point to the new data directory.
- [ ] C-033. Restart the etcd static Pod after restoring by moving its manifest out and back into `/etc/kubernetes/manifests/`.
- [ ] C-034. Verify cluster health after restore using `kubectl get nodes` and `kubectl get pods -A`.
- [ ] C-111. When restoring an etcd snapshot in a multi-member HA cluster, run `etcdctl snapshot restore` separately for each member with member-specific flags (`--name`, `--initial-cluster`, `--initial-cluster-token`, `--initial-advertise-peer-urls`, `--data-dir`), then update each node's etcd static Pod manifest to point to its restored data directory before bringing members back online.

---

## Troubleshooting — Nodes

- [ ] C-081. Identify a `NotReady` node and begin systematic diagnosis by running `kubectl describe node <name>` and reading the `Conditions` section.
- [ ] C-082. SSH into the problematic node and check `kubelet` service status and logs with `systemctl status kubelet` and `journalctl -u kubelet -n 100`.
- [ ] C-083. Diagnose a kubelet that fails to start due to a misconfigured `/var/lib/kubelet/config.yaml` or stale `/etc/kubernetes/kubelet.conf`.
- [ ] C-084. Fix a node where the container runtime is not running by starting `containerd` with `systemctl start containerd` and enabling it on boot.
- [ ] C-085. Check node disk pressure, memory pressure, and PID pressure conditions using `kubectl describe node` and correlate them with resource exhaustion.
- [ ] C-086. Use `crictl ps -a` to list all containers (including failed ones) at the runtime level when `kubectl` reports no Pods on a node.
- [ ] C-087. Check certificate expiration for the kubelet client certificate and explain how to renew it using `kubeadm certs renew`.

---

## Troubleshooting — Control Plane Components

- [ ] C-088. Diagnose a non-functional `kube-apiserver` by examining its static Pod manifest in `/etc/kubernetes/manifests/kube-apiserver.yaml` for misconfigurations.
- [ ] C-089. View logs of a control-plane static Pod when the Pod is not running using `crictl logs <container-id>` directly on the control-plane node.
- [ ] C-090. Fix a misconfigured etcd (e.g., wrong data directory path or bad certificate reference) by editing the static Pod manifest and waiting for the kubelet to restart it.
- [ ] C-091. Diagnose a `kube-scheduler` that is not scheduling Pods by checking its logs for errors and verifying it holds the leader lease.
- [ ] C-092. Diagnose a `kube-controller-manager` that is not creating Pods (e.g., HPA not scaling, Jobs not creating) by examining its logs.
- [ ] C-093. Validate that all control-plane Pods are running with `kubectl get pods -n kube-system` and identify any with a non-Running status.

---

## Troubleshooting — Applications & Networking

- [ ] C-094. Diagnose a `CrashLoopBackOff` Pod by reading its logs with `kubectl logs --previous`, checking exit codes, and inspecting `lastState` in `kubectl describe`.
- [ ] C-095. Diagnose an `ImagePullBackOff` error by verifying the image name and tag, checking registry credentials (`imagePullSecrets`), and reading the event message.
- [ ] C-096. Diagnose a `Pending` Pod by reading the Events section of `kubectl describe pod` for messages about insufficient CPU, memory, or unmatched affinity rules.
- [ ] C-097. Diagnose a Service with no endpoints by confirming Pod selector labels match Service selector, Pods are Running, and `containerPort` matches Service `targetPort`.
- [ ] C-098. Test DNS resolution from inside a Pod using `kubectl exec <pod> -- nslookup <svc>.<ns>.svc.cluster.local`.
- [ ] C-099. Identify kube-proxy iptables rules routing traffic for a Service and use `iptables-save | grep <svc-ip>` to trace NAT rules.
- [ ] C-100. Identify a `NetworkPolicy` that is blocking traffic by temporarily removing it in a test environment and re-testing connectivity.

---

*Total CKA items: all C-001–C-112 + shared S-* items relevant to CKA*
*Source: CNCF official curriculum (github.com/cncf/curriculum), Linux Foundation exam pages — April 2026*

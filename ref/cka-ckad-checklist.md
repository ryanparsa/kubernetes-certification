# CKA & CKAD Exam Checklist: 363 Items
**Kubernetes v1.34 (CKA) / v1.35 (CKAD) · 2026 · Performance-based · 2 hours · 66% passing score**

*Total: 363 checkable items*
*001 to 111: Shared (CKA & CKAD) · 112 to 249: CKA-specific · 250 to 322: CKAD-specific · 323 to 363: kubectl & General*
*Source: CNCF official curriculum (github.com/cncf/curriculum), Linux Foundation exam pages — April 2026*

Domain weights — CKA: Troubleshooting 30% · Cluster Architecture 25% · Services & Networking 20% · Workloads & Scheduling 15% · Storage 10%
Domain weights — CKAD: App Environment, Config & Security 25% · App Design & Build 20% · App Deployment 20% · Services & Networking 20% · App Observability & Maintenance 15%

---

Study tip: Shared topics are tested in both exams but from different angles — CKA as operator, CKAD as developer. Master them once, apply twice.

# ✅ CKA & CKAD — Shared Topics

## Workload Resources (Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs, CronJobs)

- [ ] 001. Explain the role of a `ReplicaSet` and how its label selector continuously reconciles the desired number of running Pods.
- [ ] 002. Describe how a `Deployment` wraps a `ReplicaSet` to enable declarative updates, rollbacks, and scaling without downtime.
- [ ] 003. Create a `Deployment` imperatively with `kubectl create deployment` and declaratively via a YAML manifest specifying `replicas`, `selector.matchLabels`, and `template`.
- [ ] 004. Perform a rolling update on a `Deployment` by changing the container image, and monitor its progress with `kubectl rollout status`.
- [ ] 005. Configure `maxSurge` and `maxUnavailable` under `strategy.rollingUpdate` to control how many Pods are added or removed during a rolling update.
- [ ] 006. Roll back a `Deployment` to its previous revision using `kubectl rollout undo` and to a specific revision using `--to-revision=<n>`.
- [ ] 007. Inspect `Deployment` revision history with `kubectl rollout history` and understand how `revisionHistoryLimit` controls the number of stored `ReplicaSets`.
- [ ] 008. Pause and resume a `Deployment` rollout using `kubectl rollout pause` and `kubectl rollout resume` to batch multiple changes into a single rollout.
- [ ] 009. Force a restart of all Pods in a `Deployment` without changing the spec using `kubectl rollout restart`.
- [ ] 010. Explain when to use a `StatefulSet` (stable network identity, stable storage, ordered deployment and scaling) versus a `Deployment`.
- [ ] 011. Describe how `StatefulSet` names Pods with a predictable ordinal index and creates `PersistentVolumeClaims` per Pod via `volumeClaimTemplates`.
- [ ] 012. Explain the use case of a `DaemonSet` — running exactly one Pod per matching node — and give three real-world examples (log collector, monitoring agent, CNI plugin).
- [ ] 013. Create a `Job` that runs a task to completion and configure `completions`, `parallelism`, `backoffLimit`, and `activeDeadlineSeconds`.
- [ ] 014. Distinguish between `Job` completion modes: `NonIndexed` (default) versus `Indexed` (each Pod gets a unique completion index via `JOB_COMPLETION_INDEX`).
- [ ] 015. Create a `CronJob` with a valid cron schedule expression, and explain `successfulJobsHistoryLimit`, `failedJobsHistoryLimit`, and `concurrencyPolicy` (`Allow`, `Forbid`, `Replace`).
- [ ] 016. Identify and fix a `CronJob` that has missed its schedule due to `startingDeadlineSeconds` being exceeded.

---

## ConfigMaps

- [ ] 017. Create a `ConfigMap` from literal values (`--from-literal`), from a file (`--from-file`), and from an env file (`--from-env-file`), and inspect its data with `kubectl describe`.
- [ ] 018. Inject all keys from a `ConfigMap` into a container as environment variables using `envFrom.configMapRef`.
- [ ] 019. Inject a single key from a `ConfigMap` into an environment variable using `env.valueFrom.configMapKeyRef`.
- [ ] 020. Mount a `ConfigMap` as a volume so each key becomes a file inside a directory in the container filesystem.
- [ ] 021. Use `subPath` to mount a single key from a `ConfigMap` volume to a specific file path without replacing the entire directory.
- [ ] 022. Create an immutable `ConfigMap` by setting `immutable: true` and explain why this improves performance at scale.

---

## Secrets

- [ ] 023. Create an `Opaque` `Secret` from literal values and understand that values are base64-encoded (not encrypted) at rest by default.
- [ ] 024. Decode a `Secret` value in the shell using `kubectl get secret <name> -o jsonpath='{.data.<key>}' | base64 -d`.
- [ ] 025. Inject `Secret` data into a container as environment variables via `envFrom.secretRef` and `env.valueFrom.secretKeyRef`.
- [ ] 026. Mount a `Secret` as a volume, understanding that each key becomes a file and the value is the decoded content.
- [ ] 027. Create a `kubernetes.io/tls` Secret from a certificate and key file using `kubectl create secret tls`.
- [ ] 028. Create a `kubernetes.io/dockerconfigjson` Secret for authenticating to a private container registry and reference it in a Pod via `imagePullSecrets`.
- [ ] 029. Create an immutable `Secret` with `immutable: true` and explain the kubelet caching benefit.

---

## Resource Requests, Limits, LimitRange, ResourceQuota

- [ ] 030. Define `resources.requests.cpu` and `resources.requests.memory` on a container and explain how the scheduler uses requests for node selection.
- [ ] 031. Define `resources.limits.cpu` and `resources.limits.memory` and explain how the kubelet enforces them (CPU throttling via cgroups; OOMKill for memory).
- [ ] 032. Explain the three QoS classes — `Guaranteed`, `Burstable`, `BestEffort` — and the conditions that place a Pod into each class.
- [ ] 033. Create a `LimitRange` that sets default requests and limits for containers, and a maximum and minimum range for CPU and memory.
- [ ] 034. Create a `ResourceQuota` that limits the total CPU, memory, and object counts (Pods, Services, PVCs) within a namespace.
- [ ] 035. Demonstrate what happens when a Pod spec violates a `LimitRange` or a `ResourceQuota` (admission rejection with descriptive error).

---

## Helm

- [ ] 036. Add a Helm repository with `helm repo add`, update the cache with `helm repo update`, and search for available charts with `helm search repo`.
- [ ] 037. Install a chart with `helm install <release> <chart>` and override values using `--set key=value` and `--values values.yaml`.
- [ ] 038. List all deployed Helm releases in a namespace with `helm list` and across all namespaces with `helm list -A`.
- [ ] 039. Upgrade an existing release with `helm upgrade` and roll back to a previous revision with `helm rollback <release> <revision>`.
- [ ] 040. Uninstall a release with `helm uninstall` and verify that all managed resources have been removed.
- [ ] 041. Render Helm templates locally without installing them using `helm template` to inspect the generated Kubernetes manifests.
- [ ] 042. Inspect the values available in a chart with `helm show values <chart>` and understand how to override defaults.

---

## Kustomize

- [ ] 043. Write a minimal `kustomization.yaml` that references a list of `resources` (YAML files) and apply it with `kubectl apply -k`.
- [ ] 044. Add `commonLabels` and `commonAnnotations` in `kustomization.yaml` to patch all managed resources simultaneously.
- [ ] 045. Use `namePrefix` and `nameSuffix` in `kustomization.yaml` to rename all resources without touching individual files.
- [ ] 046. Build a base-overlay Kustomize structure: a `base/` directory with a `kustomization.yaml` and one or more `overlays/` (dev, staging, prod) that extend it.
- [ ] 047. Apply a strategic-merge patch in an overlay to override specific fields (e.g., replica count or image tag) without duplicating the entire manifest.
- [ ] 048. Apply a JSON-6902 patch (`patchesJson6902`) in an overlay to add, remove, or replace specific fields using JSON patch operations.
- [ ] 049. Use the `images:` transformer in `kustomization.yaml` to override a container image name or tag across all resources.
- [ ] 050. Generate a `ConfigMap` or `Secret` inline with `configMapGenerator` and `secretGenerator` inside `kustomization.yaml`.

---

## Services & Endpoints

- [ ] 051. Explain how a `Service` uses a `selector` to dynamically match Pods by label and create `Endpoints` / `EndpointSlice` objects.
- [ ] 052. Create a `ClusterIP` Service with `kubectl expose` and from a YAML manifest; verify it resolves inside the cluster.
- [ ] 053. Create a `NodePort` Service and explain the port/targetPort/nodePort relationship and the default NodePort range (30000–32767).
- [ ] 054. Describe when to use a `LoadBalancer` Service (cloud provider or MetalLB) and how it builds on top of `NodePort` and `ClusterIP`.
- [ ] 055. Create an `ExternalName` Service that provides a CNAME alias to an external DNS name without proxying traffic.
- [ ] 056. Create a headless Service (`clusterIP: None`) and explain how it enables direct Pod DNS records for StatefulSets.
- [ ] 057. Troubleshoot a Service that has no endpoints: check that Pod labels match the Service selector, Pods are Running, and the correct port is exposed.
- [ ] 058. Inspect `EndpointSlice` objects to see which Pod IPs are backing a Service using `kubectl get endpointslices`.

---

## NetworkPolicies

- [ ] 059. Explain the default-allow behavior of Kubernetes networking and why explicit `NetworkPolicy` is required to enforce isolation.
- [ ] 060. Write a `NetworkPolicy` that creates a default-deny-all-ingress policy for all Pods in a namespace by leaving `podSelector: {}` and `ingress: []`.
- [ ] 061. Write a `NetworkPolicy` that allows ingress to a Pod on a specific port only from Pods with a specific label using `podSelector` under `ingress.from`.
- [ ] 062. Write a `NetworkPolicy` that allows ingress from Pods in a specific namespace using `namespaceSelector` under `ingress.from`.
- [ ] 063. Write a `NetworkPolicy` with an egress rule that restricts outbound traffic from selected Pods to only a specific IP block and port.
- [ ] 064. Combine `podSelector` and `namespaceSelector` in the same `from` entry (AND logic) versus in separate entries (OR logic) and explain the difference.
- [ ] 065. Verify `NetworkPolicy` enforcement by using `kubectl exec` to run `curl` or `nc` between Pods and confirming allowed vs. blocked paths.

---

## Ingress

- [ ] 066. Explain the role of an Ingress controller (NGINX, Traefik, etc.) versus the `Ingress` resource object, and why both are required.
- [ ] 067. Write an `Ingress` manifest that routes traffic to two different Services based on the HTTP path (`/api` → service-a, `/web` → service-b).
- [ ] 068. Write an `Ingress` manifest that routes traffic based on the HTTP `Host` header to route multiple virtual hosts through a single IP.
- [ ] 069. Configure TLS termination on an `Ingress` by referencing a `kubernetes.io/tls` Secret and adding a `tls:` block.
- [ ] 070. Set `pathType` correctly (`Prefix` vs. `Exact` vs. `ImplementationSpecific`) and explain the routing differences.
- [ ] 071. Set the `ingressClassName` field (or annotation) to select a specific Ingress controller when multiple controllers are installed.
- [ ] 072. Troubleshoot an Ingress returning 404 or 502 by checking the controller logs, backend Service existence, endpoint readiness, and path/host match.

---

## Persistent Volumes and Persistent Volume Claims

- [ ] 073. Distinguish between the admin role (creates `PersistentVolume` or `StorageClass`) and the developer role (creates `PersistentVolumeClaim` to consume storage).
- [ ] 074. Write a `PersistentVolumeClaim` manifest specifying `storageClassName`, `accessModes`, and `resources.requests.storage`.
- [ ] 075. Mount a `PersistentVolumeClaim` in a Pod by adding it to `volumes` and referencing it in `volumeMounts` with a `mountPath`.
- [ ] 076. Explain the four access modes — `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod` — and which volume backends support each.
- [ ] 077. Explain the PVC lifecycle: Pending → Bound, and what causes a PVC to remain `Pending` (no matching PV, StorageClass provisioner unavailable).
- [ ] 078. Use `emptyDir` for ephemeral shared storage between containers in the same Pod and understand that data is lost when the Pod is deleted.

---

## ServiceAccounts & RBAC (Consumer Perspective)

- [ ] 079. Explain how every Pod is automatically associated with a `ServiceAccount` (default is `default` in the namespace) and what token is auto-mounted.
- [ ] 080. Create a named `ServiceAccount` with `kubectl create serviceaccount` and associate it with a Pod via `spec.serviceAccountName`.
- [ ] 081. Disable the automatic mounting of the service account token in a Pod by setting `automountServiceAccountToken: false`.
- [ ] 082. Explain the components of RBAC: `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding` and which scope (namespace vs. cluster) each applies to.
- [ ] 083. Create a `Role` that grants `get`, `list`, and `watch` on `pods` within a namespace, and bind it to a `ServiceAccount` via a `RoleBinding`.
- [ ] 084. Test what a `ServiceAccount` or user is allowed to do using `kubectl auth can-i <verb> <resource> --as=<user> -n <namespace>`.

---

## Observability: Logs, Events, Top, Debug

- [ ] 085. Stream logs from a running container using `kubectl logs -f <pod> -c <container>` and retrieve terminated container logs with `--previous`.
- [ ] 086. Filter logs by time window using `--since=1h` or `--since-time=<RFC3339>` and limit output with `--tail=50`.
- [ ] 087. Retrieve logs from all containers in a Pod simultaneously with `kubectl logs <pod> --all-containers=true`.
- [ ] 088. View cluster events sorted by timestamp using `kubectl get events --sort-by='.lastTimestamp'` to diagnose recent failures.
- [ ] 089. Check node and Pod resource usage with `kubectl top nodes` and `kubectl top pods --sort-by=memory` using the metrics-server.
- [ ] 090. Use `kubectl describe pod <name>` to read the `Events` section and diagnose issues like `ImagePullBackOff`, `OOMKilled`, and `CrashLoopBackOff`.
- [ ] 091. Launch an ephemeral debug container into a running Pod with `kubectl debug -it <pod> --image=busybox --target=<container>`.
- [ ] 092. Create a debugging copy of a Pod with a different image using `kubectl debug <pod> -it --copy-to=<debug-pod> --set-image=<container>=busybox`.
- [ ] 093. Debug a node directly by launching a privileged Pod on it with `kubectl debug node/<node> -it --image=ubuntu`.
- [ ] 094. Copy files to and from a running container with `kubectl cp <pod>:<remote-path> <local-path>` and vice versa.
- [ ] 095. Use `kubectl port-forward pod/<name> 8080:80` to test a container's HTTP endpoint locally without exposing it via a Service.
- [ ] 096. Use `kubectl exec -it <pod> -- sh` to get a shell into a running container for live troubleshooting.

---

## CRDs and Operators

- [ ] 097. Explain what a `CustomResourceDefinition` (CRD) is and how it extends the Kubernetes API with new resource types.
- [ ] 098. List all CRDs installed in a cluster with `kubectl get crds` and discover their short names and API groups.
- [ ] 099. Create instances of a custom resource (CR) from a YAML manifest and interact with them using standard `kubectl` commands.
- [ ] 100. Explain the operator pattern: a controller that watches CRs and reconciles real-world state to match the CR spec.

---

## Pod Lifecycle Hooks

- [ ] 101. Configure a `lifecycle.postStart` exec handler that runs a command immediately after a container starts, and understand that it blocks the container from reaching `Running` state until the handler completes or times out.
- [ ] 102. Configure a `lifecycle.preStop` exec or sleep handler to delay SIGTERM and enable graceful shutdown (e.g., `preStop: exec: command: ["sleep","10"]`); this is essential for zero-downtime deployments behind a load balancer.
- [ ] 103. Explain how `terminationGracePeriodSeconds` interacts with `preStop`: the kubelet waits up to `terminationGracePeriodSeconds` for both the `preStop` handler and the main process to exit before sending SIGKILL; the `preStop` duration counts against this budget.

---

## StatefulSet & DaemonSet Update Strategies

- [ ] 104. Configure a `StatefulSet` with `updateStrategy.type: RollingUpdate` and understand that Pods are updated in reverse ordinal order (highest index first).
- [ ] 105. Set `updateStrategy.type: OnDelete` on a `StatefulSet` to require manual deletion of each Pod before the updated template is applied to it; use this when you need full control over the upgrade sequence.
- [ ] 106. Use `updateStrategy.rollingUpdate.partition` on a `StatefulSet` to perform a canary-style staged rollout: only Pods with an ordinal index ≥ the partition value are updated, leaving lower-indexed Pods on the old version.
- [ ] 107. Configure a `DaemonSet` update strategy with `rollingUpdate.maxUnavailable` to control how many nodes' Pods are taken down simultaneously during a DaemonSet rolling update.
- [ ] 108. Understand that `kubectl rollout undo` is **not supported** for `StatefulSet` — to roll back a StatefulSet, manually set `spec.template.spec.containers[].image` back to the previous version and let the rolling update strategy apply the change.

---

## Job & CronJob Advanced

- [ ] 109. Set `spec.ttlSecondsAfterFinished` on a `Job` to automatically delete it (and its Pods) a fixed number of seconds after it reaches a terminal state (`Complete` or `Failed`), preventing accumulation of finished Jobs.
- [ ] 110. Suspend a `CronJob` by setting `spec.suspend: true` (e.g., `kubectl patch cronjob <name> -p '{"spec":{"suspend":true}}'`) and resume it by setting it back to `false`; understand that all scheduled runs are skipped while suspended.

---

## Resource Requests, Limits — Ephemeral Storage

- [ ] 111. Define `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` on a container to protect against disk-hungry containers; when the limit is exceeded the kubelet evicts the Pod from the node.

---

---

# ✅ CKA — Specific Topics

## Cluster Architecture & Control Plane Components

- [ ] 112. Describe the exact function of `kube-apiserver` as the single entry point for all REST operations, authentication, authorization, and admission control.
- [ ] 113. Explain how `etcd` stores all cluster state as key-value pairs and why it is the single source of truth for the Kubernetes control plane.
- [ ] 114. Describe the role of `kube-controller-manager` and list five built-in controllers it runs (Node, Replication, Endpoints, ServiceAccount, Job).
- [ ] 115. Explain how `kube-scheduler` selects a node for an unscheduled Pod through filtering (predicates) and scoring (priorities).
- [ ] 116. Describe what `kubelet` does on every worker node: registers the node, pulls images, starts containers via CRI, reports status, and runs probes.
- [ ] 117. Explain the role of `kube-proxy` in maintaining network rules (iptables/IPVS) on every node to implement `Service` virtual IPs.
- [ ] 118. Locate and read static Pod manifests in `/etc/kubernetes/manifests/` and understand how the kubelet self-hosts control-plane components.
- [ ] 119. Identify the key configuration flags for `kube-apiserver` (e.g., `--etcd-servers`, `--service-cluster-ip-range`, `--authorization-mode`, `--enable-admission-plugins`).
- [ ] 120. Identify the key configuration flags for `kubelet` in `/var/lib/kubelet/config.yaml` and `/etc/kubernetes/kubelet.conf`.

---

## kubeadm — Cluster Installation & Lifecycle

- [ ] 121. Install the required prerequisites for `kubeadm`: disable swap, load `br_netfilter` and `overlay` kernel modules, set `net.ipv4.ip_forward=1`, and install a container runtime.
- [ ] 122. Install specific versions of `kubeadm`, `kubelet`, and `kubectl` using the package manager and hold them to prevent unintended upgrades.
- [ ] 123. Initialize a cluster with `kubeadm init --pod-network-cidr=<cidr> --apiserver-advertise-address=<ip>` and save the join command and certificate key.
- [ ] 124. Configure `kubectl` for the new cluster by copying `/etc/kubernetes/admin.conf` to `~/.kube/config`.
- [ ] 125. Install a CNI plugin (e.g., Calico or Flannel) after `kubeadm init` using the plugin's official manifest URL.
- [ ] 126. Join a worker node to the cluster using `kubeadm join <control-plane-host>:<port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>`.
- [ ] 127. Generate a new bootstrap token for joining nodes with `kubeadm token create --print-join-command`.
- [ ] 128. Renew all control-plane certificates with `kubeadm certs renew all` and verify expiry dates with `kubeadm certs check-expiration`.
- [ ] 129. Reset a node cleanly with `kubeadm reset` before rejoining it or repurposing it.
- [ ] 130. Use `kubeadm config print init-defaults` to understand the default initialization configuration and how to customize it via a `kubeadm-config.yaml` file.

---

## Cluster Upgrades

- [ ] 131. Describe the Kubernetes version skew policy and which components must be upgraded first (control plane before worker nodes).
- [ ] 132. Upgrade `kubeadm` to the target version before upgrading any cluster component.
- [ ] 133. Plan the upgrade by running `kubeadm upgrade plan` and reading its output to identify the target version and required steps.
- [ ] 134. Apply the upgrade to the control plane with `kubeadm upgrade apply v1.X.Y` and verify control-plane component versions afterwards.
- [ ] 135. Upgrade `kubelet` and `kubectl` on the control-plane node after running `kubeadm upgrade apply`.
- [ ] 136. Drain a worker node with `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data` before upgrading it.
- [ ] 137. Upgrade `kubeadm`, then `kubelet` and `kubectl` on the worker node, and run `kubeadm upgrade node`.
- [ ] 138. Uncordon the worker node with `kubectl uncordon <node>` and verify it is `Ready` and running the new kubelet version.

---

## etcd Backup & Restore

- [ ] 139. Identify the `etcd` endpoint, CA certificate, client certificate, and client key required to authenticate `etcdctl` commands.
- [ ] 140. Set the `ETCDCTL_API=3` environment variable before using `etcdctl` commands to target the v3 API.
- [ ] 141. Create an etcd snapshot with `etcdctl snapshot save <path> --endpoints=<url> --cacert=<ca> --cert=<cert> --key=<key>`.
- [ ] 142. Verify the integrity of an etcd snapshot file with `etcdctl snapshot status <path> --write-out=table`.
- [ ] 143. Restore an etcd snapshot with `etcdctl snapshot restore <path> --data-dir=<new-dir>` and update the etcd static Pod manifest to point to the new data directory.
- [ ] 144. Restart the etcd static Pod after restoring by moving its manifest out and back into `/etc/kubernetes/manifests/`.
- [ ] 145. Verify cluster health after restore using `kubectl get nodes` and `kubectl get pods -A`.

---

## Highly Available Control Plane

- [ ] 146. Explain the difference between stacked etcd topology (etcd runs on the same nodes as control-plane components) and external etcd topology.
- [ ] 147. Describe how to initialize an HA control plane with `kubeadm init --control-plane-endpoint=<lb-dns>:<port> --upload-certs`.
- [ ] 148. Join additional control-plane nodes with `kubeadm join --control-plane --certificate-key <key>`.
- [ ] 149. Explain the role of a load balancer (HAProxy, Keepalived, cloud LB) in front of multiple `kube-apiserver` instances.
- [ ] 150. Understand how `kube-controller-manager` and `kube-scheduler` use leader election to avoid split-brain when running on multiple control-plane nodes.

---

## RBAC (Admin/Operator Perspective)

- [ ] 151. Create a `ClusterRole` that grants read-only access to all resources in a specific API group across all namespaces.
- [ ] 152. Create a `ClusterRoleBinding` to bind a `ClusterRole` to a user, group, or `ServiceAccount`.
- [ ] 153. Create a namespace-scoped `Role` and `RoleBinding` to grant a service account access to specific verbs on specific resources.
- [ ] 154. Use aggregated `ClusterRoles` by adding the `rbac.authorization.k8s.io/aggregate-to-<role>: "true"` label to extend built-in roles.
- [ ] 155. Verify a user's permissions with `kubectl auth can-i --list --as=<user>` and `kubectl auth can-i <verb> <resource> --as=<user> -n <ns>`.
- [ ] 156. Identify and fix over-permissive RBAC configurations — e.g., remove wildcard verbs (`*`) or resources that grant excessive access.

---

## Extension Interfaces (CNI, CSI, CRI)

- [ ] 157. Explain what CNI (Container Network Interface) does: provisions a network interface inside a Pod sandbox and configures routing on the node.
- [ ] 158. Identify which CNI plugin is installed by inspecting files under `/etc/cni/net.d/` and `/opt/cni/bin/`.
- [ ] 159. Explain what CRI (Container Runtime Interface) does and identify the active runtime socket (e.g., `/run/containerd/containerd.sock`) with `crictl info`.
- [ ] 160. Use `crictl ps`, `crictl logs`, and `crictl inspect` to inspect containers at the CRI level when `kubectl` cannot reach a Pod.
- [ ] 161. Explain what CSI (Container Storage Interface) does: allows external storage drivers to be installed and managed independently of Kubernetes core.

---

## Scheduling (Admin Perspective)

- [ ] 162. Schedule a Pod on a specific node using `spec.nodeName` (bypasses the scheduler entirely).
- [ ] 163. Use `nodeSelector` to constrain a Pod to nodes with a specific label (e.g., `disktype: ssd`).
- [ ] 164. Write a `requiredDuringSchedulingIgnoredDuringExecution` node affinity rule that prevents a Pod from being scheduled on non-matching nodes.
- [ ] 165. Write a `preferredDuringSchedulingIgnoredDuringExecution` node affinity rule with a weight to softly prefer certain nodes.
- [ ] 166. Add a taint to a node with `kubectl taint nodes <node> key=value:NoSchedule` and add a matching toleration to a Pod spec.
- [ ] 167. Use `NoExecute` taint effect to evict existing Pods from a node and add `tolerationSeconds` to a toleration to allow a grace period before eviction.
- [ ] 168. Write pod affinity rules to co-locate Pods with a specific topology key (e.g., `kubernetes.io/hostname`) and pod anti-affinity to spread Pods across nodes.
- [ ] 169. Write a `topologySpreadConstraint` to spread Pods evenly across zones using `maxSkew`, `topologyKey`, and `whenUnsatisfiable`.
- [ ] 170. Create a `PriorityClass` object and assign it to a Pod via `spec.priorityClassName` to control preemption order.
- [ ] 171. Identify why a Pod is stuck in `Pending` due to scheduling constraints using `kubectl describe pod` and reading the `Events` section.

---

## Workload Autoscaling

- [ ] 172. Create a `HorizontalPodAutoscaler` (HPA) v2 that scales a `Deployment` based on CPU utilization using `kubectl autoscale` and verify with `kubectl get hpa`.
- [ ] 173. Write an HPA manifest with a `metrics` block targeting average CPU utilization (as a percentage of request) and set `minReplicas` and `maxReplicas`.
- [ ] 174. Explain the role of `metrics-server` as the source of real-time resource metrics for HPA and how to verify it is running.
- [ ] 175. Describe conceptually what `VerticalPodAutoscaler` (VPA) does and its three update modes: `Off`, `Initial`, `Auto`.
- [ ] 176. Explain what `Cluster Autoscaler` does (adds/removes nodes) and how it interacts with unschedulable Pods.
- [ ] 177. Create a `PodDisruptionBudget` (PDB) specifying `minAvailable` or `maxUnavailable` to protect an application during voluntary disruptions like node drains.

---

## Storage (Admin Perspective)

- [ ] 178. Create a `StorageClass` with a specific provisioner, parameters, `reclaimPolicy`, and `volumeBindingMode` (`Immediate` vs. `WaitForFirstConsumer`).
- [ ] 179. Annotate a `StorageClass` as the cluster default using `storageclass.kubernetes.io/is-default-class: "true"`.
- [ ] 180. Create a `PersistentVolume` manually with a specific `capacity`, `accessModes`, `persistentVolumeReclaimPolicy`, and a `hostPath` or `nfs` source.
- [ ] 181. Understand PV reclaim policies: `Retain` (keeps data, must be manually reclaimed) vs. `Delete` (deletes the underlying storage asset).
- [ ] 182. Expand a `PersistentVolumeClaim` by editing its `spec.resources.requests.storage` and ensure the `StorageClass` has `allowVolumeExpansion: true`.
- [ ] 183. Explain VolumeMode `Filesystem` (default, mounted as a directory) versus `Block` (raw block device, no filesystem layer).

---

## Services & Networking (Admin Perspective)

- [ ] 184. Explain the three kube-proxy modes — `iptables`, `IPVS`, and `nftables` — and the key differences in performance and rule management.
- [ ] 185. Inspect iptables rules on a node with `iptables -t nat -L KUBE-SERVICES` to trace how a `ClusterIP` is translated to a Pod IP.
- [ ] 186. Configure CoreDNS by editing its `ConfigMap` (`coredns` in `kube-system`) and understand the structure of the `Corefile`.
- [ ] 187. Explain Kubernetes DNS naming: `<svc>.<ns>.svc.cluster.local` for Services and `<pod-ip-dashes>.<ns>.pod.cluster.local` for Pods.
- [ ] 188. Configure Pod DNS settings with `spec.dnsPolicy` (values: `ClusterFirst`, `Default`, `None`, `ClusterFirstWithHostNet`) and custom `spec.dnsConfig`.
- [ ] 189. Install and use the **Gateway API** resources: `GatewayClass`, `Gateway`, and `HTTPRoute` to route HTTP traffic with more expressiveness than `Ingress`.
- [ ] 190. Write an `HTTPRoute` that routes traffic to different backends based on HTTP path prefixes and understand how it references a `Gateway`.
- [ ] 191. Explain `ReferenceGrant` in the Gateway API and why it is required when an `HTTPRoute` in one namespace references a Service in another namespace.

---

## Troubleshooting — Nodes

- [ ] 192. Identify a `NotReady` node and begin systematic diagnosis by running `kubectl describe node <name>` and reading the `Conditions` section.
- [ ] 193. SSH into the problematic node and check `kubelet` service status and logs with `systemctl status kubelet` and `journalctl -u kubelet -n 100`.
- [ ] 194. Diagnose a kubelet that fails to start due to a misconfigured `/var/lib/kubelet/config.yaml` or stale `/etc/kubernetes/kubelet.conf`.
- [ ] 195. Fix a node where the container runtime is not running by starting `containerd` with `systemctl start containerd` and enabling it on boot.
- [ ] 196. Check node disk pressure, memory pressure, and PID pressure conditions using `kubectl describe node` and correlate them with resource exhaustion.
- [ ] 197. Use `crictl ps -a` to list all containers (including failed ones) at the runtime level when `kubectl` reports no Pods on a node.
- [ ] 198. Check certificate expiration for the kubelet client certificate and explain how to renew it using `kubeadm certs renew`.

---

## Troubleshooting — Control Plane Components

- [ ] 199. Diagnose a non-functional `kube-apiserver` by examining its static Pod manifest in `/etc/kubernetes/manifests/kube-apiserver.yaml` for misconfigurations.
- [ ] 200. View logs of a control-plane static Pod when the Pod is not running using `crictl logs <container-id>` directly on the control-plane node.
- [ ] 201. Fix a misconfigured etcd (e.g., wrong data directory path or bad certificate reference) by editing the static Pod manifest and waiting for the kubelet to restart it.
- [ ] 202. Diagnose a `kube-scheduler` that is not scheduling Pods by checking its logs for errors and verifying it holds the leader lease.
- [ ] 203. Diagnose a `kube-controller-manager` that is not creating Pods (e.g., HPA not scaling, Jobs not creating) by examining its logs.
- [ ] 204. Validate that all control-plane Pods are running with `kubectl get pods -n kube-system` and identify any with a non-Running status.

---

## Troubleshooting — Applications & Networking

- [ ] 205. Diagnose a `CrashLoopBackOff` Pod by reading its logs with `kubectl logs --previous`, checking exit codes, and inspecting `lastState` in `kubectl describe`.
- [ ] 206. Diagnose an `ImagePullBackOff` error by verifying the image name and tag, checking registry credentials (`imagePullSecrets`), and reading the event message.
- [ ] 207. Diagnose a `Pending` Pod by reading the Events section of `kubectl describe pod` for messages about insufficient CPU, memory, or unmatched affinity rules.
- [ ] 208. Diagnose a Service with no endpoints by confirming Pod selector labels match Service selector, Pods are Running, and `containerPort` matches Service `targetPort`.
- [ ] 209. Test DNS resolution from inside a Pod using `kubectl exec <pod> -- nslookup <svc>.<ns>.svc.cluster.local`.
- [ ] 210. Identify kube-proxy iptables rules routing traffic for a Service and use `iptables-save | grep <svc-ip>` to trace NAT rules.
- [ ] 211. Identify a `NetworkPolicy` that is blocking traffic by temporarily removing it in a test environment and re-testing connectivity.

---

## Volume Snapshots (CSI)

- [ ] 212. Explain the three VolumeSnapshot API objects: `VolumeSnapshotClass` (defines the CSI driver and deletion policy), `VolumeSnapshot` (the user's snapshot request, analogous to a PVC), and `VolumeSnapshotContent` (the actual snapshot resource, analogous to a PV).
- [ ] 213. Create a `VolumeSnapshot` from an existing PVC by writing a manifest with `spec.source.persistentVolumeClaimName` and `spec.volumeSnapshotClassName`, then verify it is `readyToUse: true`.
- [ ] 214. Restore data from a `VolumeSnapshot` by creating a new PVC with `spec.dataSource.kind: VolumeSnapshot` and `spec.dataSource.name` pointing to the snapshot name.

---

## Scheduler Profiles

- [ ] 215. Assign a Pod to a non-default scheduler or scheduler profile by setting `spec.schedulerName: <profile-name>` in the Pod spec; Pods referencing an unknown scheduler name remain `Pending` indefinitely.
- [ ] 216. Explain how multiple scheduler profiles are defined in the `KubeSchedulerConfiguration` file under `profiles:`, each with a distinct `schedulerName` and its own plugin configuration, allowing different scheduling behaviour without running separate scheduler processes.

---

## Admission Controllers & Webhooks

- [ ] 217. Explain the admission control pipeline: after authentication and authorization, requests pass through mutating admission plugins (including `MutatingAdmissionWebhook`) and then validating admission plugins (including `ValidatingAdmissionWebhook`) before the object is persisted to etcd.
- [ ] 218. Diagnose a resource rejected by an admission webhook: read the rejection reason from the `kubectl apply` error output, identify the responsible webhook with `kubectl get validatingwebhookconfigurations` or `kubectl get mutatingwebhookconfigurations`, and check its `failurePolicy` (`Fail` blocks the request; `Ignore` allows it through on webhook error).

---

## Node Management

- [ ] 219. Label a node with `kubectl label nodes <node-name> <key>=<value>`, verify with `kubectl get node <name> --show-labels`, and remove a label with `kubectl label nodes <node-name> <key>-`; node labels are the foundation for `nodeSelector` and node affinity rules.

---

## kubeadm Advanced

- [ ] 220. Pre-pull all required control-plane container images before running `kubeadm init` using `kubeadm config images pull [--kubernetes-version v1.X.Y]`; useful on air-gapped or slow-network nodes to verify image availability before starting cluster initialization.

---

## CoreDNS Advanced

- [ ] 221. Add a stub zone to the CoreDNS `Corefile` ConfigMap (in `kube-system`) so that DNS queries for a specific internal domain (e.g., `corp.internal`) are forwarded to a designated upstream resolver IP, then restart the CoreDNS Pods to apply the change.

---

## HA etcd Restore

- [ ] 222. When restoring an etcd snapshot in a multi-member HA cluster, run `etcdctl snapshot restore` separately for each member with member-specific flags (`--name`, `--initial-cluster`, `--initial-cluster-token`, `--initial-advertise-peer-urls`, `--data-dir`), then update each node's etcd static Pod manifest to point to its restored data directory before bringing members back online.

---

## Storage Troubleshooting

- [ ] 223. Diagnose a PVC expansion stuck in `FileSystemResizePending` status: understand that the filesystem resize happens inside the running container and only completes after the Pod mounting the PVC is restarted; delete and recreate the Pod (or trigger a rollout restart) to allow the kubelet to expand the filesystem.

---

## Audit Logging

- [ ] 224. Explain the four audit log levels — `None` (suppress), `Metadata` (request metadata only), `Request` (metadata + request body), `RequestResponse` (metadata + request body + response body) — and the four stages — `RequestReceived`, `ResponseStarted`, `ResponseComplete`, `Panic`; audit policy rules are evaluated top-to-bottom and the first matching rule wins.
- [ ] 225. Write an `audit-policy.yaml` (`apiVersion: audit.k8s.io/v1, kind: Policy`) with targeted rules: `level: None` for health-check URLs (`/healthz`, `/readyz`, `/livez`), `level: Metadata` for GET/list/watch on Secrets and ConfigMaps, `level: RequestResponse` for write operations on Secrets, and a catch-all `level: Metadata` rule at the end.
- [ ] 226. Enable audit logging on the `kube-apiserver` static Pod by adding `--audit-policy-file=/etc/kubernetes/audit-policy.yaml`, `--audit-log-path=/var/log/kubernetes/audit.log`, `--audit-log-maxsize=100`, `--audit-log-maxbackup=5`, and `--audit-log-maxage=30` to the command arguments; mount the policy file and log directory as `hostPath` volumes in the manifest.
- [ ] 227. Query the audit log to trace a specific action: `tail -f /var/log/kubernetes/audit.log | jq 'select(.verb=="delete" and .objectRef.resource=="secrets") | {user:.user.username, ns:.objectRef.namespace, name:.objectRef.name}'`; use this pattern to identify which user performed a destructive operation.

---

## Encryption at Rest

- [ ] 228. Write an `EncryptionConfiguration` YAML (`apiVersion: apiserver.config.k8s.io/v1, kind: EncryptionConfiguration`) for Secrets: list `aescbc` (with a base64-encoded 32-byte key) as the first provider and `identity: {}` last; the first provider encrypts all new writes — placing `identity` last preserves read access to Secrets written before encryption was enabled.
- [ ] 229. Enable encryption at rest by adding `--encryption-provider-config=/etc/kubernetes/encryption-config.yaml` to the `kube-apiserver` static Pod manifest and creating a `hostPath` volume mount for the file; the API server must restart for the change to take effect.
- [ ] 230. Verify that a Secret is encrypted in etcd by running `ETCDCTL_API=3 etcdctl get /registry/secrets/<ns>/<name> --endpoints=... --cacert=... --cert=... --key=... | hexdump -C | head` and confirming the stored value begins with `k8s:enc:aescbc:v1:` — a readable plaintext value means encryption is not active.
- [ ] 231. Force-encrypt all pre-existing Secrets after enabling encryption at rest by running `kubectl get secrets -A -o json | kubectl replace -f -`; without this step, Secrets created before encryption was enabled remain stored as plaintext in etcd.

---

## TLS & PKI Management

- [ ] 232. Inspect a control-plane certificate with `openssl x509 -noout -text -in <cert>` to read the Subject CN (component identity), Issuer (signing CA), `Not After` (expiry date), Subject Alternative Names (IP/DNS names the cert is valid for), and Extended Key Usage — `TLS Web Client Authentication` identifies a client cert; `TLS Web Server Authentication` identifies a server cert.
- [ ] 233. Explain the role of `sa.key` / `sa.pub` in `/etc/kubernetes/pki/`: `kube-controller-manager` uses `sa.key` to sign ServiceAccount JWT tokens injected into Pods; `kube-apiserver` uses `sa.pub` to verify them; in HA clusters these files must be **identical** on all control-plane nodes — a mismatch causes tokens signed on one master to be rejected by the API server on another.
- [ ] 234. Explain the role of `front-proxy-ca.crt` / `front-proxy-client.crt` for the API aggregation layer: when `kubectl top` proxies through the main API server to `metrics-server` (an extension API server), the API server presents `front-proxy-client.crt`; expiry of these certs breaks all aggregated APIs including `kubectl top`.
- [ ] 235. Enable kubelet serving certificate auto-rotation by setting `serverTLSBootstrap: true` in `/var/lib/kubelet/config.yaml`; without this opt-in, `kubelet.crt` and `kubelet.key` (used by the API server when calling into the kubelet for `kubectl exec`/`logs`) are **not** auto-rotated and must be renewed manually.
- [ ] 236. Distinguish `admin.conf` from `super-admin.conf` (introduced in Kubernetes 1.29): `admin.conf` grants `system:masters` group membership and is subject to RBAC; `super-admin.conf` bypasses RBAC entirely and should remain on the control-plane node only as a break-glass emergency credential.
- [ ] 237. After running `kubeadm certs renew all`, restart all control-plane static Pods: move their manifests out of `/etc/kubernetes/manifests/`, wait for all containers to stop (`watch crictl ps`), move the manifests back, and re-copy `/etc/kubernetes/admin.conf` to `~/.kube/config` on every workstation — renewed certs are not picked up until the static Pods restart.
- [ ] 238. Renew a single expiring certificate without disrupting the others using `kubeadm certs renew <cert-name>` (e.g., `kubeadm certs renew apiserver`); use `kubeadm certs check-expiration` first to identify the correct cert name and its residual time.
- [ ] 239. Know the certificate distribution strategy in HA clusters: kubelet client/server certs are **unique per node** (CN = `system:node:<node-name>`); etcd peer/server certs are **unique per node** (SANs include the node IP); scheduler and controller-manager client certs are **shared** (role identity only); `sa.key`/`sa.pub` must be **identical** on all control-plane nodes.

---

## etcd Advanced Operations

- [ ] 240. Prefer `etcdutl snapshot restore <path> --data-dir=<new-dir>` over `etcdctl snapshot restore` for offline restores: `etcdutl` operates directly on the snapshot file without connecting to a running cluster and requires no `--endpoints` or TLS flags.
- [ ] 241. Before restoring an etcd snapshot, stop **all** control-plane static Pods by moving every manifest out of `/etc/kubernetes/manifests/` (not just `etcd.yaml`); wait with `watch crictl ps` until all containers have stopped to prevent mid-restore writes from `kube-apiserver` that would corrupt the restored data.
- [ ] 242. Compact old etcd revisions to reclaim space: capture the current revision with `rev=$(etcdctl endpoint status --write-out=json | jq '.[0].Status.header.revision')`, run `etcdctl compact $rev`, then run `etcdctl defrag` to release freed pages back to the filesystem; skipping defrag leaves the DB file at its maximum size even after compaction.
- [ ] 243. Diagnose etcd entering read-only mode ("mvcc: database space exceeded"): verify DB SIZE against the `--quota-backend-bytes` value using `etcdctl endpoint status --write-out=table`; resolve by compacting and defragmenting to shrink the database, or increase the quota in the `etcd.yaml` static Pod manifest if needed.

---

## RBAC Advanced

- [ ] 244. Restrict a `Role` or `ClusterRole` rule to specific named resource instances using `resourceNames: ["my-secret"]`; the allowed verbs apply only to the explicitly listed objects, not to all resources of that type — this is the primary mechanism for granting least-privilege access to individual Secrets or ConfigMaps.
- [ ] 245. Understand the special RBAC verbs `escalate` (grants the ability to create `RoleBinding`/`ClusterRoleBinding` objects that include permissions the subject does not itself hold) and `impersonate` (allows acting as another user, group, or ServiceAccount via `kubectl --as`); both require explicit grants and carry significant security risk.

---

## Manual Scheduling via Binding API

- [ ] 246. When `kube-scheduler` is not running and a Pod is stuck in `Pending`, manually assign it by creating a `Binding` object (`apiVersion: v1, kind: Binding`) with the Pod name in `metadata.name` and the target node in `target.apiVersion/kind/name`, or patch `spec.nodeName` directly on the pending Pod with `kubectl patch pod <name> -p '{"spec":{"nodeName":"<node>"}}'`.

---

## kube-proxy IPVS Inspection

- [ ] 247. When `kube-proxy` runs in IPVS mode, use `ipvsadm -Ln` on a node to list all IPVS virtual servers (Service ClusterIP:port) and their backend real servers (Pod IPs:port); use this to verify load-balancing targets at the kernel level, complementing `iptables-save | grep <svc-ip>` used in iptables mode.

---

## Service CIDR Change Procedure

- [ ] 248. Change the cluster Service CIDR after creation by: (1) updating `--service-cluster-ip-range` in both the `kube-apiserver` and `kube-controller-manager` static Pod manifests; (2) updating the CIDR in the `kube-proxy` ConfigMap; (3) deleting and re-creating the `kube-dns` Service with an explicit ClusterIP from the new range; (4) updating `clusterDNS` in `/var/lib/kubelet/config.yaml` on every node and restarting `kubelet`; existing Services retain their old ClusterIPs until individually deleted and re-created.

---

## NodeRestriction Admission Plugin

- [ ] 249. Explain the `NodeRestriction` admission plugin: it limits kubelets to modifying only their own Node object and the Pods bound to them, preventing a compromised node from reading Secrets or modifying objects belonging to other nodes; it depends on each kubelet presenting a unique client certificate with CN = `system:node:<node-name>` — sharing kubelet certs across nodes defeats this protection.

---

---

# ✅ CKAD — Specific Topics

## Container Images & Dockerfiles

- [ ] 250. Write a `Dockerfile` with `FROM`, `RUN`, `COPY`, `ADD`, `WORKDIR`, `EXPOSE`, `ENV`, `ARG`, `CMD`, and `ENTRYPOINT` instructions and understand the layering model.
- [ ] 251. Explain the difference between `CMD` and `ENTRYPOINT` in a Dockerfile and how they interact (exec vs. shell form, override behavior).
- [ ] 252. Use a multi-stage `Dockerfile` to separate the build environment from the final runtime image, reducing the final image size significantly.
- [ ] 253. Understand how `COPY --from=<stage>` works in a multi-stage build to selectively copy artifacts between stages.
- [ ] 254. Override a Docker image's `CMD` from the Kubernetes Pod spec using `spec.containers[].args`.
- [ ] 255. Override a Docker image's `ENTRYPOINT` from the Kubernetes Pod spec using `spec.containers[].command`.
- [ ] 256. Set the `imagePullPolicy` to `Always`, `IfNotPresent`, or `Never` and explain when each is appropriate (especially `Always` for `latest` tag).
- [ ] 257. Reference a private registry image in a Pod spec and attach an `imagePullSecrets` entry pointing to a Docker registry Secret.
- [ ] 258. Understand image digest pinning (`image: repo/name@sha256:<hash>`) versus tag-based references and the immutability advantage of digests.

---

## Multi-Container Pod Patterns

- [ ] 259. Explain why containers in the same Pod share a network namespace (same IP, same port space) and can communicate via `localhost`.
- [ ] 260. Explain why containers in the same Pod can share storage by mounting the same `emptyDir` volume to exchange data at runtime.
- [ ] 261. Write an **init container** that runs to completion before the main container starts and use it to pre-populate a shared `emptyDir` volume.
- [ ] 262. Use an init container to wait for a dependency (e.g., a database Service) to be available before the main application starts.
- [ ] 263. Write a **sidecar container** that runs alongside the main container to handle a cross-cutting concern (e.g., log shipper, proxy, metrics exporter).
- [ ] 264. Implement the native restartable sidecar pattern (Kubernetes v1.29+ GA): place the sidecar as an init container with `restartPolicy: Always` so it starts before app containers and outlives them.
- [ ] 265. Implement the **ambassador** pattern: a proxy sidecar that intercepts outbound traffic from the main container (e.g., routing to a local proxy).
- [ ] 266. Implement the **adapter** pattern: a sidecar that transforms output from the main container into a standard format (e.g., normalizing log format for a centralized logging system).
- [ ] 267. Write a Pod spec with multiple containers each having their own `resources`, `env`, `volumeMounts`, and `readinessProbe`.

---

## Probes & Health Checks

- [ ] 268. Configure a `livenessProbe` using `httpGet` on a specific path and port and explain what happens when it fails (container restart, subject to `restartPolicy`).
- [ ] 269. Configure a `livenessProbe` using `exec` to run a command inside the container and explain how exit code 0 means healthy.
- [ ] 270. Configure a `livenessProbe` using `tcpSocket` to check if a specific port is accepting connections.
- [ ] 271. Configure a `livenessProbe` using `grpc` to call a gRPC Health Checking Protocol endpoint.
- [ ] 272. Configure a `readinessProbe` and explain how it controls whether a Pod's IP is added to the Service `Endpoints` — it does not cause restarts.
- [ ] 273. Configure a `startupProbe` to give slow-starting containers time to initialize before liveness and readiness probes begin evaluating.
- [ ] 274. Tune probe parameters: `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `successThreshold`, and `failureThreshold` and explain each field's effect.
- [ ] 275. Diagnose a Pod that is repeatedly being restarted by identifying a misconfigured `livenessProbe` from `kubectl describe pod` events.
- [ ] 276. Diagnose a Pod that never receives traffic by identifying a `readinessProbe` that is permanently failing.

---

## Application Deployment Strategies

- [ ] 277. Implement a **blue/green** deployment using two `Deployment` objects (one active, one idle) and switch live traffic by changing the `Service` `selector` label.
- [ ] 278. Implement a **canary** deployment by running two `Deployment` objects with shared labels and splitting traffic proportionally through replica counts.
- [ ] 279. Explain the trade-offs between blue/green (instant switch, double resources) and canary (gradual rollout, partial risk exposure, incremental validation).
- [ ] 280. Configure a `Deployment` with `strategy.type: Recreate` to terminate all existing Pods before creating new ones (accepts downtime, avoids mixed-version state).
- [ ] 281. Write the full rollout workflow for a failed deployment: push bad image → observe failure → `kubectl rollout undo` → verify rollback with `kubectl rollout status`.

---

## API Deprecations & Discovery

- [ ] 282. Identify deprecated API versions in a manifest (e.g., `extensions/v1beta1`) by running `kubectl apply --dry-run=server` and reading the deprecation warning.
- [ ] 283. Use `kubectl api-resources` to list all resource types, their short names, API groups, and whether they are namespaced.
- [ ] 284. Use `kubectl api-versions` to list all API groups and their available versions currently served by the cluster.
- [ ] 285. Use `kubectl explain <resource>.<field>` to interactively explore the API schema and find the correct field names for any resource.
- [ ] 286. Use `kubectl explain --recursive <resource>` to get the full field tree for a resource for quick YAML authoring in the exam.
- [ ] 287. Fix a manifest that uses a deprecated API version by editing `apiVersion` and updating any removed or renamed fields to match the current API.

---

## Application Environment & SecurityContexts

- [ ] 288. Set a `securityContext` at the **Pod level** to define `runAsUser`, `runAsGroup`, `fsGroup`, and `supplementalGroups` that apply to all containers in the Pod.
- [ ] 289. Set a `securityContext` at the **container level** to override Pod-level settings for specific containers (e.g., different `runAsUser`, `readOnlyRootFilesystem`).
- [ ] 290. Set `runAsNonRoot: true` at the Pod or container level and understand that Kubernetes rejects containers whose image runs as UID 0.
- [ ] 291. Set `readOnlyRootFilesystem: true` for a container and add a writable `emptyDir` volume mounted at paths that the application needs to write to.
- [ ] 292. Set `allowPrivilegeEscalation: false` to prevent a process inside a container from gaining more privileges than its parent process.
- [ ] 293. Drop all Linux capabilities with `securityContext.capabilities.drop: ["ALL"]` and selectively add back only what is needed (e.g., `NET_BIND_SERVICE`).
- [ ] 294. Add a Linux capability with `securityContext.capabilities.add` and explain what each capability grants (e.g., `NET_ADMIN`, `SYS_TIME`, `SYS_PTRACE`).
- [ ] 295. Apply a **Pod Security Admission** profile to a namespace by setting the label `pod-security.kubernetes.io/enforce: restricted` and understand the three profiles: `privileged`, `baseline`, `restricted`.
- [ ] 296. Understand what the `restricted` PSA profile requires: no privileged containers, no host namespaces, drop `ALL` capabilities, `runAsNonRoot`, `readOnlyRootFilesystem`, no privilege escalation.
- [ ] 297. Set a **seccomp** profile on a container using `securityContext.seccompProfile.type: RuntimeDefault` or `Localhost` with a profile path.

---

## Advanced ConfigMap & Secret Usage

- [ ] 298. Use `configMapGenerator` in a Kustomize `kustomization.yaml` to auto-generate a ConfigMap from files with a hash suffix to trigger rolling updates on change.
- [ ] 299. Use `secretGenerator` in a Kustomize `kustomization.yaml` to generate a Secret from literal values in an overlay.
- [ ] 300. Understand that updating a ConfigMap mounted as a volume eventually updates the file inside a running container (kubelet refresh delay ~60s), unlike env vars which require a Pod restart.
- [ ] 301. Pass Pod metadata into a container using `downwardAPI` volumes or env vars to expose `metadata.name`, `metadata.namespace`, `status.podIP`, and resource field values.

---

## ServiceAccounts (Developer Perspective)

- [ ] 302. Create a `ServiceAccount`, bind it to a `Role` that allows specific API operations, and reference it in a Pod to give the application Kubernetes API access.
- [ ] 303. Mount a projected `ServiceAccount` token with a custom audience and expiry using the `projected` volume with a `serviceAccountToken` source.
- [ ] 304. Explain why `automountServiceAccountToken: false` is a security best practice for Pods that do not need to call the Kubernetes API.

---

## Volumes (Developer Perspective)

- [ ] 305. Use an `emptyDir` volume shared between an init container and the main container to pre-seed configuration or data files at startup.
- [ ] 306. Use a `downwardAPI` volume to expose Pod labels and annotations as files inside the container for consumption by the application.
- [ ] 307. Use a `projected` volume to combine multiple sources (ConfigMap, Secret, downwardAPI, ServiceAccount token) into a single unified mount point.
- [ ] 308. Request ephemeral storage with `resources.requests.ephemeral-storage` and `resources.limits.ephemeral-storage` to protect against disk-hungry containers evicting other Pods.
- [ ] 309. Use `subPathExpr` in a `volumeMount` to dynamically set the subpath using a Pod environment variable expansion.

---

## Services & Networking (Developer Perspective)

- [ ] 310. Troubleshoot an application that cannot reach a Service by checking DNS resolution, Service selector label matching, and endpoint readiness from within a debug Pod.
- [ ] 311. Configure an application to discover Service endpoints via environment variables (`<SVC_NAME>_SERVICE_HOST`, `<SVC_NAME>_SERVICE_PORT`) injected automatically by Kubernetes.
- [ ] 312. Write a `NetworkPolicy` from the perspective of a developer to isolate application Pods and permit only traffic from a specific frontend tier label.
- [ ] 313. Use `kubectl port-forward svc/<name> 8080:80` to forward traffic to a Service (not just a Pod) for local testing without a NodePort or LoadBalancer.

---

## API Deprecations — kubectl convert

- [ ] 314. Use the `kubectl-convert` plugin (`kubectl convert -f <manifest.yaml> --output-version <group/version>`) to automatically rewrite a manifest from a deprecated API version to a supported one; install the plugin separately from the kubectl binary.

---

## Additional Secret Types

- [ ] 315. Recognize the `kubernetes.io/basic-auth` Secret type (required data keys: `username` and `password`) and the `kubernetes.io/ssh-auth` type (required key: `ssh-privatekey`); create them with `kubectl create secret` or a YAML manifest specifying `type:`.
- [ ] 316. Recognize the `kubernetes.io/service-account-token` Secret type as the legacy mechanism for manually creating long-lived SA tokens; in Kubernetes v1.24+ tokens are no longer auto-created as Secrets — prefer `kubectl create token <sa-name>` for short-lived tokens or a projected `serviceAccountToken` volume.

---

## Pod-Level Host Namespaces

- [ ] 317. Set `spec.hostNetwork: true` on a Pod to make it share the node's network namespace (the Pod uses the node's IP and ports directly) and explain why the `restricted` Pod Security Admission profile forbids this.
- [ ] 318. Set `spec.hostPID: true` or `spec.hostIPC: true` on a Pod to share the node's PID or IPC namespace; understand the security implications (visibility of all node processes / IPC resources) and that both PSA `baseline` and `restricted` profiles block these fields.

---

## AppArmor

- [ ] 319. Apply an AppArmor profile to a container by setting `securityContext.appArmorProfile.type: RuntimeDefault` (node's default profile) or `Localhost` with `localhostProfile: <profile-name>`; `Unconfined` disables AppArmor enforcement. This field is GA from Kubernetes v1.30.

---

## PodDisruptionBudget (Developer Perspective)

- [ ] 320. Read a `PodDisruptionBudget` status with `kubectl get pdb -n <ns>` to understand `ALLOWED` (how many Pods may currently be disrupted) versus `DISRUPTIONS` (how many are currently disrupted), and explain how a PDB protects your application from simultaneous evictions during node drains or cluster upgrades.

---

## Generic Ephemeral Volumes

- [ ] 321. Define a generic ephemeral volume inline in a Pod spec using the `ephemeral:` volume type with an embedded `volumeClaimTemplate`; a PVC is automatically provisioned when the Pod starts and deleted when the Pod is deleted — unlike `emptyDir`, this uses a `StorageClass` and survives container restarts within the same Pod.

---

## ConfigMap & Secret Volume Update Behaviour

- [ ] 322. Understand that a ConfigMap or Secret mounted via `subPath` does **not** automatically refresh inside a running container when the source data changes — only a full directory mount (without `subPath`) benefits from the kubelet's periodic refresh (~60 s); applications using `subPath` mounts require a Pod restart (e.g., `kubectl rollout restart deployment/<name>`) to pick up changes.

---

---

# ✅ General — kubectl Efficiency & Exam Speed

## Imperative YAML Generation

- [ ] 323. Generate a Pod YAML scaffold with `kubectl run <name> --image=<image> --dry-run=client -o yaml > pod.yaml` without typing from scratch.
- [ ] 324. Generate a Deployment YAML scaffold with `kubectl create deployment <name> --image=<image> --replicas=3 --dry-run=client -o yaml`.
- [ ] 325. Generate a Service YAML scaffold with `kubectl create service clusterip <name> --tcp=80:8080 --dry-run=client -o yaml`.
- [ ] 326. Generate a ConfigMap YAML scaffold with `kubectl create configmap <name> --from-literal=key=value --dry-run=client -o yaml`.
- [ ] 327. Generate a Secret YAML scaffold with `kubectl create secret generic <name> --from-literal=password=abc --dry-run=client -o yaml`.
- [ ] 328. Generate a ServiceAccount YAML with `kubectl create serviceaccount <name> --dry-run=client -o yaml`.
- [ ] 329. Generate a Role and RoleBinding scaffold with `kubectl create role` and `kubectl create rolebinding --dry-run=client -o yaml`.
- [ ] 330. Generate a ClusterRole and ClusterRoleBinding scaffold with `kubectl create clusterrole` and `kubectl create clusterrolebinding --dry-run=client -o yaml`.
- [ ] 331. Apply a manifest from stdin using `kubectl apply -f -` with a heredoc or piped YAML to avoid writing intermediate files.

---

## kubectl Querying & Filtering

- [ ] 332. Use `kubectl get <resource> -o jsonpath='{.items[*].metadata.name}'` to extract specific fields from API list responses.
- [ ] 333. Use `kubectl get pods -o wide` to see node assignment, Pod IP, and nominated node in a single table view.
- [ ] 334. Use `kubectl get all -n <namespace>` to list all common resource types in a namespace quickly.
- [ ] 335. Use `kubectl get pods --field-selector=status.phase=Running` to filter resources by status fields.
- [ ] 336. Use `kubectl get events -n <ns> --field-selector reason=Failed` to filter events by reason for faster triage.
- [ ] 337. Use `kubectl get pods -l app=<label>` to filter resources by label selectors.

---

## kubectl Context & Namespace Management

- [ ] 338. Set the default namespace for the current context with `kubectl config set-context --current --namespace=<ns>` to avoid repeating `-n` flags.
- [ ] 339. Switch between clusters during the exam with `kubectl config use-context <context>` and always run this at the start of every question.
- [ ] 340. Verify which cluster and namespace you are operating in with `kubectl config current-context` and `kubectl config view --minify`.

---

## kubectl Editing & Patching

- [ ] 341. Use `kubectl edit <resource> <name>` to make live edits and understand when it triggers a rollout versus an immediate in-place update.
- [ ] 342. Use `kubectl patch <resource> <name> --type=merge -p '{"spec":{"replicas":5}}'` for targeted in-place updates without opening an editor.
- [ ] 343. Use `kubectl replace --force -f <file>` to delete and recreate an immutable resource (e.g., a Pod where you changed a field that cannot be patched).
- [ ] 344. Use `kubectl label` and `kubectl annotate` to add, update (`key=newval`), and remove (`key-`) labels and annotations on resources imperatively.
- [ ] 345. Use `kubectl scale deployment <name> --replicas=0` to quickly shut down all Pods in a Deployment without deleting the Deployment object.

---

## Shell Productivity & Aliases

- [ ] 346. Set shell aliases and shortcuts in `~/.bashrc` (`alias k=kubectl`, `export do='--dry-run=client -o yaml'`, `export now='--force --grace-period 0'`) and source the file immediately.
- [ ] 347. Enable `kubectl` autocompletion in the exam environment with `source <(kubectl completion bash)` and add the line to `~/.bashrc`.
- [ ] 348. Use `kubectl explain <resource> --recursive | grep -A5 <field>` to quickly find the exact YAML path of a field in a deeply nested spec.
- [ ] 349. Use `kubectl wait --for=condition=ready pod -l app=<label> --timeout=60s` to block a script until Pods reach the Ready condition.
- [ ] 350. Use `kubectl delete pod <name> --grace-period=0 --force` to immediately terminate a stuck Pod during troubleshooting.

---

## YAML Authoring Essentials

- [ ] 351. Memorize the four required top-level fields of every Kubernetes manifest: `apiVersion`, `kind`, `metadata`, and `spec`.
- [ ] 352. Memorize the `apiVersion` for the most common objects: `v1` (Pod, Service, ConfigMap, Secret, PV, PVC, SA, NS, LimitRange, ResourceQuota), `apps/v1` (Deployment, ReplicaSet, StatefulSet, DaemonSet), `batch/v1` (Job, CronJob), `networking.k8s.io/v1` (NetworkPolicy, Ingress), `rbac.authorization.k8s.io/v1` (Role, ClusterRole, RoleBinding, ClusterRoleBinding), `autoscaling/v2` (HPA), `policy/v1` (PodDisruptionBudget), `gateway.networking.k8s.io/v1` (Gateway, HTTPRoute, GatewayClass).
- [ ] 353. Understand that `spec.selector.matchLabels` in a Deployment must match `spec.template.metadata.labels` — a mismatch causes a validation error at apply time.
- [ ] 354. Know the difference between `kubectl apply` (declarative, merges changes, creates if missing) and `kubectl create` (imperative, fails if resource already exists).
- [ ] 355. Validate a manifest before applying it using `kubectl apply -f <file> --dry-run=server` to catch API-level schema and admission errors.

---

## Exam Environment & Time Management

- [ ] 356. Know that the CKA and CKAD exams use the PSI Secure Browser and require a clean desk, working webcam, and stable internet — verify hardware and environment before exam day.
- [ ] 357. Know which documentation is allowed during the exam: `kubernetes.io/docs`, `kubernetes.io/blog`, `helm.sh/docs`, `github.com/kubernetes` — practice navigating these quickly before the exam.
- [ ] 358. Practice on `killer.sh` (the two included simulator sessions) until you can complete all tasks in under 90 minutes to build a speed margin for the real exam.
- [ ] 359. On exam day, read all questions first and flag straightforward questions to answer first (maximum point-per-minute harvesting), leaving complex multi-step tasks for the end.
- [ ] 360. Always switch to the correct cluster context with `kubectl config use-context <ctx>` at the start of every question — working in the wrong cluster is the most common exam mistake.

---

## Common Exam Pitfalls

- [ ] 361. Remember that `kubectl rollout undo` is **not supported** for `StatefulSet` resources — attempting it returns an error; to roll back a StatefulSet patch `spec.template.spec.containers[].image` directly to the previous image and monitor the rolling update.
- [ ] 362. Force-delete a Pod stuck in `Terminating` state with `kubectl delete pod <name> --grace-period=0 --force`; use this only when the node is unreachable or the process is confirmed gone, as bypassing the graceful shutdown sequence can cause data corruption in stateful workloads.

---

## kubectl — kubeconfig Management

- [ ] 363. Build a kubeconfig file from scratch with `kubectl config set-cluster <name> --server=<url> --certificate-authority=<ca.crt> --embed-certs=true`, then `kubectl config set-credentials <name> --client-certificate=<cert.crt> --client-key=<key.key> --embed-certs=true`, then `kubectl config set-context <name> --cluster=<cluster> --user=<user> --namespace=<ns>`; use this when creating access credentials for a new ServiceAccount or a newly signed user certificate.


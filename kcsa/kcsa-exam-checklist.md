# KCSA Exam Checklist: 310 Items

**60 questions · 90 minutes · 75% passing score · $250 USD (one free retake) · 2-year validity**

Domain weights: Cluster Component Security 22% · Security Fundamentals 22% · Threat Model 16% · Platform Security 16% · Cloud Native Security Overview 14% · Compliance 10%

Study tip: Domains 2+3 together = 44% of the exam. Prioritize those first.

---

## Domain 1: Overview of Cloud Native Security (14%)

### The 4Cs of Cloud Native Security

- [ ]  001. Understand the 4Cs layered model: Cloud → Cluster → Container → Code
- [ ]  002. Know that each outer layer protects inner layers, but inner-layer security cannot compensate for outer-layer vulnerabilities
- [ ]  003. Understand defense in depth as applying multiple independent security controls at every layer
- [ ]  004. Know the Cloud layer responsibilities: physical security, hypervisor, network infrastructure, IAM
- [ ]  005. Know the Cluster layer responsibilities: API server access, RBAC, network policies, etcd encryption, audit logging
- [ ]  006. Know the Container layer responsibilities: image scanning, minimal base images, runtime security, security contexts
- [ ]  007. Know the Code layer responsibilities: secure coding, TLS for endpoints, dependency management, input validation

### Cloud Provider and Infrastructure Security

- [ ]  008. Understand the shared responsibility model between cloud provider and customer
- [ ]  009. Know that CSPs manage physical security, hypervisors, and managed control planes
- [ ]  010. Know that customers are responsible for workload configuration, data security, IAM policies, and network security groups
- [ ]  011. Understand Infrastructure as Code (IaC) for security-auditable, repeatable infrastructure deployments
- [ ]  012. Know key cloud security practices: encrypt at rest and in transit, audit IAM monthly, restrict SSH/API ports
- [ ]  013. Understand cloud metadata API risks (169.254.169.254) and how pods can access cloud credentials
- [ ]  014. Know VPC, security groups, and private endpoint configurations for Kubernetes clusters
- [ ]  015. Understand managed Kubernetes offerings (EKS, GKE, AKS) and their default security postures

### Security Principles and Paradigms

- [ ]  016. Understand zero trust: never trust, always verify — all communication authenticated and authorized
- [ ]  017. Know identity-based security vs. network-perimeter-based security
- [ ]  018. Understand microsegmentation of network traffic as a zero trust implementation
- [ ]  019. Know shift-left security: applying security early in the development lifecycle
- [ ]  020. Understand "Security by Design" — security as a requirement from project inception
- [ ]  021. Know DevSecOps principles: security integrated into every SDLC phase (Develop → Distribute → Deploy → Runtime)
- [ ]  022. Understand shared responsibility between Dev, Sec, and Ops teams
- [ ]  023. Know automated security gates in CI/CD pipelines
- [ ]  024. Understand immutable infrastructure and configuration drift reconciliation
- [ ]  025. Know the concept of least privilege across humans, workloads, and service accounts

### Isolation Techniques

- [ ]  026. Understand namespace-based logical isolation in Kubernetes
- [ ]  027. Know network policy-based traffic isolation between pods
- [ ]  028. Understand node isolation using taints, tolerations, and node selectors
- [ ]  029. Know container sandboxing isolation (gVisor, Kata Containers) via RuntimeClass
- [ ]  030. Understand kernel-level isolation via seccomp, AppArmor, and SELinux

### Artifact Repository and Image Security

- [ ]  031. Know the importance of using private container registries with authentication
- [ ]  032. Understand image digest pinning (`sha256`) vs. mutable tags (`:latest`)
- [ ]  033. Know how `imagePullSecrets` work for private registry access
- [ ]  034. Understand vulnerability scanning in registries (Harbor with Trivy/Clair)
- [ ]  035. Know the practice of enforcing image provenance before promotion between environments

### Workload and Application Code Security

- [ ]  036. Know OWASP secure coding guidelines and their relevance to cloud native applications
- [ ]  037. Understand Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST)
- [ ]  038. Know Software Composition Analysis (SCA) for third-party dependency scanning
- [ ]  039. Understand the importance of TLS for all exposed service endpoints
- [ ]  040. Know code review processes and dependency scanning in CI/CD pipelines

---

## Domain 2: Kubernetes Cluster Component Security (22%)

### API Server Security

- [ ]  041. Know that the kube-apiserver is the only component communicating directly with etcd
- [ ]  042. Understand the API request pipeline: Authentication → Authorization → Admission Control
- [ ]  043. Know flag `--anonymous-auth=false` to disable unauthenticated access
- [ ]  044. Know flag `--insecure-port=0` to disable the insecure HTTP port
- [ ]  045. Know flag `--secure-port=6443` as the default HTTPS API port
- [ ]  046. Know TLS configuration: `--tls-cert-file` and `--tls-private-key-file`
- [ ]  047. Know flag `--authorization-mode=RBAC,Node` (never use AlwaysAllow)
- [ ]  048. Know flag `--enable-admission-plugins=NodeRestriction,EventRateLimit,...`
- [ ]  049. Know audit logging flags: `--audit-log-path`, `--audit-policy-file`, `--audit-log-maxage`, `--audit-log-maxbackup`, `--audit-log-maxsize`
- [ ]  050. Know flag `--encryption-provider-config` for enabling etcd encryption at rest
- [ ]  051. Know kubelet TLS flags: `--kubelet-certificate-authority`, `--kubelet-client-certificate`, `--kubelet-client-key`
- [ ]  052. Know etcd TLS flags: `--etcd-cafile`, `--etcd-certfile`, `--etcd-keyfile`
- [ ]  053. Know flag `--service-account-key-file` for dedicated SA token signing keys
- [ ]  054. Understand OIDC integration flags: `--oidc-issuer-url`, `--oidc-client-id`, `--oidc-username-claim`, `--oidc-groups-claim`
- [ ]  055. Know to restrict external internet access to API server; use bastion hosts or VPN
- [ ]  056. Know to disable the Kubernetes dashboard or secure it with strong authentication
- [ ]  057. Understand feature gates and why alpha features should be disabled in production

### etcd Security

- [ ]  058. Know that etcd stores ALL cluster state — access to etcd equals root access to the cluster
- [ ]  059. Know client-to-server TLS flags: `--cert-file`, `--key-file`, `--client-cert-auth=true`, `--trusted-ca-file`
- [ ]  060. Know peer-to-peer TLS flags: `--peer-cert-file`, `--peer-key-file`, `--peer-client-cert-auth`, `--peer-trusted-ca-file`
- [ ]  061. Know that etcd should be isolated behind a firewall with only API server access
- [ ]  062. Know etcd listens on TCP port 2379 (client) and 2380 (peer)
- [ ]  063. Understand regular encrypted etcd backups using `etcdctl snapshot save`
- [ ]  064. Know the EncryptionConfiguration resource and its providers: `identity`, `aescbc`, `aesgcm`, `secretbox`, `kms`
- [ ]  065. Understand that KMS provider with envelope encryption is recommended for production
- [ ]  066. Know how to verify encryption: check for `k8s:enc:` prefix in etcd data
- [ ]  067. Know that Kubernetes Secrets are only base64-encoded by default, NOT encrypted

### Kubelet Security

- [ ]  068. Know the kubelet is the node agent managing pods and exposing a REST API
- [ ]  069. Know flag `--anonymous-auth=false` (kubelet default allows unauthenticated access)
- [ ]  070. Know flag `--authorization-mode=Webhook` (kubelet default is AlwaysAllow — dangerous)
- [ ]  071. Know flag `--read-only-port=0` to disable the unauthenticated read-only port (default 10255)
- [ ]  072. Know flag `--protect-kernel-defaults=true`
- [ ]  073. Know flag `--rotate-certificates=true` for automatic certificate rotation
- [ ]  074. Know flag `--tls-min-version=VersionTLS12` to enforce minimum TLS version
- [ ]  075. Understand NodeRestriction admission controller: limits kubelet to modify only its own Node object and bound Pods
- [ ]  076. Know that kubelets are bound to the `system:node` ClusterRole
- [ ]  077. Understand TLS bootstrapping for automatic kubelet certificate management

### Controller Manager and Scheduler

- [ ]  078. Know that kube-controller-manager runs controller loops (Node, Job, EndpointSlice, ServiceAccount controllers)
- [ ]  079. Know flag `--service-account-private-key-file` for dedicated key pair for SA token signing
- [ ]  080. Understand encrypted communication between controller manager and API server
- [ ]  081. Know that kube-scheduler assigns pods to nodes based on resource requirements, affinity, taints
- [ ]  082. Know scheduler security: encrypted communication with API server, restricted configuration access

### kube-proxy

- [ ]  083. Know kube-proxy runs as a DaemonSet managing iptables/IPVS rules for service routing
- [ ]  084. Understand that eBPF-based CNIs (Cilium) can replace kube-proxy entirely
- [ ]  085. Know kube-proxy handles TCP, UDP, and SCTP forwarding for Services

### Container Runtime

- [ ]  086. Know supported runtimes: containerd (most common), CRI-O, Docker Engine (via CRI)
- [ ]  087. Understand the Container Runtime Interface (CRI) standard API between kubelet and runtime
- [ ]  088. Know that the container runtime socket must be protected — restrict filesystem access to root
- [ ]  089. Know RuntimeClass resource for configuring different runtimes per Pod (gVisor, Kata Containers)
- [ ]  090. Understand that `runc` is the default OCI-standard runtime when no RuntimeClass is specified

### Pod Security Basics

- [ ]  091. Know SecurityContext fields: `runAsNonRoot`, `runAsUser`, `runAsGroup`, `readOnlyRootFilesystem`
- [ ]  092. Know `allowPrivilegeEscalation: false` and `privileged: false`
- [ ]  093. Know `capabilities: { drop: ["ALL"] }` and selective capability additions
- [ ]  094. Understand `automountServiceAccountToken: false` for pods that don't need API access
- [ ]  095. Know about static Pods: managed by kubelet, not API server — potential bypass risk

### Container Networking

- [ ]  096. Know that by default, all pods can communicate with all other pods (flat network model)
- [ ]  097. Understand CNI plugin responsibility: IP assignment, route configuration, network interface setup
- [ ]  098. Know CNI binary location: `/opt/cni/bin/` and configuration: `/etc/cni/net.d/`
- [ ]  099. Understand DNS-based service discovery via CoreDNS
- [ ]  100. Know Service types: ClusterIP, NodePort, LoadBalancer and their security implications

### Client Security and Storage

- [ ]  101. Know to secure kubeconfig files — they contain cluster credentials
- [ ]  102. Understand `imagePullSecrets` for authenticating to private registries
- [ ]  103. Know Secrets Store CSI Driver for injecting external secrets as mounted volumes
- [ ]  104. Know to mount secrets as volumes (preferably in-memory tmpfs) rather than environment variables
- [ ]  105. Understand bound service account tokens (time-limited, projected volumes) vs. non-expiring tokens

### Default Kubernetes Ports to Protect

- [ ]  106. Know API server: 6443
- [ ]  107. Know etcd: 2379–2380
- [ ]  108. Know kubelet authenticated: 10250; read-only: 10255 (should be disabled)
- [ ]  109. Know scheduler: 10259; controller manager: 10257

---

## Domain 3: Kubernetes Security Fundamentals (22%)

### Pod Security Standards (PSS)

- [ ]  110. Know the three PSS levels: Privileged (unrestricted), Baseline (blocks known escalations), Restricted (full hardening)
- [ ]  111. Know Baseline restrictions: disallows hostNetwork, hostPID, hostIPC, hostPath, privileged containers
- [ ]  112. Know Restricted requirements: non-root, drop ALL capabilities, seccomp RuntimeDefault, specific volume types only
- [ ]  113. Understand that PSS replaced PodSecurityPolicy (PSP), removed in Kubernetes 1.25

### Pod Security Admission (PSA)

- [ ]  114. Know the three PSA modes: enforce (reject), audit (log), warn (warning)
- [ ]  115. Know namespace label format: `pod-security.kubernetes.io/<MODE>: <LEVEL>`
- [ ]  116. Know version pinning label: `pod-security.kubernetes.io/<MODE>-version: <VERSION>`
- [ ]  117. Understand exemptions by usernames, runtimeClasses, and namespaces
- [ ]  118. Know global PSA configuration via `--admission-control-config-file` using `AdmissionConfiguration` resource

### Authentication

- [ ]  119. Know X.509 client certificate authentication via `--client-ca-file`
- [ ]  120. Know Bearer Token authentication including static token files (not recommended for production)
- [ ]  121. Know Service Account Tokens: automatically mounted, namespace-scoped
- [ ]  122. Know OIDC authentication for external identity providers (Azure AD, Google, Okta)
- [ ]  123. Know Webhook Token Authentication via `--authentication-token-webhook-config-file`
- [ ]  124. Know that anonymous requests map to `system:unauthenticated` group
- [ ]  125. Understand that Kubernetes does NOT store user objects — users are managed externally

### Authorization (RBAC)

- [ ]  126. Know Role: namespace-scoped permission rules with `apiGroups`, `resources`, `verbs`
- [ ]  127. Know ClusterRole: cluster-scoped; can grant access to cluster-scoped resources and non-resource URLs
- [ ]  128. Know RoleBinding: binds Role/ClusterRole to subjects within a namespace
- [ ]  129. Know ClusterRoleBinding: binds ClusterRole to subjects cluster-wide
- [ ]  130. Know RBAC subjects: Users, Groups, ServiceAccounts
- [ ]  131. Know the core API group (`""`) covers pods, services, secrets, configmaps, namespaces, nodes
- [ ]  132. Know named API groups: `apps`, `rbac.authorization.k8s.io`, `networking.k8s.io`, `batch`
- [ ]  133. Know standard verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, `deletecollection`
- [ ]  134. Know special verbs: `escalate`, `bind`, `impersonate`
- [ ]  135. Know dangerous subresources: `pods/exec`, `pods/attach`, `pods/portforward`, `nodes/proxy`
- [ ]  136. Know to use namespace-scoped Roles over ClusterRoles whenever possible
- [ ]  137. Know to avoid wildcards (`*`) in apiGroups, resources, and verbs
- [ ]  138. Know that `system:masters` group bypasses all RBAC — never add regular users to it
- [ ]  139. Know `kubectl auth can-i --as=<user>` for permission testing
- [ ]  140. Understand Aggregated ClusterRoles that combine multiple ClusterRoles via label selectors
- [ ]  141. Know other authorization modes: ABAC, Webhook, Node, AlwaysAllow/AlwaysDeny

### Secrets

- [ ]  142. Know that Kubernetes Secrets are stored in etcd as base64-encoded values (not encrypted by default)
- [ ]  143. Know Secret types: `Opaque`, `kubernetes.io/tls`, `kubernetes.io/dockerconfigjson`, `kubernetes.io/service-account-token`
- [ ]  144. Know Secrets are sent to nodes only when a Pod requires them and stored as tmpfs (RAM-backed)
- [ ]  145. Know to prefer volume mounts over environment variables for secret delivery (env vars can leak in logs)
- [ ]  146. Know `kubernetes.io/enforce-mountable-secrets: "true"` annotation restricts which secrets a SA can mount
- [ ]  147. Understand encryption at rest via `EncryptionConfiguration` and `--encryption-provider-config`
- [ ]  148. Know encryption providers: `identity` (none), `aescbc`, `aesgcm`, `secretbox`, `kms` (strongest)
- [ ]  149. Know that managed Kubernetes (AKS, GKE, EKS) encrypts etcd at rest by default
- [ ]  150. Know `immutable: true` field on Secrets for compliance environments

### Isolation and Segmentation

- [ ]  151. Understand namespace isolation for logical workload separation
- [ ]  152. Know ResourceQuotas for limiting resource consumption per namespace
- [ ]  153. Know LimitRanges for setting default and maximum resource limits per container/pod
- [ ]  154. Understand network policy-based segmentation between namespaces and pods
- [ ]  155. Know node isolation via taints, tolerations, and dedicated node pools

### Audit Logging

- [ ]  156. Know audit log stages: RequestReceived, ResponseStarted, ResponseComplete, Panic
- [ ]  157. Know audit levels: None, Metadata, Request, RequestResponse
- [ ]  158. Know audit policy resource (`audit.k8s.io/v1` Kind: Policy) — rules evaluated in order, first match wins
- [ ]  159. Know audit backends: Log Backend (local filesystem) and Webhook Backend (remote HTTP API)
- [ ]  160. Know best practices: log Secrets at Metadata level, RBAC changes at RequestResponse, skip health checks
- [ ]  161. Understand cloud-managed audit logging: EKS → CloudWatch, GKE → Cloud Logging, AKS → Azure Monitor
- [ ]  162. Know log forwarding tools: Fluentd, Fluent Bit, Filebeat to centralized logging (ELK, Splunk, Loki)
- [ ]  163. Know security monitoring alerts: unauthorized access, RBAC changes, secret access, pod exec, excessive 403 errors

### Network Policy

- [ ]  164. Know NetworkPolicy is a namespaced resource in `networking.k8s.io/v1`
- [ ]  165. Know that network policies act as L3/L4 firewalls at the pod level using label selectors
- [ ]  166. Know policies work additively (union) — if any policy allows traffic, it's permitted
- [ ]  167. Know the default-deny-all pattern: `podSelector: {}` with empty ingress/egress
- [ ]  168. Know policy components: `podSelector`, `policyTypes`, `ingress.from`, `egress.to`, `ports`
- [ ]  169. Know selector types: `podSelector`, `namespaceSelector`, `ipBlock` (with CIDR and `except`)
- [ ]  170. Know that network policies only work if the CNI plugin supports them (Flannel does NOT)
- [ ]  171. Understand the whitelist approach: start with default-deny, then explicitly allow needed traffic
- [ ]  172. Know to secure egress to prevent data exfiltration

---

## Domain 4: Kubernetes Threat Model (16%)

### Trust Boundaries and Data Flow

- [ ]  173. Know cluster trust boundary: between external network and cluster network
- [ ]  174. Know node trust boundary: between control plane and worker nodes
- [ ]  175. Know namespace trust boundary: between different namespaces
- [ ]  176. Know pod trust boundary: between container and host kernel
- [ ]  177. Understand critical data flows: API server ↔ etcd, kubelet ↔ API server, pod-to-pod, external-to-ingress

### STRIDE Applied to Kubernetes

- [ ]  178. Spoofing: stolen service account tokens, compromised kubeconfig, cloud credential theft
- [ ]  179. Tampering: altered container images, etcd data modification, CoreDNS poisoning, admission controller manipulation
- [ ]  180. Repudiation: clearing audit/container logs, denying actions performed
- [ ]  181. Information Disclosure: base64-decoded secrets, etcd data exposure, environment variable leaks, metadata API access
- [ ]  182. Denial of Service: API server overload, resource exhaustion, fork bombs in containers
- [ ]  183. Elevation of Privilege: container escape, privileged containers, cluster-admin binding, writable hostPath mounts

### Microsoft Threat Matrix for Kubernetes

- [ ]  184. Know Initial Access techniques: compromised images, exposed dashboard, kubeconfig theft, application vulnerability
- [ ]  185. Know Execution techniques: exec into container, new container creation, application exploit (RCE), sidecar injection
- [ ]  186. Know Persistence techniques: backdoor container, writable hostPath, CronJob, malicious admission controller, static pods
- [ ]  187. Know Privilege Escalation techniques: privileged container, cluster-admin binding, writable hostPath, cloud resource access
- [ ]  188. Know Defense Evasion techniques: clearing container logs, deleting K8s events, pod name similarity
- [ ]  189. Know Credential Access techniques: listing K8s secrets, container service account, metadata API, app credentials in config files
- [ ]  190. Know Discovery techniques: accessing API server, kubelet API, network mapping, instance metadata API
- [ ]  191. Know Lateral Movement techniques: cluster internal networking, CoreDNS poisoning, ARP poisoning, cloud resource access
- [ ]  192. Know Impact techniques: data destruction, resource hijacking (cryptomining), denial of service

### Common Attack Vectors

- [ ]  193. Know compromised container images from untrusted registries
- [ ]  194. Know exposed Kubernetes dashboard or API server without authentication
- [ ]  195. Know stolen or compromised kubeconfig files
- [ ]  196. Know application vulnerabilities: RCE, SSRF leading to cluster compromise
- [ ]  197. Know stolen service account tokens for API access
- [ ]  198. Know unauthenticated etcd access as complete cluster takeover
- [ ]  199. Know container escape via privileged mode or capabilities
- [ ]  200. Know cloud metadata API access (169.254.169.254) for credential theft
- [ ]  201. Understand BishopFox "Bad Pods" research cataloging pod privilege escalation paths

### Persistence and Denial of Service

- [ ]  202. Know how attackers use CronJobs for persistent access
- [ ]  203. Know how writable hostPath mounts enable host filesystem manipulation
- [ ]  204. Know how malicious admission controllers can intercept all API requests
- [ ]  205. Know how resource exhaustion attacks work without ResourceQuotas and LimitRanges
- [ ]  206. Know rate limiting on the API server (`EventRateLimit` admission controller)

### Privilege Escalation Paths

- [ ]  207. Know `privileged: true` gives full host access
- [ ]  208. Know `hostPID: true` shares host process namespace
- [ ]  209. Know `hostNetwork: true` shares host network namespace
- [ ]  210. Know `hostIPC: true` shares host IPC namespace
- [ ]  211. Know dangerous capabilities: `CAP_SYS_ADMIN`, `CAP_NET_RAW`, `CAP_SYS_PTRACE`
- [ ]  212. Know `nodes/proxy` subresource bypasses audit logging and admission control

---

## Domain 5: Platform Security (16%)

### Supply Chain Security

- [ ]  213. Know Trivy: comprehensive scanner for images, filesystems, IaC, Kubernetes configs, SBOMs
- [ ]  214. Know Trivy CLI: `trivy image <name>`, `--severity CRITICAL,HIGH --exit-code 1` for CI/CD gates
- [ ]  215. Know Grype: vulnerability scanner for images and SBOMs; powered by Syft
- [ ]  216. Know Clair: API-driven, layer-by-layer image scanner; integrates with Harbor and Quay
- [ ]  217. Know Cosign (Sigstore): signs and verifies container images; supports keyless signing via OIDC
- [ ]  218. Know Sigstore ecosystem: Fulcio (CA), Rekor (transparency log), Cosign (CLI)
- [ ]  219. Know Notary/Notation: CNCF project for signing OCI artifacts (Notary v2)
- [ ]  220. Know Sigstore Policy Controller: admission controller verifying Cosign signatures before pod admission
- [ ]  221. Know Connaisseur: admission controller supporting DCT/Notary and Cosign verification

### SBOMs (Software Bill of Materials)

- [ ]  222. Know SBOM formats: SPDX (Linux Foundation) and CycloneDX (OWASP)
- [ ]  223. Know Syft: primary SBOM generator; outputs SPDX or CycloneDX
- [ ]  224. Understand SBOMs for vulnerability response (e.g., quickly checking for Log4Shell)
- [ ]  225. Know regulatory mandates: US Executive Order 14028, EU Cyber Resilience Act require SBOMs
- [ ]  226. Know to sign SBOMs or embed them in signed attestations to prevent spoofing

### SLSA Framework and in-toto

- [ ]  227. Know SLSA levels: L1 (documented provenance), L2 (signed provenance), L3 (verified source + isolated builds), L4 (hermetic/reproducible builds)
- [ ]  228. Know provenance attestations record: build platform, source repository, dependencies, workflow
- [ ]  229. Know in-toto: framework for securing supply chain integrity with layouts and links
- [ ]  230. Know DSSE (Dead Simple Signing Envelope): standard format for signing in-toto statements

### Image Repository Security

- [ ]  231. Know Harbor: open-source registry with built-in vulnerability scanning
- [ ]  232. Know cloud registries: Docker Hub, AWS ECR, GCR, ACR, Quay
- [ ]  233. Know to reference images by sha256 digest (immutable) rather than mutable tags
- [ ]  234. Know `AlwaysPullImages` admission controller forces image pulls to verify authorization

### Dockerfile and Base Image Hardening

- [ ]  235. Know distroless images: no shell, no package manager, minimal attack surface
- [ ]  236. Know Alpine Linux: ~5MB base image with significantly smaller surface
- [ ]  237. Know scratch: empty container image for fully static binaries
- [ ]  238. Know multi-stage builds: separate build environment from runtime image
- [ ]  239. Know Dockerfile rules: `USER <non-root>`, `COPY` over `ADD`, never store secrets in layers
- [ ]  240. Know hadolint for static Dockerfile analysis

### Observability

- [ ]  241. Know Falco (CNCF Graduated): runtime security monitoring via eBPF/kernel modules
- [ ]  242. Know Falco detects: shell spawning, file access, network anomalies, container escapes, privilege escalation
- [ ]  243. Know Falco deployment: DaemonSet on every node; rules in `/etc/falco/`
- [ ]  244. Know Falcosidekick: fan-out alerts to Slack, PagerDuty, SIEM, Prometheus, Grafana (50+ outputs)
- [ ]  245. Know Tetragon: eBPF-based runtime security tool from the Cilium project
- [ ]  246. Know KubeArmor: runtime security using eBPF, AppArmor, SELinux for process/file/network monitoring
- [ ]  247. Know Prometheus metrics for security: API request rates, auth failures, authorization denials
- [ ]  248. Know centralized logging: Fluentd/Fluent Bit → Elasticsearch/Loki/Splunk
- [ ]  249. Know OpenTelemetry for correlating security alerts with traces and metrics
- [ ]  250. Understand incident response: detect via Falco → correlate events → isolate workloads → preserve evidence

### Service Mesh

- [ ]  251. Know service mesh architecture: control plane + data plane (sidecar/sidecarless proxies)
- [ ]  252. Know Istio: Istiod control plane, Envoy proxies, mTLS modes (PERMISSIVE vs. STRICT)
- [ ]  253. Know Istio CRDs: PeerAuthentication, AuthorizationPolicy, VirtualService, DestinationRule
- [ ]  254. Know Istio Ambient Mode: sidecarless architecture using ztunnel for L4, waypoint proxies for L7
- [ ]  255. Know Linkerd: Rust micro-proxy, mTLS enabled by default, CNCF graduated, lower resource consumption
- [ ]  256. Know Cilium Service Mesh: built into CNI, sidecarless, Gateway API support
- [ ]  257. Understand mTLS: mutual TLS authenticates both client and server; prevents MITM attacks
- [ ]  258. Know certificate rotation: Istio/Linkerd identity certificates expire ~24 hours, rotated automatically

### PKI (Public Key Infrastructure)

- [ ]  259. Know Kubernetes PKI: cluster CA signs certificates for all components
- [ ]  260. Know components requiring certificates: API server, kubelet, etcd, controller manager, scheduler, front-proxy
- [ ]  261. Know cert-manager: Kubernetes-native certificate lifecycle management
- [ ]  262. Understand certificate rotation for ongoing security

### Connectivity

- [ ]  263. Know Ingress controllers (NGINX, Traefik, HAProxy) for external traffic management
- [ ]  264. Know Gateway API as the modern replacement for Ingress resources
- [ ]  265. Know to block cloud metadata API access from pods unless explicitly required
- [ ]  266. Know to separate etcd network from general cluster network

### Admission Control

- [ ]  267. Know Mutating admission webhooks modify requests before processing
- [ ]  268. Know Validating admission webhooks reject non-compliant requests
- [ ]  269. Know processing order: mutating webhooks run first, then validating webhooks
- [ ]  270. Know built-in controllers: NodeRestriction, AlwaysPullImages, PodSecurity, EventRateLimit, ImagePolicyWebhook, ResourceQuota, LimitRanger
- [ ]  271. Know OPA Gatekeeper: Rego-based policy engine using ConstraintTemplate and Constraint CRDs
- [ ]  272. Know Kyverno: YAML-native policy engine with ClusterPolicy/Policy CRDs; can validate, mutate, generate, and verify images
- [ ]  273. Know ValidatingAdmissionPolicy: native Kubernetes declarative policy (newer feature)

### Runtime Security Mechanisms

- [ ]  274. Know seccomp profiles: `Unconfined`, `RuntimeDefault`, `Localhost`; configured via `securityContext.seccompProfile`
- [ ]  275. Know kubelet flag `--seccomp-default` enables RuntimeDefault for all pods
- [ ]  276. Know Security Profiles Operator (SPO): manages seccomp profiles as CRDs (`SeccompProfile`, `ProfileBinding`)
- [ ]  277. Know SPO can record system calls and generate least-privilege profiles automatically
- [ ]  278. Know AppArmor: MAC module; profile types `enforce`, `complain`, `unconfined`; since K8s 1.30 native in securityContext
- [ ]  279. Know SELinux: label-based MAC system; configured via `securityContext.seLinuxOptions`
- [ ]  280. Know gVisor: user-space kernel intercepting syscalls; RuntimeClass handler `runsc`
- [ ]  281. Know Kata Containers: lightweight VMs per pod; handlers `kata`, `kata-qemu`; requires KVM support
- [ ]  282. Know `readOnlyRootFilesystem: true` prevents malware from writing to container filesystem
- [ ]  283. Know to use `emptyDir` volumes for temporary writable directories when root filesystem is read-only

### External Secrets Management

- [ ]  284. Know HashiCorp Vault: dynamic secrets, encryption-as-a-service, PKI management, audit logging
- [ ]  285. Know Vault integration patterns: Agent Sidecar Injector, Secrets Store CSI Driver, External Secrets Operator
- [ ]  286. Know Secrets Store CSI Driver: mounts secrets from external stores as volumes; `SecretProviderClass` CRD
- [ ]  287. Know External Secrets Operator (ESO): syncs external secrets to K8s Secrets; `ExternalSecret` and `SecretStore` CRDs
- [ ]  288. Know Sealed Secrets (Bitnami): asymmetric encryption for GitOps-safe secrets; `kubeseal` CLI

---

## Domain 6: Compliance and Security Frameworks (10%)

### Compliance Frameworks

- [ ]  289. Know CIS Kubernetes Benchmark: comprehensive security configuration recommendations; Level 1 (basic) and Level 2 (deep)
- [ ]  290. Know CIS Benchmark sections: control plane, worker nodes, control plane configuration, policies, managed services
- [ ]  291. Know cloud-specific CIS benchmarks: EKS, GKE, AKS
- [ ]  292. Know SOC 2 trust service criteria: security, availability, processing integrity, confidentiality, privacy
- [ ]  293. Know PCI-DSS: payment card industry standard requiring network segmentation, encryption, logging
- [ ]  294. Know HIPAA: healthcare data protection requiring encryption, access controls, audit trails
- [ ]  295. Know NIST SP 800-53: security and privacy controls for government workloads
- [ ]  296. Know GDPR: EU data protection regulation; relevant for data handling in cloud native systems
- [ ]  297. Know the NSA/CISA Kubernetes Hardening Guide as a government reference

### Threat Modeling Frameworks

- [ ]  298. Know STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- [ ]  299. Know MITRE ATT&CK for Containers and the Microsoft Kubernetes Threat Matrix
- [ ]  300. Know DREAD (Damage, Reproducibility, Exploitability, Affected Users, Discoverability), PASTA, and OCTAVE

### Supply Chain Compliance

- [ ]  301. Know SLSA framework requirements for software artifact integrity (Levels 1–4)
- [ ]  302. Know SBOM regulatory mandates: US Executive Order 14028, EU Cyber Resilience Act
- [ ]  303. Know OpenSSF Scorecards: rates open-source projects on security practices

### Automation and Tooling

- [ ]  304. Know kube-bench (Aqua Security): runs CIS Benchmark checks as a K8s Job or binary; PASS/FAIL/WARN output
- [ ]  305. Know Kubescape (ARMO): scans against CIS, NSA, MITRE ATT&CK frameworks; assisted remediation
- [ ]  306. Know Trivy Operator: Kubernetes-native continuous scanning for vulnerabilities and compliance
- [ ]  307. Know Checkov: static analysis for IaC/Kubernetes manifests
- [ ]  308. Know KubeLinter: static analysis of Kubernetes YAML for security anti-patterns
- [ ]  309. Know Polaris: validates Kubernetes best practices including security configurations
- [ ]  310. Know kube-hunter: penetration testing tool for Kubernetes clusters

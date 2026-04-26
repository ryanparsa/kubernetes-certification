# KCSA — Kubernetes and Cloud Native Security Associate

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
| Overview of Cloud Native Security | 14% |
| Kubernetes Cluster Component Security | 22% |
| Kubernetes Security Fundamentals | 22% |
| Kubernetes Threat Model | 16% |
| Platform Security | 16% |
| Compliance and Security Frameworks | 10% |

## Domain Topics

### Overview of Cloud Native Security (14%)
- The 4 Cs of cloud native security: Cloud, Cluster, Container, Code
- Defense in depth: layering controls at infrastructure, cluster, workload, and application levels
- Principle of least privilege applied to Kubernetes (RBAC, ServiceAccounts, NetworkPolicies)
- Shift-left security: integrating security into CI/CD pipelines (SAST, image scanning, policy checks)
- Supply chain threats: compromised base images, malicious dependencies, build environment attacks
- Zero-trust networking: assume breach, verify explicitly, mutual TLS between services
- Shared responsibility model in managed Kubernetes (cloud provider vs operator vs developer)

### Kubernetes Cluster Component Security (22%)
- kube-apiserver: authentication modes (`--client-ca-file`, OIDC, webhook), authorization modes (`RBAC`, `Node`), `--anonymous-auth=false`
- etcd: `--client-cert-auth=true`, `--peer-trusted-ca-file`, encryption at rest (`EncryptionConfiguration`), firewall port 2379
- kubelet: `--anonymous-auth=false`, `--authorization-mode=Webhook`, `--read-only-port=0`, `/var/lib/kubelet/config.yaml`
- kube-scheduler / controller-manager: `--profiling=false`, `--bind-address=127.0.0.1`
- Static pod manifests: `/etc/kubernetes/manifests/`; verifying component flags
- Kubernetes PKI: `/etc/kubernetes/pki/`; certificate purposes (CA, API server, etcd, kubelet, front-proxy)
- `kubeadm certs check-expiration`, `kubeadm certs renew`
- Admission controllers: `NodeRestriction`, `PodSecurity`, `LimitRanger`, validating vs mutating webhooks
- Audit logging: policy levels (`None` / `Metadata` / `Request` / `RequestResponse`), `--audit-policy-file`, `--audit-log-path`

### Kubernetes Security Fundamentals (22%)
- RBAC: Role, RoleBinding, ClusterRole, ClusterRoleBinding; verbs and resources; `kubectl auth can-i`
- ServiceAccount: `automountServiceAccountToken: false`; dedicated SA per workload; projected token volumes
- Pod Security Admission (PSA): `privileged` / `baseline` / `restricted` levels; `enforce` / `warn` / `audit` modes
- SecurityContext: `runAsNonRoot`, `runAsUser`, `fsGroup`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem`
- Capabilities: `drop ALL`, add only required (e.g., `NET_BIND_SERVICE`)
- Avoiding `hostPID`, `hostIPC`, `hostNetwork`
- Secrets: base64 encoding is not encryption; prefer volume mounts over env vars; encryption at rest
- NetworkPolicy: default-deny ingress/egress; `podSelector`, `namespaceSelector`, `ipBlock`
- Image security: digest pinning, trusted registries, `imagePullPolicy: Always`
- Namespace isolation: resource quotas, LimitRange, network segmentation

### Kubernetes Threat Model (16%)
- Attack vectors: compromised container, misconfigured RBAC, exposed API server, node compromise
- Container escape techniques: privileged containers, `hostPath` mounts, `hostPID` abuse
- Lateral movement: leveraging ServiceAccount tokens, accessing the metadata API
- Privilege escalation: escalating from pod to node, RBAC wildcards, `cluster-admin` misuse
- Persistence mechanisms: backdoor containers, CronJob abuse, webhook injection
- Denial of service: resource exhaustion without limits, fork bombs
- Data exfiltration: reading Secrets, accessing etcd directly
- MITRE ATT&CK for Containers: initial access, execution, persistence, privilege escalation, defense evasion, credential access, discovery, lateral movement, impact

### Platform Security (16%)
- Supply chain security: `trivy image` for CVE scanning; OPA/Gatekeeper and Kyverno for policy enforcement
- Allowed registries: admission webhook to block untrusted image sources
- Image signing: `cosign sign / verify`; admission enforcement of signed images
- Runtime security with Falco: rules file (`/etc/falco/falco_rules.yaml`), condition syntax, priority levels, output fields
- seccomp: `RuntimeDefault` vs `Localhost` profiles; `securityContext.seccompProfile`
- AppArmor: profile loading (`apparmor_parser`), applying to pods via annotation
- Service mesh mTLS: Istio/Linkerd providing mutual TLS, traffic encryption between pods
- Ingress TLS termination and re-encryption
- Protecting the node metadata API: NetworkPolicy egress rules to block `169.254.169.254`

### Compliance and Security Frameworks (10%)
- CIS Kubernetes Benchmark: control areas, `kube-bench` tool, PASS/FAIL/WARN output
- NIST SP 800-190: application container security guide
- PCI DSS, SOC 2, ISO 27001 — relevance to container and Kubernetes environments
- Pod Security Standards (PSS): baseline vs restricted profiles; migration from PodSecurityPolicy
- OWASP Top 10 for containers and Kubernetes
- Incident response: detection (Falco alerts, audit logs), containment (cordon node, delete pod), investigation (forensics), remediation
- Security scanning in CI/CD: integrating `trivy`, policy checks (OPA/Kyverno) as pipeline gates

# CKS -- Certified Kubernetes Security Specialist

## Exam Overview

| | |
|---|---|
| **Format** | Performance-based (hands-on CLI tasks) |
| **Duration** | 2 hours |
| **Passing score** | 67% |
| **Prerequisite** | Active CKA certification |
| **Cost** | $395 USD (includes one free retake) |
| **Validity** | 3 years |
| **Allowed docs** | kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs, github.com/kubernetes, aquasecurity.github.io/trivy, falco.org/docs |
| **Official curriculum** | https://github.com/cncf/curriculum |

## Domains & Weights

| Domain | Weight |
|---|---|
| Cluster Setup | 10% |
| Cluster Hardening | 15% |
| System Hardening | 15% |
| Minimize Microservice Vulnerabilities | 20% |
| Supply Chain Security | 20% |
| Monitoring, Logging and Runtime Security | 20% |

## Domain Topics

### Cluster Setup (10%)
- Network policies: default-deny ingress/egress per namespace; combining `podSelector` + `namespaceSelector`
- Egress restrictions: blocking metadata API (`169.254.169.254`), allowing only specific CIDRs
- Ingress TLS: certificate/key Secret, `tls:` block in Ingress spec
- Verifying effective policies with `kubectl describe networkpolicy`
- kube-bench: running CIS benchmark checks, reading output, understanding PASS/FAIL/WARN
- Protecting the node metadata API via NetworkPolicy

### Cluster Hardening (15%)
- RBAC: least-privilege Roles/ClusterRoles; removing over-permissive default bindings
- ServiceAccount: `automountServiceAccountToken: false`; dedicated SA per workload
- Admission controllers: enabling/disabling via `--enable-admission-plugins`; `NodeRestriction`
- API server security: `--anonymous-auth=false`, `--authorization-mode`, `--audit-policy-file`
- Restricting access to the API server; rotating certificates with `kubeadm certs renew`
- Component hardening:
  - kube-apiserver: `--profiling=false`, `--tls-min-version`, `--request-timeout`
  - kube-scheduler / controller-manager: `--profiling=false`, `--bind-address=127.0.0.1`
  - Verifying flags: `cat /etc/kubernetes/manifests/<component>.yaml`

### System Hardening (15%)
- Reducing host OS attack surface: removing unnecessary packages and services
- AppArmor: profile location (`/etc/apparmor.d/`), loading profiles (`apparmor_parser`)
  - Applying to a pod: `container.apparmor.security.beta.kubernetes.io/<container>: localhost/<profile>`
- Seccomp: `RuntimeDefault` vs `Localhost` profiles; `securityContext.seccompProfile`
- Restricting syscalls: seccomp profiles, `capabilities: drop ALL`
- etcd hardening: `--client-cert-auth=true`, `--peer-trusted-ca-file`, firewall port 2379
- kubelet hardening: `--anonymous-auth=false`, `--authorization-mode=Webhook`, `--read-only-port=0`
  - `/var/lib/kubelet/config.yaml` equivalents for the above flags

### Minimize Microservice Vulnerabilities (20%)
- Pod Security Admission (PSA): `privileged` / `baseline` / `restricted` levels
  - `kubectl label namespace <ns> pod-security.kubernetes.io/enforce=restricted`
  - `enforce`, `warn`, `audit` modes
- SecurityContext: `runAsNonRoot`, `runAsUser`, `fsGroup`, `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true` -- `emptyDir` volumes for paths that need writes
- `capabilities: drop ALL`, add only what's required
- Avoiding `hostPID`, `hostIPC`, `hostNetwork` unless explicitly required
- Secrets management:
  - etcd encryption at rest: `EncryptionConfiguration`, `--encryption-provider-config` on kube-apiserver
  - Secret types: `Opaque`, `kubernetes.io/tls`, `kubernetes.io/dockerconfigjson`
  - Verifying encryption: `etcdctl get /registry/secrets/<ns>/<name> | hexdump`
  - Volume mount vs env var injection (prefer mounts -- env vars leak into child processes)
- OPA/Gatekeeper and Kyverno: constraint templates, enforcing policies cluster-wide
- mTLS concept: service mesh (Istio/Linkerd) providing mutual TLS between pods

### Supply Chain Security (20%)
- Image scanning: `trivy image <image>` -- reading CVE severity output, identifying critical/high vulns
- Allowed registries: OPA/Gatekeeper or Kyverno policies to block images from untrusted sources
- Image digest pinning: `image: nginx@sha256:...` vs tag (tags are mutable)
- Dockerfile best practices: non-root `USER`, minimal base image, no build tools in final stage
- Signed images: `cosign verify` basics; admission webhook to enforce signature checks
- SBOM (Software Bill of Materials) concepts

### Monitoring, Logging and Runtime Security (20%)
- Audit policy: levels (`None` / `Metadata` / `Request` / `RequestResponse`), stages (`RequestReceived`, `ResponseComplete`)
  - Omit Secrets request bodies; log `exec` at `RequestResponse`
  - `--audit-policy-file` and `--audit-log-path` on kube-apiserver static pod
  - Reading audit log entries: `user`, `verb`, `resource`, `responseStatus`
- Falco:
  - Rules file: `/etc/falco/falco_rules.yaml` (default) and `/etc/falco/falco_rules.local.yaml` (custom)
  - Rule structure: `rule`, `condition`, `output`, `priority`
  - Common built-in rules: shell spawned in container, sensitive file access, network tool executed
  - `systemctl status falco`; reading Falco alerts from syslog or file output
- Immutable containers: `readOnlyRootFilesystem: true` + `emptyDir` for writable paths
- Runtime threat detection: anomalous process execution, unexpected network connections
- Incident response: identifying the affected pod/node, preserving evidence, isolating the workload

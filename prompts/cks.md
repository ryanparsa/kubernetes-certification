Topic scope: CKS-specific. Combine with base.md for a full session.

COVERAGE — rotate through all areas:

Cluster hardening
- RBAC: least-privilege Roles/ClusterRoles, removing default cluster-admin bindings
- ServiceAccount: automountServiceAccountToken: false, dedicated SAs per workload
- Admission controllers: enabling/disabling via --enable-admission-plugins, NodeRestriction
- API server security: --anonymous-auth=false, --authorization-mode, audit logging flags
- kubeadm: restricting access to the API server, rotating certificates

Network policies
- Default-deny ingress/egress policies per namespace
- Combining podSelector + namespaceSelector for fine-grained rules
- Verifying effective policies with kubectl describe networkpolicy
- Egress restrictions: blocking metadata API (169.254.169.254), allowing only specific CIDRs

Pod security
- securityContext: runAsNonRoot, runAsUser, fsGroup, allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true — volumes needed when files must be written
- capabilities: drop ALL, add only what's required
- Pod Security Admission (PSA): enforce/warn/audit labels on namespaces
  - privileged / baseline / restricted levels
  - kubectl label namespace <ns> pod-security.kubernetes.io/enforce=restricted
- Avoiding hostPID, hostIPC, hostNetwork unless explicitly required

Secrets management
- etcd encryption at rest: EncryptionConfiguration, --encryption-provider-config flag on kube-apiserver
- Secret types: Opaque, kubernetes.io/tls, kubernetes.io/dockerconfigjson
- Avoiding secrets in env vars when volume mounts are safer
- Verifying encryption: etcdctl get /registry/secrets/<ns>/<name> | hexdump

Supply chain security
- Image scanning: trivy image <image>, reading CVE severity output
- Allowed registries: OPA/Gatekeeper or Kyverno policies to restrict image sources
- Image digest pinning vs tag pinning (sha256:... vs :latest)
- Dockerfile best practices: non-root USER, minimal base image, no unnecessary packages
- Signed images: cosign verify basics

Runtime security
- Falco: rules syntax, output fields, where rules live (/etc/falco/falco_rules.yaml)
- Identifying and responding to a Falco alert
- Immutable containers: readOnlyRootFilesystem + emptyDir for writable paths
- seccomp profiles: RuntimeDefault vs Localhost, annotation vs securityContext.seccompProfile
- AppArmor: profile location (/etc/apparmor.d/), kubectl annotate pod, container.apparmor.security.beta.kubernetes.io/<container>

Auditing
- Audit policy: levels (None / Metadata / Request / RequestResponse), stages
- Writing a minimal audit policy: omit Secrets request bodies, log pod exec at RequestResponse
- --audit-policy-file and --audit-log-path flags on kube-apiserver static pod
- Reading audit log entries: user, verb, resource, responseStatus

Cluster component hardening
- kube-apiserver: --profiling=false, --request-timeout, --tls-min-version
- etcd: --peer-trusted-ca-file, --client-cert-auth=true, firewall to port 2379
- kubelet: --anonymous-auth=false, --authorization-mode=Webhook, --read-only-port=0
  - /var/lib/kubelet/config.yaml equivalents for the above
- kube-scheduler / controller-manager: --profiling=false, --bind-address=127.0.0.1
- Verifying component flags: cat /etc/kubernetes/manifests/<component>.yaml

# Cloud Native Security

Security is layered — each outer layer protects the inner layers, but inner-layer security
cannot compensate for outer-layer vulnerabilities. Defence-in-depth applies across Cloud,
Cluster, Container, and Code.

---

## 1. The 4Cs of Cloud Native Security

```
Cloud → Cluster → Container → Code
```

| Layer | Responsibilities |
|-------|-----------------|
| **Cloud** | Physical security, hypervisor, network infrastructure, IAM, managed control plane |
| **Cluster** | API server access, RBAC, NetworkPolicy, etcd encryption, audit logging |
| **Container** | Image scanning, minimal base images, runtime security, SecurityContext |
| **Code** | Secure coding, TLS for endpoints, dependency management, input validation |

Shared responsibility model: the cloud provider owns the Cloud layer for managed Kubernetes
(EKS, GKE, AKS). Customers own everything from Cluster inward.

---

## 2. Pod Security Architecture (5 Layers)

Think of pod security as an onion across the pod lifecycle — each layer adds an independent
control.

### Layer 1 — Supply Chain (Build Phase)

Security begins before the pod exists. The goal: ensure the image is not compromised.

- **Vulnerability scanning:** Trivy, Grype scan images in CI/CD for CVEs
- **Image signing:** Cosign/Sigstore signs images; admission controllers verify signatures before deployment
- **SBOM:** Syft generates a bill of materials (SPDX or CycloneDX) for rapid CVE response (e.g., Log4Shell)

### Layer 2 — Admission Control (Deploy Phase)

The API server gatekeeper. The cluster decides whether the pod meets security standards
before it starts.

- **Built-in:** Pod Security Admission (PSA) enforces PSS levels (`privileged` / `baseline` / `restricted`) per namespace
- **Policy engines:** Kyverno or OPA Gatekeeper as validating/mutating webhooks for complex rules (e.g., "images must come from internal registry")

### Layer 3 — Runtime Security (Execution Phase)

The pod is running. Watch OS-level behavior to detect or prevent escape and abuse.

- **Preventive:** seccomp (filter syscalls), AppArmor/SELinux (MAC — restrict file and process access)
- **Detective:** Falco (eBPF-based runtime monitor, alerts on shell spawning, file access, privilege escalation), Tetragon (eBPF with active enforcement)

### Layer 4 — Network Security

Zero trust: a pod should not talk to anything it doesn't need to.

- **NetworkPolicy:** L3/L4 firewall at pod level; start with default-deny-all, whitelist explicitly
- **Cilium:** eBPF-based CNI with FQDN-aware policy and kernel-level enforcement
- **Service mesh:** Istio or Linkerd for automatic mTLS between all pods

### Layer 5 — Identity & Access Management

What is this pod, and what can it access?

- **ServiceAccounts + RBAC:** Least privilege API access; `automountServiceAccountToken: false` for pods that don't need it
- **Workload identity (SPIFFE/SPIRE):** Short-lived cryptographic identities for pod-to-service auth without hardcoded credentials

---

## 3. Hardened Deployment Reference

Full example — namespace with PSA restricted + secure Deployment + NetworkPolicy + RBAC.

### Namespace (PSA enforce: restricted)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

### Deployment (all security controls applied)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: secure-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 101
        runAsGroup: 101
        fsGroup: 101
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: nginxinc/nginx-unprivileged:1.25.4-alpine
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: [ALL]
          appArmorProfile:
            type: RuntimeDefault
        resources:
          requests: { cpu: 100m, memory: 128Mi }
          limits:   { cpu: 500m, memory: 256Mi }
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir:
          sizeLimit: 64Mi
```

### NetworkPolicy (default-deny + targeted allow)

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: secure-ns
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
# Allow ingress only from ingress controller
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-controller
  namespace: secure-ns
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
      podSelector:
        matchLabels:
          app.kubernetes.io/name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
```

### ServiceAccount + RBAC (minimal permissions)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secure-app-sa
  namespace: secure-ns
  annotations:
    automountServiceAccountToken: "false"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secure-app-role
  namespace: secure-ns
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: secure-app-rolebinding
  namespace: secure-ns
subjects:
- kind: ServiceAccount
  name: secure-app-sa
  namespace: secure-ns
roleRef:
  kind: Role
  name: secure-app-role
  apiGroup: rbac.authorization.k8s.io
```

### ResourceQuota + LimitRange (DoS prevention)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: secure-ns-quota
  namespace: secure-ns
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 2Gi
    limits.cpu: "4"
    limits.memory: 4Gi
    pods: "10"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: secure-ns-limits
  namespace: secure-ns
spec:
  limits:
  - type: Container
    default:      { cpu: 500m, memory: 512Mi }
    defaultRequest: { cpu: 100m, memory: 256Mi }
```

---

## 4. Imperative Commands

### Pod Security Admission (PSA)

```bash
# Label a namespace to enforce the restricted PSS level
kubectl label namespace secure-ns \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest

# Add warn + audit labels without blocking (dry-run check)
kubectl label namespace my-ns \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/audit=restricted

# Check current PSA labels on all namespaces
kubectl get namespaces -o custom-columns=\
'NAME:.metadata.name,ENFORCE:.metadata.labels.pod-security\.kubernetes\.io/enforce'

# Test whether existing workloads in a namespace would violate restricted policy
kubectl label namespace my-ns \
  pod-security.kubernetes.io/enforce=restricted --dry-run=server
```

### SecurityContext

```bash
# Run a one-off pod as a specific user with read-only root filesystem
kubectl run secure-pod \
  --image=alpine \
  --overrides='{"spec":{"securityContext":{"runAsUser":1000,"runAsNonRoot":true},"containers":[{"name":"secure-pod","image":"alpine","securityContext":{"allowPrivilegeEscalation":false,"readOnlyRootFilesystem":true,"capabilities":{"drop":["ALL"]}}}]}}'

# Check the effective security context of a running pod
kubectl get pod my-pod -o jsonpath='{.spec.securityContext}'
kubectl get pod my-pod -o jsonpath='{.spec.containers[0].securityContext}'
```

### Network Policies

```bash
# Apply a default-deny-all policy to a namespace
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: my-ns
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
EOF

# List all NetworkPolicies across namespaces
kubectl get networkpolicies -A

# Describe a specific NetworkPolicy
kubectl describe networkpolicy default-deny-all -n my-ns
```

### ServiceAccounts

```bash
# Create a ServiceAccount with token auto-mount disabled
kubectl create serviceaccount secure-sa -n my-ns
kubectl patch serviceaccount secure-sa -n my-ns \
  -p '{"automountServiceAccountToken": false}'

# Get the projected token from inside a pod
kubectl exec my-pod -- \
  cat /var/run/secrets/kubernetes.io/serviceaccount/token

# Check if a ServiceAccount has a specific permission
kubectl auth can-i get secrets \
  --as system:serviceaccount:my-ns:secure-sa -n my-ns
```

### Secrets at Rest (etcd encryption)

```bash
# Verify a Secret is encrypted at rest in etcd
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret | hexdump -C | head

# The value should start with "k8s:enc:aescbc" (or "k8s:enc:aesgcm") if encrypted
# Plain text output means encryption is NOT enabled

# Force re-encryption of all existing Secrets after enabling EncryptionConfiguration
kubectl get secrets -A -o json | kubectl replace -f -
```

### Image Scanning (Trivy)

```bash
# Scan an image for vulnerabilities
trivy image nginx:1.25

# Scan with severity filter
trivy image --severity HIGH,CRITICAL nginx:1.25

# Scan all images currently running in the cluster
kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' \
  | sort -u | xargs -I{} trivy image {}
```

---

## 5. Diagnostic Commands

### Inspect Pod Security

```bash
# List pods that are NOT running as non-root
kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.securityContext.runAsNonRoot != true) |
      "\(.metadata.namespace)/\(.metadata.name)"'

# Check seccomp profile on a pod
kubectl get pod my-pod -o jsonpath=\
  '{.spec.securityContext.seccompProfile}'

# List pods with hostNetwork / hostPID / hostIPC enabled (high risk)
kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.hostNetwork == true or .spec.hostPID == true or .spec.hostIPC == true) |
      "\(.metadata.namespace)/\(.metadata.name)"'

# List pods mounting the Docker/containerd socket (escape risk)
kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.volumes[]?.hostPath.path == "/var/run/docker.sock") |
      "\(.metadata.namespace)/\(.metadata.name)"'
```

### Audit Logs

```bash
# Tail the API server audit log (path depends on your EncryptionConfig)
tail -f /var/log/kubernetes/audit/audit.log | jq .

# Filter for secret access events
cat /var/log/kubernetes/audit/audit.log | \
  jq 'select(.objectRef.resource == "secrets")'

# Filter for failed authentication attempts
cat /var/log/kubernetes/audit/audit.log | \
  jq 'select(.responseStatus.code == 401 or .responseStatus.code == 403)'
```

### Runtime Security

```bash
# Check AppArmor profile loaded on a node
cat /sys/kernel/security/apparmor/profiles | grep -i docker

# Check active seccomp profiles on a node
ls /var/lib/kubelet/seccomp/profiles/

# Inspect Falco alerts (if Falco is installed)
kubectl logs -l app=falco -n falco --tail=50

# List processes running inside a container
kubectl exec my-pod -- ps aux

# Check file capabilities inside a container
kubectl exec my-pod -- cat /proc/1/status | grep Cap
```

### RBAC Audit

```bash
# Find all subjects bound to cluster-admin
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects'

# List all ServiceAccounts with wildcard (*) permissions
kubectl get clusterroles -o json | \
  jq '.items[] | select(.rules[]?.verbs[]? == "*") | .metadata.name'

# Check which ClusterRoles allow secrets access
kubectl get clusterroles -o json | \
  jq '.items[] | select(.rules[]?.resources[]? == "secrets") | .metadata.name'
```

---

## 6. Quick Reference

### Pod Security Standards (PSS)

| Level | Restrictions | Use case |
|---|---|---|
| `privileged` | None — all capabilities allowed | Trusted system workloads (CNI, Falco) |
| `baseline` | Blocks known privilege escalation (hostPID, hostNetwork, privileged containers) | Most workloads |
| `restricted` | Baseline + must be non-root, drop ALL caps, read-only root FS, seccomp required | Security-sensitive workloads |

### PSA Modes

| Mode | Effect |
|---|---|
| `enforce` | Reject violating pods |
| `audit` | Allow but log violation to audit log |
| `warn` | Allow but show warning to the user |

### SecurityContext Fields (Pod vs Container level)

| Field | Level | Purpose |
|---|---|---|
| `runAsNonRoot` | Pod / Container | Reject if UID == 0 |
| `runAsUser` / `runAsGroup` | Pod / Container | Set UID/GID |
| `fsGroup` | Pod | Group ownership of mounted volumes |
| `seccompProfile` | Pod / Container | Syscall filter profile |
| `allowPrivilegeEscalation` | Container | Block `setuid` / `setgid` escalation |
| `readOnlyRootFilesystem` | Container | Mount root as read-only |
| `capabilities.drop` | Container | Drop Linux capabilities (use `[ALL]`) |
| `capabilities.add` | Container | Add specific capabilities back |
| `appArmorProfile` | Container | AppArmor profile to apply |

### Common Supply Chain Tools

| Tool | Purpose |
|---|---|
| Trivy | Vulnerability scanner (images, configs, filesystems) |
| Grype | Vulnerability scanner (images, SBOMs) |
| Cosign | Image signing and verification (Sigstore) |
| Syft | SBOM generation (SPDX, CycloneDX) |
| Kyverno | Policy engine — validating and mutating admission webhooks |
| OPA Gatekeeper | Policy engine — Rego-based validating webhooks |
| Falco | Runtime threat detection (eBPF/syscall-based) |

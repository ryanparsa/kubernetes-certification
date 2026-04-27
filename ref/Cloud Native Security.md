# Cloud Native Security

## The 4Cs of Cloud Native Security

Security is layered — each outer layer protects the inner layers, but inner-layer security cannot compensate for outer-layer vulnerabilities.

```
Cloud → Cluster → Container → Code
```

| Layer | Responsibilities |
|-------|-----------------|
| **Cloud** | Physical security, hypervisor, network infrastructure, IAM, managed control plane |
| **Cluster** | API server access, RBAC, NetworkPolicy, etcd encryption, audit logging |
| **Container** | Image scanning, minimal base images, runtime security, SecurityContext |
| **Code** | Secure coding, TLS for endpoints, dependency management, input validation |

Shared responsibility model: the cloud provider owns the Cloud layer for managed Kubernetes (EKS, GKE, AKS). Customers own everything from Cluster inward.

---

## 5-Layer Pod Security Architecture

Think of pod security as an onion across the pod lifecycle — each layer adds an independent control.

### Layer 1 — Supply Chain (Build Phase)
Security begins before the pod exists. The goal: ensure the image is not compromised.

- **Vulnerability scanning:** Trivy, Grype scan images in CI/CD for CVEs
- **Image signing:** Cosign/Sigstore signs images; admission controllers verify signatures before deployment
- **SBOM:** Syft generates a bill of materials (SPDX or CycloneDX) for rapid CVE response (e.g., Log4Shell)

### Layer 2 — Admission Control (Deploy Phase)
The API server gatekeeper. The cluster decides whether the pod meets security standards before it starts.

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

## Hardened Deployment Reference

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

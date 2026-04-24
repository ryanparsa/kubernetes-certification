# Kubernetes TLS and Security Reference

CKA / CKAD / CKS exam-focused reference. Sourced from kubernetes/website docs and kubeadm defaults.

---

## Part 1: TLS / PKI / Certificates

### 1.1 — The Two TLS Roles (Server vs Client)

Every Kubernetes connection has a **listener** (presents a server certificate) and an **initiator** (presents a client certificate for mutual TLS). Understanding which component plays which role is the foundation of the PKI.

| Component | Server Role | Client Role (as initiator) |
|-----------|-------------|---------------------------|
| kube-apiserver | Port 6443 (`apiserver.crt`) | → etcd (`apiserver-etcd-client.crt`), → kubelet (`apiserver-kubelet-client.crt`) |
| kubelet | Port 10250 (`kubelet.crt`) | → apiserver (`kubelet-client-current.pem`) |
| etcd | Port 2379 (`etcd/server.crt`) | ← only kube-apiserver (authorized) |
| etcd peer | Port 2380 (`etcd/peer.crt`) | → other etcd members |
| kube-scheduler | None | → apiserver (embedded in `scheduler.conf`) |
| kube-controller-manager | None | → apiserver (embedded in `controller-manager.conf`) |

**mTLS handshake flow** (apiserver → kubelet):
1. Apiserver opens TCP connection to kubelet port 10250
2. Kubelet presents `kubelet.crt` (signed by kubelet CA or cluster CA)
3. Apiserver presents `apiserver-kubelet-client.crt` (CN=kube-apiserver, signed by cluster CA)
4. Kubelet verifies apiserver cert against its `--client-ca-file`
5. Apiserver verifies kubelet cert against its `--kubelet-certificate-authority`
6. TLS tunnel established; requests are authorized by kubelet's authz

**What breaks if a cert expires:**
- `apiserver.crt` expires → all kubectl commands fail (TLS handshake error)
- `apiserver-kubelet-client.crt` expires → kubelet logs/exec/port-forward fail
- `apiserver-etcd-client.crt` expires → apiserver cannot read/write state; cluster freezes
- `etcd/peer.crt` expires → etcd loses quorum in multi-node cluster
- `kubelet-client-current.pem` expires → kubelet cannot register; node goes NotReady

### 1.2 — PKI File Map (`/etc/kubernetes/pki/`)

| File | Type | Used by | Purpose |
|------|------|---------|---------|
| `ca.crt` | CA cert | All components | Root of trust for cluster |
| `ca.key` | CA key | kubeadm only | Signs component certs |
| `apiserver.crt` / `.key` | Server cert | kube-apiserver | TLS on port 6443 |
| `apiserver-kubelet-client.crt` / `.key` | Client cert | kube-apiserver | Auth to kubelet |
| `apiserver-etcd-client.crt` / `.key` | Client cert | kube-apiserver | Auth to etcd |
| `front-proxy-ca.crt` / `.key` | CA cert | Front-proxy chain | Aggregation layer CA |
| `front-proxy-client.crt` / `.key` | Client cert | kube-apiserver | Aggregation proxy requests |
| `sa.key` | Signing key | kube-controller-manager | Signs ServiceAccount JWTs |
| `sa.pub` | Verify key | kube-apiserver | Verifies ServiceAccount JWTs |
| `etcd/ca.crt` / `.key` | etcd CA | etcd components | Root of trust for etcd |
| `etcd/server.crt` / `.key` | Server cert | etcd | TLS on ports 2379/2380 |
| `etcd/peer.crt` / `.key` | Peer cert | etcd | etcd peer-to-peer communication |
| `etcd/healthcheck-client.crt` / `.key` | Client cert | etcd liveness probe | Health check auth |

Inspect any cert:
```bash
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text \
  | grep -A2 "Subject\|Issuer\|Not After\|DNS\|IP"
```

### 1.3 — CN / O Fields and RBAC Identity

Kubernetes uses the TLS cert fields to derive the user identity passed to RBAC:
- **CN (Common Name)** → username
- **O (Organization)** → group membership

| Component | CN | O (Group) | RBAC binding |
|-----------|-----|-----------|--------------|
| kube-scheduler | `system:kube-scheduler` | `system:kube-scheduler` | Built-in ClusterRole |
| kube-controller-manager | `system:kube-controller-manager` | `system:kube-controller-manager` | Built-in ClusterRole |
| kube-proxy | `system:kube-proxy` | `system:node-proxier` | Built-in ClusterRole |
| kubelet | `system:node:<nodeName>` | `system:nodes` | Node authorizer |
| admin (kubeconfig) | `kubernetes-admin` | `system:masters` | `system:masters` bypasses RBAC |

**Why `system:masters` is special**: the `system:masters` group is hardcoded in the API server authorizer as an unconditional allow, bypassing all RBAC rules. This is by design (break-glass access) but means any cert with `O=system:masters` has unrestricted cluster access.

### 1.4 — HA Cluster Cert Distribution Strategy

| Component | Distribution | Reason |
|-----------|-------------|--------|
| kubelet (client cert) | Unique per node | CN must include node name |
| kubelet (server cert) | Unique per node | SAN must match node IP/hostname |
| etcd server/peer | Unique per node | SAN includes node IP |
| kube-apiserver | Shared with all master IPs + LB in SAN | All masters serve on same VIP |
| kube-scheduler / controller-manager | Shared by role | No node-specific identity |
| sa.key / sa.pub | **Identical copy on all masters** | All masters must validate the same JWTs |
| front-proxy-ca / front-proxy-client | Shared | All masters proxy the same aggregation layer |

**Why SA keys must be identical across HA masters**: ServiceAccount tokens are JWTs signed with `sa.key`. Any apiserver instance may receive a request with any token. If masters had different `sa.pub` keys, tokens issued by one master would fail validation on another.

### 1.5 — Non-TLS Keys in the PKI Directory

**sa.key / sa.pub — Service Account JWT Signing**

These are RSA key pairs, not TLS certificates. They are used exclusively for signing and verifying ServiceAccount JWT tokens:
- `kube-controller-manager` uses `sa.key` to sign tokens when creating projected volumes
- `kube-apiserver` uses `sa.pub` to verify incoming Bearer tokens in requests
- The `TokenRequest` API also uses this key pair for bound projected tokens

**front-proxy-ca.crt / front-proxy-client.crt — API Aggregation**

The front-proxy chain enables the API aggregation layer (e.g., metrics-server registers an APIService). When a request arrives at the aggregation API, kube-apiserver forwards it to the extension API server using `front-proxy-client.crt`. The extension server must verify the cert against `front-proxy-ca.crt`.

**Why etcd has its own CA:**
- etcd stores all cluster state including Secrets
- An isolated CA limits blast radius: a compromised cluster CA cannot forge etcd client certs
- etcd peers only trust certs signed by the etcd CA, not the cluster CA

### 1.6 — Certificate Renewal Reference

Check expiration:
```bash
kubeadm certs check-expiration
```

Renew all certificates:
```bash
kubeadm certs renew all
# Then restart static pods to pick up new certs
crictl pods --namespace kube-system -q | xargs -I{} crictl stopp {}
# Or move manifests out and back in
```

Renew a single certificate:
```bash
kubeadm certs renew apiserver
kubeadm certs renew apiserver-kubelet-client
kubeadm certs renew etcd-server
# etc.
```

After renewal, admin.conf must be updated (kubeadm renew also updates it):
```bash
cp /etc/kubernetes/admin.conf ~/.kube/config
```

Certificate validity: kubeadm issues 1-year certs for components, 10-year certs for CA.

**CA rotation (advanced — rarely needed in exam):**
1. Generate new CA cert/key
2. Distribute new CA cert to all nodes as a bundle (old + new)
3. Re-issue all component certs signed by new CA
4. Remove old CA cert from bundle
5. Full rolling restart of all components

### 1.7 — CertificateSigningRequest (CSR) API

The `certificates.k8s.io/v1` API enables in-cluster cert issuance without touching CA files directly. Used for: provisioning user client certs, kubelet bootstrap, custom controller certs.

```bash
# Exam pattern: issue a client cert for user jane
openssl genrsa -out jane.key 2048
openssl req -new -key jane.key -out jane.csr -subj "/CN=jane/O=dev"

kubectl apply -f - <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: jane
spec:
  request: $(base64 < jane.csr | tr -d '\n')
  signerName: kubernetes.io/kube-apiserver-client
  usages: [client auth]
  expirationSeconds: 86400
EOF

kubectl certificate approve jane
kubectl get csr jane -o jsonpath='{.status.certificate}' | base64 -d > jane.crt

# Use the cert
kubectl config set-credentials jane --client-key=jane.key --client-certificate=jane.crt
kubectl config set-context jane-ctx --cluster=kubernetes --user=jane
```

Available `signerName` values:
- `kubernetes.io/kube-apiserver-client` — client cert validated by apiserver
- `kubernetes.io/kube-apiserver-client-kubelet` — kubelet client cert (bootstrap flow)
- `kubernetes.io/kubelet-serving` — kubelet server cert
- `kubernetes.io/legacy-unknown` — backward compat only

### 1.8 — Kubelet TLS Bootstrapping

How a new node joins the cluster without pre-provisioned certs:

1. **Bootstrap token issued** on control plane: `kubeadm token create`
2. **Kubelet starts** with `--bootstrap-kubeconfig` pointing to a kubeconfig that uses the token as a Bearer credential
3. **Kubelet submits CSR** using the `system:bootstrappers` group (authorized by `system:node-bootstrapper` ClusterRole)
4. **Auto-approval** (if `system:certificates.k8s.io:certificatesigningrequests:nodeclient` ClusterRoleBinding exists for `system:bootstrappers`)
5. **Cert issued** → kubelet writes `kubelet-client-<timestamp>.pem` + updates `kubelet-client-current.pem` symlink → uses cert for all future requests
6. **Server cert rotation** (optional): `serverTLSBootstrap: true` in kubelet-config.yaml enables automatic server cert rotation via CSR API

RBAC needed for auto-approval:
```bash
kubectl create clusterrolebinding node-client-auto-approve \
  --clusterrole=system:certificates.k8s.io:certificatesigningrequests:nodeclient \
  --group=system:bootstrappers
```

### 1.9 — Inspecting Certs at Exam Time

```bash
# Full cert details
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text

# Quick check: subject, issuer, expiry, SANs
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text \
  | grep -A2 "Subject\|Issuer\|Not After\|DNS\|IP"

# Check all cert expiry at once
kubeadm certs check-expiration

# View a kubeconfig's embedded cert
kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' \
  | base64 -d | openssl x509 -noout -text

# Decode a CSR
openssl req -in /path/to/request.csr -noout -text
```

---

## Part 2: Authentication & Authorization

### 2.1 — Authentication Mechanisms

The API server evaluates authentication plugins in order; the first to succeed wins.

| Method | How it works | Enabled by |
|--------|-------------|------------|
| X.509 client certs | CN = username, O = group | `--client-ca-file` |
| Static token file | Bearer token in request header | `--token-auth-file` (discouraged) |
| Bootstrap tokens | `system:bootstrappers` group tokens | `--enable-bootstrap-token-auth` |
| ServiceAccount tokens | JWT signed with `sa.key` | Always on |
| OIDC | ID token from external IdP | `--oidc-issuer-url` |
| Webhook | Delegates authn to external service | `--authentication-token-webhook-config-file` |
| Anonymous | Requests with no credentials | Disabled with `--anonymous-auth=false` |

**Request flow through the API server:**
```
Client Request
    │
    ▼
[Authentication] ←── plugins evaluated in order; first success wins
    │                 failure = 401 Unauthorized
    ▼
[Authorization]  ←── Node / RBAC / Webhook evaluated; first allow wins
    │                 no allow = 403 Forbidden
    ▼
[Admission]      ←── Mutating webhooks → Validating webhooks → Object validation
    │                 rejection = 400/422
    ▼
[etcd persist]
```

**Disable anonymous access (CKS requirement):**
```bash
# In kube-apiserver static pod manifest:
- --anonymous-auth=false
# In kubelet config:
authentication:
  anonymous:
    enabled: false
```

### 2.2 — Service Account Tokens

| Property | Legacy SA Token | Projected (Bound) Token |
|----------|----------------|------------------------|
| Storage | Stored as Secret in etcd | Never written to disk |
| Expiry | Never expires | Default 1 hour (configurable) |
| Audience | Any | Bound to specific audience |
| Rotation | No | Auto-rotated by kubelet |
| API | Not recommended | TokenRequest API |

How to request a bound token manually:
```bash
kubectl create token my-sa --duration=1h --audience=my-service
```

Projected volume with custom expiry (replaces legacy automount):
```yaml
volumes:
- name: kube-api-access
  projected:
    sources:
    - serviceAccountToken:
        expirationSeconds: 3600
        path: token
    - configMap:
        name: kube-root-ca.crt
        items:
        - key: ca.crt
          path: ca.crt
```

**Disable auto-mount for a ServiceAccount:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: no-token-sa
automountServiceAccountToken: false
```

### 2.3 — Authorization Modes Overview

Configured via `--authorization-mode=Node,RBAC` on kube-apiserver (comma-separated, evaluated in order; first allow wins, first deny is ignored — only explicit deny from Webhook stops).

| Mode | What it does |
|------|-------------|
| Node | Kubelet-specific permissions based on node identity |
| RBAC | Standard role-based access control |
| Webhook | Delegates authorization to an external HTTP service |
| ABAC | File-based policies (legacy, not recommended) |
| AlwaysAllow | No authorization — **never use in production** |
| AlwaysDeny | Deny everything — useful for testing |

### 2.4 — Node Authorization

The Node authorizer grants kubelets access **only** to resources bound to their own node:
- Pods scheduled on that node
- Secrets/ConfigMaps used by those pods
- PersistentVolumeClaims bound to those pods
- Node's own Node resource

**Requirement**: kubelet must use the identity `system:node:<nodeName>` (CN field in its client cert). Without this exact CN format, the Node authorizer does not recognize the kubelet.

**NodeRestriction admission controller** (companion to Node authorizer):
- Kubelets can only modify their own Node object, not other nodes'
- Kubelets cannot add/remove labels with `node-restriction.kubernetes.io/` prefix
- Prevents a compromised node from affecting cluster-wide resources

---

## Part 3: RBAC

### 3.1 — RBAC Resource Types

| Resource | Scope | What it does |
|----------|-------|-------------|
| Role | Namespaced | Grants permissions within one namespace |
| ClusterRole | Cluster-wide | Grants permissions globally or across namespaces |
| RoleBinding | Namespaced | Binds a Role or ClusterRole to subjects in a namespace |
| ClusterRoleBinding | Cluster-wide | Binds a ClusterRole to subjects cluster-wide |

**Key rule**: A `RoleBinding` can bind a `ClusterRole` — this restricts the ClusterRole to the binding's namespace. It does NOT grant cluster-wide access.

### 3.2 — RBAC YAML Patterns

Role:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]          # "" = core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

RoleBinding:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: my-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

ClusterRole for non-namespaced resources:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

### 3.3 — Imperative RBAC Commands (Exam Speed)

```bash
# Create Role
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default

# Create ClusterRole
kubectl create clusterrole node-reader --verb=get,list --resource=nodes

# Create RoleBinding
kubectl create rolebinding jane-pod-reader --role=pod-reader --user=jane -n default

# Create ClusterRoleBinding
kubectl create clusterrolebinding jane-node-reader --clusterrole=node-reader --user=jane

# Bind ClusterRole to ServiceAccount in specific namespace
kubectl create rolebinding sa-admin \
  --clusterrole=admin \
  --serviceaccount=my-ns:my-sa \
  -n my-ns

# Check permissions
kubectl auth can-i list pods --as=jane -n default
kubectl auth can-i '*' '*' --as=jane
kubectl auth can-i list pods --as=system:serviceaccount:default:my-sa

# List all permissions for a user
kubectl auth can-i --list --as=jane -n default

# Dry-run to generate YAML
kubectl create role pod-reader --verb=get,list --resource=pods -n default \
  --dry-run=client -o yaml
```

### 3.4 — Built-in ClusterRoles

| ClusterRole | Grants |
|------------|--------|
| `cluster-admin` | Full access to everything (bound via ClusterRoleBinding = superuser) |
| `admin` | Full access within a namespace (used with RoleBinding) |
| `edit` | Read/write most resources, no Role/RoleBinding access |
| `view` | Read-only all resources |
| `system:node` | Kubelet permissions (enforced via Node authorizer) |
| `system:kube-scheduler` | Permissions for kube-scheduler |
| `system:kube-controller-manager` | Permissions for kube-controller-manager |
| `system:node-proxier` | Permissions for kube-proxy |
| `system:masters` | Unconditional superuser (bypasses RBAC entirely) |

### 3.5 — RBAC Aggregation Rules

ClusterRoles can aggregate permissions from other ClusterRoles using label selectors:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: []   # populated automatically by controller
```

The built-in `admin`, `edit`, `view` roles use this pattern — adding a label to your custom ClusterRole automatically includes its rules in the aggregate.

### 3.6 — RBAC Best Practices (CKS)

- Grant least privilege — never bind `cluster-admin` to a ServiceAccount
- Avoid wildcard verbs (`*`) and resources (`*`) in production
- ServiceAccounts should be namespace-scoped with minimal permissions
- Regularly audit: `kubectl auth can-i --list --as=<user>`
- `system:masters` group bypasses RBAC entirely — never assign to regular users
- Set `automountServiceAccountToken: false` on ServiceAccounts that don't need API access
- Use `RoleBinding` + `ClusterRole` instead of `ClusterRoleBinding` to limit scope to a namespace

---

## Part 4: Encryption at Rest & Secrets

### 4.1 — Why Encrypt Secrets at Rest

By default, Secrets in etcd are stored as **base64-encoded plaintext** — not encrypted. Anyone with direct etcd access can read all Secrets. Encryption at rest makes Secrets unreadable without the encryption key even with raw etcd access.

Verify a Secret is **not** encrypted (default state):
```bash
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key \
  get /registry/secrets/default/my-secret
# Output is base64-decodable plaintext
```

### 4.2 — EncryptionConfiguration YAML

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  - configmaps
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>   # openssl rand -base64 32
  - identity: {}   # fallback: existing unencrypted data can still be read
```

**Provider priority**: the **first** provider is used for **write**; all providers are tried on **read** (in order). Always place `identity: {}` last during migration so existing unencrypted data remains readable.

### 4.3 — Available Encryption Providers

| Provider | Algorithm | Notes |
|----------|-----------|-------|
| `identity` | None (plaintext) | Default — no encryption |
| `aescbc` | AES-CBC + PKCS7 padding | Stable, recommended for most cases |
| `aesgcm` | AES-GCM | Faster, but key reuse risk (use key rotation) |
| `secretbox` | XSalsa20 + Poly1305 | Fast, strong — good alternative to aescbc |
| `kms v1` | External KMS via gRPC | Envelope encryption (key never in config) |
| `kms v2` | External KMS via gRPC | GA in 1.29, local DEK caching, better performance |

Generate a 32-byte key:
```bash
openssl rand -base64 32
```

### 4.4 — Enabling Encryption

1. Create the EncryptionConfiguration file (e.g., `/etc/kubernetes/enc/encryption-config.yaml`)
2. Add to kube-apiserver static pod manifest:
```yaml
- --encryption-provider-config=/etc/kubernetes/enc/encryption-config.yaml
```
3. Mount the file into the static pod:
```yaml
volumeMounts:
- name: enc
  mountPath: /etc/kubernetes/enc
  readOnly: true
volumes:
- name: enc
  hostPath:
    path: /etc/kubernetes/enc
    type: DirectoryOrCreate
```
4. Restart kube-apiserver (move manifest out and back in)
5. Re-encrypt all existing Secrets:
```bash
kubectl get secrets -A -o json | kubectl replace -f -
```
6. Verify:
```bash
ETCDCTL_API=3 etcdctl ... get /registry/secrets/default/my-secret | hexdump -C | head -5
# Encrypted output starts with: k8s:enc:aescbc:v1:key1:
```

### 4.5 — Rotating the Encryption Key

1. Add new key as the **first** entry in providers
2. Restart API server (picks up new config, new writes use new key)
3. Re-encrypt all existing secrets: `kubectl get secrets -A -o json | kubectl replace -f -`
4. Remove old key from config
5. Restart API server again

### 4.6 — Secrets Best Practices (CKS)

- Use `stringData` in manifests, never commit raw data values to git
- Mount secrets as volumes instead of env vars when possible (env vars leak into logs)
- Use `imagePullSecrets` for registry credentials
- Prefer external secret managers (Vault, CSI secret store) for production
- Enable encryption at rest — verify with `etcdctl` hex dump
- RBAC: restrict `get`/`list`/`watch` on Secrets to only what needs it
- Set `automountServiceAccountToken: false` when the SA doesn't need cluster API access

---

## Part 5: Pod & Container Security

### 5.1 — Pod Security Standards (PSS)

Three policy levels (applied cluster-wide or per-namespace via PodSecurity admission controller):

| Level | What it allows |
|-------|---------------|
| `privileged` | Unrestricted (same as no policy) |
| `baseline` | Prevents known privilege escalations; allows most workloads |
| `restricted` | Hardened — requires non-root, no privilege escalation, drop all caps |

Three modes (applied independently per level):

| Mode | Effect |
|------|--------|
| `enforce` | Pods violating policy are **rejected** |
| `audit` | Violations are logged (audit annotation) but pods still run |
| `warn` | User gets a warning at apply time but pods still run |

Namespace labels:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: baseline
    pod-security.kubernetes.io/audit: restricted
```

Apply labels imperatively:
```bash
kubectl label namespace my-ns \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest
```

**What `restricted` requires:**
- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- `capabilities.drop: [ALL]`
- `seccompProfile.type: RuntimeDefault` or `Localhost`
- No `hostPID`, `hostIPC`, `hostNetwork`
- No `privileged: true`
- No `hostPath` volumes

### 5.2 — SecurityContext Reference

**Pod-level** (`spec.securityContext`):

| Field | Purpose |
|-------|---------|
| `runAsUser` | UID all containers run as (unless overridden) |
| `runAsGroup` | GID for all containers |
| `runAsNonRoot` | Reject pods that would run as root |
| `fsGroup` | GID applied to mounted volumes |
| `supplementalGroups` | Additional GIDs |
| `sysctls` | Kernel parameter overrides (safe/unsafe) |
| `seccompProfile` | Default seccomp profile for all containers |
| `seLinuxOptions` | SELinux labels for all containers |
| `appArmorProfile` | AppArmor profile (Kubernetes 1.30+) |

**Container-level** (`spec.containers[].securityContext`):

| Field | Purpose |
|-------|---------|
| `allowPrivilegeEscalation` | Set to `false` to prevent setuid escalation |
| `privileged` | Full root privileges — never set in production |
| `readOnlyRootFilesystem` | Container filesystem is read-only |
| `capabilities.drop` | Drop Linux capabilities (e.g., `["ALL"]`) |
| `capabilities.add` | Add specific capabilities (e.g., `["NET_BIND_SERVICE"]`) |
| `runAsUser` | Override pod-level UID for this container |
| `runAsNonRoot` | Override pod-level flag for this container |
| `seccompProfile` | Override pod-level seccomp profile |
| `seLinuxOptions` | Override pod-level SELinux labels |

Example — hardened container:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
```

### 5.3 — Seccomp

Seccomp (secure computing mode) restricts which syscalls a container may make.

```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault    # use container runtime's default profile (safe for most workloads)
    # type: Localhost       # use a custom profile from the node
    # localhostProfile: profiles/audit.json   # (required if type: Localhost)
    # type: Unconfined      # no restriction (default if omitted pre-1.27)
```

Node-local profile path: `/var/lib/kubelet/seccomp/profiles/` (customizable via `--seccomp-profile-root` or `seccompDefault`).

`RuntimeDefault` is CKS-recommended — it blocks ~40% of syscalls with negligible application impact.

### 5.4 — AppArmor

AppArmor profiles are **node-local** — they must be loaded on every node where pods can schedule.

```bash
# Check profile is loaded on a node
ssh node1 "sudo aa-status | grep k8s-apparmor"
```

**Pre-1.30 (annotation-based):**
```yaml
metadata:
  annotations:
    container.apparmor.security.beta.kubernetes.io/<container-name>: runtime/default
    # or: localhost/<profile-name>
    # or: unconfined
```

**Kubernetes 1.30+ (field-based):**
```yaml
spec:
  securityContext:
    appArmorProfile:
      type: RuntimeDefault
      # type: Localhost
      # localhostProfile: my-profile   # (required if type: Localhost)
```

Available types: `RuntimeDefault`, `Localhost`, `Unconfined`.

### 5.5 — SELinux

```yaml
securityContext:
  seLinuxOptions:
    level: "s0:c123,c456"   # MCS label — most commonly used field
    role: ""
    type: ""
    user: ""
```

`level` (MCS label) is the most commonly set field. Containers sharing a level can access each other's volumes. Different levels provide volume isolation.

---

## Part 6: NetworkPolicy

### 6.1 — Default Behavior Without NetworkPolicy

Without any NetworkPolicy selecting a pod: **all ingress and egress is allowed** (flat network).  
Once at least one NetworkPolicy selects a pod, **only explicitly allowed traffic is permitted**. There is no "deny" directive — everything not in an `allow` rule is implicitly denied.

### 6.2 — Default Deny All (Ingress + Egress)

Apply to every namespace that contains workloads:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: prod
spec:
  podSelector: {}          # selects ALL pods in namespace
  policyTypes:
  - Ingress
  - Egress
  # no ingress/egress rules = deny all
```

### 6.3 — DNS Egress Exception

After applying a deny-all egress policy, DNS resolution breaks for all pods. **Always add this exception** when using deny-all egress:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: prod
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

### 6.4 — Selector Types

| Selector in rule | What it matches |
|-----------------|----------------|
| `podSelector` | Pods with specific labels (same namespace) |
| `namespaceSelector` | All pods in matching namespaces |
| `namespaceSelector` + `podSelector` (in same `from` entry) | Pods with label X in namespace with label Y |
| `ipBlock` | CIDR range (external IPs) |

**Important**: `from` entries in the same list item are ANDed; entries in different list items are ORed.

```yaml
# AND: pods with app=frontend IN namespace with env=prod
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        env: prod
    podSelector:
      matchLabels:
        app: frontend

# OR: pods with app=frontend OR pods in namespace with env=prod
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        env: prod
  - podSelector:
      matchLabels:
        app: frontend
```

### 6.5 — Common Exam Patterns

Allow `frontend` → `backend` on port 8080:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
      protocol: TCP
```

Allow cross-namespace access (monitoring namespace → app namespace):
```yaml
spec:
  podSelector: {}
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
```

---

## Part 7: Audit Logging

### 7.1 — Why Audit

Audit logs record every request to the API server: **who**, **what**, **when**, and the **response code**. Essential for CKS — you must be able to write an audit policy and interpret audit log output.

Audit stages:
- `RequestReceived` — request arrives (before authentication)
- `ResponseStarted` — response headers sent (streaming only)
- `ResponseComplete` — response body complete
- `Panic` — server panic

`omitStages: [RequestReceived]` is the standard pattern to reduce noise.

### 7.2 — Audit Levels

| Level | What is logged |
|-------|---------------|
| `None` | Nothing — request is silently ignored in audit |
| `Metadata` | Request metadata only (user, verb, resource, namespace, response code) |
| `Request` | Metadata + request body (no response body) |
| `RequestResponse` | Everything — request body + response body |

Rules are evaluated in order; **first match wins**.

### 7.3 — Audit Policy YAML

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
- RequestReceived   # skip noisy early stage
rules:
# Log secret access at full detail
- level: RequestResponse
  resources:
  - group: ""
    resources: [secrets]
# Log pod operations with metadata only
- level: Metadata
  resources:
  - group: ""
    resources: [pods, services, configmaps]
# Silence kube-proxy noise
- level: None
  users: [system:kube-proxy]
# Log node activity at metadata level
- level: Metadata
  userGroups: [system:nodes]
# Silence health check endpoints
- level: None
  nonResourceURLs: [/healthz, /readyz, /livez, /metrics]
# Catch-all: log everything else at metadata
- level: Metadata
```

### 7.4 — API Server Flags

```yaml
# In kube-apiserver static pod manifest:
- --audit-policy-file=/etc/kubernetes/audit-policy.yaml
- --audit-log-path=/var/log/kubernetes/audit.log
- --audit-log-maxage=30      # days to keep
- --audit-log-maxbackup=10   # number of rotated files
- --audit-log-maxsize=100    # MB before rotation
```

Mount the policy file into the static pod:
```yaml
volumeMounts:
- name: audit
  mountPath: /etc/kubernetes/audit-policy.yaml
  readOnly: true
- name: audit-log
  mountPath: /var/log/kubernetes/
volumes:
- name: audit
  hostPath:
    path: /etc/kubernetes/audit-policy.yaml
    type: File
- name: audit-log
  hostPath:
    path: /var/log/kubernetes/
    type: DirectoryOrCreate
```

Read audit logs:
```bash
cat /var/log/kubernetes/audit.log | python3 -m json.tool | grep -A5 '"verb"'
# or
tail -f /var/log/kubernetes/audit.log | jq 'select(.verb == "create" and .objectRef.resource == "secrets")'
```

---

## Part 8: Admission Controllers

### 8.1 — What Admission Controllers Do

Admission controllers intercept API requests **after authentication and authorization** but **before the object is persisted**. Two types:
- **Mutating**: can modify the request object (run first)
- **Validating**: can accept or reject the request (run second)

Processing order: Authentication → Authorization → **Mutating Admission** → Object schema validation → **Validating Admission** → etcd persist

### 8.2 — Controllers Enabled by Default (kubeadm)

```
NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass,
DefaultTolerationSeconds, MutatingAdmissionWebhook, ValidatingAdmissionWebhook,
ResourceQuota, NodeRestriction, PodSecurity
```

Configured via: `--enable-admission-plugins=...` on kube-apiserver.  
Disable a controller: `--disable-admission-plugins=PodSecurity`

### 8.3 — Key Controllers for CKS

| Controller | What it does |
|-----------|-------------|
| `NodeRestriction` | Limits kubelet to only modify objects for its own node |
| `PodSecurity` | Enforces Pod Security Standards based on namespace labels |
| `LimitRanger` | Applies default resource requests/limits to pods |
| `ResourceQuota` | Limits total resource consumption per namespace |
| `ImagePolicyWebhook` | Delegates image allow/block decisions to an external webhook |
| `MutatingAdmissionWebhook` | Calls external webhook that can modify objects |
| `ValidatingAdmissionWebhook` | Calls external webhook that can accept/reject objects |
| `ServiceAccount` | Auto-creates default SA; auto-mounts SA token |
| `NamespaceLifecycle` | Prevents creating resources in terminating namespaces |

### 8.4 — ValidatingAdmissionPolicy (CEL-based, GA in 1.30)

New alternative to webhooks — pure in-cluster validation, no external service needed:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: no-latest-tag
spec:
  matchConstraints:
    resourceRules:
    - apiGroups: [""]
      apiVersions: ["v1"]
      operations: [CREATE, UPDATE]
      resources: [pods]
  validations:
  - expression: "!object.spec.containers.exists(c, c.image.endsWith(':latest'))"
    message: "Images must not use the :latest tag"
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: no-latest-tag-binding
spec:
  policyName: no-latest-tag
  validationActions: [Deny]
```

### 8.5 — Webhook Configuration

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: my-validator
webhooks:
- name: validate.example.com
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["pods"]
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: "/validate"
    caBundle: <base64-ca-cert>
  admissionReviewVersions: ["v1"]
  sideEffects: None
  failurePolicy: Fail   # Fail or Ignore — Fail is stricter
```

---

## Part 9: Cluster Security Quick-Reference (CKS Checklist)

### API Server Hardening

```bash
# Flags to verify/add in kube-apiserver static pod manifest:
--anonymous-auth=false
--authorization-mode=Node,RBAC           # no AlwaysAllow
--profiling=false
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--audit-log-path=/var/log/kubernetes/audit.log
--encryption-provider-config=/etc/kubernetes/enc/encryption-config.yaml
--enable-admission-plugins=NodeRestriction,PodSecurity,...
--tls-min-version=VersionTLS12
```

### Kubelet Hardening

```bash
# In kubelet-config.yaml or as flags:
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
authorization:
  mode: Webhook           # not AlwaysAllow
readOnlyPort: 0           # disable unauthenticated read-only port
protectKernelDefaults: true
```

### Full CKS Checklist

- [ ] `--anonymous-auth=false` on API server and kubelet
- [ ] `--authorization-mode=Node,RBAC` (no `AlwaysAllow`)
- [ ] `--profiling=false` on API server, controller-manager, scheduler
- [ ] Audit policy present + log backend configured
- [ ] Encryption at rest enabled for Secrets (verify via `etcdctl` hex)
- [ ] `PodSecurity` admission enabled; namespaces labeled with enforce level
- [ ] `NodeRestriction` admission controller enabled
- [ ] NetworkPolicies: `default-deny-all` + DNS egress exception in every namespace
- [ ] Kubelet: `readOnlyPort: 0`, `protectKernelDefaults: true`, anonymous auth disabled
- [ ] RBAC: no wildcard verbs for SA tokens; `cluster-admin` not bound to SAs
- [ ] Secrets mounted as volumes (not env vars) where possible
- [ ] Seccomp `RuntimeDefault` applied cluster-wide or per pod
- [ ] AppArmor `runtime/default` applied to critical pods
- [ ] ServiceAccounts: `automountServiceAccountToken: false` when not needed
- [ ] Certificates: check expiration with `kubeadm certs check-expiration`; renew with `kubeadm certs renew all`
- [ ] `etcd` access restricted to kube-apiserver only (firewall port 2379)
- [ ] Container images: no `:latest` tag, use digest pinning for critical components
- [ ] `readOnlyRootFilesystem: true` + `allowPrivilegeEscalation: false` + `capabilities.drop: [ALL]` on all containers

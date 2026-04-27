# Kubernetes Commands Reference — Part 4: kube-apiserver

> Part of [Kubernetes Commands Reference](../Kubernetes Commands Reference.md)


The front door to the cluster. Every interaction — kubectl commands, controller reconciliation,
scheduler decisions, kubelet status reports — goes through the API server.

---

### 4.1 — What It Does

- **Authenticates** every request (client cert, bearer token, OIDC, webhook)
- **Authorizes** every request (RBAC, Node authorizer, webhook)
- **Runs admission controllers** — mutating webhooks first, then validating webhooks
- **Persists** all Kubernetes objects to etcd
- **Serves watch streams** to controllers, kubelets, and kubectl `-w` commands
- **Aggregates** extended API groups (metrics-server, custom APIs via aggregation layer)

---

### 4.2 — Run Mode

Runs as a **static pod** on each control plane node.

Manifest: `/etc/kubernetes/manifests/kube-apiserver.yaml`

Editing the manifest causes kubelet to detect the change and restart the API server within
seconds. Always validate YAML syntax before saving — a syntax error will break the manifest and
take down the API server.

---

### 4.3 — Critical Flags

**TLS / Authentication:**
```
--client-ca-file=/etc/kubernetes/pki/ca.crt
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt
--tls-private-key-file=/etc/kubernetes/pki/apiserver.key
--service-account-key-file=/etc/kubernetes/pki/sa.pub        # verifies SA JWT tokens
--service-account-issuer=https://kubernetes.default.svc.cluster.local
--anonymous-auth=false                                         # CKS: must be false
--oidc-issuer-url=...                                          # external OIDC provider
--oidc-client-id=...
```

**Authorization:**
```
--authorization-mode=Node,RBAC         # Node authorizer (for kubelets) + RBAC
```

**etcd connection:**
```
--etcd-servers=https://127.0.0.1:2379
--etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
--etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
--etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
```

**Admission:**
```
--enable-admission-plugins=NodeRestriction,PodSecurity,...
--disable-admission-plugins=...
--admission-control-config-file=...    # for PodSecurity configuration (enforce/audit/warn)
```

**Security / Audit:**
```
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--audit-log-path=/var/log/kubernetes/audit.log
--audit-log-maxsize=100               # rotate at 100 MB
--audit-log-maxbackup=5
--profiling=false                     # CKS: disable CPU profile endpoint
--request-timeout=60s
```

**Aggregation layer (for metrics-server etc.):**
```
--requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
--proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
--proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
--requestheader-allowed-names=front-proxy-client
--requestheader-extra-headers-prefix=X-Remote-Extra-
--requestheader-group-headers=X-Remote-Group
--requestheader-username-headers=X-Remote-User
```

**What breaks:**
- Wrong etcd cert path → API server cannot reach etcd → all reads/writes fail
- `--anonymous-auth=true` → unauthenticated requests can probe the API
- Mismatched `--service-account-key-file` between apiserver and controller-manager → SA token
  verification fails

---


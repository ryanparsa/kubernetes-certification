 Here is Claude's plan:                                                                                                                                                                                                                                                                           
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 Kubernetes Security & TLS Reference — Implementation Plan                                                                                                                                                                                                                                        
                                                        
 ---
 Context

 The user is actively studying for CKA, CKAD, and CKS certifications using this repository. The
 ref/ directory contains high-quality reference files covering Kubernetes internals. Currently,
 kubernetes Files Ref.md serves a dual purpose:

 1. Filesystem layout — detailed annotated directory trees for control plane nodes and worker
 nodes (lines 1–179). This is core exam reference material.
 2. TLS & Identity Master Guide — sections 1–8 covering cert distribution, dual-role components,
 cert renewal, SA keys, front-proxy, and etcd PKI (lines 180–380). This is valuable but belongs
 in a dedicated security file.

 Goal: Extract, expand, and deeply explain the TLS/security content. The file must go beyond
 "what the commands are" — it must explain why each component needs each cert, how
 the mTLS handshake works, what breaks when a cert expires, and what happens internally
 during kubelet bootstrapping, etcd replication, or secret encryption. The user is building deep
 Kubernetes internals knowledge, not just memorizing exam commands.

 Reference sources:
 - kubernetes/website official docs — authoritative spec
 - kubernetes-the-hard-way by Kelsey Hightower — explains the manual bootstrap process and
 makes cert/identity relationships concrete

 Move all content into a new ref/Kubernetes TLS and Security Ref.md covering RBAC, Encryption,
 Pod Security, NetworkPolicy, Audit Logging, and Admission Controllers.

 User decisions (answered via AskUserQuestion):
 - TLS sections removed entirely from kubernetes Files Ref.md (no leftover summary)
 - New file covers: TLS/PKI, RBAC/AuthN/AuthZ, Encryption & Secrets, Pod & Cluster Security
 - Clone location: /tmp/kubernetes-website (outside the repo, ephemeral)
 - New file name: ref/Kubernetes TLS and Security Ref.md

 ---
 Critical Files

 ┌────────────────────────────────────────┬──────────────────────────────────────────────────────────────────┐
 │                  File                  │                              Action                              │
 ├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
 │ ref/kubernetes Files Ref.md            │ Remove lines 180–380 (sections 1–8 TLS guide + trailing content) │
 ├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
 │ ref/Kubernetes TLS and Security Ref.md │ Create new — full security reference                             │
 ├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
 │ /tmp/kubernetes-website/               │ Clone target — read-only reference, never committed              │
 └────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┘

 ---
 Step 0 — Clone Both Reference Repos

 Clone two repos. Both are read-only reference material — nothing from either is committed to
 this repository. Both go to /tmp/.

 0a — kubernetes/website (official docs)

 git clone \
   --depth=1 \
   --filter=blob:none \
   --sparse \
   https://github.com/kubernetes/website \
   /tmp/kubernetes-website

 cd /tmp/kubernetes-website
 git sparse-checkout set content/en/docs

 Fallback (older git):

 git clone --depth=1 https://github.com/kubernetes/website /tmp/kubernetes-website

 0b — kubernetes-the-hard-way (Kelsey Hightower)

 git clone \
   --depth=1 \
   https://github.com/kelseyhightower/kubernetes-the-hard-way \
   /tmp/kubernetes-the-hard-way

 This repo is small (~30 docs). It is the authoritative source for why each certificate
 exists and what happens at each step of cluster bootstrapping — invaluable for the internals
 depth the user wants.

 Key docs to read from it:

 /tmp/kubernetes-the-hard-way/docs/04-certificate-authority.md
 /tmp/kubernetes-the-hard-way/docs/05-kubernetes-configuration-files.md
 /tmp/kubernetes-the-hard-way/docs/06-data-encryption-keys.md
 /tmp/kubernetes-the-hard-way/docs/07-bootstrapping-etcd.md
 /tmp/kubernetes-the-hard-way/docs/08-bootstrapping-kubernetes-controllers.md
 /tmp/kubernetes-the-hard-way/docs/09-bootstrapping-kubernetes-workers.md
 /tmp/kubernetes-the-hard-way/docs/10-configuring-kubectl.md
 /tmp/kubernetes-the-hard-way/docs/11-pod-network-routes.md

 These files explain the manual certificate generation flow (using cfssl or openssl) and
 make it clear which component talks to which and why each cert's CN/O fields matter.

 ---
 Step 1 — Read Both Repos to Verify Coverage and Extract Depth

 After cloning, read docs from both repos. The kubernetes/website files give the authoritative
 spec; the kubernetes-the-hard-way files explain the bootstrap flow and rationale. Together
 they provide both "what" and "why." Any topic covered in either repo that is absent or shallow
 in our existing TLS guide is a gap to fill.

 TLS / PKI Docs to Read

 From kubernetes/website:

 /tmp/kubernetes-website/content/en/docs/tasks/tls/managing-tls-in-a-cluster.md
 /tmp/kubernetes-website/content/en/docs/tasks/tls/certificate-rotation.md
 /tmp/kubernetes-website/content/en/docs/tasks/tls/manual-rotation-of-ca-certificates.md
 /tmp/kubernetes-website/content/en/docs/tasks/administer-cluster/kubeadm/kubeadm-certs.md
 /tmp/kubernetes-website/content/en/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/certificate-signing-requests.md

 From kubernetes-the-hard-way:

 /tmp/kubernetes-the-hard-way/docs/04-certificate-authority.md
 /tmp/kubernetes-the-hard-way/docs/05-kubernetes-configuration-files.md
 /tmp/kubernetes-the-hard-way/docs/09-bootstrapping-kubernetes-workers.md

 The KTHW docs show the exact openssl / cfssl commands to generate each cert, with
 the CN and O fields spelled out for every component. This makes it clear why the kubelet
 CN must be system:node:<name> and why the controller manager uses system:kube-controller-manager.

 Key questions to answer from these files:
 - Does the existing guide cover CertificateSigningRequest (CSR) API objects and the
 certificates.k8s.io/v1 API group?
 - Is kubelet TLS bootstrapping (the initial bootstrap token flow) documented?
 - Is manual CA rotation (replacing ca.crt/ca.key) covered?
 - Are kubeadm certs check-expiration and kubeadm certs renew <name> (per-cert renewal)
 documented alongside the renew all shortcut?
 - What exact CN / O fields go in each cert (kube-scheduler, kube-controller-manager,
 kube-proxy, admin) and how do those map to RBAC identities?

 Authentication / Authorization Docs to Read

 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/authentication.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/authorization.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/rbac.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/node.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/bootstrap-tokens.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/kubelet-authn-authz.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/service-accounts-admin.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/controlling-access.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/service-accounts.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/rbac-good-practices.md

 Key questions to answer:
 - What authentication modes exist (X.509 client certs, bearer tokens, OIDC, webhook, static file)?
 - What is the Node authorizer and why does it exist alongside RBAC?
 - What are the built-in ClusterRoles every exam candidate should know
 (cluster-admin, admin, edit, view, system:node, system:masters)?
 - What is --anonymous-auth and what risk does it carry?
 - How does bound service account token projection differ from the legacy secret-based SA token?
 - What is the TokenRequest API and TokenRequestProjection?

 Encryption at Rest Docs to Read

 /tmp/kubernetes-website/content/en/docs/tasks/administer-cluster/encrypt-data.md
 /tmp/kubernetes-website/content/en/docs/tasks/administer-cluster/decrypt-data.md
 /tmp/kubernetes-website/content/en/docs/tasks/administer-cluster/kms-provider.md
 /tmp/kubernetes-website/content/en/docs/concepts/configuration/secret.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/secrets-good-practices.md

 Key questions to answer:
 - What providers are available in EncryptionConfiguration? (identity, aescbc, aesgcm,
 secretbox, kms)
 - What resources can be encrypted? (Secrets, ConfigMaps, ServiceAccounts, Leases, etc.)
 - How does KMS v2 differ from v1?
 - What is the correct process to verify encryption is active (read raw etcd value)?

 Pod Security Docs to Read

 /tmp/kubernetes-website/content/en/docs/concepts/security/pod-security-standards.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/pod-security-admission.md
 /tmp/kubernetes-website/content/en/docs/tasks/configure-pod-container/security-context.md
 /tmp/kubernetes-website/content/en/docs/tutorials/security/seccomp.md
 /tmp/kubernetes-website/content/en/docs/tutorials/security/apparmor.md
 /tmp/kubernetes-website/content/en/docs/concepts/security/linux-kernel-security-constraints.md

 Key questions to answer:
 - What are the three Pod Security Standard levels (privileged, baseline, restricted)?
 - What namespace labels are used to enforce PSS (pod-security.kubernetes.io/enforce, warn, audit)?
 - What fields does a SecurityContext accept at pod level vs container level?
 - How is a seccomp profile specified (runtime/default, localhost, unconfined)?
 - How is AppArmor applied (annotation vs field in 1.30+)?
 - What are the SELinux context fields (level, role, type, user)?

 Admission Controller Docs to Read

 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/admission-controllers.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/extensible-admission-controllers.md
 /tmp/kubernetes-website/content/en/docs/reference/access-authn-authz/validating-admission-policy.md

 Key questions to answer:
 - Which admission controllers are enabled by default?
 - What is the difference between MutatingAdmissionWebhook and ValidatingAdmissionWebhook?
 - What is CEL-based ValidatingAdmissionPolicy and when was it GA?
 - Which admission controllers are specifically relevant to CKS (NodeRestriction,
 PodSecurity, ImagePolicyWebhook)?

 Audit Logging Docs to Read

 /tmp/kubernetes-website/content/en/docs/tasks/debug/debug-cluster/audit.md

 Key questions to answer:
 - What are the four audit levels: None, Metadata, Request, RequestResponse?
 - What are the three audit backends: log, webhook, dynamic?
 - What does omitStages do?
 - What are the --audit-policy-file and --audit-log-path API server flags?

 Network Policy Docs to Read

 /tmp/kubernetes-website/content/en/docs/concepts/services-networking/network-policies.md
 /tmp/kubernetes-website/content/en/docs/tasks/administer-cluster/declare-network-policy.md

 Key questions to answer:
 - What is the default behavior when no NetworkPolicy selects a pod?
 - How do you implement default-deny-all ingress and egress?
 - What is the DNS egress exception (port 53 UDP+TCP) and why is it always needed with deny-all?
 - What is the difference between ipBlock, namespaceSelector, podSelector in a
 NetworkPolicy rule?

 ---
 Step 2 — Gap Analysis

 After reading each set of files in Step 1, record every topic present in the official docs that is
 absent or underdeveloped in the existing TLS guide. Confirmed gaps based on research:

 Gaps in TLS Section (vs existing content)

 - CertificateSigningRequest API (CSR objects, kubectl certificate approve/deny)
 - Kubelet TLS bootstrapping (initial bootstrap token, RBAC for bootstrapping, the
 system:bootstrappers group)
 - Manual CA rotation procedure (replacing ca.crt+ca.key across all nodes)
 - kubeadm certs check-expiration command (shows days-to-expiry per cert)
 - kubeadm certs renew <specific-cert> (renewing one cert at a time)
 - openssl x509 -in cert.crt -noout -text pattern for inspecting certs at exam time

 Gaps — New Sections (wholly absent from existing file)

 - Authentication modes: X.509 client certs, bootstrap tokens, static token file, OIDC,
 webhook, anonymous-auth disable pattern
 - RBAC: Role, ClusterRole, RoleBinding, ClusterRoleBinding — YAML structure, built-in
 roles, aggregation rules, --dry-run=client -o yaml imperative pattern
 - Node Authorizer: why it exists, system:node:<name> CN requirement, NodeRestriction plugin
 - Service Account Tokens: legacy secret-based vs bound projected token, expirationSeconds,
 TokenRequest API
 - Encryption at Rest: full EncryptionConfiguration YAML, provider priority order, how to
 verify encryption, KMS overview
 - Pod Security Standards: three levels, namespace labels, warn vs enforce vs audit modes
 - SecurityContext: full pod-level vs container-level fields reference table
 - Seccomp: RuntimeDefault, Localhost, profile path, securityContext.seccompProfile
 - AppArmor: annotation syntax (pre-1.30) vs securityContext.appArmorProfile (1.30+)
 - SELinux: seLinuxOptions fields, when to use
 - NetworkPolicy: default-deny pattern, DNS exception, ingress/egress combined spec
 - Audit Logging: policy YAML, four levels, log backend flags, exam patterns
 - Admission Controllers: which are on by default, NodeRestriction, PodSecurity,
 LimitRanger, ResourceQuota

 ---
 Step 3 — Edit kubernetes Files Ref.md

 Remove the TLS guide from the existing file. The content to remove starts at line 180:

 # Kubernetes TLS and Identity: The Master Guide

 and ends at line 380 (end of file). The file should end at line 178 (        └── kubernetes.io~configmap/             # ConfigMap volumes mounted into the pod) closing the worker node tree block.

 Exact edit: Delete from the blank line after the closing ``` of the worker node tree
 (line 178) through the end of file. The file should end cleanly after the worker node code block.

 ---
 Step 4 — Create ref/Kubernetes TLS and Security Ref.md

 Create the new file with the full structure below. Content is written from scratch using the
 official docs (cloned in Step 0, read in Step 1), the migrated existing TLS guide content,
 and gap-filling from Step 2. Every section must be actionable at exam time — commands,
 YAML patterns, and quick-reference tables preferred over prose.

 ---
 Full Outline of ref/Kubernetes TLS and Security Ref.md

 ---
 Preamble

 # Kubernetes TLS and Security Reference

 CKA / CKAD / CKS exam-focused reference. Sourced from kubernetes/website docs and kubeadm defaults.

 ---
 Part 1: TLS / PKI / Certificates

 1.1 — The Two TLS Roles (Server vs Client)

 Explain that every connection has a listener (server cert) and an initiator (client cert). Table:

 ┌────────────────┬─────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
 │   Component    │         Server Role         │                          Client Role (as initiator)                          │
 ├────────────────┼─────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ kube-apiserver │ Port 6443 (apiserver.crt)   │ → etcd (apiserver-etcd-client.crt), → kubelet (apiserver-kubelet-client.crt) │
 ├────────────────┼─────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ kubelet        │ Port 10250 (kubelet.crt)    │ → apiserver (kubelet-client-current.pem)                                     │
 ├────────────────┼─────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ etcd           │ Port 2379 (etcd/server.crt) │ ← only kube-apiserver (authorized)                                           │
 ├────────────────┼─────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
 │ etcd peer      │ Port 2380 (etcd/peer.crt)   │ → other etcd members                                                         │
 └────────────────┴─────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

 1.2 — PKI File Map (/etc/kubernetes/pki/)

 Full annotated table of every cert/key under /etc/kubernetes/pki/ and /etc/kubernetes/pki/etcd/
 — migrated and expanded from the existing TLS guide.

 1.3 — HA Cluster Cert Distribution Strategy

 Migrated from existing section 3. Table showing: Kubelet (unique per node), etcd (unique per node),
 API Server (shared with all master IPs + LB SAN), Scheduler/Controller-Manager (shared by role),
 SA keys (identical copy on all masters).

 1.4 — Non-TLS Keys in the PKI Directory

 - sa.key / sa.pub — JWT signing key pair (migrated from existing section 5)
 - front-proxy-ca.crt / front-proxy-client.crt — API aggregation proxy (migrated)
 - etcd isolated CA rationale (migrated)

 1.5 — Certificate Renewal Reference

 Migrated renewal tables from existing sections 6 and 7, plus new content:

 - kubeadm certs check-expiration — shows days-to-expiry per cert
 - kubeadm certs renew <name> — renew a single cert (e.g., kubeadm certs renew apiserver)
 - kubeadm certs renew all — renew all certs at once
 - After renewal: restart static pods + re-copy admin.conf
 - CA cert rotation: 10-year validity, full manual procedure overview

 1.6 — CertificateSigningRequest (CSR) API

 Complete new section covering the certificates.k8s.io/v1 API:

 - Why it exists: allows in-cluster cert issuance without touching CA files directly
 - YAML structure of a CertificateSigningRequest object
 - kubectl certificate approve <name> / kubectl certificate deny <name>
 - Exam pattern: generate key + CSR → create CSR object → approve → extract cert

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
 EOF

 kubectl certificate approve jane
 kubectl get csr jane -o jsonpath='{.status.certificate}' | base64 -d > jane.crt

 1.7 — Kubelet TLS Bootstrapping

 Explain the flow for adding a new node to the cluster:

 1. Bootstrap token issued on the control plane
 2. Node starts kubelet with --bootstrap-kubeconfig pointing to a kubeconfig that uses the token
 3. Kubelet submits a CSR for its client cert (using system:bootstrappers group)
 4. Bootstrap CSR auto-approved (if system:node-bootstrapper ClusterRoleBinding exists)
 5. Cert issued → kubelet writes dated .pem + updates symlink → normal operation begins
 6. kubelet cert rotation: serverTLSBootstrap: true in kubelet-config.yaml enables
 server cert auto-rotation

 1.8 — Inspecting Certs at Exam Time

 Quick reference for cert inspection commands:

 openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | grep -A2 "Subject\|Issuer\|Not After\|DNS\|IP"
 kubeadm certs check-expiration

 ---
 Part 2: Authentication & Authorization

 2.1 — Authentication Mechanisms

 Table of all authentication strategies the API server supports:

 ┌───────────────────────┬─────────────────────────────────────┬────────────────────────────────────────────┐
 │        Method         │            How it works             │                 Enabled by                 │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ X.509 client certs    │ CN = username, O = group            │ --client-ca-file                           │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ Static token file     │ Bearer token in request header      │ --token-auth-file (discouraged)            │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ Bootstrap tokens      │ system:bootstrappers group tokens   │ --enable-bootstrap-token-auth              │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ ServiceAccount tokens │ JWT signed with sa.key              │ Always on                                  │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ OIDC                  │ ID token from external IdP          │ --oidc-issuer-url                          │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ Webhook               │ Delegates authn to external service │ --authentication-token-webhook-config-file │
 ├───────────────────────┼─────────────────────────────────────┼────────────────────────────────────────────┤
 │ Anonymous             │ Requests with no credentials        │ Disabled with --anonymous-auth=false       │
 └───────────────────────┴─────────────────────────────────────┴────────────────────────────────────────────┘

 2.2 — Service Account Tokens

 Difference between legacy and projected tokens:

 ┌──────────┬──────────────────────────┬───────────────────────────────┐
 │          │     Legacy SA Token      │    Projected (Bound) Token    │
 ├──────────┼──────────────────────────┼───────────────────────────────┤
 │ Storage  │ Stored as Secret in etcd │ Never written to disk         │
 ├──────────┼──────────────────────────┼───────────────────────────────┤
 │ Expiry   │ Never expires            │ Default 1 hour (configurable) │
 ├──────────┼──────────────────────────┼───────────────────────────────┤
 │ Audience │ Any                      │ Bound to specific audience    │
 ├──────────┼──────────────────────────┼───────────────────────────────┤
 │ Rotation │ No                       │ Auto-rotated by kubelet       │
 ├──────────┼──────────────────────────┼───────────────────────────────┤
 │ API      │ Not recommended          │ TokenRequest API              │
 └──────────┴──────────────────────────┴───────────────────────────────┘

 How to request a token manually:

 kubectl create token my-sa --duration=1h --audience=my-service

 2.3 — Authorization Modes Overview

 Explain that the API server evaluates authorizers in order (first allow wins):

 - Node — kubelet-specific permissions
 - RBAC — standard rules
 - Webhook — delegate to external service
 - ABAC — file-based (legacy, not recommended)

 Configured via --authorization-mode=Node,RBAC on kube-apiserver.

 2.4 — Node Authorization

 - The Node authorizer grants kubelets access only to resources bound to their own node
 - Kubelet's identity must match system:node:<nodeName> CN format
 - Enforced by NodeRestriction admission controller (kubelets cannot modify other nodes' objects)

 ---
 Part 3: RBAC

 3.1 — RBAC Resource Types

 Four API objects:

 ┌────────────────────┬──────────────┬────────────────────────────────────────────────────────┐
 │      Resource      │    Scope     │                      What it does                      │
 ├────────────────────┼──────────────┼────────────────────────────────────────────────────────┤
 │ Role               │ Namespaced   │ Grants permissions within one namespace                │
 ├────────────────────┼──────────────┼────────────────────────────────────────────────────────┤
 │ ClusterRole        │ Cluster-wide │ Grants permissions globally or across namespaces       │
 ├────────────────────┼──────────────┼────────────────────────────────────────────────────────┤
 │ RoleBinding        │ Namespaced   │ Binds a Role or ClusterRole to subjects in a namespace │
 ├────────────────────┼──────────────┼────────────────────────────────────────────────────────┤
 │ ClusterRoleBinding │ Cluster-wide │ Binds a ClusterRole to subjects cluster-wide           │
 └────────────────────┴──────────────┴────────────────────────────────────────────────────────┘

 3.2 — RBAC YAML Patterns

 Role example:

 apiVersion: rbac.authorization.k8s.io/v1
 kind: Role
 metadata:
   namespace: default
   name: pod-reader
 rules:
 - apiGroups: [""]
   resources: ["pods"]
   verbs: ["get", "watch", "list"]

 RoleBinding example:

 apiVersion: rbac.authorization.k8s.io/v1
 kind: RoleBinding
 metadata:
   name: read-pods
   namespace: default
 subjects:
 - kind: User
   name: jane
   apiGroup: rbac.authorization.k8s.io
 roleRef:
   kind: Role
   name: pod-reader
   apiGroup: rbac.authorization.k8s.io

 3.3 — Imperative RBAC Commands (Exam Speed)

 # Create Role
 kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default

 # Create ClusterRole
 kubectl create clusterrole node-reader --verb=get,list --resource=nodes

 # Create RoleBinding
 kubectl create rolebinding jane-pod-reader --role=pod-reader --user=jane -n default

 # Create ClusterRoleBinding
 kubectl create clusterrolebinding jane-node-reader --clusterrole=node-reader --user=jane

 # Check permissions
 kubectl auth can-i list pods --as=jane -n default
 kubectl auth can-i '*' '*' --as=jane

 3.4 — Built-in ClusterRoles

 ┌────────────────────────────────┬──────────────────────────────────────────────────────────────────────┐
 │          ClusterRole           │                                Grants                                │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ cluster-admin                  │ Full access to everything (bound via ClusterRoleBinding = superuser) │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ admin                          │ Full access within a namespace (used with RoleBinding)               │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ edit                           │ Read/write most resources, no Role/RoleBinding access                │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ view                           │ Read-only all resources                                              │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ system:node                    │ Kubelet permissions (bound via NodeRestriction)                      │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ system:kube-scheduler          │ Permissions for kube-scheduler                                       │
 ├────────────────────────────────┼──────────────────────────────────────────────────────────────────────┤
 │ system:kube-controller-manager │ Permissions for kube-controller-manager                              │
 └────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘

 3.5 — RBAC Best Practices (CKS-Relevant)

 - Grant least privilege — never bind cluster-admin to a ServiceAccount
 - Avoid wildcard verbs (*) and resources (*) in production
 - ServiceAccounts should be namespace-scoped with minimal permissions
 - Regularly audit with kubectl auth can-i --list --as=<user>
 - system:masters group bypasses RBAC entirely — never assign to regular users

 ---
 Part 4: Encryption at Rest & Secrets

 4.1 — Why Encrypt Secrets at Rest

 By default, Secrets in etcd are stored as base64-encoded plaintext. Anyone with etcd access
 can read them. Encryption at rest makes Secrets unreadable without the key even with raw etcd access.

 4.2 — EncryptionConfiguration YAML

 Full example covering all providers:

 apiVersion: apiserver.config.k8s.io/v1
 kind: EncryptionConfiguration
 resources:
 - resources: [secrets, configmaps]
   providers:
   - aescbc:
       keys:
       - name: key1
         secret: <base64-encoded-32-byte-key>
   - identity: {}   # fallback: existing unencrypted data can still be read

 Provider priority: first provider is used for write; all providers are tried on read.
 identity: {} as last provider allows reading pre-existing unencrypted data during migration.

 4.3 — Available Encryption Providers

 ┌───────────┬─────────────────────────┬────────────────────────────────────┐
 │ Provider  │        Algorithm        │               Notes                │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ identity  │ None (plaintext)        │ Default — no encryption            │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ aescbc    │ AES-CBC + PKCS7 padding │ Stable, recommended for most cases │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ aesgcm    │ AES-GCM                 │ Faster, but key reuse risk         │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ secretbox │ XSalsa20+Poly1305       │ Fast, strong                       │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ kms v1    │ External KMS via gRPC   │ Envelope encryption                │
 ├───────────┼─────────────────────────┼────────────────────────────────────┤
 │ kms v2    │ External KMS via gRPC   │ GA in 1.29, local DEK caching      │
 └───────────┴─────────────────────────┴────────────────────────────────────┘

 4.4 — Enabling Encryption: API Server Flags

 --encryption-provider-config=/etc/kubernetes/encryption-config.yaml

 Add to kube-apiserver static pod manifest. After restart:

 # Verify a secret is encrypted in etcd
 ETCDCTL_API=3 etcdctl \
   --endpoints=https://127.0.0.1:2379 \
   --cacert=/etc/kubernetes/pki/etcd/ca.crt \
   --cert=/etc/kubernetes/pki/etcd/server.crt \
   --key=/etc/kubernetes/pki/etcd/server.key \
   get /registry/secrets/default/my-secret | hexdump -C | head -5
 # Encrypted output starts with "k8s:enc:aescbc:v1:key1:..."

 4.5 — Rotating the Encryption Key

 1. Add new key as the first entry in providers
 2. Restart API server (picks up new config)
 3. Re-encrypt all existing secrets: kubectl get secrets -A -o json | kubectl replace -f -
 4. Remove old key from config
 5. Restart API server again

 4.6 — Secrets Best Practices (CKS)

 - Use stringData in manifests, never commit raw data values to git
 - Mount secrets as volumes instead of env vars when possible (env vars leak into logs)
 - Use imagePullSecrets for registry credentials
 - Prefer external secret managers (Vault, CSI secret store) for production
 - Enable encryption at rest — verify with etcdctl hex dump
 - RBAC: restrict get/list/watch on Secrets to only what needs it

 ---
 Part 5: Pod & Container Security

 5.1 — Pod Security Standards (PSS)

 Three policy levels (applied cluster-wide or per-namespace):

 ┌────────────┬─────────────────────────────────────────────────────────────┐
 │   Level    │                       What it allows                        │
 ├────────────┼─────────────────────────────────────────────────────────────┤
 │ privileged │ Unrestricted (same as no policy)                            │
 ├────────────┼─────────────────────────────────────────────────────────────┤
 │ baseline   │ Prevents known privilege escalations; allows most workloads │
 ├────────────┼─────────────────────────────────────────────────────────────┤
 │ restricted │ Hardened — requires non-root, no privilege escalation, etc. │
 └────────────┴─────────────────────────────────────────────────────────────┘

 Three modes (applied independently per level):

 ┌─────────┬─────────────────────────────────────────────────────────────┐
 │  Mode   │                           Effect                            │
 ├─────────┼─────────────────────────────────────────────────────────────┤
 │ enforce │ Pods violating policy are rejected                          │
 ├─────────┼─────────────────────────────────────────────────────────────┤
 │ audit   │ Violations are logged (audit annotation) but pods still run │
 ├─────────┼─────────────────────────────────────────────────────────────┤
 │ warn    │ User gets a warning at apply time but pods still run        │
 └─────────┴─────────────────────────────────────────────────────────────┘

 Namespace labels:

 # Enforce restricted, warn on baseline violations too
 apiVersion: v1
 kind: Namespace
 metadata:
   name: secure-ns
   labels:
     pod-security.kubernetes.io/enforce: restricted
     pod-security.kubernetes.io/enforce-version: latest
     pod-security.kubernetes.io/warn: baseline
     pod-security.kubernetes.io/audit: restricted

 5.2 — SecurityContext Reference

 Pod-level (spec.securityContext):

 ┌────────────────────┬───────────────────────────────────────────────┐
 │       Field        │                    Purpose                    │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ runAsUser          │ UID all containers run as (unless overridden) │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ runAsGroup         │ GID for all containers                        │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ runAsNonRoot       │ Reject pods that would run as root            │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ fsGroup            │ GID applied to mounted volumes                │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ supplementalGroups │ Additional GIDs                               │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ sysctls            │ Kernel parameter overrides (safe/unsafe)      │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ seccompProfile     │ Default seccomp profile for all containers    │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ seLinuxOptions     │ SELinux labels for all containers             │
 ├────────────────────┼───────────────────────────────────────────────┤
 │ appArmorProfile    │ AppArmor profile (Kubernetes 1.30+)           │
 └────────────────────┴───────────────────────────────────────────────┘

 Container-level (spec.containers[].securityContext):

 ┌──────────────────────────┬────────────────────────────────────────────────────────┐
 │          Field           │                        Purpose                         │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ allowPrivilegeEscalation │ Set to false to prevent setuid escalation              │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ privileged               │ Full root privileges — never set in production         │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ readOnlyRootFilesystem   │ Container filesystem is read-only                      │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ capabilities.drop        │ Drop Linux capabilities (e.g., ["ALL"])                │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ capabilities.add         │ Add specific capabilities (e.g., ["NET_BIND_SERVICE"]) │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ runAsUser                │ Override pod-level UID for this container              │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ runAsNonRoot             │ Override pod-level flag for this container             │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ seccompProfile           │ Override pod-level seccomp profile                     │
 ├──────────────────────────┼────────────────────────────────────────────────────────┤
 │ seLinuxOptions           │ Override pod-level SELinux labels                      │
 └──────────────────────────┴────────────────────────────────────────────────────────┘

 5.3 — Seccomp

 Seccomp (secure computing mode) restricts which syscalls a container may make.

 securityContext:
   seccompProfile:
     type: RuntimeDefault    # use container runtime's default profile
     # type: Localhost       # use a custom profile from the node
     # localhostProfile: profiles/my-profile.json  # (required if type: Localhost)
     # type: Unconfined      # no restriction (default if omitted pre-1.27)

 RuntimeDefault is safe for most workloads and is CKS-recommended.

 5.4 — AppArmor

 AppArmor profiles are node-local (must be loaded on every node where pods can schedule).

 Pre-1.30 (annotation-based):

 metadata:
   annotations:
     container.apparmor.security.beta.kubernetes.io/<container-name>: runtime/default
     # or: localhost/<profile-name>
     # or: unconfined

 Kubernetes 1.30+ (field-based):

 securityContext:
   appArmorProfile:
     type: RuntimeDefault
     # type: Localhost
     # localhostProfile: my-profile   # (required if type: Localhost)

 5.5 — SELinux

 securityContext:
   seLinuxOptions:
     level: "s0:c123,c456"
     role: ""
     type: ""
     user: ""

 level (MCS label) is the most commonly set field. Containers sharing a level can access
 each other's volumes.

 ---
 Part 6: NetworkPolicy

 6.1 — Default Behavior Without NetworkPolicy

 Without any NetworkPolicy selecting a pod: all ingress and egress is allowed.
 Once at least one NetworkPolicy selects a pod, only explicitly allowed traffic is permitted.

 6.2 — Default Deny All (Ingress + Egress)

 Apply to every namespace that contains workloads:

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

 6.3 — DNS Egress Exception

 After applying a deny-all egress policy, DNS resolution breaks for all pods in the namespace.
 Always add this exception when using deny-all egress:

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

 6.4 — Selector Types

 ┌─────────────────────────────────┬─────────────────────────────────────────────┐
 │        Selector in rule         │               What it matches               │
 ├─────────────────────────────────┼─────────────────────────────────────────────┤
 │ podSelector                     │ Pods with specific labels (same namespace)  │
 ├─────────────────────────────────┼─────────────────────────────────────────────┤
 │ namespaceSelector               │ All pods in matching namespaces             │
 ├─────────────────────────────────┼─────────────────────────────────────────────┤
 │ namespaceSelector + podSelector │ Pods with label X in namespace with label Y │
 ├─────────────────────────────────┼─────────────────────────────────────────────┤
 │ ipBlock                         │ CIDR range (external IPs)                   │
 └─────────────────────────────────┴─────────────────────────────────────────────┘

 6.5 — Common Exam Patterns

 Allow frontend → backend on port 8080:

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

 ---
 Part 7: Audit Logging

 7.1 — Why Audit

 Audit logs record every request to the API server: who, what, when, and the response code.
 Required for CKS — you must be able to write an audit policy and read audit log output.

 7.2 — Audit Levels

 ┌─────────────────┬────────────────────────────────────────────────────────────────────────┐
 │      Level      │                             What is logged                             │
 ├─────────────────┼────────────────────────────────────────────────────────────────────────┤
 │ None            │ Nothing — request is silently ignored in audit                         │
 ├─────────────────┼────────────────────────────────────────────────────────────────────────┤
 │ Metadata        │ Request metadata only (user, verb, resource, namespace, response code) │
 ├─────────────────┼────────────────────────────────────────────────────────────────────────┤
 │ Request         │ Metadata + request body (no response body)                             │
 ├─────────────────┼────────────────────────────────────────────────────────────────────────┤
 │ RequestResponse │ Everything — request body + response body                              │
 └─────────────────┴────────────────────────────────────────────────────────────────────────┘

 7.3 — Audit Policy YAML

 apiVersion: audit.k8s.io/v1
 kind: Policy
 omitStages: [RequestReceived]   # skip noisy early stage
 rules:
 - level: RequestResponse
   resources:
   - group: ""
     resources: [secrets]
 - level: Metadata
   resources:
   - group: ""
     resources: [pods, services]
 - level: None
   users: [system:kube-proxy]
 - level: Metadata
   userGroups: [system:nodes]
 - level: None
   nonResourceURLs: [/healthz, /readyz, /livez]
 - level: Metadata        # catch-all

 7.4 — API Server Flags

 --audit-policy-file=/etc/kubernetes/audit-policy.yaml
 --audit-log-path=/var/log/kubernetes/audit.log
 --audit-log-maxage=30
 --audit-log-maxbackup=10
 --audit-log-maxsize=100

 Add these to the kube-apiserver static pod manifest command args. Mount the policy file
 into the static pod with a hostPath volume.

 ---
 Part 8: Admission Controllers

 8.1 — What Admission Controllers Do

 Admission controllers intercept API requests after authentication and authorization but before
 the object is persisted. They can mutate or validate the request.

 8.2 — Controllers Enabled by Default (kubeadm)

 NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass,
 DefaultTolerationSeconds, MutatingAdmissionWebhook, ValidatingAdmissionWebhook,
 ResourceQuota, NodeRestriction, PodSecurity

 Configured via: --enable-admission-plugins=... on kube-apiserver.

 8.3 — Key Controllers for CKS

 ┌────────────────────────────┬──────────────────────────────────────────────────────────────┐
 │         Controller         │                         What it does                         │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ NodeRestriction            │ Limits kubelet to only modify objects for its own node       │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ PodSecurity                │ Enforces Pod Security Standards based on namespace labels    │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ LimitRanger                │ Applies default resource requests/limits to pods             │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ ResourceQuota              │ Limits total resource consumption per namespace              │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ ImagePolicyWebhook         │ Delegates image allow/block decisions to an external webhook │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ MutatingAdmissionWebhook   │ Calls external webhook that can modify objects               │
 ├────────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ ValidatingAdmissionWebhook │ Calls external webhook that can accept/reject objects        │
 └────────────────────────────┴──────────────────────────────────────────────────────────────┘

 8.4 — ValidatingAdmissionPolicy (CEL-based, GA in 1.30)

 New alternative to webhooks — pure in-cluster, no external service needed:

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
 Part 9: Cluster Security Quick-Reference (CKS Checklist)

 A final condensed checklist for exam day:

 - --anonymous-auth=false on API server and kubelet
 - --authorization-mode=Node,RBAC (no AlwaysAllow)
 - --profiling=false on API server, controller-manager, scheduler
 - Audit policy present + log backend configured
 - Encryption at rest enabled for Secrets (verify via etcdctl hex)
 - PodSecurity admission enabled; namespaces labeled with enforce level
 - NodeRestriction admission controller enabled
 - Network policies: default-deny-all + DNS egress exception in every namespace
 - Kubelet: --read-only-port=0, --protect-kernel-defaults=true, anonymous auth disabled
 - RBAC: no wildcard verbs for SA tokens; cluster-admin not bound to SAs
 - Secrets mounted as volumes (not env vars) where possible
 - Seccomp RuntimeDefault applied cluster-wide or per pod
 - AppArmor runtime/default applied to critical pods
 - ServiceAccounts: automountServiceAccountToken: false when not needed
 - Certificates: check expiration with kubeadm certs check-expiration; renew with
 kubeadm certs renew all

 ---
 Step 5 — Verification

 After completing Steps 3 and 4:

 1. Read kubernetes Files Ref.md — confirm it ends after the worker node tree block
 (line ~178) and contains no TLS content. Word count should be around 180 lines.
 2. Read Kubernetes TLS and Security Ref.md — confirm all 9 parts are present,
 YAML examples are valid, tables are formatted correctly.
 3. Line count check — the new security file should be at minimum 400 lines of content
 (not counting blank lines), reflecting the depth required for CKS coverage.
 4. Spot-check against official docs — confirm the CSR exam pattern (Step 1.6),
 the EncryptionConfiguration provider table (Step 4.3), and the PSS label format
 (Step 5.1) match what was read from /tmp/kubernetes-website/.
 5. Cross-reference the controllers reference — open
 ref/Kubernetes Controllers Reference.md and confirm there is no TLS content
 duplicated there that also lives in the new security file.

 ---
 Execution Order Summary

 ┌─────┬─────────────────────────────────────────────────────────────────────────┬─────────────────┐
 │  #  │                                 Action                                  │      Tool       │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 0a  │ Clone kubernetes/website to /tmp/kubernetes-website (sparse, docs only) │ Bash            │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 0b  │ Clone kubernetes-the-hard-way to /tmp/kubernetes-the-hard-way           │ Bash            │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 1a  │ Read TLS+PKI files from both repos in parallel                          │ Read (parallel) │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 1b  │ Read auth/authz/RBAC files from kubernetes/website                      │ Read (parallel) │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 1c  │ Read encryption, pod security, admission, audit, NetworkPolicy files    │ Read (parallel) │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 1d  │ Read KTHW bootstrap chapters (cert CN/O fields, kubeconfig generation)  │ Read (parallel) │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 2   │ Gap analysis: identify missing/shallow topics vs both repos             │ (analysis)      │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 3   │ Edit kubernetes Files Ref.md: delete lines 180–end of file              │ Edit            │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 4   │ Create ref/Kubernetes TLS and Security Ref.md with all 9 parts          │ Write           │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 5a  │ Read both ref files to verify completeness                              │ Read            │
 ├─────┼─────────────────────────────────────────────────────────────────────────┼─────────────────┤
 │ 5b  │ Line count: wc -l ref/*.md                                              │ Bash            │
 └─────┴─────────────────────────────────────────────────────────────────────────┴─────────────────┘

 Steps 0a and 0b run in parallel (two Bash calls in one message).
 Steps 1a, 1b, 1c, 1d run in parallel after both clones complete.
 Steps 3 and 4 run sequentially after analysis.
 Step 5 runs after Step 4.

 Depth Requirements for the New File

 The new file must go beyond a cheatsheet. Every major section must include at least one of:
 - Internal flow diagram (ASCII or prose walk-through of what happens step-by-step)
 - "What breaks if X is missing/expired" — concrete failure mode for each cert/config
 - CN/O field tables — showing how TLS identity maps to RBAC group membership
 - "Why" explanations — e.g. why etcd has its own CA, why SA keys must be identical across
 HA masters, why the kubelet CN must include the node name

 This ensures the file teaches internals, not just commands.


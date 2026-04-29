# CKS Exam Practice Context

The following provides the specific grading rubrics and parameters for the Certified Kubernetes Security Specialist (CKS) simulation. Combine this with the base Terminal Simulation Prompt.

---

## QUICK REFERENCE

You MUST use the `search-reference-material`, `search-k8s-docs`, and `search-checklist(checklist_md_path)` skills to find what you need before generating questions or scenarios.

---

## SCENARIO DESIGN RULES

- At session start, silently invent ONE broken scenario from the CKS syllabus.
- **ANTI-BIAS & REALISM:**
  - **Avoid Cliches:** Do not use `nginx`, `busybox`, or `redis` for every scenario. Invent realistic enterprise-like app names (e.g., `vault-agent`, `audit-collector`, `compliance-scanner`, `secret-rotator`).
  - **Add Noise:** Real clusters are not empty. Include unrelated pods, namespaces, ServiceAccounts, or Roles to distract the user. Deploy an unrelated workload with overly permissive RBAC that has nothing to do with the task.
  - **SSH-Based Tasks:** The real exam requires SSHing to the correct node for every question. Every task MUST specify which node(s) to SSH to when node-level work is needed. Aliases and `.vimrc` settings do NOT survive SSH -- simulate this faithfully.
  - **CKS is security-first:** Unlike CKA, CKS tasks focus on hardening, restricting, and auditing. The "correct" answer often involves removing permissions, denying access, or adding constraints -- not creating new resources.
- Rotate through these scenario types across the session:

### Cluster Setup scenarios
  - Apply a NetworkPolicy to restrict traffic between namespaces (default deny + allow specific).
  - Fix or create a NetworkPolicy that allows only specific pod-to-pod communication on specific ports.
  - Verify and remediate CIS Benchmark violations using `kube-bench` output.
  - Configure TLS termination on an Ingress with proper cert/key Secrets.
  - Audit and fix insecure API server flags in `/etc/kubernetes/manifests/kube-apiserver.yaml` (e.g., `--insecure-port`, `--anonymous-auth=true`, `--authorization-mode` missing RBAC).

### Cluster Hardening scenarios
  - Restrict access to the Kubernetes API -- configure RBAC (Role, ClusterRole, RoleBinding, ClusterRoleBinding) with least-privilege.
  - Identify and revoke overly permissive ClusterRoleBindings (e.g., a ServiceAccount bound to `cluster-admin`).
  - Disable automounting of ServiceAccount tokens in Pods that don't need API access (`automountServiceAccountToken: false`).
  - Restrict ServiceAccount token audience and expiration.
  - Upgrade a kubeadm cluster to patch a known CVE.

### System Hardening scenarios
  - Create and apply an AppArmor profile to a Pod (annotation-based or field-based in v1.35).
  - Create and apply a seccomp profile to restrict syscalls (using `securityContext.seccompProfile`).
  - Configure a Pod SecurityContext with `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, and drop all capabilities.
  - Reduce the host attack surface: identify and disable unnecessary services on a node via `systemctl`.
  - Use `RuntimeClass` to run a Pod in a sandboxed runtime (e.g., gVisor/runsc).

### Minimize Microservice Vulnerabilities scenarios
  - Enforce Pod Security Standards (PSS) on a namespace using labels (`pod-security.kubernetes.io/enforce: restricted`).
  - Create or fix an OPA Gatekeeper / Kyverno policy to deny privileged containers.
  - Manage Kubernetes Secrets encryption at rest -- configure `EncryptionConfiguration` for the API server.
  - Implement pod-to-pod mTLS using a service mesh sidecar or native certificate rotation.
  - Fix a Pod that violates the `restricted` Pod Security Standard (e.g., uses `hostNetwork`, `hostPID`, or `privileged`).

### Supply Chain Security scenarios
  - Scan container images for vulnerabilities using `trivy` and identify images with CRITICAL CVEs.
  - Create an ImagePolicyWebhook or admission controller to reject images from untrusted registries.
  - Verify image signatures using `cosign verify`.
  - Write or fix an admission policy that enforces a specific image registry prefix (e.g., all images must come from `registry.internal.io/`).
  - Identify Pods running images with known vulnerabilities and update them to patched versions.

### Monitoring, Logging, and Runtime Security scenarios
  - Create or fix a Falco rule to detect suspicious activity (e.g., shell spawned in a container, sensitive file read).
  - Analyze audit log entries to identify who performed a specific unauthorized action.
  - Configure Kubernetes audit policy (`/etc/kubernetes/audit-policy.yaml`) to log specific API requests at the `RequestResponse` level.
  - Set up audit logging by modifying the API server static pod manifest with `--audit-policy-file` and `--audit-log-path`.
  - Identify a compromised container by examining `crictl` output, process lists, and audit logs, then kill and remediate.

### Security-focused trap scenarios (high-value exam gotchas)
  - **RBAC verb trap:** RoleBinding exists but the Role is missing the `get` verb -> user can `list` but not `get` individual resources.
  - **NetworkPolicy direction trap:** User creates an ingress policy but the traffic is egress-bound -> policy has no effect.
  - **SecurityContext inheritance:** Pod-level SecurityContext is overridden by container-level SecurityContext -> user sets `runAsNonRoot` at pod level but one container overrides it.
  - **ServiceAccount token auto-mount:** User creates a Pod with a restricted ServiceAccount but forgets `automountServiceAccountToken: false` on the SA or Pod -> token is still mounted at `/var/run/secrets/kubernetes.io/serviceaccount/`.
  - **Audit policy not loaded:** User creates the audit policy file but forgets to add `--audit-policy-file` flag to the API server manifest -> no audit logs generated.
  - **AppArmor profile not loaded:** User references an AppArmor profile in the Pod spec but the profile is not loaded on the target node -> Pod stays in `Blocked` state.
  - **EncryptionConfiguration restart:** User updates the encryption config but doesn't wait for the API server static pod to restart -> Secrets are still stored unencrypted.
  - **Falco rule syntax:** Missing YAML quoting or incorrect field names in Falco rules -> Falco silently ignores the rule.
  - **SSH environment trap:** Same as CKA -- aliases and `.vimrc` are lost on SSH to cluster nodes.

---

## SYLLABUS ROTATION

Track coverage. **Do not repeat a domain until all six are done.** Then cycle again.

```
[ ] Cluster Setup                                  10%
[ ] Cluster Hardening                              15%
[ ] System Hardening                               15%
[ ] Minimize Microservice Vulnerabilities          20%
[ ] Supply Chain Security                          20%
[ ] Monitoring, Logging, and Runtime Security      20%
```

Weight toward **Minimize Microservice Vulnerabilities** (20%), **Supply Chain Security** (20%), and **Monitoring, Logging, and Runtime Security** (20%) -- they collectively make up 60% of the exam.

---

## ADDITIONAL TOOLS ON `dev`

In addition to the tools listed in `simulator.md`, the CKS environment has these security tools available on `dev`:

- `trivy` -- container image vulnerability scanner
- `cosign` -- image signature verification
- `falco` -- runtime security monitoring (also installed on cluster nodes)
- `kube-bench` -- CIS Kubernetes Benchmark checker (run on cluster nodes via SSH)

On cluster nodes:
- `falco` -- installed and running as a systemd service
- `kube-bench` -- available as a binary
- AppArmor utilities: `apparmor_parser`, `aa-status`, `aa-enforce`
- seccomp profiles directory: `/var/lib/kubelet/seccomp/`

---

## DIFFICULTY CURVE

| Challenge # | Difficulty | Characteristics                                                              |
|-------------|------------|------------------------------------------------------------------------------|
| 1-2         | Easy       | Single policy creation, straightforward RBAC fix                             |
| 3-4         | Medium     | Multi-step (e.g., create audit policy + update API server manifest + verify) |
| 5+          | Hard       | Cascading security issues, Falco rule writing, image scanning + remediation  |

Increase difficulty after two consecutive quick correct answers.
Hold difficulty steady if the user struggled (3+ wrong attempts on the previous scenario).

---

## SESSION START PREFERENCE

Silently invent the first scenario. Start from `Cluster Hardening` or `Minimize Microservice Vulnerabilities`.
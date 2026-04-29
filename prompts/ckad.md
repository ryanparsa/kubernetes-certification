# CKAD Exam Practice Context

The following provides the specific grading rubrics and parameters for the Certified Kubernetes Application Developer (CKAD) simulation. Combine this with the base Terminal Simulation Prompt.

---
> **Reference:** See `ckad/README.md` for the authoritative domain list, weightings, and lab mapping.

## QUICK REFERENCE

If you need a Kubernetes quick reference during the simulation, you can access the reference directory at:
`ref/`

You MUST search in `ref/` and `ckad/` for samples and factual information. You MUST use the `search-reference-material` and `search-k8s-docs` skills to find what you need before generating questions or scenarios.

---

## SCENARIO DESIGN RULES

- At session start, silently invent ONE broken scenario from the CKAD syllabus.
- **ANTI-BIAS & REALISM:**
  - **Avoid Cliches:** Do not use `nginx`, `busybox`, or `redis` for every scenario. Invent realistic enterprise-like app names (e.g., `order-processor`, `notification-svc`, `data-pipeline`, `cache-warmer`).
  - **Add Noise:** Real clusters are not empty. Include unrelated pods, namespaces, ConfigMaps, or Services to distract the user. Deploy a failing CronJob in a different namespace that has nothing to do with the task.
  - **SSH-Based Tasks:** The real exam requires SSHing to the correct node for every question. Every task MUST specify which node(s) to SSH to when node-level work is needed. Aliases and `.vimrc` settings do NOT survive SSH -- simulate this faithfully.
  - **CKAD is app-centric:** Unlike CKA, CKAD rarely requires node-level troubleshooting. Most tasks are `kubectl`-driven from `dev`. SSH is only needed when the task explicitly requires node-level inspection (e.g., checking a hostPath or verifying a container process).
- Rotate through these scenario types across the session:

### Core application scenarios
  - Build a multi-container Pod with init containers, sidecars, and shared volumes.
  - Create a Deployment with specific resource requests/limits, rolling update strategy, and readiness/liveness probes.
  - Configure a CronJob with `concurrencyPolicy`, `activeDeadlineSeconds`, and `backoffLimit`.
  - Define a Job with `completions`, `parallelism`, and a specific `restartPolicy`.
  - Build a Pod using a ConfigMap as environment variables AND as a mounted volume simultaneously.
  - Create a Secret (opaque, TLS, docker-registry) and mount it as a volume or inject as env vars.
  - Expose a Deployment via ClusterIP, NodePort, or headless Service.
  - Create a NetworkPolicy allowing ingress from a specific namespace label selector and egress to a CIDR block.
  - Configure a PersistentVolumeClaim with a specific StorageClass and access mode, then mount it in a Pod.
  - Write a Helm chart or use `helm install` with `--set` overrides.
  - Apply a Kustomize overlay with `kubectl apply -k`.

### v1.35 new topics
  - **Native Sidecar Containers:** `initContainers` with `restartPolicy: Always` -- the GA sidecar pattern. Test that the sidecar starts before and runs alongside the main container.
  - **Gateway API:** Create an `HTTPRoute` with path-based or header-based routing rules attached to an existing Gateway; use `backendRefs[].weight` for canary traffic splitting.
  - **Helm/Kustomize:** `helm repo add` + `helm install` with value overrides; `kubectl apply -k <dir>` for Kustomize overlays with patches and transformers.
  - **In-place Pod Resource Resize:** Use `kubectl patch pod <name> --subresource resize` to update CPU/memory without restarting the pod; understand `resizePolicy` per container resource (`NotRequired` vs `RestartContainer`).
  - **User Namespaces:** Set `spec.hostUsers: false` to map container UIDs/GIDs to unprivileged host IDs — mitigates privilege escalation; understand interaction with `runAsNonRoot` and `fsGroup`.
  - **Pod Certificates:** Configure a `projected` volume with a `podCertificate` source (`signerName`, `keyType: ED25519`) to give a workload an auto-rotated X.509 identity issued by the kubelet.
  - **CEL ValidatingAdmissionPolicy (consumer perspective):** A namespace-scoped policy rejects your Deployment because `object.spec.replicas > 3`; diagnose the admission error and fix the Deployment without touching the policy itself.

### Developer-focused trap scenarios
  - **Probe misconfiguration:** `readinessProbe` pointing to wrong port or path -> Pod is Running but Endpoints list is empty -> Service returns no backends.
  - **Resource quota exhaustion:** Namespace has a ResourceQuota; Deployment creates Pods that exceed the quota -> ReplicaSet events show `forbidden: exceeded quota`.
  - **ImagePullBackOff:** Image tag typo, wrong registry, or missing imagePullSecret -> Pod stuck in `ImagePullBackOff`.
  - **ConfigMap/Secret not found:** Pod references a ConfigMap or Secret that doesn't exist -> `CreateContainerConfigError`.
  - **SecurityContext conflict:** Pod spec sets `runAsNonRoot: true` but image runs as root -> `CrashLoopBackOff` with `container has runAsNonRoot and image will run as root`.
  - **Volume mount path collision:** Two volume mounts target the same `mountPath` -> last one wins, silently shadows the other.
  - **Immutable ConfigMap/Secret:** Attempt to update an immutable ConfigMap -> error. Must delete and recreate.
  - **NetworkPolicy default deny:** A `default-deny-all` NetworkPolicy exists in the namespace -> all new Pods lose connectivity until an explicit allow policy is created.
  - **Service selector mismatch:** Service `selector` labels don't match Pod `metadata.labels` -> `kubectl get endpoints` shows no endpoints.
  - **Container command vs args:** Confusing `command` (overrides ENTRYPOINT) with `args` (overrides CMD) -> container exits immediately or runs wrong process.
  - **JSONPath / custom-columns:** Extract specific fields from `kubectl get` output using `-o jsonpath` or `-o custom-columns`. Sorting with `--sort-by`.
  - **User Namespaces + fsGroup conflict:** Pod has `hostUsers: false` and `securityContext.fsGroup: 2000`; hostPath volume is owned by root (UID 0) on the host -> container cannot write to the mount. Fix: use an `emptyDir` or remove `hostUsers: false`.
  - **In-place resize on `RestartContainer` policy:** Developer patches memory on a running container expecting zero downtime; the container restarts silently because `resizePolicy: RestartContainer` is in effect. Fix: check `resizePolicy` and either accept the restart or set `NotRequired` when supported.
  - **PSA `restricted` profile blocks privileged init container:** Namespace is labeled `pod-security.kubernetes.io/enforce: restricted`; init container runs as root (no `runAsNonRoot: true`) -> admission denied. Fix: add proper `securityContext` to init container.
  - **API deprecation silent failure:** Manifest uses `batch/v1beta1` CronJob -> `kubectl apply` on a v1.35 cluster returns `no matches for kind "CronJob" in version "batch/v1beta1"`. Fix with `kubectl convert` or update `apiVersion` to `batch/v1`.
  - **Canary rollout stuck:** Blue/green Service selector updated (`kubectl set selector`) but the `sessionAffinity: ClientIP` on the Service causes existing clients to stay pinned to old pods. Fix: set `sessionAffinity: None` before traffic switch.

---

## SYLLABUS ROTATION

Track coverage. **Do not repeat a domain until all five are done.** Then cycle again.

```
[ ] Application Design and Build                          20%
[ ] Application Deployment                                20%
[ ] Application Observability and Maintenance             15%
[ ] Application Environment, Configuration and Security   25%
[ ] Services and Networking                               20%
```

Weight toward **Application Environment, Configuration and Security** (25%) -- it's the heaviest domain and covers ConfigMaps, Secrets, SecurityContexts, ServiceAccounts, and ResourceQuotas.
Do NOT skip **Services and Networking** (20%) -- NetworkPolicy default-deny traps, Service selector mismatches, Ingress path-type gotchas, Gateway API HTTPRoutes, and DNS resolution (`nslookup`/`dig` inside pods) are all high-value traps.

---

## DIFFICULTY CURVE

| Challenge # | Difficulty | Characteristics                                                         |
|-------------|------------|-------------------------------------------------------------------------|
| 1-2         | Easy       | Single resource creation, straightforward imperative command            |
| 3-4         | Medium     | Multi-resource, requires cross-referencing (e.g., ConfigMap + Pod + Service) |
| 5+          | Hard       | Cascading misconfig, subtle label mismatches, multi-container debugging  |

Increase difficulty after two consecutive quick correct answers.
Hold difficulty steady if the user struggled (3+ wrong attempts on the previous scenario).

---

## SESSION START PREFERENCE

Silently invent the first scenario. Start from `Application Design and Build` or `Application Environment, Configuration and Security`.
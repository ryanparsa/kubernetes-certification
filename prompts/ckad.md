# CKAD Exam Practice Context

The following provides the specific grading rubrics and parameters for the Certified Kubernetes Application Developer (CKAD) simulation. Combine this with the base Terminal Simulation Prompt.

---

## QUICK REFERENCE

If you need a Kubernetes quick reference during the simulation, you can access the reference directory at:
`/Users/ryan/Projects/kubernetes-certification/ref`

If you need to search each time for a sample or more info, you can search in `/Users/ryan/Projects/kubernetes-certification/ref` and `/Users/ryan/Projects/kubernetes-certification/ckad`. Use the `grep -i -A10` command to find what you need.

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
  - **Gateway API:** Create an `HTTPRoute` with path-based or header-based routing rules attached to an existing Gateway.
  - **Helm/Kustomize:** `helm repo add` + `helm install` with value overrides; `kubectl apply -k <dir>` for Kustomize overlays with patches and transformers.

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
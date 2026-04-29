# KCNA Exam Practice Context

The following provides the specific grading rubrics and parameters for the Kubernetes and Cloud Native Associate (KCNA) simulation. Combine this with the base Terminal Simulation Prompt.

---

## QUICK REFERENCE

Your primary source of truth for the exam syllabus and specific topics to test is the checklist at:
`kcna/checklist.md`

Ensure you draw your questions and scenarios directly from the items in `kcna/checklist.md`.
Do not check the `ref/` directory or use any skills for this exam. Just use `kcna/checklist.md`.

---

## SCENARIO DESIGN RULES

- At session start, silently invent ONE question or conceptual scenario from the KCNA syllabus.
- **KCNA is a multiple-choice / conceptual exam:** The real exam tests foundational knowledge and concepts, not deep imperative terminal troubleshooting. 
- **ANTI-BIAS & REALISM:**
  - **Avoid Cliches:** Use varied, realistic examples when asking conceptual questions (e.g., instead of just "what is a pod", ask "how would an e-commerce app benefit from a Deployment over a bare Pod").
  - **Format:** Default to Multiple-Choice questions unless a different format is explicitly specified. You can present YAML spotting or architectural comparisons as multiple-choice options.
- Rotate through these scenario types across the session:

### Kubernetes Fundamentals scenarios
  - Identify the roles of control plane components (kube-apiserver, etcd, scheduler, controller-manager).
  - Determine the correct workload resource for a scenario (Deployment vs. StatefulSet vs. DaemonSet vs. Job).
  - Identify correct/incorrect label selectors and how Services route to Pods.
  - Basic kubectl command knowledge (e.g., how to get logs, describe pods, apply manifests).
  - Understand the concept of Namespaces, Resource Requests/Limits, and basic scheduling.

### Container Orchestration scenarios
  - Explain the difference between container runtimes (containerd, CRI-O) and tools like Docker.
  - Understanding OCI standards (Image, Runtime, Distribution specs).
  - Service Networking concepts (ClusterIP vs NodePort vs LoadBalancer).
  - Storage basics (Ephemeral vs Persistent, PV/PVC concepts, ConfigMaps, Secrets).

### Cloud Native Architecture scenarios
  - Distinguish between monolithic and microservices architectures.
  - Concept of autoscaling (HPA, VPA, Cluster Autoscaler).
  - CNCF maturity model (Sandbox, Incubating, Graduated) and personas (App Dev, Platform Engineer, SRE).
  - Immutable infrastructure, serverless computing, and event-driven architecture.

### Cloud Native Application Delivery scenarios
  - CI/CD concepts and the difference between Continuous Integration, Delivery, and Deployment.
  - GitOps principles and pull-based vs push-based delivery.
  - Deployment strategies (Rolling update, Blue-Green, Canary).
  - Purpose of Helm and Kustomize.

### Cloud Native Observability scenarios
  - The three pillars of observability (Metrics, Logs, Traces).
  - Understanding Prometheus metric types (Counter, Gauge, Histogram, Summary).
  - Concept of distributed tracing and tools like Jaeger/OpenTelemetry.
  - Cost optimization (FinOps) and alerting best practices.

### Conceptual trap scenarios (high-value exam gotchas)
  - **Component confusion:** Mixing up kube-proxy (networking) with ingress controller (L7 routing).
  - **Stateful vs Stateless:** Recommending Deployments for stateful database workloads.
  - **Runtime vs Tooling:** Confusing Docker (developer tool) with containerd/CRI-O (CRI runtime).
  - **Storage misunderstanding:** Thinking Secrets are encrypted at rest by default (they are only base64 encoded).
  - **Observability overlap:** Using a logging tool (Fluentd) for metrics or a tracing tool for logging.

---

## SYLLABUS ROTATION

Track coverage. **Do not repeat a domain until all five are done.** Then cycle again.

```
[ ] Kubernetes Fundamentals                              46%
[ ] Container Orchestration                              22%
[ ] Cloud Native Architecture                            16%
[ ] Cloud Native Application Delivery                    8%
[ ] Cloud Native Observability                           8%
```

Weight heavily toward **Kubernetes Fundamentals** (46%) and **Container Orchestration** (22%) -- they dominate the exam.

---

## DIFFICULTY CURVE

| Challenge # | Difficulty | Characteristics                                                    |
|-------------|------------|--------------------------------------------------------------------|
| 1-2         | Easy       | Straightforward definitions, single-component identification       |
| 3-4         | Medium     | Architectural comparisons, identifying errors in YAML snippets     |
| 5+          | Hard       | Multi-step conceptual troubleshooting, nuanced CNCF tool selection |

Increase difficulty after two consecutive quick correct answers.
Hold difficulty steady if the user struggled (3+ wrong attempts or requests for hints on the previous scenario).

---

## SESSION START PREFERENCE

Silently invent the first scenario. Start from `Kubernetes Fundamentals` or `Cloud Native Architecture`.

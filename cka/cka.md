# CKA exam guide for 2025–2026

**The CKA exam underwent its most significant curriculum overhaul in five years on February 18, 2025**, adding Gateway
API, Helm, Kustomize, CRDs/Operators, and workload autoscaling while quietly dropping etcd backup/restore and standalone
cluster upgrades from the official competency list. Despite these changes, the five domain names and their percentage
weightings remain identical to the pre-2025 version. The exam now runs on **Kubernetes v1.34** (with v1.35 rolling in),
uses an SSH-based remote desktop environment, and carries a **66% passing score** across **~17 hands-on tasks in 2 hours
**. Multiple 2025–2026 exam takers report that the updated exam is substantially harder than its predecessor, with
roughly 40% of questions covering newly added topics that standard training courses haven't yet caught up with.

---

## The five domains and their exact weightings

The official curriculum, maintained at the CNCF GitHub repository and confirmed on the Linux Foundation program changes
page, defines five domains. The domain names and percentages have not changed since the 2020 restructure — only the
competencies within each domain were updated on February 18, 2025.

| Domain                                             | Weight  | Key change                                                  |
|----------------------------------------------------|---------|-------------------------------------------------------------|
| Troubleshooting                                    | **30%** | Expanded to cover services and networking troubleshooting   |
| Cluster Architecture, Installation & Configuration | **25%** | Added Helm, Kustomize, CRDs/Operators, extension interfaces |
| Services & Networking                              | **20%** | Added Gateway API alongside traditional Ingress             |
| Workloads & Scheduling                             | **15%** | Added autoscaling (HPA/VPA), consolidated pod admission     |
| Storage                                            | **10%** | Refined to emphasize dynamic provisioning and access modes  |

**Troubleshooting at 30%** is the single largest domain and the area where candidates most often lose points. The exam
heavily tests your ability to diagnose broken clusters, failed nodes, misconfigured control plane components, and
networking issues under time pressure. Cluster Architecture at 25% is the second-largest domain and now encompasses the
broadest range of topics, from RBAC to Helm to CRDs.

---

## Detailed topic breakdown for every domain

### Cluster Architecture, Installation & Configuration (25%)

This domain expanded the most in the 2025 update. The eight competencies are:

1. **Manage role-based access control (RBAC)** — creating Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, and
   understanding service accounts
2. **Prepare underlying infrastructure for installing a Kubernetes cluster** — reworded from "provision" to "prepare,"
   reflecting a shift toward managed platforms
3. **Create and manage Kubernetes clusters using kubeadm** — covers `kubeadm init`, `kubeadm join`, and basic cluster
   lifecycle
4. **Manage the lifecycle of Kubernetes clusters** — version upgrades are folded in here rather than listed as a
   standalone competency
5. **Implement and configure a highly-available control plane** — multi-master setups, stacked vs. external etcd
   topologies
6. **Use Helm and Kustomize to install cluster components** ← *new*
7. **Understand extension interfaces (CNI, CSI, CRI, etc.)** ← *new*
8. **Understand CRDs, install and configure operators** ← *new*

### Workloads & Scheduling (15%)

1. **Understand application deployments and how to perform rolling updates and rollbacks**
2. **Use ConfigMaps and Secrets to configure applications**
3. **Configure workload autoscaling** ← *new* (HPA and VPA; replaces "know how to scale applications")
4. **Understand the primitives used to create robust, self-healing application deployments** — ReplicaSets, DaemonSets,
   StatefulSets
5. **Configure Pod admission and scheduling (limits, node affinity, etc.)** ← *new* (merges resource limits and manifest
   management)

### Services & Networking (20%)

1. **Understand connectivity between Pods** — Pod-to-Pod communication, CNI fundamentals
2. **Define and enforce Network Policies** — ingress/egress rules, namespace selectors
3. **Use ClusterIP, NodePort, LoadBalancer service types and endpoints**
4. **Use the Gateway API to manage Ingress traffic** ← *new*
5. **Know how to use Ingress controllers and Ingress resources** — traditional Ingress remains tested
6. **Understand and use CoreDNS** — service discovery, DNS debugging

### Storage (10%)

1. **Implement storage classes and dynamic volume provisioning** ← *refined*
2. **Configure volume types, access modes and reclaim policies** ← *refined*
3. **Manage persistent volumes and persistent volume claims**

### Troubleshooting (30%)

1. **Troubleshoot clusters and nodes** — NotReady nodes, kubelet failures, certificate issues
2. **Troubleshoot cluster components** — broken kube-apiserver, scheduler, controller-manager
3. **Monitor cluster and application resource usage** — `kubectl top`, metrics server
4. **Manage and evaluate container output streams** — stdout/stderr logs, `kubectl logs --previous`
5. **Troubleshoot services and networking** ← *expanded*

---

## What was removed and what's explicitly out of scope

### Competencies removed from the official curriculum

The February 2025 update removed or merged several topics that were previously standalone competencies:

- **etcd backup and restore** — removed entirely from the curriculum (though exam takers in 2025–2026 still report
  encountering etcd-related questions, likely under the broader "manage cluster lifecycle" umbrella)
- **Perform a version upgrade on a Kubernetes cluster using kubeadm** — no longer standalone; folded into "manage the
  lifecycle of Kubernetes clusters"
- **Understand host networking configuration on cluster nodes** — removed
- **Choose an appropriate container network interface plugin** — removed as standalone; CNI now falls under "extension
  interfaces"
- **Awareness of manifest management and common templating tools** — removed as standalone; Helm/Kustomize now explicit
  in Cluster Architecture

### Topics generally out of scope

There is no official exclusion list, but based on the curriculum boundaries and exam-taker reports, the following are *
*not tested**:

- Cloud provider-specific configurations (EKS, GKE, AKS specifics)
- Service mesh installation or configuration (Istio, Linkerd)
- CI/CD pipeline setup or GitOps tooling (ArgoCD configuration is borderline — some report Helm-based ArgoCD install
  questions)
- Container image building (Docker, Buildah, Kaniko)
- Advanced eBPF or Cilium-specific features beyond basic NetworkPolicy
- Multi-cluster management (Cluster API, fleet management)
- Kubernetes source code compilation or development
- Application-level development (writing code, debugging application logic)
- Multiple-choice theory questions (the exam is 100% hands-on)

---

## What changed from the previous curriculum

The CNCF announced the changes on September 5, 2024, initially targeting November 25, 2024, before confirming the *
*February 18, 2025** effective date. Any exam taken on or after that date uses the new curriculum regardless of purchase
date.

### The most consequential additions

**Gateway API** is the single biggest curriculum shift. Candidates must now understand Gateway and HTTPRoute resources
alongside traditional Ingress. The Ingress API itself (`networking.k8s.io/v1`) is not deprecated in Kubernetes core, but
the **Ingress NGINX Controller was retired in November 2025** with best-effort maintenance ending March 2026. The exam
now tests both approaches, and `https://gateway-api.sigs.k8s.io/` is an allowed documentation source during the exam.

**Helm and Kustomize** moved from a vague "awareness of manifest management and common templating tools" to explicit,
testable competencies. Exam takers report questions requiring `helm install`, `helm template`, troubleshooting stuck
Helm releases, and `kubectl apply -k` for Kustomize overlays. The `https://helm.sh/docs/` is now allowed during the
exam.

**CRDs and Operators** require understanding what Custom Resource Definitions are, how to install operators, and how
extension interfaces (CNI, CSI, CRI) work at a conceptual and practical level.

**Workload autoscaling** replaces the old "know how to scale applications" with explicit HPA and VPA configuration
tasks.

### Other notable changes

- **Passing score**: Lowered from 74% to **66%** (this change predates 2025 but is the current threshold)
- **Certification validity**: Reduced from 3 years to **2 years** for certifications earned after April 1, 2024
- **Exam simulator**: Now split into two separate Killer.sh sessions (Simulator A and Simulator B), each with 17
  questions and 36 hours of access

---

## The exam environment in detail

### Format and logistics

| Parameter              | Detail                                            |
|------------------------|---------------------------------------------------|
| Duration               | 2 hours                                           |
| Questions              | ~16–17 performance-based tasks                    |
| Passing score          | **66%**                                           |
| Format                 | 100% hands-on command-line tasks on live clusters |
| Cost                   | $445 (includes one free retake)                   |
| Results                | Emailed within 24 hours                           |
| Languages              | English, Simplified Chinese, Japanese             |
| Certification validity | 2 years                                           |

### Tools and environment

The exam runs on a **Linux remote desktop** accessed through PSI's Secure Browser. The architecture consists of a **base
node** from which you SSH into designated hosts for each task. Pre-installed tools on the SSH hosts include:

- **kubectl** with the `k` alias and bash autocompletion pre-configured
- **yq** for YAML processing
- **curl** and **wget** for connectivity testing
- **man** with man pages
- **vim** and **nano** are available on SSH hosts
- **tmux** may or may not be available; with the GUI desktop, multiple terminal windows can be opened instead

The base node itself does **not** have kubectl or other tools pre-installed — all work must happen on the SSH hosts
specified in each question.

### Allowed documentation

You get **one additional browser tab** (Firefox within the VM) for documentation. Allowed sites are:

- `https://kubernetes.io/docs/` and `https://kubernetes.io/blog/`
- `https://helm.sh/docs/`
- `https://gateway-api.sigs.k8s.io/` (CKA only)
- Task-specific documentation links provided in each question's Quick Reference box

The kubernetes.io search function works, but you **must not follow external links** from search results. The
`https://github.com/kubernetes/` repository is **no longer listed** as an allowed resource.

### Critical keyboard shortcuts

Use **Ctrl+Shift+C / Ctrl+Shift+V** for terminal copy/paste (regular Ctrl+C sends SIGINT). Use **Ctrl+Alt+W** instead of
Ctrl+W to avoid closing browser tabs. There is a ~1–2 second delay when copying from the question panel.

---

## Where candidates fail: the hardest question types

### Gateway API catches most people off guard

Multiple 2025–2026 exam takers cite **Gateway API** as the single most unexpected and difficult topic. One candidate
scored 80% on the Killer.sh simulator but only **45% on the real exam**, attributing the gap largely to Gateway API and
Helm questions. Tasks include creating Gateway resources with TLS configuration, writing HTTPRoute matching rules, and
migrating from Ingress to Gateway + HTTPRoute. Standard training courses (Udemy, KodeKloud) are still catching up to
this topic.

### Helm goes beyond basic install

The exam tests Helm troubleshooting, not just `helm install`. Reported scenarios include fixing releases stuck in
`pending-install` state, using `helm template` to render and save YAML output, upgrading releases with `--set` values
and specific `--version` flags, and installing applications (including ArgoCD) via Helm when basic commands fail.
Understanding `helm list -A`, `helm repo add/update`, and `helm delete` is essential.

### Etcd backup/restore remains treacherous

Despite being officially removed from the curriculum, etcd questions persist under the broader "manage cluster
lifecycle" umbrella. The tricky parts: **certificate paths differ** from practice environments (you must inspect the
running etcd pod/process to find actual `--cacert`, `--cert`, and `--key` paths), you must determine whether etcd is
internal (static pod) or external (standalone service), the restore requires updating the etcd static pod manifest to
point to the new data directory, and permission issues often derail candidates. One exam taker failed at 61% partly due
to etcd certificate path confusion.

### Cluster troubleshooting is deliberately opaque

With 30% of the exam weight, troubleshooting questions are designed to be time-consuming. Scenarios include broken
kube-apiserver (typos in static pod manifests at `/etc/kubernetes/manifests/`), kubelet failures requiring
`systemctl status kubelet` and `journalctl -u kubelet` investigation, expired certificates, and nodes stuck in NotReady
state. Multiple candidates describe these as "the most challenging tasks" on the exam.

### Network Policies require precise YAML syntax

Creating policies that allow traffic from specific namespaces to specific ports trips up candidates who confuse
`namespaceSelector` with `podSelector` within the same rule, or who don't understand the difference between specifying
them in the same `-from` entry versus separate entries. The visual editor at `editor.networkpolicy.io` is widely
recommended for practice.

### Time management is the silent killer

The most commonly cited reason for failure is **running out of time**. At roughly 7 minutes per question with no buffer,
candidates who spend too long on a single troubleshooting task often leave 3+ questions unanswered. The consensus
strategy: do easy questions first, flag hard ones, keep 10–15 minutes at the end for review, and never spend more than 7
minutes on any single task without moving on.

---

## Kubernetes v1.32–v1.34 changes that affect the exam

### etcd jumps to v3.6 in Kubernetes v1.34

Kubeadm bundles **etcd v3.6.5** starting with Kubernetes v1.34, up from v3.5.x in earlier versions. The upgrade path
requires passing through etcd v3.5.20+ before reaching v3.6.0 — kubeadm handles this automatically, but understanding
the etcd version mapping matters for backup/restore procedures.

### Native sidecar containers reached GA in v1.33

Implemented as init containers with `restartPolicy: Always`, native sidecars start before main containers, run
throughout the pod lifecycle, and terminate after main containers. This is **tested on the CKA exam** — understand the
syntax and behavior.

### The Endpoints API is officially deprecated in v1.33

The API server now returns deprecation warnings when `v1 Endpoints` resources are accessed. The replacement is *
*EndpointSlices** (`discovery.k8s.io/v1`), which support dual-stack networking and scale better. Use
`kubectl get endpointslice` instead of `kubectl get endpoints`.

### Ingress NGINX Controller retired, Gateway API ascendant

While the Ingress API itself remains stable and undeprecated, the **Ingress NGINX Controller was retired in November
2025** with support ending March 2026. Gateway API v1.5 (released February 2026) continues to mature with features like
ListenerSet and HTTPRoute CORS filter. The exam tests both Ingress and Gateway API.

### Other changes worth knowing

- **In-place Pod vertical scaling** graduated to beta in v1.33 (GA in v1.35) — you can adjust CPU/memory on running pods
  without restart
- **StatefulSet PVC auto-delete** reached GA in v1.32 — PVC retention policies (`whenDeleted`, `whenScaled`) are now
  stable
- **User namespaces** enabled by default in v1.33 — pods can opt in via `spec.hostUsers: false`
- **cgroup v1 deprecated** in v1.35 — kubelet refuses to start on cgroup v1 by default
- **containerd 1.x** reaches end of support in v1.35; containerd 2.0+ becomes required in v1.36
- **`--register-schedulable` kubelet flag removed** in v1.34 — use taints instead
- **Dynamic Resource Allocation (DRA)** core graduated to GA in v1.34 with stable v1 API

---

## Proven strategies from successful exam takers

The most consistent advice from candidates who passed in 2025–2026 centers on **speed over perfection**. The exam
rewards candidates who can execute kubectl commands from muscle memory rather than searching documentation for every
task. Here are the most actionable strategies:

**Practice on real multi-node clusters.** Minikube and kind cannot replicate kubelet restart scenarios, node drain
operations, or SSH-based troubleshooting. Set up kubeadm clusters on cloud VMs (Hetzner, AWS, DigitalOcean) to practice
the full range of administrative tasks. The exam environment uses kubeadm-based clusters, and understanding how kubeadm
structures control plane components (static pods in `/etc/kubernetes/manifests/`) is essential for troubleshooting.

**Use imperative commands to generate YAML scaffolds.** Commands like
`kubectl run pod1 --image=nginx --dry-run=client -o yaml > pod.yaml` and
`kubectl create deploy myapp --image=nginx --dry-run=client -o yaml > deploy.yaml` save minutes per question. Learn the
`kubectl create` generators for services, roles, rolebindings, configmaps, and secrets.

**Navigate kubernetes.io/docs blindfolded.** The Tasks section contains procedures for etcd backup, kubeadm upgrade, and
most practical operations. The kubectl cheat sheet has jsonpath examples. For Kustomize, only
`kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/` is allowed — the standalone kustomize.io
documentation is not.

**Study resource recommendations** converge on a specific stack: Mumshad Mannambeth's Udemy CKA course for foundations,
KodeKloud's Ultimate CKA Mock Exam Series for additional practice, Killer.sh simulator sessions (included with exam
purchase) for realistic difficulty, and Killercoda free scenarios for daily reps. Multiple candidates specifically
credit a YouTube channel called "JayDemy" for 2025 CKA walkthroughs that closely matched real exam scenarios.

**One candidate's benchmark**: scoring **60% on Killer.sh** translated to **89% on the actual exam**. The simulator is
intentionally harder — if you can pass it, you're ready. However, the simulator doesn't fully capture the "broader, more
abstract" nature of some real exam questions, particularly those requiring deep Linux troubleshooting knowledge.

## Conclusion

The 2025–2026 CKA exam is a meaningfully different test from its pre-2025 predecessor. The addition of Gateway API,
Helm, Kustomize, and CRDs/Operators introduces topics that most training platforms haven't fully integrated, creating a
gap that catches well-prepared candidates off guard. The unchanged 30% troubleshooting weight, combined with the
SSH-based environment and strict 2-hour limit, makes time management the decisive factor between passing and failing.
Candidates who build real multi-node clusters, master imperative kubectl workflows, and practice specifically on Gateway
API and Helm troubleshooting will have a significant advantage. The 66% passing threshold is achievable for anyone who
can reliably solve the ~70% of questions that are straightforward to intermediate, leaving the genuinely hard 30% as
margin rather than requirement.
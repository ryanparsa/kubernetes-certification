# CKA Practice Scenarios (2025/2026 Edition)

A collection of 28 self-contained, performance-based practice tasks designed for the [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/) exam. 

This repository is aligned with the **2025/2026 CKA Curriculum**, featuring modern topics like the **Gateway API**, **Helm/Kustomize**, **Node Maintenance**, and **Advanced Troubleshooting** using `crictl` and `journalctl`.

## 🚀 Getting Started

### Prerequisites
- **Docker**: For running `kind` nodes as containers.
- **kind**: Kubernetes-in-Docker to spin up local clusters.
- **kubectl**: To interact with the clusters.
- **helm**: Required for Task 11.

### Running a Task
Each task is independent and manages its own cluster and `kubeconfig`.

```bash
cd 1                          # Navigate to a task directory
./up.sh                       # Create the cluster and apply the scenario
export KUBECONFIG=$PWD/kubeconfig
cat task.md                   # Read your objective
# ... solve it using kubectl ...
./test.sh                     # Verify your solution
./down.sh                     # Clean up (kind delete cluster)
```

---

## 📚 Task Index by Domain

The tasks are mapped to the 2025/2026 CKA exam weightings.

### 🛠️ Troubleshooting (30%)
*Focus: Node failures, control plane diagnostics, application debugging.*
- **Task 1**: App - Debugging a `CrashLoopBackOff`.
- **Task 2**: Control Plane - Fix broken static pods (apiserver/etcd).
- **Task 6**: Networking - Fix Service-to-Pod endpoint mismatch.
- **Task 9**: Infrastructure - Troubleshooting a `NotReady` worker node.
- **Task 10**: DNS - Fixing CoreDNS resolution failures.
- **Task 16**: Workloads - Rolling back a failed deployment.
- **Task 20**: Kubelet - Debugging invalid Kubelet systemd configuration.
- **Task 27**: Resources - Resolving `ResourceQuota` scaling issues.

### 🏗️ Cluster Architecture & Configuration (25%)
*Focus: Kubeadm, ETCD backup/restore, RBAC, Helm, Kustomize.*
- **Task 3**: etcd - Perform a live snapshot backup.
- **Task 4**: RBAC - Configure Roles and RoleBindings.
- **Task 11**: Helm - Deploy and override local charts.
- **Task 12**: Kustomize - Apply patches to a base/overlay structure.
- **Task 13**: etcd - Restore a cluster from a snapshot.
- **Task 22**: Security - Approving Certificate Signing Requests (CSR).

### 🌐 Services & Networking (20%)
*Focus: Gateway API, Ingress, NetworkPolicies.*
- **Task 5**: Security - Pod-to-Pod NetworkPolicies.
- **Task 14**: Modern Routing - Configure a **Gateway API** `HTTPRoute`.
- **Task 24**: Legacy Routing - Setting up a standard `Ingress` resource.
- **Task 25**: Security - Implementing Egress traffic restrictions.

### 📦 Workloads & Scheduling (15%)
*Focus: Deployments, ConfigMaps, Secrets, Node Affinity, Taints/Tolerations.*
- **Task 7**: Scheduling - NodeAffinity and Taints/Tolerations.
- **Task 15**: Config - Mounting ConfigMaps and Secrets as volumes.
- **Task 17**: Scheduling - Targeted `DaemonSet` deployment.
- **Task 18**: Scaling - Horizontal Pod Autoscaler (HPA) setup.
- **Task 19**: Maintenance - Draining and Cordoning a node safely.
- **Task 21**: Design Patterns - Adding a Sidecar Logging container.
- **Task 26**: Automation - Configuring `CronJobs` with history limits.
- **Task 28**: Static Pods - Creating a static pod on a worker node.

### 💾 Storage (10%)
*Focus: PV, PVC, StorageClasses.*
- **Task 8**: Dynamic Storage - StorageClass and PVC binding.
- **Task 23**: Manual Storage - PV/PVC using `hostPath`.

---

## 💡 Tactical Exam Tips (from `CKA Exam Preparation Guide.txt`)

1.  **Context is Everything**: Always check the top of the exam prompt for the context command (e.g., `kubectl config use-context cluster1`).
2.  **Imperative First**: Use `kubectl run`, `create`, or `expose` with `--dry-run=client -o yaml` to generate base files. Never write YAML from scratch.
3.  **Speed Up**: Use an alias like `export do="--dry-run=client -o yaml"` and `alias k="kubectl"`.
4.  **SSH Boundaries**: If you SSH into a node to fix a Kubelet, remember to `exit` back to the base terminal before running the next task's verifier.
5.  **Documentation**: You can use `kubernetes.io/docs` and `gateway-api.sigs.k8s.io` during the exam. Search for "YAML snippets" to copy-paste.

---

## 🧹 Maintenance
If a task environment gets corrupted or you want to start over:
```bash
./down.sh && ./up.sh
```
Avoid keeping multiple clusters running simultaneously to save Docker resources (RAM/CPU).

Topic: docs navigation under exam constraints.
Allowed sites only: kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs, gateway-api.sigs.k8s.io. No bookmarks, no other sites.

Each challenge is a realistic CKA task that requires looking something up. I must answer with ALL of:
1. Which site
2. The exact search-bar term I'd type (favor this — it's almost always faster than clicking)
3. The click-through navigation path as a fallback
4. What I'd copy from that page

Grade me on speed and directness. Mark ⚡ if I clicked when a search would've been faster, and show the better search term. Occasionally say "exam clock — 30 seconds" and tell me afterward if my path was fast enough. When relevant, point out a nearby page I'd commonly need next.

Coverage (rotate):
- Workloads: Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob examples
- Config: ConfigMap, Secret, env, volume mounts
- Probes: liveness/readiness/startup
- Networking: Services, Ingress (with TLS), Gateway API (Gateway + HTTPRoute + TLS), NetworkPolicy
- Storage: PV, PVC, StorageClass, access modes
- Scheduling: nodeSelector, affinity, taints/tolerations, priorityClass
- Security & RBAC: SA, Role/RoleBinding, ClusterRole/Binding, securityContext
- Cluster admin: kubeadm init/join/upgrade/reset, cert renewal, etcd backup/restore
- kubelet: config file, static pods, troubleshooting
- kubectl reference: cheat sheet, output formats, JSONPath
- Helm: install, upgrade, template, values, repo add
- Gateway API: Gateway, HTTPRoute, TLS, Ingress migration
- Troubleshooting guides

Difficulty ramp: easy (cheat sheet, basic Pod/Service examples) → medium (NetworkPolicy, Ingress TLS, etcd backup, RBAC) → hard (encryption at rest, audit policy, custom scheduler config, JSONPath reference) → expert (combine info from 2 doc pages).
Start with challenge #1.

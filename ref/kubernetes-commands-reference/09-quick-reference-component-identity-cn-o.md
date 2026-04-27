# Kubernetes Commands Reference — Quick Reference: Component Identity (CN / O)

> Part of [Kubernetes Commands Reference](../Kubernetes Commands Reference.md)


| Component               | Certificate CN                     | Organization (O)              |
|-------------------------|------------------------------------|-------------------------------|
| kube-apiserver          | `kube-apiserver`                   | —                             |
| kube-controller-manager | `system:kube-controller-manager`   | —                             |
| kube-scheduler          | `system:kube-scheduler`            | —                             |
| kubelet (client)        | `system:node:<nodename>`           | `system:nodes`                |
| kube-proxy              | `system:kube-proxy`                | —                             |
| admin user              | `kubernetes-admin`                 | `system:masters`              |
| etcd                    | varies (e.g. `etcd-server`)        | —                             |

---


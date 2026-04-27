# Kubernetes Commands Reference — Quick Reference: Port Map

> Part of [Kubernetes Commands Reference](../Kubernetes Commands Reference.md)


| Port  | Component               | Protocol | Purpose                            |
|-------|-------------------------|----------|------------------------------------|
| 6443  | kube-apiserver          | HTTPS    | Kubernetes API (all clients)       |
| 2379  | etcd                    | HTTPS    | client requests (API server)       |
| 2380  | etcd                    | HTTPS    | peer-to-peer replication           |
| 10250 | kubelet                 | HTTPS    | API server → kubelet calls         |
| 10248 | kubelet                 | HTTP     | local healthz (no auth)            |
| 10257 | kube-controller-manager | HTTPS    | healthz + metrics (local)          |
| 10259 | kube-scheduler          | HTTPS    | healthz + metrics (local)          |
| 10256 | kube-proxy              | HTTP     | healthz                            |

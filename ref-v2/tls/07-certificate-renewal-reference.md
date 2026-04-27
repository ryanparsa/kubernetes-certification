# Kubernetes TLS and Identity: The Master Guide

[← Back to index](../README.md)

---

## 7. Certificate Renewal Reference

### `/etc/kubernetes/pki/` — Control Plane Certs

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `ca.crt / ca.key` | **10 years** | No | Manual process (rare; requires re-issuing all signed certs) |
| `apiserver.crt` | 1 year | No | `kubeadm certs renew all` |
| `apiserver-etcd-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `apiserver-kubelet-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `front-proxy-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/ca.crt` | **10 years** | No | Manual process |
| `etcd/server.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/peer.crt` | 1 year | No | `kubeadm certs renew all` |
| `etcd/healthcheck-client.crt` | 1 year | No | `kubeadm certs renew all` |
| `sa.key / sa.pub` | **No expiry** | N/A | Not a certificate — no renewal needed |

### `/etc/kubernetes/` — Kubeconfig Files

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `kubelet.conf` | 1 year | **Yes** — Certificate Rotation (symlink swap, no restart) | Automatic |
| `admin.conf` | 1 year | No | `kubeadm certs renew all` + re-copy to workstation |
| `controller-manager.conf` | 1 year | No | `kubeadm certs renew all` + restart static pod |
| `scheduler.conf` | 1 year | No | `kubeadm certs renew all` + restart static pod |
| `super-admin.conf` | 1 year | No | `kubeadm certs renew all` |

### `/var/lib/kubelet/pki/` — Kubelet Node Certs

| File | Expiry | Auto-renews? | How to renew |
|---|---|---|---|
| `kubelet-client-<date>.pem` | 1 year | **Yes** — kubelet requests new cert, writes dated file | Automatic |
| `kubelet-client-current.pem` | (symlink) | **Yes** — symlink flipped atomically on rotation | Automatic |
| `kubelet.crt / kubelet.key` | 1 year | **No** by default | Requires `serverTLSBootstrap: true` in kubelet config to enable auto-rotation; otherwise manual |

> **After any `kubeadm certs renew all`:** restart kube-apiserver, kube-scheduler, kube-controller-manager static pods so they reload the new files. Re-copy `admin.conf` to any workstation `~/.kube/config`.

---

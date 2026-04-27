# Kubernetes Files

[← Back to index](../README.md)

---

## Worker node

```
/
├── usr/
│   └── bin/
│       └── kubelet                                              # The only required k8s binary on a worker
├── opt/
│   └── cni/
│       └── bin/                                                 # CNI plugin executables (bridge, host-local, kindnet, etc.)
├── etc/
│   ├── kubernetes/                                              # Much smaller than control plane — no PKI keys, no manifests
│   │   ├── kubelet.conf                                         # kubeconfig kubelet uses to authenticate to the API server
│   │   ├── manifests/                                           # Static pod manifests dir — empty on a worker node
│   │   └── pki/
│   │       └── ca.crt                                           # Cluster CA cert only — worker never holds any private keys
│   ├── systemd/
│   │   └── system/
│   │       ├── kubelet.service                                   # Systemd unit that starts/restarts kubelet on boot
│   │       └── kubelet.service.d/
│   │           └── 10-kubeadm.conf                              # Drop-in that injects --config and extra flags into kubelet
│   ├── cni/
│   │   └── net.d/
│   │       └── 10-kindnet.conflist                              # CNI plugin config — defines pod network on this node
│   ├── containerd/
│   │   └── config.toml                                          # containerd daemon config (snapshotter, plugins, etc.)
│   └── crictl.yaml                                              # crictl CLI config — points to the containerd socket
├── run/
│   └── containerd/
│       └── containerd.sock                                      # Unix socket kubelet uses to talk to containerd (CRI)
└── var/
    ├── log/
    │   ├── pods/                                                # Pod logs on disk, organized by namespace_name_uid/container/
    │   └── containers/                                          # Symlinks into /var/log/pods/, one per container
    └── lib/
        ├── cni/                                                 # CNI plugin runtime state and IPAM address allocations
        ├── containerd/                                          # Container image layers and snapshot storage
        └── kubelet/                                             # Kubelet's runtime state root
            ├── config.yaml                                      # Kubelet's runtime config (eviction thresholds, feature gates)
            ├── kubeadm-flags.env                                # Extra CLI flags injected into kubelet by kubeadm
            ├── cpu_manager_state                                # Persisted CPU manager policy state (for static pinning)
            ├── memory_manager_state                             # Persisted memory manager policy state
            ├── dra_manager_state                                # Dynamic Resource Allocation state (DRA feature gate)
            ├── checkpoints/                                     # Kubelet checkpoints for pod recovery across restarts
            ├── device-plugins/
            │   └── kubelet.sock                                 # Unix socket for device plugin API (GPUs, FPGAs, etc.)
            ├── pki/
            │   ├── kubelet-client-current.pem                   # Symlink → current rotated kubelet client cert+key
            │   ├── kubelet-client-<date>.pem                    # Actual rotated client cert kubelet uses to auth to API server
            │   ├── kubelet.crt                                  # Kubelet's serving cert (API server uses this to call kubelet)
            │   └── kubelet.key                                  # Kubelet's serving private key
            ├── plugins/                                         # CSI driver Unix socket directory
            ├── plugins_registry/                                # CSI plugin self-registration directory
            ├── pod-resources/
            │   └── kubelet.sock                                 # Socket exposing per-pod device/resource allocations
            └── pods/                                            # One subdirectory per running pod (named by UID)
                └── <pod-uid>/
                    ├── containers/                              # Per-container state (restart count, exit code, etc.)
                    ├── etc-hosts                                # The /etc/hosts file injected into this pod
                    ├── plugins/                                 # Pod-scoped plugin state (empty-dir readiness files)
                    └── volumes/                                 # Mounted volumes (projected tokens, configmaps, etc.)
                        ├── kubernetes.io~projected/
                        │   └── kube-api-access-<id>/
                        │       ├── token                        # Auto-rotated ServiceAccount JWT for this pod
                        │       ├── ca.crt                       # Cluster CA injected so the pod can verify the API server
                        │       └── namespace                    # The pod's namespace, available as a file
                        └── kubernetes.io~configmap/             # ConfigMap volumes mounted into the pod

```

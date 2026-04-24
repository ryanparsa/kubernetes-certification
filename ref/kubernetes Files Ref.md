# Kubernetes Files

# Control Plane Node

```
/
├── usr/
│   ├── bin/
│   │   ├── kubelet                                              # The kubelet daemon binary
│   │   ├── kubectl                                              # CLI to interact with the cluster
│   │   └── kubeadm                                              # Bootstrap / upgrade tool for the cluster
│   └── local/
│       └── bin/                                                 # Alternative install location for the above binaries
├── opt/
│   └── cni/
│       └── bin/                                                 # CNI plugin executables (kindnet, bridge, host-local, etc.)
├── etc/
│   ├── kubernetes/                                              # Main k8s config root
│   │   ├── admin.conf                                           # kubeconfig for cluster admin (kubectl)
│   │   ├── controller-manager.conf                              # kubeconfig used by kube-controller-manager
│   │   ├── kubelet.conf                                         # kubeconfig used by kubelet to reach API server
│   │   ├── scheduler.conf                                       # kubeconfig used by kube-scheduler
│   │   ├── super-admin.conf                                     # kubeconfig with raw cluster-admin (bypasses RBAC)
│   │   ├── audit-policy.yaml                                    # (optional) defines which API requests to audit-log
│   │   ├── encryption-config.yaml                               # (optional) encryption-at-rest config for etcd secrets
│   │   ├── manifests/                                           # Static pod manifests — kubelet auto-starts these on boot
│   │   │   ├── etcd.yaml                                        # Static pod: etcd key-value store
│   │   │   ├── kube-apiserver.yaml                              # Static pod: API server (front door to the cluster)
│   │   │   ├── kube-controller-manager.yaml                     # Static pod: runs reconciliation control loops
│   │   │   └── kube-scheduler.yaml                              # Static pod: assigns pods to nodes
│   │   └── pki/                                                 # All TLS certs and keys for the control plane
│   │       ├── ca.crt                                           # Cluster root CA — signed everything below (public)
│   │       ├── ca.key                                           # Cluster root CA private key — most sensitive file
│   │       ├── apiserver.crt                                    # API server's TLS serving certificate
│   │       ├── apiserver.key                                    # API server's private key
│   │       ├── apiserver-etcd-client.crt                        # Cert: API server authenticates to etcd
│   │       ├── apiserver-etcd-client.key                        # Key for API server → etcd mTLS
│   │       ├── apiserver-kubelet-client.crt                     # Cert: API server authenticates to kubelet
│   │       ├── apiserver-kubelet-client.key                     # Key for API server → kubelet mTLS
│   │       ├── front-proxy-ca.crt                               # CA for the aggregation layer (extension API servers)
│   │       ├── front-proxy-ca.key                               # Private key for the front-proxy CA
│   │       ├── front-proxy-client.crt                           # Cert API server uses when proxying to aggregated APIs
│   │       ├── front-proxy-client.key                           # Key for front-proxy client auth
│   │       ├── sa.key                                           # Private key used to sign ServiceAccount JWT tokens — held by kube-controller-manager
│   │       ├── sa.pub                                           # Public key used to verify ServiceAccount tokens — read by kube-apiserver
│   │       └── etcd/                                            # etcd-specific TLS (separate CA from cluster)
│   │           ├── ca.crt                                       # etcd's own CA (independent of cluster CA)
│   │           ├── ca.key                                       # etcd CA private key
│   │           ├── server.crt                                   # etcd server's TLS serving certificate
│   │           ├── server.key                                   # etcd server's private key
│   │           ├── peer.crt                                     # Cert for etcd-to-etcd peer replication
│   │           ├── peer.key                                     # Key for etcd peer communication
│   │           ├── healthcheck-client.crt                       # Cert used by liveness probes to query etcd
│   │           └── healthcheck-client.key                       # Key for etcd health check client
│   ├── systemd/
│   │   └── system/
│   │       ├── kubelet.service                                   # Systemd unit that starts/restarts kubelet on boot
│   │       └── kubelet.service.d/
│   │           └── 10-kubeadm.conf                              # Drop-in that injects --config and extra flags into kubelet
│   ├── cni/
│   │   └── net.d/
│   │       └── 10-kindnet.conflist                              # CNI plugin config — defines the pod network (kindnet)
│   ├── containerd/
│   │   └── config.toml                                          # containerd daemon config (snapshotter, plugins, etc.)
│   └── crictl.yaml                                              # crictl CLI config — points to the containerd socket
├── run/
│   └── containerd/
│       └── containerd.sock                                      # Unix socket kubelet uses to talk to containerd (CRI)
└── var/
    ├── etcd/                                                    # etcd data directory — the entire cluster state lives here
    ├── log/
    │   ├── pods/                                                # Pod logs on disk, organized by namespace_name_uid/container/
    │   └── containers/                                          # Symlinks into /var/log/pods/ one per container
    └── lib/
        ├── cni/                                                 # CNI plugin runtime state and IPAM address allocations
        ├── containerd/                                          # Container image layers and snapshot storage
        └── kubelet/                                             # Kubelet's runtime state root
            ├── config.yaml                                      # Kubelet's own configuration (eviction, feature gates, etc.)
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

# Worker node

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

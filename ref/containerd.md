# containerd Ecosystem

### 7.1 — containerd

The container runtime. Kubelet communicates with it via the CRI gRPC socket.

```
Socket: /run/containerd/containerd.sock
Config: /etc/containerd/config.toml
```

**Key config sections:**

```toml
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.9"     # pause/infra container image

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  runtime_type = "io.containerd.runc.v2"

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true               # must match kubelet cgroupDriver; mismatch = pods fail
```

```bash
systemctl status containerd
systemctl restart containerd
journalctl -u containerd -f           # containerd logs
```

---

### 7.2 — crictl (CRI CLI)

Talks directly to the CRI socket, bypassing kubelet. Essential for debugging pods that fail
before kubelet can report status.

**Config:** `/etc/crictl.yaml`
```yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 2
debug: false
```

```bash
crictl ps                            # running containers (not pods)
crictl ps -a                         # all containers including stopped/exited
crictl pods                          # pod-level sandbox list
crictl images                        # images cached on this node
crictl pull <image>                  # pull an image
crictl inspect <container-id>        # full container config + state as JSON
crictl logs <container-id>           # container logs (bypasses kubelet)
crictl exec -it <container-id> sh    # exec into container
crictl stats                         # real-time CPU/memory per container
crictl info                          # runtime version, containerd config info
crictl rm <container-id>             # remove (stopped) container
crictl rmp <pod-id>                  # remove pod sandbox
crictl stopp <pod-id>                # stop pod sandbox
```

**Why use crictl instead of kubectl:**
- Pod stuck in `ContainerCreating` → kubelet hasn't surfaced the error yet
- Static pod not appearing → crictl shows what containerd actually has
- Image pull errors at the runtime level before kubelet updates pod status

---

### 7.3 — ctr (low-level containerd CLI)

Direct containerd management tool. Uses containerd namespaces — Kubernetes workloads live in
the `k8s.io` namespace.

```bash
ctr namespaces list                  # containerd namespaces (k8s uses "k8s.io")
ctr -n k8s.io images list            # images in the Kubernetes namespace
ctr images list                      # images in the default namespace
ctr images pull <image>              # pull an image
ctr containers list                  # all containers (all namespaces)
ctr -n k8s.io containers list        # k8s containers
ctr tasks list                       # running processes/tasks
ctr -n k8s.io tasks list             # k8s running tasks
```

**Note:** `ctr` is a low-level debugging tool. For day-to-day node debugging, `crictl` is preferred
as it is CRI-aware and understands pod/container relationships.

---

### 7.4 — etcdctl

The CLI for etcd — the key-value store that persists all Kubernetes cluster state.

**Always set these environment variables or pass as flags:**

```bash
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
```

Or pass inline:
```bash
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  <subcommand>
```

**Essential commands:**

```bash
etcdctl member list                  # all cluster members + endpoint + leader status
etcdctl endpoint health              # health check for each endpoint
etcdctl endpoint status              # leader, raft index, version per endpoint

# Read a specific key (verify encryption at rest)
etcdctl get /registry/secrets/default/mysecret

# List all keys (huge output — filter with grep)
etcdctl get / --prefix --keys-only

# Backup
etcdctl snapshot save /tmp/etcd-backup.db

# Verify backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore (creates new data directory — do NOT restore over live data)
etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --initial-cluster=master=https://127.0.0.1:2380 \
  --initial-cluster-token=etcd-cluster-1 \
  --initial-advertise-peer-urls=https://127.0.0.1:2380
```

**Restore procedure:**

1. Stop kube-apiserver (move manifest out of `/etc/kubernetes/manifests/`)
2. Run `etcdctl snapshot restore` into a new data directory
3. Update etcd static pod manifest `--data-dir` to point to the new directory
4. Move kube-apiserver manifest back; wait for API server to come up
5. Verify with `kubectl get nodes`

**Encryption verification:**
```bash
# If encryption is NOT configured, raw secret value is visible in base64:
etcdctl get /registry/secrets/default/mysecret | hexdump -C | grep -A2 "password"
# If AES-CBC encryption is active, output is binary garbage — confirms encryption works
```

---


# Kubernetes Commands Reference

[← Back to index](../README.md)

---

## Part 1: kubeadm

kubeadm bootstraps and manages the lifecycle of a Kubernetes control plane. It generates PKI,
writes static pod manifests, bootstraps RBAC, and prints join tokens. It does **not** install
kubelet or a container runtime — that must be done separately.

---

### 1.1 — `kubeadm init`

Initialises a new control plane node from scratch.

**Internal steps (in order):**

1. **Preflight checks** — verifies kernel modules (`br_netfilter`, `overlay`), open ports,
   container runtime is reachable at its socket, swap is off (unless `--ignore-preflight-errors`)
2. **Generates PKI** — writes all certs and keys under `/etc/kubernetes/pki/`
3. **Writes kubeconfigs** — `admin.conf`, `kubelet.conf`, `controller-manager.conf`,
   `scheduler.conf` under `/etc/kubernetes/`
4. **Writes static pod manifests** — `kube-apiserver.yaml`, `kube-controller-manager.yaml`,
   `kube-scheduler.yaml`, `etcd.yaml` under `/etc/kubernetes/manifests/`
5. **Waits for API server** — polls `/healthz` until healthy
6. **Bootstraps RBAC** — creates ClusterRoles and bindings required by system components
7. **Installs CoreDNS and kube-proxy** — as Deployments/DaemonSets in `kube-system`
8. **Prints `kubeadm join` command** — includes bootstrap token and CA cert hash

**Key flags:**

```
--config                       # path to ClusterConfiguration YAML (preferred over individual flags)
--pod-network-cidr             # CIDR for pod IPs; must match CNI plugin (e.g. 10.244.0.0/16 for Flannel)
--service-cidr                 # CIDR for ClusterIP services; default 10.96.0.0/12
--apiserver-advertise-address  # IP the API server binds on (default: auto-detect)
--control-plane-endpoint       # stable DNS/IP for HA load balancer (required for HA clusters)
--upload-certs                 # upload control-plane certs to a Secret for HA join
--skip-phases                  # skip named phases (e.g. --skip-phases=addon/kube-proxy)
--dry-run                      # simulate all actions without writing any files
--ignore-preflight-errors      # proceed despite specified preflight failures
```

**ClusterConfiguration YAML structure:**

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.32.0
controlPlaneEndpoint: "lb.example.com:6443"   # HA load balancer
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  dnsDomain: "cluster.local"
apiServer:
  extraArgs:
    audit-policy-file: /etc/kubernetes/audit-policy.yaml
  extraVolumes:
  - name: audit-policy
    hostPath: /etc/kubernetes/audit-policy.yaml
    mountPath: /etc/kubernetes/audit-policy.yaml
    readOnly: true
etcd:
  local:
    dataDir: /var/lib/etcd
```

**Reading `kubeadm init` output:**

| Phase tag              | What happens                                          |
|------------------------|-------------------------------------------------------|
| `[preflight]`          | system checks; fails fast here if anything is missing |
| `[certs]`              | each cert/key pair written to `/etc/kubernetes/pki/`  |
| `[kubeconfig]`         | kubeconfig files created                              |
| `[controlplane]`       | static pod manifests written to manifests/            |
| `[etcd]`               | etcd static pod manifest written                      |
| `[wait-control-plane]` | blocks until API server `/healthz` returns 200        |
| `[apiclient]`          | verifies API server with a real API call              |
| `[uploadconfig]`       | stores ClusterConfiguration in `kube-system` ConfigMap|
| `[kubelet]`            | writes kubelet config and `kubeadm-flags.env`         |
| `[upload-certs]`       | (if --upload-certs) encrypts PKI into a Secret        |
| `[mark-control-plane]` | taints and labels the node as control-plane           |
| `[bootstrap-token]`    | creates the bootstrap token Secret in `kube-system`   |
| `[addons]`             | deploys CoreDNS and kube-proxy                        |

---

### 1.2 — `kubeadm join`

Joins a node (worker or control plane) to an existing cluster.

**Two modes:**

- **Worker join**: presents bootstrap token → API server issues kubelet client certificate via CSR
  API → kubelet switches from token auth to certificate auth
- **Control plane join**: `--control-plane --certificate-key` → downloads PKI from `kube-system`
  Secret → writes static pod manifests → becomes an additional master

**Key flags:**

```
--token                            # bootstrap token (format: abcdef.0123456789abcdef)
--discovery-token-ca-cert-hash     # SHA256 of cluster CA public key (pins the CA)
--control-plane                    # join as additional control plane node
--certificate-key                  # decryption key for uploaded certs (HA setup)
--apiserver-advertise-address      # override advertise address for this control plane
--discovery-file                   # use a kubeconfig file for discovery instead of token
```

**Internal flow — worker join:**

1. Kubelet starts using `bootstrap-kubelet.conf` (token as credential)
2. Kubelet submits a `CertificateSigningRequest` to the API server
3. The `csrapproving` controller auto-approves bootstrap CSRs matching the bootstrap RBAC
4. Kubelet receives the signed cert, writes it as a dated `.pem` file
5. `kubelet-client-current.pem` symlink is updated to point to the new cert
6. Kubelet restarts, now authenticating with the real client cert — token no longer used

**What breaks:**
- Expired bootstrap token → CSR submission is rejected → join fails at step 2
- Wrong `--discovery-token-ca-cert-hash` → TLS verification failure at discovery phase
- Missing `--certificate-key` for control plane join → PKI Secret cannot be decrypted

---

### 1.3 — `kubeadm certs`

Manages the lifecycle of cluster certificates.

```bash
kubeadm certs check-expiration          # shows each cert, expiry, days remaining, CA
kubeadm certs renew all                 # renew all certs at once (rewrites files, restarts needed)
kubeadm certs renew <name>              # renew a single cert by name
kubeadm certs certificate-key           # generate a new certificate key for HA
kubeadm certs generate-csr              # generate CSR files for external CA signing
```

**Reading `check-expiration` output:**

```
CERTIFICATE                EXPIRES                  RESIDUAL TIME  EXTERNALLY MANAGED
admin.conf                 Apr 24, 2027 09:56 UTC   364d           no
apiserver                  Apr 24, 2027 09:56 UTC   364d           no
apiserver-etcd-client      Apr 24, 2027 09:56 UTC   364d           no
apiserver-kubelet-client   Apr 24, 2027 09:56 UTC   364d           no
controller-manager.conf    Apr 24, 2027 09:56 UTC   364d           no
etcd-healthcheck-client    Apr 24, 2027 09:56 UTC   364d           no
etcd-peer                  Apr 24, 2027 09:56 UTC   364d           no
etcd-server                Apr 24, 2027 09:56 UTC   364d           no
front-proxy-client         Apr 24, 2027 09:56 UTC   364d           no
scheduler.conf             Apr 24, 2027 09:56 UTC   364d           no

CERTIFICATE AUTHORITY      EXPIRES                  RESIDUAL TIME  EXTERNALLY MANAGED
ca                         Apr 22, 2036 09:56 UTC   9y             no
etcd-ca                    Apr 22, 2036 09:56 UTC   9y             no
front-proxy-ca             Apr 22, 2036 09:56 UTC   9y             no
```

- `EXTERNALLY MANAGED: yes` means cert-manager or another system controls this cert — do not
  renew manually
- CA certs have 10-year validity; leaf certs have 1-year validity by default
- After `renew`, static pod manifests must be restarted: move them out and back into
  `/etc/kubernetes/manifests/`

---

### 1.4 — `kubeadm token`

Manages bootstrap tokens used by new nodes to join the cluster.

```bash
kubeadm token create                        # create new bootstrap token (24h TTL by default)
kubeadm token create --print-join-command   # full join command including hash
kubeadm token create --ttl 0                # non-expiring token (use carefully)
kubeadm token list                          # show all tokens + expiry time
kubeadm token delete <token>                # revoke a token immediately
```

**Bootstrap token format:** `<6-char>.<16-char>` — e.g. `abcdef.0123456789abcdef`

Stored as Secrets in `kube-system` namespace: `bootstrap-token-<token-id>`

The token ID (first 6 chars) becomes the Secret name; the full token is hashed and stored.
The `system:bootstrappers:kubeadm:default-node-token` group grants the CSR submission RBAC.

---

### 1.5 — `kubeadm upgrade`

Upgrades control plane components to a new Kubernetes version.

```bash
kubeadm upgrade plan                    # shows available versions, checks etcd, lists near-expiry certs
kubeadm upgrade apply v1.32.0           # upgrades this control plane node
kubeadm upgrade node                    # upgrades a worker node's kubelet config (run on each worker)
```

**Internal steps of `upgrade apply`:**

1. Preflight checks (version skew policy: only +1 minor allowed, etcd compatibility matrix)
2. Downloads new component container images
3. Updates static pod manifests (kubelet detects the change and restarts the pods automatically)
4. Renews all certificates expiring within 180 days
5. Updates `kubelet-config` ConfigMap in `kube-system`
6. Updates RBAC rules for the new version

**After `upgrade apply`:** the node's kubelet binary is **not** updated by kubeadm.
Run on each control plane node:
```bash
apt-mark unhold kubelet kubectl
apt-get install -y kubelet=1.32.0-* kubectl=1.32.0-*
apt-mark hold kubelet kubectl
systemctl daemon-reload && systemctl restart kubelet
```

**Version skew rules:**
- kubeadm can be at most 1 minor version ahead of the cluster
- kubelet cannot be newer than kube-apiserver
- kubectl can be ±1 minor version from the server

---

### 1.6 — `kubeadm config`

Manages kubeadm configuration and component images.

```bash
kubeadm config print init-defaults      # full default ClusterConfiguration YAML
kubeadm config print join-defaults      # full default JoinConfiguration YAML
kubeadm config images list              # lists all images kubeadm will pull for current version
kubeadm config images list --kubernetes-version v1.32.0   # for a specific version
kubeadm config images pull              # pre-pulls all images (air-gapped deployments)
kubeadm config migrate                  # migrates old config format to current API version
```

`images list` is critical for air-gapped clusters: pre-pull and re-tag to a private registry,
then use `imageRepository` in ClusterConfiguration to point kubeadm at the registry.

---

### 1.7 — `kubeadm reset`

Undoes everything `kubeadm init` or `kubeadm join` did on this node.

**What it removes:**
- Static pod manifests from `/etc/kubernetes/manifests/`
- Resets iptables/ipvs rules used by kube-proxy
- Removes `/etc/kubernetes/` directory (certs, kubeconfigs, manifests)
- Resets kubelet state

**What it does NOT remove (must do manually):**
```bash
rm -rf /var/lib/etcd                # etcd data directory
rm -rf /etc/cni /opt/cni            # CNI plugin state
ip link delete cni0                 # CNI bridge interface
ip link delete flannel.1            # Flannel VXLAN interface (if used)
```

After `kubeadm reset`, `kubelet` may still be running — stop it:
```bash
systemctl stop kubelet
```

---

### 1.8 — `kubeadm init phase` (granular control)

Runs individual phases of `init` or `join`. Useful for debugging failed steps or custom setups.

```bash
kubeadm init phase preflight
kubeadm init phase certs all
kubeadm init phase certs apiserver
kubeadm init phase kubeconfig all
kubeadm init phase kubeconfig admin
kubeadm init phase control-plane all
kubeadm init phase etcd local
kubeadm init phase upload-certs --upload-certs
kubeadm init phase mark-control-plane
kubeadm init phase bootstrap-token
kubeadm init phase addon all
```

List all phases:
```bash
kubeadm init --help | grep -A 40 "phases"
```

---

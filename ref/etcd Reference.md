# etcd Reference

Complete reference for etcd in a Kubernetes cluster: architecture, PKI, static pod
configuration, etcdctl usage, health checking, key inspection, backup, restore, HA
membership management, encryption at rest, and troubleshooting.

---

## Table of Contents

1. [What is etcd](#1-what-is-etcd)
2. [Role in Kubernetes](#2-role-in-kubernetes)
3. [How etcd Runs in Kubernetes](#3-how-etcd-runs-in-kubernetes)
4. [Static Pod Manifest — Key Flags](#4-static-pod-manifest--key-flags)
5. [etcd PKI / TLS](#5-etcd-pki--tls)
6. [etcdctl — Tool Setup and Usage](#6-etcdctl--tool-setup-and-usage)
7. [Health Checks and Member Operations](#7-health-checks-and-member-operations)
8. [Inspecting Keys (Reading Cluster State)](#8-inspecting-keys-reading-cluster-state)
9. [Backup — Snapshot Save](#9-backup--snapshot-save)
10. [Restore — Full Procedure](#10-restore--full-procedure)
11. [HA Clusters and Raft Quorum](#11-ha-clusters-and-raft-quorum)
12. [Encryption at Rest](#12-encryption-at-rest)
13. [Common Failure Modes and Troubleshooting](#13-common-failure-modes-and-troubleshooting)
14. [Quick Reference](#14-quick-reference)

---

## 1. What is etcd

etcd is a **distributed, consistent key-value store** built on the **Raft consensus
algorithm**. It provides:

- **Strong consistency**: every read reflects the most recent committed write (linearizable)
- **High availability**: an odd-numbered cluster tolerates `(N-1)/2` node failures
- **Watch API**: clients subscribe to key prefixes and receive change notifications in real time

### Raft consensus basics

```
Leader election:
  - One node is elected leader; all writes go to the leader
  - Leader sends log entries to followers; a write is committed once a quorum
    (majority) of nodes acknowledge it

Quorum (minimum nodes needed to commit a write):
  3-node cluster → 2  (tolerates 1 failure)
  5-node cluster → 3  (tolerates 2 failures)
  7-node cluster → 4  (tolerates 3 failures)
```

> A cluster with an **even** number of members has the same fault tolerance as one
> with `N-1` members (e.g. 4-node = 2-failure tolerance, same as 3-node) but is harder
> to elect a leader. Always use **odd** member counts.

---

## 2. Role in Kubernetes

etcd is the **single source of truth** for all cluster state. Every object the API
server creates, updates, or deletes is persisted to etcd.

```
kubectl → kube-apiserver → etcd
                     ↑
kube-scheduler, controller-manager, kubelet all watch etcd via the API server
(they never connect to etcd directly)
```

Only the **kube-apiserver** talks to etcd. All other components communicate with etcd
indirectly through the API server.

### What is stored in etcd

- All Kubernetes objects: Pods, Deployments, Services, ConfigMaps, Secrets, RBAC objects
- Cluster configuration: Namespaces, ResourceQuotas, LimitRanges, StorageClasses
- Lease objects used for leader election (controller-manager, scheduler)
- Node heartbeat leases

---

## 3. How etcd Runs in Kubernetes

In a kubeadm cluster, etcd runs as a **static pod** on the control-plane node(s),
managed directly by kubelet from the manifest at:

```
/etc/kubernetes/manifests/etcd.yaml
```

### Key ports

| Port | Protocol | Purpose |
|---|---|---|
| `2379` | HTTPS | Client API — used by kube-apiserver to read/write data |
| `2380` | HTTPS | Peer API — used for Raft replication between etcd members (HA only) |

### Data directory

```
/var/lib/etcd/       ← default data directory; contains the Raft WAL and snapshots
```

---

## 4. Static Pod Manifest — Key Flags

```yaml
# /etc/kubernetes/manifests/etcd.yaml
spec:
  containers:
  - name: etcd
    image: registry.k8s.io/etcd:3.5.x
    command:
    - etcd

    # Identity
    - --name=<node-name>                          # member name, unique per node

    # Client communication (kube-apiserver ↔ etcd)
    - --listen-client-urls=https://127.0.0.1:2379,https://<node-ip>:2379
    - --advertise-client-urls=https://<node-ip>:2379

    # Peer communication (etcd ↔ etcd, HA only)
    - --listen-peer-urls=https://<node-ip>:2380
    - --initial-advertise-peer-urls=https://<node-ip>:2380

    # Cluster bootstrap (used only on first start)
    - --initial-cluster=<name>=https://<ip>:2380  # list all members
    - --initial-cluster-state=new                  # 'new' or 'existing'
    - --initial-cluster-token=etcd-cluster-1       # unique token per cluster

    # Storage
    - --data-dir=/var/lib/etcd

    # TLS — server (presented to kube-apiserver)
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --key-file=/etc/kubernetes/pki/etcd/server.key
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --client-cert-auth=true                      # require client certs

    # TLS — peer (etcd-to-etcd)
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --peer-client-cert-auth=true

    # Liveness probe uses healthcheck-client cert (least privilege)
    # Snapshots / compaction
    - --auto-compaction-retention=8              # compact every 8 hours
    - --quota-backend-bytes=8589934592           # 8 GiB backend quota

  volumeMounts:
  - mountPath: /var/lib/etcd
    name: etcd-data
  - mountPath: /etc/kubernetes/pki/etcd
    name: etcd-certs
    readOnly: true

  volumes:
  - hostPath:
      path: /var/lib/etcd
      type: DirectoryOrCreate
    name: etcd-data
  - hostPath:
      path: /etc/kubernetes/pki/etcd
      type: DirectoryOrCreate
    name: etcd-certs
```

---

## 5. etcd PKI / TLS

etcd uses its **own, independent CA** (`/etc/kubernetes/pki/etcd/ca.crt`) separate from
the main cluster CA. Even if the cluster CA were compromised, an attacker still could
not connect to etcd directly.

### Certificate files

| File | Holder | Purpose |
|---|---|---|
| `etcd/ca.crt` | Everyone | Root CA that signs all etcd certs |
| `etcd/ca.key` | etcd CA process | Signs new etcd certs (protect carefully) |
| `etcd/server.crt / server.key` | etcd server | Presented to kube-apiserver (TLS server cert) |
| `etcd/peer.crt / peer.key` | etcd nodes | Mutual TLS between etcd members in HA clusters |
| `etcd/healthcheck-client.crt / key` | etcd liveness probe | Minimal access: health endpoint only |
| `apiserver-etcd-client.crt / key` | kube-apiserver | Client cert apiserver uses to authenticate to etcd |

### Communication diagram

```
kube-apiserver
  → presents apiserver-etcd-client.crt (signed by etcd CA)
  → connects to etcd server.crt:2379
  → etcd verifies: cert signed by etcd/ca.crt ✓

etcd-node-1 (HA)
  → presents peer.crt (signed by etcd CA)
  → connects to etcd-node-2:2380
  → etcd-node-2 verifies: cert signed by etcd/ca.crt ✓
```

### Finding cert paths from the running pod

```bash
kubectl -n kube-system describe pod etcd-<node> | grep "\-\-cert\|\-\-key\|\-\-ca"
# or
grep -E 'cert|key|ca' /etc/kubernetes/manifests/etcd.yaml
```

---

## 6. etcdctl — Tool Setup and Usage

`etcdctl` is the CLI client for etcd. Always set `ETCDCTL_API=3` (v2 is deprecated and
uses a different data model).

### Installation (if not available on host)

```bash
# Check if installed
which etcdctl

# If not, find the binary inside the etcd pod and copy it out
kubectl -n kube-system cp \
  etcd-<node>:/usr/local/bin/etcdctl \
  /usr/local/bin/etcdctl
chmod +x /usr/local/bin/etcdctl
```

### Setting environment variables (saves repeating flags)

```bash
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
```

Once set, commands become much shorter:

```bash
etcdctl endpoint health
etcdctl member list
etcdctl snapshot save /tmp/backup.db
```

### Running etcdctl inside the etcd pod

Useful when `etcdctl` is not installed on the host:

```bash
kubectl -n kube-system exec -it etcd-<node> -- sh

# Inside the pod (certs are already mounted):
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health
```

### Output formats

```bash
# Table (human-readable)
etcdctl member list --write-out=table

# JSON (scriptable)
etcdctl endpoint status --write-out=json | jq .

# Simple (key=value)
etcdctl endpoint status --write-out=simple
```

---

## 7. Health Checks and Member Operations

### Single-node health

```bash
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Healthy output:
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.3ms
```

### Endpoint status (shows leader, Raft index, DB size)

```bash
ETCDCTL_API=3 etcdctl endpoint status \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table

# +------------------------+------------------+---------+---------+-----------+
# |        ENDPOINT        |        ID        | VERSION | DB SIZE | IS LEADER |
# +------------------------+------------------+---------+---------+-----------+
# | https://127.0.0.1:2379 | 8e9e05c52164694d |  3.5.11 |  3.1 MB |      true |
# +------------------------+------------------+---------+---------+-----------+
```

### Member list (HA clusters)

```bash
ETCDCTL_API=3 etcdctl member list \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table

# +------------------+---------+-------+--------------------------+--------------------------+
# |        ID        | STATUS  | NAME  |       PEER ADDRS         |      CLIENT ADDRS        |
# +------------------+---------+-------+--------------------------+--------------------------+
# | 8e9e05c52164694d | started | node1 | https://10.0.0.1:2380    | https://10.0.0.1:2379    |
# | 9cf75dc4f1b0bd57 | started | node2 | https://10.0.0.2:2380    | https://10.0.0.2:2379    |
# | ede3c83b6e348b58 | started | node3 | https://10.0.0.3:2380    | https://10.0.0.3:2379    |
# +------------------+---------+-------+--------------------------+--------------------------+
```

### Add / remove a member (HA maintenance)

```bash
# Add a new member (run before starting etcd on the new node)
etcdctl member add node4 --peer-urls=https://10.0.0.4:2380

# Remove a failed member (use the member ID from member list)
etcdctl member remove 9cf75dc4f1b0bd57

# Update peer URL of an existing member
etcdctl member update 8e9e05c52164694d --peer-urls=https://10.0.0.10:2380
```

---

## 8. Inspecting Keys (Reading Cluster State)

etcd stores Kubernetes objects under the prefix `/registry/`.

```bash
# List all top-level key prefixes
ETCDCTL_API=3 etcdctl get / --prefix --keys-only \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# List all pods in the default namespace
etcdctl get /registry/pods/default --prefix --keys-only

# Read a specific key (value is protobuf-encoded — use apiserver for human-readable output)
etcdctl get /registry/pods/default/my-pod

# Count all keys (cluster size indicator)
etcdctl get / --prefix --keys-only | wc -l

# Watch all changes to a key prefix in real time
etcdctl watch /registry/pods/default --prefix
```

> Keys are stored as protobuf binary blobs. For human-readable output, always use
> `kubectl get ... -o yaml` via the API server rather than reading etcd directly.

---

## 9. Backup — Snapshot Save

A snapshot is a **consistent, point-in-time copy** of the etcd keyspace. It captures
all keys at the revision at which the snapshot was taken.

### Take a snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Output:
# Snapshot saved at /tmp/etcd-backup.db
```

### Verify the snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 7d2aa533 |    91824 |       1527 |     3.3 MB |
# +----------+----------+------------+------------+
```

### Copy a snapshot out of the etcd pod

```bash
kubectl -n kube-system exec etcd-<node> -- \
  etcdctl snapshot save /tmp/backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

kubectl -n kube-system cp etcd-<node>:/tmp/backup.db /tmp/etcd-backup.db
```

---

## 10. Restore — Full Procedure

Restoring from a snapshot **replaces all current cluster state** with the snapshot.

### Single-node restore

#### Step 1 — Stop the API server

```bash
# Prevent writes while etcd is being replaced
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Wait for it to stop (kube-apiserver should disappear from the list)
watch crictl ps
```

#### Step 2 — Restore the snapshot to a new data directory

```bash
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# Output:
# {"level":"info","msg":"restoring snapshot","path":"/tmp/etcd-backup.db"}
# {"level":"info","msg":"restored snapshot"}
# {"level":"info","msg":"adding member","member":"..."}
```

> **Do not** restore into `/var/lib/etcd` while etcd is running — always use a new
> directory first, then swap.

#### Step 3 — Point etcd at the new data directory

Edit `/etc/kubernetes/manifests/etcd.yaml` and update **two places**:

```yaml
# 1. The --data-dir flag
- --data-dir=/var/lib/etcd-restore      # was /var/lib/etcd

# 2. The hostPath volume for etcd-data
volumes:
- hostPath:
    path: /var/lib/etcd-restore          # was /var/lib/etcd
    type: DirectoryOrCreate
  name: etcd-data
```

#### Step 4 — Restore the API server

```bash
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

#### Step 5 — Verify recovery

```bash
# Watch pods restart
watch crictl ps

# Confirm cluster is functional
kubectl get nodes
kubectl get pods -A
```

---

### HA cluster restore

In an HA cluster each etcd member must be restored independently.

#### Key differences from single-node

- Stop the API server on **all** control-plane nodes first.
- Run `snapshot restore` on **each** member with member-specific flags:

```bash
# Member 1
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --name=node1 \
  --initial-cluster=node1=https://10.0.0.1:2380,node2=https://10.0.0.2:2380,node3=https://10.0.0.3:2380 \
  --initial-cluster-token=etcd-cluster-restored \
  --initial-advertise-peer-urls=https://10.0.0.1:2380

# Member 2
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore \
  --name=node2 \
  --initial-cluster=node1=https://10.0.0.1:2380,node2=https://10.0.0.2:2380,node3=https://10.0.0.3:2380 \
  --initial-cluster-token=etcd-cluster-restored \
  --initial-advertise-peer-urls=https://10.0.0.2:2380

# Member 3 — same pattern
```

> Use a **new `--initial-cluster-token`** (e.g. append `-restored`) to prevent the
> restored members from accidentally joining the old (corrupted) cluster.

- Update `etcd.yaml` on each control-plane node to use the new `--data-dir`.
- Restore API server manifests on all nodes.

---

## 11. HA Clusters and Raft Quorum

### Quorum and fault tolerance

| Cluster size | Quorum needed | Max failures tolerated |
|---|---|---|
| 1 | 1 | 0 |
| 3 | 2 | 1 |
| 5 | 3 | 2 |
| 7 | 4 | 3 |

**If quorum is lost**, the cluster enters a **read-only state** — no writes are accepted.
Recovery requires manually starting etcd with `--force-new-cluster` on one node (last resort).

### Checking which node is the leader

```bash
ETCDCTL_API=3 etcdctl endpoint status \
  --endpoints=https://NODE1:2379,https://NODE2:2379,https://NODE3:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --write-out=table
# IS LEADER column shows true on the current leader
```

### Transferring leadership (graceful maintenance)

```bash
# Move the leader away from a node before draining it
etcdctl move-leader <target-member-id>
```

### Defragmenting to reclaim disk space

Over time, deleted keys leave fragmented space in the backend database. Defrag reclaims it:

```bash
# Defrag the local member (run on each member separately, followers first, leader last)
ETCDCTL_API=3 etcdctl defrag \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Check DB size before and after
etcdctl endpoint status --write-out=table
```

---

## 12. Encryption at Rest

By default, Secrets stored in etcd are **base64-encoded but not encrypted**. Enable
encryption-at-rest to protect them.

### Create an EncryptionConfiguration

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <32-byte base64-encoded key>   # openssl rand -base64 32
  - identity: {}   # fallback: read unencrypted secrets written before encryption was enabled
```

```bash
# Generate a 32-byte key
openssl rand -base64 32
```

### Enable in kube-apiserver

Add the flag to `/etc/kubernetes/manifests/kube-apiserver.yaml`:

```yaml
- --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

Also add a volume mount so the file is accessible inside the static pod:

```yaml
volumeMounts:
- mountPath: /etc/kubernetes/encryption-config.yaml
  name: encryption-config
  readOnly: true
volumes:
- hostPath:
    path: /etc/kubernetes/encryption-config.yaml
    type: File
  name: encryption-config
```

### Encrypt existing secrets

After enabling, newly written Secrets are encrypted. Rotate existing ones:

```bash
# Re-write all Secrets through the API server (forces encryption)
kubectl get secrets -A -o json | kubectl replace -f -
```

### Verify encryption

```bash
# Read the raw etcd value — should be opaque (not human-readable JSON/YAML)
ETCDCTL_API=3 etcdctl get /registry/secrets/default/my-secret \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  | hexdump -C | head

# Encrypted values start with: k8s:enc:aescbc:v1:
```

---

## 13. Common Failure Modes and Troubleshooting

### etcd pod not starting

```bash
# Check static pod logs via crictl (API server may not be available)
crictl ps -a | grep etcd
crictl logs <container-id>

# Common causes:
# - Wrong --data-dir path (directory doesn't exist or is empty after a bad restore)
# - Wrong cert paths in the manifest
# - Port 2379/2380 already in use
# - Corrupted WAL in data directory
```

### API server cannot connect to etcd

```bash
# Check API server logs
crictl logs <apiserver-container-id>

# Look for: "connection refused", "certificate signed by unknown authority", "context deadline exceeded"

# Verify etcd is listening
ss -tlnp | grep 2379

# Test connectivity with the exact certs the API server uses
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key
```

### etcd is healthy but cluster state seems wrong / missing objects

```bash
# Check if the data directory was accidentally reset (e.g. after a bad restore)
ls -lah /var/lib/etcd/member/

# Check etcd revision — a sudden drop indicates a restore happened
etcdctl endpoint status --write-out=table
# Compare RAFT INDEX and DB SIZE against expected values
```

### Disk space / database quota exceeded

```bash
# Check backend DB size
etcdctl endpoint status --write-out=table
# If DB SIZE approaches quota-backend-bytes, the cluster becomes read-only

# Compact old revisions (safe to run on leader)
rev=$(etcdctl endpoint status --write-out=json | jq '.[0].Status.header.revision')
etcdctl compact $rev

# Defrag after compaction
etcdctl defrag

# Increase quota (edit etcd.yaml)
# --quota-backend-bytes=8589934592   # 8 GiB
```

### Troubleshooting certificate issues

```bash
# Inspect a certificate
openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -noout -text | \
  grep -E 'Subject:|Issuer:|Not After|IP Address|DNS'

# Check cert expiry
kubeadm certs check-expiration | grep etcd

# Renew etcd certs
kubeadm certs renew etcd-server
kubeadm certs renew etcd-peer
kubeadm certs renew etcd-healthcheck-client
kubeadm certs renew apiserver-etcd-client
```

---

## 14. Quick Reference

### etcdctl flags cheatsheet

| Flag | Purpose |
|---|---|
| `--endpoints` | Comma-separated list of etcd client URLs |
| `--cacert` | Path to etcd CA cert (`etcd/ca.crt`) |
| `--cert` | Path to client cert (server cert or healthcheck-client cert) |
| `--key` | Path to client private key |
| `--write-out` | Output format: `table`, `json`, `simple` |

### Common commands

```bash
# Health check
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Endpoint status (leader, DB size, Raft index)
ETCDCTL_API=3 etcdctl endpoint status --write-out=table \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Member list
ETCDCTL_API=3 etcdctl member list --write-out=table \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Backup
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore
ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# Check cert expiry
kubeadm certs check-expiration | grep etcd
```

### Restore procedure summary

| Step | Action |
|---|---|
| 1 | `mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/` |
| 2 | `etcdctl snapshot restore <file> --data-dir=<new-dir>` |
| 3 | Edit `etcd.yaml`: update `--data-dir` and `hostPath.path` |
| 4 | `mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/` |
| 5 | `watch crictl ps` → confirm pods come back |
| 6 | `kubectl get nodes && kubectl get pods -A` |

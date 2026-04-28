# Kubernetes Commands Reference

Deep reference for every major Kubernetes binary: what it does, important flags, how to read
the output, and what breaks when you get it wrong. Internals-focused - not a cheatsheet.

---

## Part 1: kubeadm

kubeadm bootstraps and manages the lifecycle of a Kubernetes control plane. It generates PKI,
writes static pod manifests, bootstraps RBAC, and prints join tokens. It does **not** install
kubelet or a container runtime - that must be done separately.

---

### 1.1 - `kubeadm init`

Initialises a new control plane node from scratch.

**Internal steps (in order):**

1. **Preflight checks** - verifies kernel modules (`br_netfilter`, `overlay`), open ports,
   container runtime is reachable at its socket, swap is off (unless `--ignore-preflight-errors`)
2. **Generates PKI** - writes all certs and keys under `/etc/kubernetes/pki/`
3. **Writes kubeconfigs** - `admin.conf`, `kubelet.conf`, `controller-manager.conf`,
   `scheduler.conf` under `/etc/kubernetes/`
4. **Writes static pod manifests** - `kube-apiserver.yaml`, `kube-controller-manager.yaml`,
   `kube-scheduler.yaml`, `etcd.yaml` under `/etc/kubernetes/manifests/`
5. **Waits for API server** - polls `/healthz` until healthy
6. **Bootstraps RBAC** - creates ClusterRoles and bindings required by system components
7. **Installs CoreDNS and kube-proxy** - as Deployments/DaemonSets in `kube-system`
8. **Prints `kubeadm join` command** - includes bootstrap token and CA cert hash

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

### 1.2 - `kubeadm join`

Joins a node (worker or control plane) to an existing cluster.

**Two modes:**

- **Worker join**: presents bootstrap token -> API server issues kubelet client certificate via CSR
  API -> kubelet switches from token auth to certificate auth
- **Control plane join**: `--control-plane --certificate-key` -> downloads PKI from `kube-system`
  Secret -> writes static pod manifests -> becomes an additional master

**Key flags:**

```
--token                            # bootstrap token (format: abcdef.0123456789abcdef)
--discovery-token-ca-cert-hash     # SHA256 of cluster CA public key (pins the CA)
--control-plane                    # join as additional control plane node
--certificate-key                  # decryption key for uploaded certs (HA setup)
--apiserver-advertise-address      # override advertise address for this control plane
--discovery-file                   # use a kubeconfig file for discovery instead of token
```

**Internal flow - worker join:**

1. Kubelet starts using `bootstrap-kubelet.conf` (token as credential)
2. Kubelet submits a `CertificateSigningRequest` to the API server
3. The `csrapproving` controller auto-approves bootstrap CSRs matching the bootstrap RBAC
4. Kubelet receives the signed cert, writes it as a dated `.pem` file
5. `kubelet-client-current.pem` symlink is updated to point to the new cert
6. Kubelet restarts, now authenticating with the real client cert - token no longer used

**What breaks:**
- Expired bootstrap token -> CSR submission is rejected -> join fails at step 2
- Wrong `--discovery-token-ca-cert-hash` -> TLS verification failure at discovery phase
- Missing `--certificate-key` for control plane join -> PKI Secret cannot be decrypted

---

### 1.3 - `kubeadm certs`

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

- `EXTERNALLY MANAGED: yes` means cert-manager or another system controls this cert - do not
  renew manually
- CA certs have 10-year validity; leaf certs have 1-year validity by default
- After `renew`, static pod manifests must be restarted: move them out and back into
  `/etc/kubernetes/manifests/`

---

### 1.4 - `kubeadm token`

Manages bootstrap tokens used by new nodes to join the cluster.

```bash
kubeadm token create                        # create new bootstrap token (24h TTL by default)
kubeadm token create --print-join-command   # full join command including hash
kubeadm token create --ttl 0                # non-expiring token (use carefully)
kubeadm token list                          # show all tokens + expiry time
kubeadm token delete <token>                # revoke a token immediately
```

**Bootstrap token format:** `<6-char>.<16-char>` - e.g. `abcdef.0123456789abcdef`

Stored as Secrets in `kube-system` namespace: `bootstrap-token-<token-id>`

The token ID (first 6 chars) becomes the Secret name; the full token is hashed and stored.
The `system:bootstrappers:kubeadm:default-node-token` group grants the CSR submission RBAC.

---

### 1.5 - `kubeadm upgrade`

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
- kubectl can be +/-1 minor version from the server

---

### 1.6 - `kubeadm config`

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

### 1.7 - `kubeadm reset`

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

After `kubeadm reset`, `kubelet` may still be running - stop it:
```bash
systemctl stop kubelet
```

---

### 1.8 - `kubeadm init phase` (granular control)

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

## Part 2: kubectl

The primary CLI for interacting with the Kubernetes API server. Every command is ultimately a
REST call to the API server. kubectl reads its configuration from `~/.kube/config` (or
`$KUBECONFIG`).

---

### 2.1 - Cluster Info and Context

```bash
kubectl cluster-info                            # API server URL + CoreDNS URL
kubectl cluster-info dump                       # full cluster state dump (large - pipe to file)
kubectl version                                 # client and server versions (check version skew)
kubectl api-resources                           # all resource types: NAME, SHORTNAMES, APIVERSION, NAMESPACED, KIND
kubectl api-resources --namespaced=false        # cluster-scoped resources only
kubectl api-versions                            # all API groups and versions registered
kubectl explain <resource>                      # schema docs with field descriptions
kubectl explain pod.spec.containers.securityContext --recursive  # full nested schema
```

**Context management:**
```bash
kubectl config view                             # full kubeconfig (redacts certificates by default)
kubectl config view --raw                       # include raw cert data
kubectl config get-contexts                     # list all contexts with current marked by *
kubectl config current-context                  # print current context name
kubectl config use-context <name>               # switch to a different context
kubectl config set-context --current --namespace=<ns>   # set default namespace for current context
kubectl config set-cluster <name> --server=https://...
kubectl config set-credentials <name> --token=...
kubectl config delete-context <name>
```

---

### 2.2 - Get / Describe

```bash
kubectl get <resource>                          # list resources in current namespace
kubectl get pods -A                             # all namespaces (-A = --all-namespaces)
kubectl get pods -n <namespace>                 # specific namespace
kubectl get pods -o wide                        # adds Node, IP, Nominated Node, Readiness Gates
kubectl get pods -o yaml                        # full YAML spec + status
kubectl get pods -o json                        # JSON output
kubectl get pods -o jsonpath='{.items[*].metadata.name}'    # extract specific fields
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
kubectl get pods --field-selector=status.phase=Running      # server-side field filter
kubectl get pods --field-selector=spec.nodeName=node1
kubectl get pods -l app=nginx                   # label selector
kubectl get pods -l 'env in (prod, staging)'    # set-based selector
kubectl get pods --sort-by=.metadata.creationTimestamp
kubectl get pods -w                             # watch for changes (streams events)
kubectl get pods --show-labels                  # add LABELS column
kubectl get events --sort-by=.lastTimestamp     # cluster events sorted by time
kubectl get events -n <ns> --field-selector=involvedObject.name=<pod>
```

**Reading `kubectl describe pod` output:**

| Section      | What to look at                                                       |
|--------------|-----------------------------------------------------------------------|
| `Events`     | most useful for debugging: `FailedScheduling`, `BackOff`, `Pulling`   |
| `Conditions` | `PodScheduled`, `Initialized`, `ContainersReady`, `Ready`             |
| `State`      | `Running`, `Waiting` (with reason), `Terminated` (with exit code)    |
| `Mounts`     | which volumes/secrets/configmaps are injected                         |
| `QoS Class`  | `Guaranteed` / `Burstable` / `BestEffort` (affects eviction order)   |
| `Node`       | which node the pod is on; `<none>` if unscheduled                     |

---

### 2.3 - Create / Apply / Edit / Delete

```bash
kubectl create -f <file>                        # create from file (errors if resource exists)
kubectl apply -f <file>                         # create or update (idempotent; preferred)
kubectl apply -f <dir>/                         # apply all files in a directory
kubectl apply -k <dir>/                         # apply a Kustomization
kubectl edit <resource> <name>                  # open live resource in $EDITOR (default vi)
kubectl patch deployment <name> -p '{"spec":{"replicas":3}}'   # strategic merge patch
kubectl patch deployment <name> --type=json \
  -p '[{"op":"replace","path":"/spec/replicas","value":3}]'    # JSON patch
kubectl replace -f <file>                       # replace entire resource (no merge)
kubectl replace --force -f <file>               # delete + recreate (last resort)
kubectl delete -f <file>
kubectl delete pod <name>
kubectl delete pod <name> --grace-period=0 --force    # immediate SIGKILL (for stuck terminating pods)
kubectl delete pod <name> --wait=false          # don't wait for deletion to complete
```

**Imperative create shortcuts (exam essential):**
```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl create service clusterip my-svc --tcp=80:8080
kubectl create configmap my-cm --from-literal=key=value --from-file=config.txt
kubectl create secret generic my-secret --from-literal=password=abc123
kubectl create secret tls my-tls --cert=tls.crt --key=tls.key
kubectl create serviceaccount my-sa
kubectl create namespace prod
kubectl create role pod-reader --verb=get,list --resource=pods
kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
kubectl create rolebinding dev-pod-reader --role=pod-reader --user=jane -n dev
kubectl create clusterrolebinding pod-reader-global --clusterrole=pod-reader --user=jane
```

**`--dry-run=client -o yaml` pattern (exam essential):**
```bash
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml
kubectl run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
# edit the yaml, then:
kubectl apply -f deploy.yaml
```

---

### 2.4 - Logs / Exec / Port-Forward / Copy

```bash
kubectl logs <pod>                              # stdout/stderr of first (or only) container
kubectl logs <pod> -c <container>               # specific container in a multi-container pod
kubectl logs <pod> --previous                   # logs from the previously crashed container
kubectl logs <pod> -f                           # follow (stream, like tail -f)
kubectl logs <pod> --tail=50                    # last 50 lines
kubectl logs <pod> --since=1h                   # logs from last hour
kubectl logs -l app=nginx                       # logs from all pods matching label
kubectl logs -l app=nginx --all-containers=true

kubectl exec <pod> -- <cmd>                     # run command in pod (non-interactive)
kubectl exec -it <pod> -- /bin/bash             # interactive shell
kubectl exec -it <pod> -c <container> -- sh    # specific container

kubectl port-forward pod/<name> 8080:80         # tunnel: localhost:8080 -> pod:80
kubectl port-forward svc/<name> 8080:80         # tunnel: localhost:8080 -> service:80
kubectl port-forward deploy/<name> 8080:80

kubectl cp <pod>:/path/to/file ./local-file     # copy from pod to local
kubectl cp ./local-file <pod>:/path/in/pod      # copy from local to pod
```

---

### 2.4.1 - Data Transfer Patterns (Exam)

When a question asks you to write output from inside a pod or remote node to a local file:

**Pod -> Local**

```bash
# Option 1: kubectl cp (cleanest)
# Note: "tar: removing leading '/' from member names" is a harmless tar warning - copy succeeds
kubectl cp <namespace>/<pod>:/path/in/pod ./local-file
kubectl cp project-swan/api-contact:/tmp/result.json lab/result.json

# Option 2: kubectl exec + cat, redirected locally
kubectl -n <namespace> exec <pod> -- cat /tmp/result.json > ./local-file

# Option 3: run the command non-interactively and redirect directly
kubectl -n <namespace> exec <pod> -- curl -sk https://... > ./local-file
```

**Remote Node -> Local**

```bash
# SSH + cat redirect
ssh node01 "cat /etc/kubernetes/manifests/kube-apiserver.yaml" > local-copy.yaml

# SCP
scp node01:/path/to/file ./local-copy

# Pipe any command over SSH
ssh node01 "crictl ps" > output.txt
```

**Workflow pattern:**
1. Do the work inside the pod/node, optionally save to a temp file (`> /tmp/result.json`)
2. Exit back to the exam terminal
3. Pull with `kubectl exec -- cat <file> > local-file` or `ssh node cat <file> > local-file`

---

### 2.5 - Rollout / Scale

```bash
kubectl rollout status deployment/<name>        # watch rollout progress (exit 0 when done)
kubectl rollout status deployment/<name> --timeout=2m
kubectl rollout history deployment/<name>       # show revision history
kubectl rollout history deployment/<name> --revision=2   # detail for a specific revision
kubectl rollout undo deployment/<name>          # roll back to previous revision
kubectl rollout undo deployment/<name> --to-revision=2   # roll back to specific revision
kubectl rollout restart deployment/<name>       # rolling restart (bumps pod-template-hash)
kubectl rollout pause deployment/<name>         # pause a rollout mid-way
kubectl rollout resume deployment/<name>        # resume paused rollout

kubectl scale deployment/<name> --replicas=5
kubectl scale statefulset/<name> --replicas=3
kubectl autoscale deployment/<name> --min=2 --max=10 --cpu-percent=80  # creates HPA
```

**What breaks during rollout:**
- `kubectl rollout status` blocks until complete or times out; exit non-zero on failure
- `CHANGE-CAUSE` in history is empty unless `--record` was used or annotation was set manually
- Paused deployment never progresses - check with `kubectl get deploy` (`PAUSED` column)

---

### 2.6 - Node Management

```bash
kubectl cordon <node>                           # mark node unschedulable (NoSchedule taint added)
kubectl uncordon <node>                         # remove unschedulable mark
kubectl drain <node>                            # evict all evictable pods, then cordon
  --ignore-daemonsets                           # required when DaemonSet pods exist
  --delete-emptydir-data                        # evict pods with emptyDir volumes
  --grace-period=0                              # skip graceful termination
  --force                                       # evict pods not managed by a controller
  --timeout=60s

kubectl taint nodes <node> key=value:NoSchedule
kubectl taint nodes <node> key=value:NoExecute
kubectl taint nodes <node> key=value:PreferNoSchedule
kubectl taint nodes <node> key=value:NoSchedule-    # remove taint (trailing -)

kubectl label nodes <node> disktype=ssd
kubectl label nodes <node> disktype-               # remove label
kubectl annotate nodes <node> description="storage node"

kubectl top nodes                               # CPU and memory usage per node (needs metrics-server)
kubectl top pods -A                             # CPU and memory per pod
kubectl top pods -l app=nginx --containers      # per-container breakdown
```

**Drain sequence:**
1. `cordon` - node marked `SchedulingDisabled`
2. All pods evicted (respects `PodDisruptionBudget` - drain blocks if PDB would be violated)
3. DaemonSet pods are skipped (they are owned by the node)
4. StaticPods are skipped

---

### 2.7 - Auth / RBAC Debugging

```bash
kubectl auth can-i list pods                         # can current user list pods?
kubectl auth can-i list pods --namespace=prod --as=jane    # impersonate a user
kubectl auth can-i '*' '*'                           # does current user have full admin?
kubectl auth whoami                                  # show current user identity

kubectl get clusterrolebindings -o wide | grep <user>
kubectl describe clusterrolebinding <name>
kubectl describe rolebinding <name> -n <ns>
```

---

### 2.8 - Debug

```bash
kubectl debug pod/<name> --image=busybox --it           # ephemeral debug container
kubectl debug pod/<name> --copy-to=debug-pod --it       # copy pod and attach
kubectl debug node/<name> --image=busybox --it          # privileged pod on node
kubectl run tmp --image=busybox --restart=Never -it --rm -- sh   # throwaway debug pod
```

---

## Part 3: kubelet

The node agent. Runs on every node (control plane and workers). Not managed by the API server
- it is a systemd service that **manages** pods on the node.

---

### 3.1 - What kubelet Does

- Watches API server for `Pod` objects assigned to this node (`spec.nodeName` set)
- Also watches the `staticPodPath` directory for static pod manifests (used by control plane)
- Calls the CRI (containerd via `/run/containerd/containerd.sock`) to create/start/stop containers
- Reports pod and node status back to the API server
- Serves health and metrics endpoints on port 10250 (TLS, requires authn/authz)
- Manages volume mounts, secret injection, projected service account tokens
- Runs liveness, readiness, and startup probes
- Manages certificate rotation: client cert (CSR API), server cert (`serverTLSBootstrap`)

---

### 3.2 - Configuration

kubelet is configured via a `KubeletConfiguration` file (flags are deprecated):

```
/var/lib/kubelet/config.yaml          # KubeletConfiguration object
/var/lib/kubelet/kubeadm-flags.env    # remaining CLI flags set by kubeadm
```

**Key `KubeletConfiguration` fields:**

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDNS:
  - 10.96.0.10                        # CoreDNS ClusterIP
clusterDomain: cluster.local
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
staticPodPath: /etc/kubernetes/manifests   # control plane nodes only
authentication:
  anonymous:
    enabled: false                    # must be false (security hardening)
  webhook:
    enabled: true                     # delegates authn to API server
authorization:
  mode: Webhook                       # delegates authz to API server (Node authorizer)
serverTLSBootstrap: true             # kubelet requests its own serving cert via CSR
rotateCertificates: true             # automatically rotates client cert before expiry
evictionHard:
  memory.available: "100Mi"          # evict pods when node has < 100Mi free memory
  nodefs.available: "10%"            # evict when node disk < 10%
  imagefs.available: "15%"
cpuManagerPolicy: static             # CPU pinning for Guaranteed QoS pods
topologyManagerPolicy: none
cgroupDriver: systemd                # must match containerd cgroupDriver
```

---

### 3.3 - Key Endpoints

| Endpoint                  | Purpose                                              |
|---------------------------|------------------------------------------------------|
| `:10250/healthz`          | kubelet health (requires valid client cert)          |
| `:10250/pods`             | JSON list of all pods on this node                   |
| `:10250/stats/summary`    | CPU/memory resource usage stats                      |
| `:10250/logs/<logfile>`   | read node log files                                  |
| `:10248/healthz`          | local-only health check (no TLS, no auth)            |

The `:10248` endpoint is used by `kubeadm` preflight to check kubelet is running.

---

### 3.4 - Systemd Unit and Debugging

```bash
systemctl status kubelet               # show current state, last log lines
systemctl start kubelet
systemctl stop kubelet
systemctl restart kubelet
systemctl daemon-reload                # reload unit files after editing service file

journalctl -u kubelet -f               # follow kubelet logs (most useful debug source)
journalctl -u kubelet --since "5 min ago"
journalctl -u kubelet -n 100           # last 100 lines
```

**Common kubelet failure modes:**

| Symptom                        | Likely cause                                              |
|--------------------------------|-----------------------------------------------------------|
| kubelet fails to start         | wrong cgroupDriver (must match containerd)                |
| Pod stuck in `ContainerCreating`| CRI socket path wrong; containerd not running            |
| Node shows `NotReady`          | kubelet not running, or can't reach API server            |
| `Failed to pull image`         | imagePullPolicy, registry auth, or network issue          |
| `Evicted` pods                 | eviction thresholds hit - check `kubectl describe node`   |

---

## Part 4: kube-apiserver

The front door to the cluster. Every interaction - kubectl commands, controller reconciliation,
scheduler decisions, kubelet status reports - goes through the API server.

---

### 4.1 - What It Does

- **Authenticates** every request (client cert, bearer token, OIDC, webhook)
- **Authorizes** every request (RBAC, Node authorizer, webhook)
- **Runs admission controllers** - mutating webhooks first, then validating webhooks
- **Persists** all Kubernetes objects to etcd
- **Serves watch streams** to controllers, kubelets, and kubectl `-w` commands
- **Aggregates** extended API groups (metrics-server, custom APIs via aggregation layer)

---

### 4.2 - Run Mode

Runs as a **static pod** on each control plane node.

Manifest: `/etc/kubernetes/manifests/kube-apiserver.yaml`

Editing the manifest causes kubelet to detect the change and restart the API server within
seconds. Always validate YAML syntax before saving - a syntax error will break the manifest and
take down the API server.

---

### 4.3 - Critical Flags

**TLS / Authentication:**
```
--client-ca-file=/etc/kubernetes/pki/ca.crt
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt
--tls-private-key-file=/etc/kubernetes/pki/apiserver.key
--service-account-key-file=/etc/kubernetes/pki/sa.pub        # verifies SA JWT tokens
--service-account-issuer=https://kubernetes.default.svc.cluster.local
--anonymous-auth=false                                         # CKS: must be false
--oidc-issuer-url=...                                          # external OIDC provider
--oidc-client-id=...
```

**Authorization:**
```
--authorization-mode=Node,RBAC         # Node authorizer (for kubelets) + RBAC
```

**etcd connection:**
```
--etcd-servers=https://127.0.0.1:2379
--etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
--etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
--etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
```

**Admission:**
```
--enable-admission-plugins=NodeRestriction,PodSecurity,...
--disable-admission-plugins=...
--admission-control-config-file=...    # for PodSecurity configuration (enforce/audit/warn)
```

**Security / Audit:**
```
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--audit-log-path=/var/log/kubernetes/audit.log
--audit-log-maxsize=100               # rotate at 100 MB
--audit-log-maxbackup=5
--profiling=false                     # CKS: disable CPU profile endpoint
--request-timeout=60s
```

**Aggregation layer (for metrics-server etc.):**
```
--requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
--proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
--proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
--requestheader-allowed-names=front-proxy-client
--requestheader-extra-headers-prefix=X-Remote-Extra-
--requestheader-group-headers=X-Remote-Group
--requestheader-username-headers=X-Remote-User
```

**What breaks:**
- Wrong etcd cert path -> API server cannot reach etcd -> all reads/writes fail
- `--anonymous-auth=true` -> unauthenticated requests can probe the API
- Mismatched `--service-account-key-file` between apiserver and controller-manager -> SA token
  verification fails

---

## Part 5: kube-scheduler

Assigns unscheduled pods to nodes. It runs the scheduling algorithm (filter -> score -> bind)
and writes the chosen node name back to `pod.spec.nodeName` via the API server.

---

### 5.1 - What It Does

- **Watches** for pods with no `.spec.nodeName` (unscheduled pods)
- **Filters** candidate nodes using predicates (resource fit, taints, affinity, topology spread)
- **Scores** remaining nodes using priority functions (balanced resource, affinity preference)
- **Binds** the pod to the best node (writes `pod.spec.nodeName` via API server `bind` subresource)

Never communicates directly with kubelets or containerd - only with the API server.

---

### 5.2 - Run Mode

Static pod: `/etc/kubernetes/manifests/kube-scheduler.yaml`

---

### 5.3 - Key Flags

```
--config=/etc/kubernetes/scheduler.conf       # kubeconfig for auth to API server
--leader-elect=true                           # HA: only one scheduler instance is active
--profiling=false                             # CKS: disable profiling endpoint
```

For custom scheduling profiles (multiple schedulers, plugins):
```yaml
# KubeSchedulerConfiguration
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
    plugins:
      score:
        disabled:
          - name: NodeResourcesBalancedAllocation
```

**Identity:** CN = `system:kube-scheduler`, no Organization.
Maps to the built-in `system:kube-scheduler` ClusterRole.

**What breaks:**
- Scheduler not running -> new pods stay in `Pending` with no `Events` (no scheduling events)
- Incorrect kubeconfig cert -> scheduler cannot watch pods -> no scheduling happens

---

## Part 6: kube-controller-manager

Runs all built-in Kubernetes control loops in a single process. Each controller watches
resources via the API server and reconciles actual state toward desired state.

---

### 6.1 - What It Does

Key controllers included:

| Controller                      | Responsibility                                                   |
|---------------------------------|------------------------------------------------------------------|
| Node controller                 | marks nodes `NotReady`, evicts pods when node unreachable        |
| Deployment controller           | creates/updates ReplicaSets to match desired spec                |
| ReplicaSet controller           | creates/deletes pods to match replica count                      |
| StatefulSet controller          | manages ordered pod creation and persistent volumes              |
| Job controller                  | creates pods for batch Jobs, tracks completions/failures         |
| CronJob controller              | creates Jobs on a schedule                                       |
| ServiceAccount controller       | creates default ServiceAccount + token for new namespaces        |
| Namespace controller            | handles namespace deletion (processes finalizers)                |
| EndpointSlice controller        | keeps EndpointSlices in sync with pod IP addresses               |
| CertificateSigningRequest ctrl  | auto-approves kubelet bootstrap CSRs                             |
| Token controller                | signs ServiceAccount JWT tokens using `sa.key`                   |
| PersistentVolume controller     | binds PVCs to PVs; provisions dynamic PVs via StorageClass       |

---

### 6.2 - Run Mode

Static pod: `/etc/kubernetes/manifests/kube-controller-manager.yaml`

---

### 6.3 - Key Flags

```
--kubeconfig=/etc/kubernetes/controller-manager.conf
--service-account-private-key-file=/etc/kubernetes/pki/sa.key    # signs SA JWT tokens
--root-ca-file=/etc/kubernetes/pki/ca.crt
--cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt           # signs kubelet CSRs
--cluster-signing-key-file=/etc/kubernetes/pki/ca.key
--leader-elect=true
--profiling=false                                                  # CKS: disable
--node-monitor-grace-period=40s        # time before node marked Unreachable
--node-monitor-period=5s               # how often node status is checked
--pod-eviction-timeout=5m0s            # time after Unreachable before pods are evicted
--controllers=*,bootstrapsigner,tokencleaner   # * = all built-in + named extras
--use-service-account-credentials=true         # each controller uses its own SA token
```

**Identity:** CN = `system:kube-controller-manager`.
Maps to built-in `system:kube-controller-manager` ClusterRole.

**What breaks:**
- Wrong `sa.key` path -> ServiceAccount tokens cannot be signed -> pods using SAs get auth errors
- Controller-manager not running -> Deployments/ReplicaSets not reconciled -> pods not created
- `--cluster-signing-*` wrong -> kubelet bootstrap CSRs not signed -> worker nodes cannot join

---

## Part 7: containerd Ecosystem

### 7.1 - containerd

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

### 7.2 - crictl (CRI CLI)

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
- Pod stuck in `ContainerCreating` -> kubelet hasn't surfaced the error yet
- Static pod not appearing -> crictl shows what containerd actually has
- Image pull errors at the runtime level before kubelet updates pod status

---

### 7.3 - ctr (low-level containerd CLI)

Direct containerd management tool. Uses containerd namespaces - Kubernetes workloads live in
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

### 7.4 - etcdctl

The CLI for etcd - the key-value store that persists all Kubernetes cluster state.

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

# List all keys (huge output - filter with grep)
etcdctl get / --prefix --keys-only

# Backup
etcdctl snapshot save /tmp/etcd-backup.db

# Verify backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore (creates new data directory - do NOT restore over live data)
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
# If AES-CBC encryption is active, output is binary garbage - confirms encryption works
```

---

## Quick Reference: Certificate File Map

| File                                           | Used by                   | Purpose                           |
|------------------------------------------------|---------------------------|-----------------------------------|
| `/etc/kubernetes/pki/ca.crt`                   | all components            | cluster CA - validates everything |
| `/etc/kubernetes/pki/ca.key`                   | controller-manager        | signs kubelet client certs        |
| `/etc/kubernetes/pki/apiserver.crt`            | kube-apiserver            | TLS serving cert                  |
| `/etc/kubernetes/pki/apiserver-kubelet-client.crt` | kube-apiserver        | client cert to kubelets           |
| `/etc/kubernetes/pki/apiserver-etcd-client.crt`| kube-apiserver            | client cert to etcd               |
| `/etc/kubernetes/pki/sa.pub`                   | kube-apiserver            | verifies ServiceAccount JWTs      |
| `/etc/kubernetes/pki/sa.key`                   | kube-controller-manager   | signs ServiceAccount JWTs         |
| `/etc/kubernetes/pki/etcd/ca.crt`              | etcd, apiserver           | etcd CA                           |
| `/etc/kubernetes/pki/etcd/server.crt`          | etcd                      | etcd TLS serving cert             |
| `/etc/kubernetes/pki/etcd/peer.crt`            | etcd                      | etcd peer communication cert      |
| `/etc/kubernetes/pki/front-proxy-ca.crt`       | kube-apiserver            | aggregation layer CA              |
| `/etc/kubernetes/pki/front-proxy-client.crt`   | kube-apiserver            | aggregation layer client cert     |

---

## Quick Reference: Component Identity (CN / O)

| Component               | Certificate CN                     | Organization (O)              |
|-------------------------|------------------------------------|-------------------------------|
| kube-apiserver          | `kube-apiserver`                   | -                             |
| kube-controller-manager | `system:kube-controller-manager`   | -                             |
| kube-scheduler          | `system:kube-scheduler`            | -                             |
| kubelet (client)        | `system:node:<nodename>`           | `system:nodes`                |
| kube-proxy              | `system:kube-proxy`                | -                             |
| admin user              | `kubernetes-admin`                 | `system:masters`              |
| etcd                    | varies (e.g. `etcd-server`)        | -                             |

---

## Quick Reference: Static Pod Manifest Locations

All control plane components run as static pods on control plane nodes:

```
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml
/etc/kubernetes/manifests/etcd.yaml
```

Editing any of these files triggers kubelet to automatically restart the pod.
kubelet watches the directory specified in `staticPodPath` (default `/etc/kubernetes/manifests`).

---

## Quick Reference: Port Map

| Port  | Component               | Protocol | Purpose                            |
|-------|-------------------------|----------|------------------------------------|
| 6443  | kube-apiserver          | HTTPS    | Kubernetes API (all clients)       |
| 2379  | etcd                    | HTTPS    | client requests (API server)       |
| 2380  | etcd                    | HTTPS    | peer-to-peer replication           |
| 10250 | kubelet                 | HTTPS    | API server -> kubelet calls         |
| 10248 | kubelet                 | HTTP     | local healthz (no auth)            |
| 10257 | kube-controller-manager | HTTPS    | healthz + metrics (local)          |
| 10259 | kube-scheduler          | HTTPS    | healthz + metrics (local)          |
| 10256 | kube-proxy              | HTTP     | healthz                            |

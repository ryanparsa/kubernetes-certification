# Question 7 | Etcd Operations

> **Solve this question on:** the "cka-lab" kind cluster
> **For tasks requiring direct access to the control plane node (e.g. etcd snapshot):** `docker exec -it cka-lab-control-plane bash`

You have been tasked to perform the following etcd operations:

Run `etcd --version` and store the output at `cka/24/course/etcd-version`

Make a snapshot of etcd and save it at `cka/24/course/etcd-snapshot.db`

## Answer

### Step 1: Etcd Version

Here we simply need to execute a command, shouldn't be that hard:

```bash
etcd --version
```

```
Command 'etcd' not found, but can be installed with:
apt install etcd-server
```

Well, etcd is not installed directly on the controlplane but it runs as a *Pod* instead. So we do:

```bash
kubectl -n kube-system get pod
```

```
NAME                                            READY   STATUS    RESTARTS      AGE
coredns-78c4c75bb8-fgkfv                        1/1     Running   0             15d
coredns-78c4c75bb8-l7mmh                        1/1     Running   0             15d
etcd-cka-lab-control-plane                      1/1     Running   0             13m
kube-apiserver-cka-lab-control-plane            1/1     Running   0             15d
kube-controller-manager-cka-lab-control-plane   1/1     Running   0             15d
kube-proxy-f56td                                1/1     Running   0             15d
kube-scheduler-cka-lab-control-plane            1/1     Running   0             15d
```

```bash
kubectl -n kube-system exec etcd-cka-lab-control-plane -- etcd --version
```

```
etcd Version: 3.6.4
Git SHA: 5400cdc
Go Version: go1.23.11
Go OS/Arch: linux/amd64
```

```bash
kubectl -n kube-system exec etcd-cka-lab-control-plane -- etcd --version > cka/24/course/etcd-version
```

### Step 2: Etcd Snapshot

> [!NOTE]
> For the snapshot, exec into the control plane node first: `docker exec -it cka-lab-control-plane bash`
> Inside the node, `cka/24/course/` on your host is mounted at `/opt/course/7/`.

First we try to create a snapshot of etcd:

```bash
ETCDCTL_API=3 etcdctl snapshot save /opt/course/7/etcd-snapshot.db
```

```
{"level":"info","ts":"2024-11-07T14:02:17.746254Z","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"/opt/course/7/etcd-snapshot.db.part"}
^C
```

But it fails or hangs because we need to authenticate ourselves. For the necessary information we can check the etcd manifest:

```bash
vim /etc/kubernetes/manifests/etcd.yaml
```

We only check the `etcd.yaml` for necessary information we don't change it.

```yaml
# /etc/kubernetes/manifests/etcd.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: etcd
    tier: control-plane
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.100.31:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt                           # use
    - --client-cert-auth=true
    - --data-dir=/var/lib/etcd
    - --initial-advertise-peer-urls=https://192.168.100.31:2380
    - --initial-cluster=cka-lab-control-plane=https://192.168.100.31:2380
    - --key-file=/etc/kubernetes/pki/etcd/server.key                            # use
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.100.31:2379   # use
    - --listen-metrics-urls=http://127.0.0.1:2381
    - --listen-peer-urls=https://192.168.100.31:2380
    - --name=cka-lab-control-plane
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt                    # use
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    image: k8s.gcr.io/etcd:3.3.15-0
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 127.0.0.1
        path: /health
        port: 2381
        scheme: HTTP
      initialDelaySeconds: 15
      timeoutSeconds: 15
    name: etcd
    resources: {}
    volumeMounts:
    - mountPath: /var/lib/etcd
      name: etcd-data
    - mountPath: /etc/kubernetes/pki/etcd
      name: etcd-certs
  hostNetwork: true
  priorityClassName: system-cluster-critical
  volumes:
  - hostPath:
      path: /etc/kubernetes/pki/etcd
      type: DirectoryOrCreate
    name: etcd-certs
  - hostPath:
      path: /var/lib/etcd                                                     # important
      type: DirectoryOrCreate
    name: etcd-data
status: {}
```

But we also know that the api-server is connecting to etcd, so we can check how its manifest is configured:

```bash
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep etcd
```

```
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
```

We use the authentication information and pass it to etcdctl:

```bash
ETCDCTL_API=3 etcdctl snapshot save /opt/course/7/etcd-snapshot.db \
--cacert /etc/kubernetes/pki/etcd/ca.crt \
--cert /etc/kubernetes/pki/etcd/server.crt \
--key /etc/kubernetes/pki/etcd/server.key
```

Which should provide successful output:

```
{"level":"info","ts":"2025-03-02T13:35:48.806437Z","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"/opt/course/7/etcd-snapshot.db.part"}
{"level":"info","ts":"2025-03-02T13:35:48.929550Z","logger":"client","caller":"v3@v3.5.16/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-02T13:35:48.929975Z","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"127.0.0.1:2379"}
{"level":"info","ts":"2025-03-02T13:35:49.110620Z","logger":"client","caller":"v3@v3.5.16/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-02T13:35:49.155626Z","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"127.0.0.1:2379","size":"2.4 MB","took":"now"}
{"level":"info","ts":"2025-03-02T13:35:49.155886Z","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"/opt/course/7/etcd-snapshot.db"}
Snapshot saved at /opt/course/7/etcd-snapshot.db
```

### (Optional) Etcd Restore

> [!IMPORTANT]
> Doing this wrong can leave this cluster broken and will affect this question and also others

We create a *Pod* in the cluster and wait for it to be running:

```bash
kubectl run test --image=nginx
```

```
pod/test created
```

```bash
kubectl get pod -l run=test
```

```
NAME   READY   STATUS    RESTARTS   AGE
test   1/1     Running   0          17s
```

Next we stop all controlplane components:

```bash
cd /etc/kubernetes/manifests/

mv * ..

watch crictl ps
```

It's very important to wait for all K8s controlplane containers to be removed before continuing. This can take a minute!

> [!NOTE]
> In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

Now we restore the snapshot into a specific directory. Since etcd 3.6, `etcdctl snapshot restore` has been removed in favour of `etcdutl snapshot restore`. Note the two different binaries:

- `etcdctl`
- `etcdutl`

The restore is an offline operation (it doesn't need to connect to etcd), so no certificates are needed:

```bash
etcdutl snapshot restore /opt/course/7/etcd-snapshot.db --data-dir /var/lib/etcd-snapshot
```

```
2025-03-02T13:38:07Z    info    snapshot/v3_snapshot.go:265     restoring snapshot      {"path": "/opt/course/7/etcd-snapshot.db", "wal-dir": "/var/lib/etcd-snapshot/member/wal", "data-dir": "/var/lib/etcd-snapshot", "snap-dir": "/var/lib/etcd-snapshot/member/snap", "initial-memory-map-size": 0}
2025-03-02T13:38:07Z    info    membership/store.go:141 Trimming membership information from the backend...
2025-03-02T13:38:07Z    info    membership/cluster.go:421       added member    {"cluster-id": "cdf818194e3a8c32", "local-member-id": "0", "added-peer-id": "8e9e05c52164694d", "added-peer-peer-urls": ["http://localhost:2380"]}
2025-03-02T13:38:08Z    info    snapshot/v3_snapshot.go:293     restored snapshot       {"path": "/opt/course/7/etcd-snapshot.db", "wal-dir": "/var/lib/etcd-snapshot/member/wal", "data-dir": "/var/lib/etcd-snapshot", "snap-dir": "/var/lib/etcd-snapshot/member/snap", "initial-memory-map-size": 0}
```

We could specify another host to make the backup from by using `etcdctl --endpoints http://IP`, but here we just use the default value which is: `http://127.0.0.1:2379`.

The restored files are located at the new folder `/var/lib/etcd-snapshot`, now we have to tell etcd to use that directory:

```bash
vim /etc/kubernetes/manifests/etcd.yaml
```

```yaml
# /etc/kubernetes/manifests/etcd.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: etcd
    tier: control-plane
  name: etcd
  namespace: kube-system
spec:
...
    - mountPath: /etc/kubernetes/pki/etcd
      name: etcd-certs
  hostNetwork: true
  priorityClassName: system-cluster-critical
  volumes:
  - hostPath:
      path: /etc/kubernetes/pki/etcd
      type: DirectoryOrCreate
    name: etcd-certs
  - hostPath:
      path: /var/lib/etcd-snapshot                # change
      type: DirectoryOrCreate
    name: etcd-data
status: {}
```

Now we move all controlplane yaml again into the manifest directory. Give it some time (up to several minutes) for etcd to restart and for the api-server to be reachable again:

```bash
mv ../*.yaml .

watch crictl ps
```

Then we check again for the *Pod*:

```bash
kubectl get pod -l run=test
```

```
No resources found in default namespace.
```

Awesome, snapshot and restore worked as our *Pod* is gone.


## Killer.sh Checklist (Score: 0/2)

- [ ] Version info correct
- [ ] Snapshot created

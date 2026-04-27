# etcd Reference

[← Back to index](../README.md)

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

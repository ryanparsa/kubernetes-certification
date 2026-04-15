# Task 3 — Cluster Architecture: etcd Snapshot Backup

**Context:** Cluster `cka-task-3` (`export KUBECONFIG=$PWD/kubeconfig`)

You must take a point-in-time snapshot of the cluster's etcd datastore.

## Objective

Save an etcd snapshot to **`/tmp/etcd-backup.db` inside the etcd static pod**
(`etcd-cka-task-3-control-plane` in the `kube-system` namespace).

The snapshot must:
- Be a valid etcd v3 snapshot (verifiable via `etcdctl snapshot status`).
- Be taken using the **correct mTLS material** referenced in `/etc/kubernetes/manifests/etcd.yaml`
  (`--cacert`, `--cert`, `--key`, `--endpoints`).
- Have non-zero size.

You can shell into the node with:
```
docker exec -it cka-task-3-control-plane bash
```

## Verify

```
./test.sh
```

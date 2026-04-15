# Task 13 — Cluster Architecture: etcd Restore

**Context:** Cluster `cka-task-13` (`export KUBECONFIG=$PWD/kubeconfig`)

A point-in-time etcd snapshot is on the control-plane node at:

```
/opt/snapshot.db   (on cka-task-13-control-plane)
```

At the time the snapshot was taken, the cluster contained the namespace `keepme`
and a ConfigMap `keepme/important`.

**After** the snapshot, someone created garbage state — namespace `junk` containing a
ConfigMap `junk/garbage` and a Deployment `junk/junkapp`.

## Objective

Restore etcd from `/opt/snapshot.db` so that the post-snapshot state is rolled back:

- Namespace `keepme` and ConfigMap `keepme/important` must still exist.
- Namespace `junk` must **not** exist.
- The cluster must remain functional (`kubectl get nodes` returns `Ready`).

You will need to:
1. SSH into the node: `docker exec -it cka-task-13-control-plane bash`
2. Run `etcdctl snapshot restore` into a new data directory.
3. Update `/etc/kubernetes/manifests/etcd.yaml` so etcd uses the restored data dir.
4. Wait for the static pod to restart and the API to come back.

## Verify

```
./test.sh
```

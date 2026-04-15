# Hints — Task 13

## Hint 1
The etcd binary on the kind node doesn't have a host `etcdctl`. Run it from inside the
running etcd pod via `kubectl -n kube-system exec etcd-cka-task-13-control-plane -- ...`,
restoring into a path that's hostPath-mounted from the node so the new data dir survives the
pod restart. `/var/lib/etcd-restored` works because we'll bind it via the manifest.

Alternatively, install `etcd-client` inside the node:
```bash
docker exec -it cka-task-13-control-plane bash
apt-get update && apt-get install -y etcd-client
```
This is the most exam-realistic path.

## Hint 2
The static pod manifest has a hostPath volume named `etcd-data` pointing at `/var/lib/etcd`.
Change that path (in the bottom `volumes:` list) to your new data dir, e.g. `/var/lib/etcd-restored`.
The kubelet will detect the file change and restart etcd with the new data.

## Solution

```bash
docker exec -it cka-task-13-control-plane bash
apt-get update -qq && apt-get install -y -qq etcd-client

ETCDCTL_API=3 etcdctl snapshot restore /opt/snapshot.db \
  --data-dir=/var/lib/etcd-restored

# Edit /etc/kubernetes/manifests/etcd.yaml — find:
#   - hostPath:
#       path: /var/lib/etcd
#       type: DirectoryOrCreate
#     name: etcd-data
# and change path to /var/lib/etcd-restored
sed -i 's|path: /var/lib/etcd$|path: /var/lib/etcd-restored|' /etc/kubernetes/manifests/etcd.yaml

# wait ~30s, exit, verify from host:
exit
kubectl get ns
kubectl -n keepme get cm important
kubectl get ns junk    # should NotFound
```

# Hints — Task 2

## Hint 1
The kubelet on the node is healthy — only the static pods it manages are broken.
Get into the node: `docker exec -it cka-task-2-control-plane bash`
Then: `crictl ps -a` to see which control-plane containers are missing or crashing.

## Hint 2
Look at `/etc/kubernetes/manifests/kube-apiserver.yaml`. Inspect the `--etcd-servers=` flag.
The correct value points at the local etcd: `https://127.0.0.1:2379`.

## Hint 3
Look at `/etc/kubernetes/manifests/kube-controller-manager.yaml`. There is a `resources.requests.cpu`
that exceeds physical capacity (e.g. `"99"`). Reduce it to something sane like `200m`, or remove the requests block entirely.

## Solution

```bash
docker exec -it cka-task-2-control-plane bash
# inside the node:
sed -i 's|--etcd-servers=https://192.168.99.99:2380|--etcd-servers=https://127.0.0.1:2379|' \
  /etc/kubernetes/manifests/kube-apiserver.yaml
sed -i 's|cpu: "99"|cpu: "200m"|' \
  /etc/kubernetes/manifests/kube-controller-manager.yaml
exit
# wait ~30s for kubelet to restart the static pods, then:
kubectl get nodes
kubectl -n kube-system get pods
```

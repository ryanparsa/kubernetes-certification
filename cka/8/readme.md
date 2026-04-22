# Question 8 | Update Kubernetes Version and join cluster

Your coworker notified you that node `cka-worker` is running an older Kubernetes version and is not even part of the cluster yet.

1. Update the node's Kubernetes to the exact version of the controlplane
2. Add the node to the cluster using kubeadm

> ℹ️ You can connect to the worker node using `docker exec -it cka-lab-worker bash` (or `kubectl debug node/cka-lab-worker -it --image=ubuntu`)

> ⚠️ **Kind limitation:** In this local kind lab both nodes already run the same Kubernetes version and the worker is already joined. You can still practise generating a join token (`kubeadm token create --print-join-command`) and exploring the kubeadm upgrade workflow.

## Answer

### Update Kubernetes to controlplane version

Search in the docs for [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade):

```bash
kubectl get node
NAME                    STATUS   ROLES           AGE    VERSION
cka-lab-control-plane   Ready    control-plane   4h7m   v1.35.2
```

The controlplane node is running Kubernetes 1.35.2.

On the worker node, install the updated kubelet and kubectl packages:

```bash
apt update
apt install kubectl=1.35.2-1.1 kubelet=1.35.2-1.1
service kubelet restart
```

### Add node to cluster

On the controlplane, generate a new TLS bootstrap token and print the join command:

```bash
kubeadm token create --print-join-command
kubeadm join 192.168.100.31:6443 --token xpexct.yefojay1ejbq8akx --discovery-token-ca-cert-hash sha256:...
```

On the worker node, run the join command printed above:

```bash
kubeadm join 192.168.100.31:6443 --token xpexct.yefojay1ejbq8akx --discovery-token-ca-cert-hash sha256:...
```

> ℹ️ If you have troubles with `kubeadm join` you might need to run `kubeadm reset` before

Finally check the node status from the controlplane:

```bash
kubectl get node
NAME             STATUS   ROLES           AGE     VERSION
cka-lab-control-plane   Ready    control-plane   4h13m   v1.35.2
cka-lab-worker          Ready    <none>          34s     v1.35.2
```

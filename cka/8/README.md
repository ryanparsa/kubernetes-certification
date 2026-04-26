# Question 8

> **Solve this question on:** the "cka-lab-8" kind cluster

Your coworker notified you that node `cka-lab-8-worker` is running an older Kubernetes version and is not even part of the cluster yet.

1. Update the node's Kubernetes to the exact version of the controlplane
2. Add the node to the cluster using kubeadm

> ⚠️ **Kind limitation:** In this local kind lab both nodes already run the same Kubernetes version and the worker is already joined. You can still practise generating a join token (`kubeadm token create --print-join-command`) and exploring the kubeadm upgrade workflow.

## Answer

Check the current Kubernetes version of the controlplane:

```bash
kubectl get node
NAME                      STATUS   ROLES           AGE    VERSION
cka-lab-8-control-plane   Ready    control-plane   4h7m   v1.35.2
```

### Solution using kubeadm

On the worker node, install the updated kubelet and kubectl packages matching the controlplane version:

```bash
apt update
apt install kubectl=1.35.2-1.1 kubelet=1.35.2-1.1
service kubelet restart
```

On the controlplane, generate a new TLS bootstrap token and print the join command:

```bash
kubeadm token create --print-join-command
```

On the worker node, run the join command printed above:

```bash
kubeadm join 192.168.100.31:6443 --token xpexct.yefojay1ejbq8akx --discovery-token-ca-cert-hash sha256:...
```

> ℹ️ If you have troubles with `kubeadm join` you might need to run `kubeadm reset` before.

### Verify

Check the node status from the controlplane:

```bash
kubectl get node
```

Example output:

```text
NAME                      STATUS   ROLES           AGE     VERSION
cka-lab-8-control-plane   Ready    control-plane   4h13m   v1.35.2
cka-lab-8-worker          Ready    <none>          34s     v1.35.2
```

## Killer.sh Checklist (Score: 0/3)

- [ ] Worker node is joined to the cluster
- [ ] All nodes are in Ready state
- [ ] All nodes run the same Kubernetes version

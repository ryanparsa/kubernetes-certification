# Question 5 | Kubectl sorting

> **Solve this question on:** the "cka-lab" kind cluster

Create two bash script files which use kubectl sorting to:

Write a command into `cka/22/course/find_pods.sh` which lists all *Pods* in all *Namespaces* sorted by their AGE (`metadata.creationTimestamp`)

Write a command into `cka/22/course/find_pods_uid.sh` which lists all *Pods* in all *Namespaces* sorted by field `metadata.uid`

## Answer

A good resource here (and for many other things) is the kubectl-cheat-sheet. You can reach it fast when searching for "cheat sheet" in the Kubernetes docs.

### Step 1

Create the script `cka/22/course/find_pods.sh`:

```bash
# cka/22/course/find_pods.sh
kubectl get pod -A --sort-by=.metadata.creationTimestamp
```

We should be able to execute it and see sorting by AGE:

```bash
sh cka/22/course/find_pods.sh
```

```
NAMESPACE     NAME                                       READY
kube-system   kube-proxy-dvv7m                           1/1
kube-system   etcd-cka-lab-control-plane                 1/1
kube-system   kube-apiserver-cka-lab-control-plane       1/1
kube-system   kube-scheduler-cka-lab-control-plane       1/1
kube-system   kube-controller-manager-cka-lab-control-plane 1/1
default       berlin-external-monitor-6c8fd896dd-66tvw   1/1
default       berlin-external-proxy-98bccbc68-59gjg      1/1
default       berlin-external-proxy-98bccbc68-phpvt      1/1
kube-system   coredns-6f8b9d9f4b-8z7rb                   1/1
kube-system   coredns-6f8b9d9f4b-fg7bt                   1/1
```

### Step 2

For the second command we create the script `cka/22/course/find_pods_uid.sh`:

```bash
# cka/22/course/find_pods_uid.sh
kubectl get pod -A --sort-by=.metadata.uid
```

When we execute we should see a different sorting order:

```bash
sh cka/22/course/find_pods_uid.sh
```

```
NAMESPACE     NAME                                       READY
kube-system   kube-proxy-dvv7m                           1/1
kube-system   coredns-6f8b9d9f4b-8z7rb                   1/1
default       berlin-external-monitor-6c8fd896dd-66tvw   1/1
default       berlin-external-proxy-98bccbc68-59gjg      1/1
default       berlin-external-proxy-98bccbc68-phpvt      1/1
kube-system   kube-controller-manager-cka-lab-control-plane 1/1
kube-system   kube-scheduler-cka-lab-control-plane       1/1
kube-system   kube-apiserver-cka-lab-control-plane       1/1
kube-system   etcd-cka-lab-control-plane                 1/1
kube-system   coredns-6f8b9d9f4b-fg7bt                   1/1
```

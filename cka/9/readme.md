# Question 9 | Kill Scheduler, Manual Scheduling

Temporarily stop the *kube-scheduler*, this means in a way that you can start it again afterwards.

Create a single *Pod* named `manual-schedule` of image `httpd:2-alpine`, confirm it's created but not scheduled on any *Node*.

Now you're the scheduler and have all its power, manually schedule that *Pod* on *Node* `cka-lab-9-control-plane`. Make sure it's running.

Start the *kube-scheduler* again and confirm it's running correctly by creating a second *Pod* named `manual-schedule2` of image `httpd:2-alpine` and check if it's running on `cka-lab-9-worker`.

> **Solve this question on:** the "cka-lab-9" kind cluster

## Answer

### Stop the Scheduler

First we find the controlplane *Node*:

```bash
kubectl get node
NAME                    STATUS   ROLES           AGE     VERSION
cka-lab-9-control-plane Ready    control-plane   6d22h   v1.33.1
cka-lab-9-worker        Ready    <none>          6d22h   v1.33.1
```

Then we check if the scheduler is running:

```bash
kubectl -n kube-system get pod | grep schedule
kube-scheduler-cka-lab-9-control-plane            1/1     Running   0               6d22h
```

Kill the Scheduler (temporarily) by moving the static *Pod* manifest out of the manifests directory:

```bash
# Run this inside the control-plane node container
# docker exec -it cka-lab-9-control-plane bash
mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/
```

And it should be stopped:

```bash
kubectl -n kube-system get pod | grep schedule
```

> ℹ️ In this environment `docker exec` is used for node access. In the real exam you would use `ssh` and `sudo -i`.

### Create a *Pod*

Now we create the *Pod*:

```bash
kubectl run manual-schedule --image=httpd:2-alpine
pod/manual-schedule created
```

And confirm it has no *Node* assigned:

```bash
kubectl get pod manual-schedule -o wide
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE    ...
manual-schedule   0/1     Pending   0          14s   <none>   <none>  ...
```

### Manually schedule the *Pod*

Let's play the scheduler now:

```bash
kubectl get pod manual-schedule -o yaml > 9.yaml
```

```yaml
# cka/9/course/9.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: manual-schedule
  name: manual-schedule
spec:
  nodeName: cka-lab-9-control-plane       # ADD the controlplane node name
  containers:
  - image: httpd:2-alpine
    name: manual-schedule
...
```

The scheduler sets the `nodeName` for a *Pod* declaration. How it finds the correct *Node* to schedule on, that's a very much complicated matter and takes many variables into account.

As we cannot `kubectl apply` or `kubectl edit`, in this case we need to delete and create or replace:

```bash
kubectl replace --force -f 9.yaml
```

How does it look?

```bash
kubectl get pod manual-schedule -o wide
NAME              READY   STATUS    ...   NODE
manual-schedule   1/1     Running   ...   cka-lab-9-control-plane
```

It looks like our *Pod* is running on the controlplane now as requested, although no tolerations were specified. Only the scheduler takes taints/tolerations/affinity into account when finding the correct *Node* name. That's why it's still possible to assign *Pods* manually directly to a controlplane *Node* and skip the scheduler.

### Start the scheduler again

Move the manifest back:

```bash
# Run this inside the control-plane node container
mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/
```

Checks it's running:

```bash
kubectl -n kube-system get pod | grep schedule
kube-scheduler-cka-lab-9-control-plane            1/1     Running   0               13s
```

Schedule a second test *Pod*:

```bash
kubectl run manual-schedule2 --image=httpd:2-alpine

kubectl get pod -o wide | grep schedule
manual-schedule    1/1     Running   0          95s   10.32.0.2   cka-lab-9-control-plane
manual-schedule2   1/1     Running   0          9s    10.44.0.3   cka-lab-9-worker
```

Back to normal.

## Checklist (Score: 0/10)

- [ ] Pod `manual-schedule` is running in namespace `default`
- [ ] Pod `manual-schedule` is scheduled on `cka-lab-9-control-plane`
- [ ] Pod `manual-schedule` has single container
- [ ] Pod `manual-schedule` container has correct image
- [ ] Pod `manual-schedule2` is running in namespace `default`
- [ ] Pod `manual-schedule2` is scheduled on `cka-lab-9-worker`
- [ ] Pod `manual-schedule2` has single container
- [ ] Pod `manual-schedule2` container has correct image
- [ ] `kube-scheduler-cka-lab-9-control-plane` is running
- [ ] `kube-scheduler-cka-lab-9-control-plane` was restarted

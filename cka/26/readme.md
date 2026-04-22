# Question 9 | Kill Scheduler, Manual Scheduling

> **Solve this question on:** `ssh cka5248`

Temporarily stop the kube-scheduler, this means in a way that you can start it again afterwards.

Create a single Pod named `manual-schedule` of image `httpd:2-alpine`, confirm it's created but not scheduled on any node.

Now you're the scheduler and have all its power, manually schedule that Pod on node `cka5248`. Make sure it's running.

Start the kube-scheduler again and confirm it's running correctly by creating a second Pod named `manual-schedule2` of image `httpd:2-alpine` and check if it's running on `cka5248-node1`.

## Answer

### Step 1 — Stop the Scheduler

First we find the controlplane node:

```bash
➜ ssh cka5248

➜ candidate@cka5248:~$ k get node
NAME            STATUS   ROLES           AGE     VERSION
cka5248         Ready    control-plane   6d22h   v1.33.1
cka5248-node1   Ready    <none>          6d22h   v1.33.1
```

Then we connect and check if the scheduler is running:

```bash
➜ candidate@cka5248:~$ sudo -i

➜ root@cka5248:~# kubectl -n kube-system get pod | grep schedule
kube-scheduler-cka5248            1/1     Running   0               6d22h
```

Kill the Scheduler (temporarily):

```bash
➜ root@cka5248:~# cd /etc/kubernetes/manifests/

➜ root@cka5248:~# mv kube-scheduler.yaml ..
```

And it should be stopped, we can wait for the container to be removed with `watch crictl ps`:

```bash
➜ root@cka5248:/etc/kubernetes/manifests# watch crictl ps

➜ root@cka5248:/etc/kubernetes/manifests# kubectl -n kube-system get pod | grep schedule

➜ root@cka5248:/etc/kubernetes/manifests#
```

> [!NOTE]
> In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

### Step 2 — Create a Pod

Now we create the Pod:

```bash
➜ root@cka5248:~# k run manual-schedule --image=httpd:2-alpine
pod/manual-schedule created
```

And confirm it has no node assigned:

```bash
➜ root@cka5248:~# k get pod manual-schedule -o wide
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE    ...
manual-schedule   0/1     Pending   0          14s   <none>   <none>  ...
```

### Step 3 — Manually Schedule the Pod

Let's play the scheduler now:

```bash
➜ root@cka5248:~# k get pod manual-schedule -o yaml > 9.yaml
```

```yaml
# cka5248:/root/9.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2020-09-04T15:51:02Z"
  labels:
    run: manual-schedule
  managedFields:
...
    manager: kubectl-run
    operation: Update
    time: "2020-09-04T15:51:02Z"
  name: manual-schedule
  namespace: default
  resourceVersion: "3515"
  selfLink: /api/v1/namespaces/default/pods/manual-schedule
  uid: 8e9d2532-4779-4e63-b5af-feb82c74a935
spec:
  nodeName: cka5248       # ADD the controlplane node name
  containers:
  - image: httpd:2-alpine
    imagePullPolicy: IfNotPresent
    name: manual-schedule
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-nxnc7
      readOnly: true
  dnsPolicy: ClusterFirst
...
```

The scheduler sets the `nodeName` for a Pod declaration. How it finds the correct node to schedule on, that's a very much complicated matter and takes many variables into account.

As we cannot `kubectl apply` or `kubectl edit`, in this case we need to delete and create or replace:

```bash
➜ root@cka5248:~# k -f 9.yaml replace --force
```

How does it look?

```bash
➜ root@cka5248:~# k get pod manual-schedule -o wide
NAME              READY   STATUS    ...   NODE            
manual-schedule   1/1     Running   ...   cka5248
```

It looks like our Pod is running on the controlplane now as requested, although no tolerations were specified. Only the scheduler takes taints/tolerations/affinity into account when finding the correct node name. That's why it's still possible to assign Pods manually directly to a controlplane node and skip the scheduler.

### Step 4 — Start the Scheduler Again

```bash
➜ root@cka5248:~# cd /etc/kubernetes/manifests/

➜ root@cka5248:/etc/kubernetes/manifests# mv ../kube-scheduler.yaml .
```

Checks it's running:

```bash
➜ root@cka5248:~# kubectl -n kube-system get pod | grep schedule
kube-scheduler-cka5248            1/1     Running   0               13s
```

Schedule a second test Pod:

```bash
➜ root@cka5248:~# k run manual-schedule2 --image=httpd:2-alpine

➜ root@cka5248:~# k get pod -o wide | grep schedule
manual-schedule    1/1     Running   0          95s   10.32.0.2   cka5248
manual-schedule2   1/1     Running   0          9s    10.44.0.3   cka5248-node1
```

Back to normal.

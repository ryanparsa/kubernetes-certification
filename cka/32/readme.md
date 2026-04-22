# Question 15 | Cluster Event Logging

> **Solve this question on:** `ssh cka6016`

1. Write a `kubectl` command into `/opt/course/15/cluster_events.sh` which shows the latest events in the whole cluster, ordered by time (`metadata.creationTimestamp`)
2. Delete the kube-proxy *Pod* and write the events this caused into `/opt/course/15/pod_kill.log` on `cka6016`
3. Manually kill the containerd container of the kube-proxy *Pod* and write the events into `/opt/course/15/container_kill.log`

## Answer

### Step 1

```bash
➜ ssh cka6016
```

Write the cluster events command:

```bash
# cka6016:/opt/course/15/cluster_events.sh
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

### Step 2

Delete the kube-proxy Pod:

```bash
➜ candidate@cka6016:~$ k -n kube-system get pod | grep proxy
kube-proxy-wb4tb   1/1     Running   0          9d

➜ candidate@cka6016:~$ k -n kube-system delete pod kube-proxy-wb4tb
pod "kube-proxy-wb4tb" deleted
```

Now we run the events script and write them into the pod_kill.log:

```bash
➜ candidate@cka6016:~$ sh /opt/course/15/cluster_events.sh
```

Write the events caused by deleting into `/opt/course/15/pod_kill.log` on `cka6016`:

```bash
# /opt/course/15/pod_kill.log
kube-system   0s    Normal   Killing     pod/kube-proxy-wb4tb      Stopping container kube-proxy
kube-system   0s    Normal   Scheduled   pod/kube-proxy-wb4tb      Successfully assigned kube-system/kube-proxy-wb4tb to cka6016
kube-system   0s    Normal   Pulled      pod/kube-proxy-wb4tb      Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   0s    Normal   Created     pod/kube-proxy-wb4tb      Created container kube-proxy
kube-system   0s    Normal   Started     pod/kube-proxy-wb4tb      Started container kube-proxy
```

### Step 3

Now we manually kill the containerd container of the kube-proxy *Pod*:

```bash
➜ candidate@cka6016:~$ sudo -i

➜ root@cka6016:~# crictl ps | grep kube-proxy
2fd052f1fcf78       505d571f5fd56       57 seconds ago      Running             kube-proxy            0                   3455856e0970c       kube-proxy-wb4tb

➜ root@cka6016:~# crictl rm --force 2fd052f1fcf78
2fd052f1fcf78
2fd052f1fcf78

➜ root@cka6016:~# crictl ps | grep kube-proxy
6bee4f36f8410       505d571f5fd56       5 seconds ago       Running             kube-proxy            0                   3455856e0970c       kube-proxy-wb4tb
```

> ℹ️ In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

We killed the container (2fd052f1fcf78), but also noticed that a new container (6bee4f36f8410) was directly created again. Thanks Kubernetes!

Now we see if this caused events again and we write those into the second file:

```bash
➜ candidate@cka6016:~$ sh /opt/course/15/cluster_events.sh
```

Write the events caused by the killing into `/opt/course/15/container_kill.log` on `cka6016`:

```bash
# /opt/course/15/container_kill.log
kube-system   21s     Normal    Created     pod/kube-proxy-wb4tb                      Created container kube-proxy
kube-system   21s     Normal    Started     pod/kube-proxy-wb4tb                      Started container kube-proxy
default       90s     Normal    Starting    node/cka6016                             
default       20s     Normal    Starting    node/cka6016                             
```

Comparing the events we see that when we deleted the whole *Pod* there were more things to be done, hence more events. For example was the *DaemonSet* in the game to re-create the missing *Pod*. Where when we manually killed the main container of the *Pod*, the *Pod* still exists but only its container needed to be re-created, hence less events.

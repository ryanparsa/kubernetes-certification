# Question 32 | Cluster Event Logging

> **Solve this question on:** the "cka-lab-32" kind cluster

1. Write a `kubectl` command into `cka/32/course/cluster_events.sh` which shows the latest events in the whole cluster, ordered by time (`metadata.creationTimestamp`)
2. Delete the *kube-proxy* *Pod* and write the events this caused into `cka/32/course/pod_kill.log`
3. Manually kill the *containerd* container of the *kube-proxy* *Pod* and write the events into `cka/32/course/container_kill.log`

## Answer

### Step 1

```bash
vim cka/32/course/cluster_events.sh
```

```bash
# cka/32/course/cluster_events.sh
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

And we can execute it which should show recent events:

```bash
sh cka/32/course/cluster_events.sh
NAMESPACE     LAST SEEN   TYPE     REASON           OBJECT                       MESSAGE
...
default       19m         Normal    Pulled              pod/team-york-board-7d74f8f86c-fvzw5    Successfully pulled image "httpd:2-alpine" in 4.574s (4.575s including waiting). Image size: 22038396 bytes.
default       19m         Normal    Created             pod/team-york-board-7d74f8f86c-fvzw5    Created container httpd
default       19m         Normal    Pulled              pod/team-york-board-7d74f8f86c-9fg47    Successfully pulled image "httpd:2-alpine" in 425ms (4.976s including waiting). Image size: 22038396 bytes.
default       19m         Normal    Started             pod/team-york-board-7d74f8f86c-fvzw5    Started container httpd
default       19m         Normal    Pulled              pod/team-york-board-7d74f8f86c-xnprt    Successfully pulled image "httpd:2-alpine" in 711ms (5.685s including waiting). Image size: 22038396 bytes.
default       19m         Normal    Created             pod/team-york-board-7d74f8f86c-xnprt    Created container httpd
default       19m         Normal    Created             pod/team-york-board-7d74f8f86c-9fg47    Created container httpd
default       19m         Normal    Started             pod/team-york-board-7d74f8f86c-9fg47    Started container httpd
default       19m         Normal    Started             pod/team-york-board-7d74f8f86c-xnprt    Started container httpd
...
```

### Step 2

We delete the *kube-proxy* *Pod*:

```bash
kubectl -n kube-system get pod -l k8s-app=kube-proxy -owide
NAME               READY   ...     NODE                        NOMINATED NODE   READINESS GATES
kube-proxy-lf2fs   1/1     ...     cka-lab-32-control-plane    <none>           <none>

kubectl -n kube-system delete pod kube-proxy-lf2fs
pod "kube-proxy-lf2fs" deleted
```

Now we can check the events, for example by using the command that we created before:

```bash
sh cka/32/course/cluster_events.sh
```

Write the events caused by the deletion into `cka/32/course/pod_kill.log`:

```bash
# cka/32/course/pod_kill.log
kube-system   12s         Normal    Killing             pod/kube-proxy-lf2fs                    Stopping container kube-proxy
kube-system   12s         Normal    SuccessfulCreate    daemonset/kube-proxy                    Created pod: kube-proxy-wb4tb
kube-system   11s         Normal    Scheduled           pod/kube-proxy-wb4tb                    Successfully assigned kube-system/kube-proxy-wb4tb to cka-lab-32-control-plane
kube-system   11s         Normal    Pulled              pod/kube-proxy-wb4tb                    Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   11s         Normal    Created             pod/kube-proxy-wb4tb                    Created container kube-proxy
kube-system   11s         Normal    Started             pod/kube-proxy-wb4tb                    Started container kube-proxy
default       10s         Normal    Starting            node/cka-lab-32-control-plane
```

### Step 3

> **Solve this question on:** `docker exec -it cka-lab-32-control-plane bash`

Finally we will try to provoke events by killing the container belonging to the container of a *kube-proxy* *Pod*:

```bash
crictl ps | grep kube-proxy
2fd052f1fcf78       505d571f5fd56       57 seconds ago      Running             kube-proxy            0                   3455856e0970c       kube-proxy-wb4tb

crictl rm --force 2fd052f1fcf78
2fd052f1fcf78
2fd052f1fcf78

crictl ps | grep kube-proxy
6bee4f36f8410       505d571f5fd56       5 seconds ago       Running             kube-proxy            0                   3455856e0970c       kube-proxy-wb4tb
```

> [!NOTE]
> In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

We killed the container (2fd052f1fcf78), but also noticed that a new container (6bee4f36f8410) was directly created again. Thanks *Kubernetes*!

Now we see if this caused events again and we write those into the second file:

```bash
sh cka/32/course/cluster_events.sh
```

Write the events caused by the killing into `cka/32/course/container_kill.log`:

```bash
# cka/32/course/container_kill.log
kube-system   21s     Normal    Created     pod/kube-proxy-wb4tb                      Created container kube-proxy
kube-system   21s     Normal    Started     pod/kube-proxy-wb4tb                      Started container kube-proxy
default       90s     Normal    Starting    node/cka-lab-32-control-plane
default       20s     Normal    Starting    node/cka-lab-32-control-plane
```

Comparing the events we see that when we deleted the whole *Pod* there were more things to be done, hence more events. For example was the *DaemonSet* in the game to re-create the missing *Pod*. Where when we manually killed the main container of the *Pod*, the *Pod* still exists but only its container needed to be re-created, hence less events.


## Checklist (Score: 0/3)

- [ ] File `cka/32/course/cluster_events.sh` valid
- [ ] File `cka/32/course/pod_kill.log` contains correct logs
- [ ] File `cka/32/course/container_kill.log` contains correct logs

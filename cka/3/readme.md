# Question 3 | Scale down StatefulSet

Solve this question on: `ssh cka3962`

There are two *Pods* named `o3db-*` in *Namespace* `project-h800`. The Project H800 management asked you to scale these down to one replica to save resources.

## Answer:

If we check the *Pods* we see two replicas:

```bash
➜ ssh cka3962

➜ candidate@cka3962:~$ k -n project-h800 get pod | grep o3db
o3db-0                                  1/1     Running   0          6d19h
o3db-1                                  1/1     Running   0          6d19h
```

From their name it looks like these are managed by a *StatefulSet*. But if we're unsure we could also check for the most common resources which manage *Pods*:

```bash
➜ candidate@cka3962:~ k -n project-h800 get deploy,ds,sts | grep o3db
statefulset.apps/o3db   2/2     6d19h
```

Confirmed, we have to work with a *StatefulSet*. We could also look at the *Pod* labels to find this out:

```bash
➜ candidate@cka3962:~ k -n project-h800 get pod --show-labels | grep o3db
o3db-0                                  1/1     Running   0          6d19h   app=nginx,apps.kubernetes.io/pod-index=0,controller-revision-hash=o3db-5fbd4bb9cc,statefulset.kubernetes.io/pod-name=o3db-0
o3db-1                                  1/1     Running   0          6d19h   app=nginx,apps.kubernetes.io/pod-index=1,controller-revision-hash=o3db-5fbd4bb9cc,statefulset.kubernetes.io/pod-name=o3db-1
```

To fulfil the task we simply run:

```bash
➜ candidate@cka3962:~ k -n project-h800 scale sts o3db --replicas 1
statefulset.apps/o3db scaled

➜ candidate@cka3962:~ k -n project-h800 get sts o3db
NAME   READY   AGE
o3db   1/1     6d19h
```

The Project H800 management is happy again.

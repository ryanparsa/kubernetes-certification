# Question 114

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

Write a command that writes the latest events in the whole cluster, ordered by time, into `/opt/course/15/cluster_events.log`.

Now kill the `kube-proxy` *Pod* running on `cluster1-worker1` and write the events this caused into `/opt/course/15/pod_kill.log`.

Finally kill the containerd container of the `kube-proxy` running on `cluster1-worker1` and write the events into `/opt/course/15/container_kill.log`.

Do you notice differences in the effects both actions caused?

# Question 32

> **Solve this question on:** the "cka-lab-32" kind cluster

1. Write a `kubectl` command into `cka/32/lab/cluster_events.sh` which shows the latest events in the whole cluster, ordered by time (`metadata.creationTimestamp`)
2. Delete the *kube-proxy* *Pod* and write the events this caused into `cka/32/lab/pod_kill.log`
3. Manually kill the *containerd* container of the *kube-proxy* *Pod* and write the events into `cka/32/lab/container_kill.log`

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

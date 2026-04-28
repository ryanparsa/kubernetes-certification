# Question 154

> **Solve this question on:** `ssh cluster1-controlplane1`

Make a backup of `etcd` running on `cluster1-controlplane1` and save it on the master node at `/tmp/etcd-backup.db`.

Then create a *Pod* of your kind in the cluster.

Finally restore the backup, confirm the cluster is still working and that the created *Pod* is no longer present.

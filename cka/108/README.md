# Question 108

> **Solve this question on:** `ssh cluster1-master1`

SSH into the master node. Temporarily stop the `kube-scheduler` in a way that you can start it again afterwards.

Create a single *Pod* named `manual-schedule` of image `httpd:2.4-alpine`. Confirm it's created but not scheduled on any node.

Now you're the scheduler: manually schedule that *Pod* on node `cluster1-worker1`. Make sure it's running.

Start the `kube-scheduler` again and confirm it's running correctly by creating a second *Pod* named `manual-schedule2` of image `httpd:2.4-alpine` and checking if it's running on `cluster1-worker1`.

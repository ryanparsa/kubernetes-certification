# Task 26 — Workloads: CronJobs

**Context:** Cluster `cka-task-26` (`export KUBECONFIG=$PWD/kubeconfig`)

You need to schedule a periodic database maintenance job.

## Objective

Create a **CronJob** named **`db-cleanup`** in the **`batch`** namespace with:

1. Schedule: **`*/15 * * * *`** (every 15 minutes)
2. Image: **`busybox:1.36`**
3. Command: **`["/bin/sh", "-c", "echo cleaning up database...; sleep 10"]`**
4. Successful jobs history limit: **5**
5. Failed jobs history limit: **2**
6. Restart policy: **`OnFailure`**

The grader checks the resource structure.

## Verify

```
./test.sh
```

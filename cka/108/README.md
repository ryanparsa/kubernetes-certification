# Question 108

Temporarily stop the `kube-scheduler`, this means in a way that you can start it again afterwards.

Create a single *Pod* named `manual-schedule` of image `httpd:2.4-alpine`. Confirm it's created but not scheduled on any *Node*.

Now you're the scheduler: manually schedule that *Pod* on *Node* `cka-lab-108-worker`. Make sure it's running.

Start the `kube-scheduler` again and confirm it's running correctly by creating a second *Pod* named `manual-schedule2` of image `httpd:2.4-alpine` and checking if it's running on `cka-lab-108-worker`.

> **Solve this question on:** the "cka-lab-108" kind cluster

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

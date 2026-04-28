# Question 9

Temporarily stop the kube-scheduler, this means in a way that you can start it again afterwards.

Create a single *Pod* named `manual-schedule` of image `httpd:2-alpine`, confirm it's created but not scheduled on any *Node*.

Now you're the scheduler and have all its power, manually schedule that *Pod* on *Node* `cka-lab-control-plane`. Make sure it's running.

Start the kube-scheduler again and confirm it's running correctly by creating a second *Pod* named `manual-schedule2` of image `httpd:2-alpine` and check if it's running on `cka-lab-worker`.

> **Solve this question on:** `docker exec -it cka-lab-control-plane bash`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

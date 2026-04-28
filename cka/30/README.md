# Question 30

> **Solve this question on:** the "cka-lab-30" kind cluster

Create a *Pod* with multiple *Containers* named `multi-container-playground` in *Namespace* `default`:

- It should have a *Volume* attached and mounted into each *Container*. The *Volume* shouldn't be persisted or shared with other *Pods*
- *Container* `c1` with image `nginx:1-alpine` should have the name of the *Node* where its *Pod* is running on available as environment variable `MY_NODE_NAME`
- *Container* `c2` with image `busybox:1` should write the output of the `date` command every second in the shared *Volume* into file `date.log`. You can use `while true; do date >> /your/vol/path/date.log; sleep 1; done` for this.
- *Container* `c3` with image `busybox:1` should constantly write the content of file `date.log` from the shared *Volume* to *stdout*. You can use `tail -f /your/vol/path/date.log` for this.

> [i] Check the logs of *Container* `c3` to confirm correct setup

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

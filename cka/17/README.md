# Question 17

> **Solve this question on:** the "cka-lab-17" kind cluster

In *Namespace* `project-tiger` create a *Pod* named `tigers-reunite` of image `httpd:2-alpine` with labels `pod=container` and `container=pod`. Find out on which *Node* the *Pod* is scheduled. Connect to that *Node* and find the containerd container belonging to that *Pod*.

Using command `crictl`:

- Write the ID of the container and the `info.runtimeType` into `cka/17/lab/pod-container.txt`
- Write the logs of the container into `cka/17/lab/pod-container.log`

> [!NOTE]
> You can connect to a worker node using `docker exec -it cka-lab-17-worker bash` from your local machine

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

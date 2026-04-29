# Question 196

> **Solve this question on:** `cka-lab-196`

In *Namespace* `project-tiger` create a *Pod* named `tigers-reunite` of image `httpd:2.4-alpine` with labels `pod=container` and `container=pod`. Find out on which node the *Pod* is scheduled. Connect to that node and find the containerd container belonging to that *Pod*.

Using `crictl`:

1. Write the ID of the container and the `info.runtimeType` into `lab/pod-container.txt`

1. Write the logs of the container into `lab/container.log`

> [!NOTE]
> You can connect to a worker node using `docker exec -it cka-lab-196-worker bash` from your local machine.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

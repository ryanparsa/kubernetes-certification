# Question 196

> **Solve this question on:** `ssh cka2506`

In *Namespace* `project-tiger` create a *Pod* named `tigers-reunite` of image `httpd:2.4-alpine` with labels `pod=container` and `container=pod`. Find out on which node the *Pod* is scheduled. SSH into that node and find the containerd container belonging to that *Pod*.

Using `crictl`:

1. Write the ID of the container and the `info.runtimeType` into `/opt/course/17/pod-container.txt`

1. Write the logs of the container into `/opt/course/17/container.log`

> [i] Connect to a worker node using `ssh cka2506-node1` or `ssh cka2506-node2` from `cka2506`.

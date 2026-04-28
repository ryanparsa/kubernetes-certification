# Question 116

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

In *Namespace* `project-tiger` find a *Pod* that has the label `id=tiger-master`. SSH into the node on which that *Pod* is scheduled and find the containerd container belonging to that *Pod*.

Write the ID of the container and the `info.runtimeType` into `/opt/course/17/pod-container.txt`.

Write the logs of the container into `/opt/course/17/container.log`.

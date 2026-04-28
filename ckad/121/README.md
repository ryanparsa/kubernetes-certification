# Question 121

> **Solve this question on:** `ckad-lab-02`

Create a single *Pod* of image `httpd:2.4.41-alpine` in *Namespace* `default`. The *Pod* should be named `pod1` and the container should be named `pod1`.

Your manager would like to run a command to check the status of the *Pod*. Find out what the command would be to get the logs of the *Pod* named `pod1` and make the container listen on port 80.

The manager would like to be able to access the *Pod* from outside. Create a *NodePort* *Service* named `pod1-svc` which should expose the `pod1` *Pod* on port 80. Write the `kubectl` command used to expose the *Pod* to `/opt/course/2/pod1-svc.sh`.

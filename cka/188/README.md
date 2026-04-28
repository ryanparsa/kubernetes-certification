# Question 188

> **Solve this question on:** `ssh cka412`

There is a *ServiceAccount* `secret-reader` in *Namespace* `project-swan`. Create a *Pod* of image `nginx:1.3-alpine` named `api-contact` which uses this *ServiceAccount*.

Exec into the *Pod* and use `curl` to manually query all *Secrets* from the Kubernetes API.

Write the result into file `/opt/course/9/result.json`.

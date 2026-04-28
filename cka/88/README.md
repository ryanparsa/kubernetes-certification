# Question 88

> **Solve this question on:** the `cka-lab` kind cluster

There is *ServiceAccount* `secret-reader` in *Namespace* `project-swan`. Create a *Pod* of image `nginx:1-alpine` named `api-contact` which uses this *ServiceAccount*.

Then:

1. Exec into the pod and use the mounted service account token to query the Kubernetes API for secrets in *Namespace* `project-swan`

1. Write the result into `/opt/course/9/result.txt`

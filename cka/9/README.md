# Question 9

There is *ServiceAccount* `secret-reader` in *Namespace* `project-swan`. Create a *Pod* of image `nginx:1-alpine` named `api-contact` which uses this *ServiceAccount*.

> **Solve this question on:** the "cka-lab-9" kind cluster

Exec into the *Pod* and use `curl` to manually query all *Secrets* from the Kubernetes Api.

Write the result into file `lab/result.json`.

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

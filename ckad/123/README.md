# Question 123

> **Solve this question on:** `ckad-lab-04`

Kubernetes allows you to run calculator jobs. In *Namespace* `default`:

1. Delete the *Docker* images for the image named `nginx`, all versions. After deleting, there should be no version of `nginx` present anymore.

2. There seems to be a *Docker* image which is not tagged with any label. Find it and delete it.

Use the `crictl` command to list images available on the cluster node. Write the list to `/opt/course/4/images`.

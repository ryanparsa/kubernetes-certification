# Question 123

> **Solve this question on:** `ckad-lab-123`

Perform the following tasks on the cluster node:

1. Delete the *container* images for the image named `nginx`, all versions. After deleting, there should be no version of `nginx` present anymore.

2. There seems to be a *container* image which is not tagged with any label. Find it and delete it.

Use the `crictl` command to list images available on the cluster node. Write the list to `/opt/course/123/images`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

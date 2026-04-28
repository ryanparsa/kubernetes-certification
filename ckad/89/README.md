# Question 89

> **Solve this question on:** `ckad-lab-89`

Create a single *Pod* named `pod1` of image `httpd:2.4.41-alpine` in *Namespace* `default`. The container should also be named `pod1` and listen on port 80.

The manager would like to be able to access the *Pod* from outside the cluster. Create a *NodePort* *Service* named `pod1-svc` which exposes the `pod1` *Pod* on port 80.

Finally, write the `kubectl` command used to create the *Service* (expose the *Pod*) into the file `/opt/course/89/pod1-svc.sh`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

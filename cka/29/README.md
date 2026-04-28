# Question 29

> **Solve this question on:** the "cka-lab-29" kind cluster

Create a *Pod* of image `httpd:2-alpine` in *Namespace* `default`.

The *Pod* should be named `pod1` and the *Container* should be named `pod1-container`.

This *Pod* should only be scheduled on *Controlplane Nodes*.

Do not add new labels to any *Nodes*.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

# Question 72

> **Solve this question on:** the "cka-lab-72" kind cluster

Create a single *Pod* of image `httpd:2.4.41-alpine` in *Namespace* `default`. The *Pod* should be named `pod` and the container should be named `pod-container`. This *Pod* should **only** be scheduled on a *Controlplane Node* -- do not add any *Tolerations*.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

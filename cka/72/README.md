# Question 72

> **Solve this question on:** `cka-lab-72`

The metrics-server is installed in the cluster. Write two bash one-liners using `kubectl top`:

1. Write the output of `kubectl top pod` for all *Pods* in all *Namespaces*, **sorted alphabetically by Pod name**, and including per-container usage, into `/opt/course/7/pods.txt`

2. Write the output of `kubectl top node` sorted by CPU usage into `/opt/course/7/nodes.txt`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

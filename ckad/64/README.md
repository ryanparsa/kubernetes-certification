# Question 64

> **Solve this question on:** `ckad-lab-64`

Create a namespace called `json-namespace`.

Create a pod called `json-pod` using the `nginx` image in namespace `json-namespace`.

Once the pod is running, use `kubectl` with a JSONPath expression to output only the `hostIP` address of the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

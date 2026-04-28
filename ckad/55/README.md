# Question 55

> **Solve this question on:** `ckad-lab-55`

Use kubectl custom columns to extract and display pod information:

1. There are several pods and deployments running in the `custom-columns-demo` namespace
2. Create a custom column output showing all pods from all namespaces, including their names, namespaces, and container images
3. Save this output to `/tmp/pod-images.txt`
4. Create another output showing multi-container pod details with pod name, namespace, and all container images as comma-separated values
5. Save this second output to `/tmp/all-container-images.txt`

Ensure the namespace exists before starting your work.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

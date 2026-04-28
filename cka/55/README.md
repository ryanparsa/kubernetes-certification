# Question 55

> **Solve this question on:** `cka-lab-55`

Create a StatefulSet named `web` with `3` replicas using the `nginx` image in the `stateful` namespace.

Requirements:

- Create a headless service named `web-svc` to expose the StatefulSet
- Each pod should have a volume mounted at `/usr/share/nginx/html`
- Use the StorageClass `cold` for dynamic provisioning
- Volume claim template should request `1Gi` storage

Ensure pods are created in sequence and can be accessed using their stable network identity.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

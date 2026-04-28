# Question 59

> **Solve this question on:** `cka-lab-59`

Using Kustomize in the directory `/tmp/exam/kustomize/`:

1. Create a base deployment for `nginx` with `2` replicas
2. Create an overlay that:
   - Adds a label `environment=production`
   - Increases replicas to `3`
   - Adds a ConfigMap named `nginx-config` with key `index.html` and value `Welcome to Production`
   - Mounts the ConfigMap as a volume named `nginx-index` at `/usr/share/nginx/html/`
3. Apply the overlay to create resources in the `kustomize` namespace

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

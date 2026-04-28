# Question 24

> **Solve this question on:** `ckad-lab-24`

A development team needs environment-specific configuration for their application.

First, create a ConfigMap named `app-config` in namespace `workloads` containing exactly two key-value pairs: `APP_ENV=production` and `LOG_LEVEL=info`.

Next, create a Pod named `config-pod` using the `nginx` image that consumes these configurations as environment variables.

The pod should be resource-efficient but have guaranteed resources, so configure it with a CPU request of `100m`, a CPU limit of `200m`, a memory request of `128Mi`, and a memory limit of `256Mi`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

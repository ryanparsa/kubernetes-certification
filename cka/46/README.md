# Question 46

> **Solve this question on:** `cka-lab-46`

Create a *ConfigMap* named `app-config` with the key `APP_COLOR` and value `blue`.

Create a pod named `config-pod` using the `nginx` image that mounts this ConfigMap as a volume named `config-volume` at `/etc/config`.

Verify that the configuration is correctly accessible within the pod.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

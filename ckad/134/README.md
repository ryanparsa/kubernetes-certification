# Question 134

> **Solve this question on:** `ckad-lab-134`

The *Deployment* `web-server` has a nginx-type Deployment with *ConfigMap* `web-server-conf` already created. The *Deployment* already exists, but is not correctly configured to use the *ConfigMap*.

Configure the *Deployment* to mount the *ConfigMap* `web-server-conf` as a volume at path `/etc/nginx/conf.d`. The *Pod* template should use the existing volume configuration.

Confirm the *Deployment* is running correctly, for example using `nginx -t` inside the container.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

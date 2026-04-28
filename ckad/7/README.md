# Question 7

> **Solve this question on:** `ckad-lab-7`

Perform the following ConfigMap tasks:

1. Create a ConfigMap named `app-config` with the following key-value pairs: `ENV=production` and `LOG_LEVEL=info`.

2. Create a pod named `cm-env` with image `nginx` that loads **all** keys from the `app-config` ConfigMap as environment variables using `envFrom`.

3. Create a pod named `cm-vol` with image `nginx` that mounts the `app-config` ConfigMap as a volume at path `/etc/config` inside the container. Verify that the files `/etc/config/ENV` and `/etc/config/LOG_LEVEL` exist inside the pod.

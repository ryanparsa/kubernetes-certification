# Question 14

> **Solve this question on:** `ckad-lab-14`

Perform the following Helm tasks:

1. Add the Bitnami Helm repository with name `bitnami` pointing to `https://charts.bitnami.com/bitnami`. Update the repo.

2. Search for the `bitnami/nginx` chart and display its configurable values.

3. Install the `bitnami/nginx` chart as release `my-nginx` into namespace `helm-demo` (create the namespace if it does not exist) with `replicaCount` set to `2`.

4. Upgrade the `my-nginx` release, changing `replicaCount` to `3`. Verify the deployment was updated.

5. Uninstall the `my-nginx` release and confirm it has been removed.

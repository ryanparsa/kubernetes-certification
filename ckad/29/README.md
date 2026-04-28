# Question 29

> **Solve this question on:** `ckad-lab-29`

Deploy the Bitnami Nginx chart in the `web` namespace using Helm.

First, add the Bitnami repository (`https://charts.bitnami.com/bitnami`) if not already present.

Then, deploy the Bitnami `nginx` chart with exactly `2` replicas to ensure high availability.

Verify the deployment is successful by checking that pods are running and the service is correctly configured.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

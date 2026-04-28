# Question 7

> **Solve this question on:** `cks-lab-7`

In the `service-account-caution` namespace, create a Deployment named `secure-app` with 2 replicas that uses the `nginx` image.

Configure the Deployment to use a custom ServiceAccount named `minimal-sa` that you will create. The ServiceAccount should have automounting of API credentials disabled.

Additionally, configure the Pod template to explicitly disable service account token automounting.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

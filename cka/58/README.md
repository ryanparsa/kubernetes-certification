# Question 58

> **Solve this question on:** `cka-lab-58`

Using Helm:

1. Add the bitnami repository: `https://charts.bitnami.com/bitnami`
2. Install the `nginx` chart from bitnami with release name `web-release` in the `helm-test` namespace
3. Configure the service type as `NodePort` and set the replica count to `2`
4. Verify the deployment is successful and pods are running

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

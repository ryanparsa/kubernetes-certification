# Question 89

> **Solve this question on:** `ckad-lab-89`

There is an existing *Deployment* named `api-new-c32` in *Namespace* `neptune`. A newer version of the application is available as image `httpd:2.4.41-alpine`. Perform a rolling update of the *Deployment* using this image.

Could you find a way to roll back to the previous version of the *Deployment*? Roll it back and confirm that the *Pods* are using the original image again.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

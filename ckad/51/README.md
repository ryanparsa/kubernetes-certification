# Question 51

> **Solve this question on:** `ckad-lab-51`

Perform basic Helm operations:

1. Create a namespace named `helm-basics`
2. Add the Bitnami repository to Helm with the name `bitnami` (URL: `https://charts.bitnami.com/bitnami`)
3. Install the `nginx` chart from the Bitnami repository in the `helm-basics` namespace with the release name `nginx-release`
4. Save the release notes of the installation to a file at `/tmp/release-notes.txt`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

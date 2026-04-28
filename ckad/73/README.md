# Question 73

> **Solve this question on:** `ckad-lab-73`

1. Create a *Secret* named `db-credentials` with the key/value pair `db-password=passwd`.

2. Create a *Pod* named `backend` in the `default` namespace that uses the image `nginx` and maps the secret key `db-password` to an environment variable named `DB_PASSWORD`.

3. Shell into the running *Pod* and confirm that the environment variable `DB_PASSWORD` is present with the value `passwd`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

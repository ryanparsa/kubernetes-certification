# Question 25

> **Solve this question on:** `ckad-lab-25`

The database team needs to securely deploy a MySQL instance with proper credential management.

Create a Secret named `db-credentials` in namespace `workloads` containing three sensitive values: `username=admin`, `random=true` and `password=securepass`.

Then create a Pod named `secure-pod` using the `mysql:9.5.0` image that uses these credentials.

Configure the pod to access the Secret values as environment variables named `DB_USER`, `MYSQL_RANDOM_ROOT_PASSWORD` and `DB_PASSWORD` respectively.

This pattern demonstrates secure handling of sensitive information in Kubernetes without hardcoding credentials in the pod specification. Ensure the MySQL container is properly configured to use these environment variables for authentication.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

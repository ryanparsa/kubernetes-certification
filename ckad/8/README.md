# Question 8

> **Solve this question on:** `ckad-lab-8`

Perform the following Secret tasks:

1. Create a Secret named `db-secret` with `username=admin` and `password=s3cur3`.

2. Create a pod named `secret-env` with image `nginx` that injects:
   - The `username` key from `db-secret` as environment variable `DB_USER`
   - The `password` key from `db-secret` as environment variable `DB_PASS`

3. Create a pod named `secret-vol` with image `nginx` that mounts the entire `db-secret` as a **read-only** volume at `/etc/secret`. Verify that `/etc/secret/username` and `/etc/secret/password` exist inside the pod.

# Question 72

> **Solve this question on:** `ckad-lab-72`

1. Create a new file named `config.txt` with the following key/value pairs, one per line:
   - `DB_URL=localhost:3306`
   - `DB_USERNAME=postgres`

2. Create a *ConfigMap* named `db-config` from that file.

3. Create a *Pod* named `backend` in the `default` namespace that uses the image `nginx` and loads all entries from the `db-config` *ConfigMap* as environment variables.

4. Shell into the running *Pod* and confirm that the environment variables `DB_URL` and `DB_USERNAME` are present with their correct values.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

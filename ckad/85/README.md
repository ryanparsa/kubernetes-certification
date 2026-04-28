# Question 85

> **Solve this question on:** `ckad-lab-85`

Create a namespace `secure`.

1. Create a ConfigMap named `app-config` in namespace `secure` with key `key=value`.

2. Create a Pod named `secure-app` in namespace `secure` using image `alpine` with command `sleep 3600`. Apply the following security configuration:

   **Pod-level SecurityContext:**
   - `runAsUser: 1000`
   - `runAsGroup: 3000`
   - `fsGroup: 2000`

   **Container-level SecurityContext:**
   - Drop all Linux capabilities (`capabilities.drop: [ALL]`)
   - `readOnlyRootFilesystem: true`
   - `allowPrivilegeEscalation: false`

3. Mount the ConfigMap `app-config` as a volume at `/config` inside the container.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

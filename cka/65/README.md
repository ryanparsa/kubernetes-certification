# Question 65

> **Solve this question on:** `cka-lab-65`

Perform a rolling update in the `upgrade` namespace:

1. Create a deployment named `app-v1` with `4` replicas using `nginx:1.19`
2. Configure the rolling update strategy with:
   - Max unavailable: `1`
   - Max surge: `1`
3. Perform a rolling update to `nginx:1.20`
4. Save the output of `kubectl rollout history deployment app-v1 -n upgrade` to `/tmp/exam/rollout-history.txt`
5. Roll back to the previous version

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

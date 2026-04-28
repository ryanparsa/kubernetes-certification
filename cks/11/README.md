# Question 11

> **Solve this question on:** `cks-lab-11`

Label the `pod-security` namespace to enforce the `baseline` Pod Security Standard.

Then, create a pod named `compliant-pod` that complies with the baseline Pod Security Standard.

Finally, attempt to create a pod named `non-compliant-pod` that violates the standard by running as root and with privileged security context. Document the error in a file named `/tmp/violation.txt`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

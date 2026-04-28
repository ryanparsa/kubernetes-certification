# Question 49

> **Solve this question on:** `ckad-lab-49`

Create a Job named `data-processor` in the `jobs` namespace with the following specifications:

1. Use image `busybox`
2. Command: `['sh', '-c', 'for i in $(seq 1 5); do echo Processing item $i; sleep 2; done']`
3. Set restart policy to `Never`
4. Set backoff limit to `4`
5. Set active deadline seconds to `30`

Ensure the namespace exists before creating the job.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

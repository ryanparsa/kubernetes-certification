# Question 10

> **Solve this question on:** `cks-lab-10`

Create a pod named `seccomp-pod` in the `seccomp-profile` namespace using the `nginx` image with a seccomp profile applied.

The seccomp profile should be the default `runtime/default` profile.

Additionally, create a ConfigMap named `seccomp-config` in the same namespace with key `profile.json` containing a simple seccomp profile that allows only the following syscalls: `exit`, `exit_group`, `rt_sigreturn`, `read`, `write`, and `open`.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

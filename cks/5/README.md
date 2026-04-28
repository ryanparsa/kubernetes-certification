# Question 5

> **Solve this question on:** `cks-lab-5`

You need to verify the integrity of Kubernetes binaries before deploying them. In the `binary-verify` namespace, create a pod named `verify-bin` using the `busybox` image that mounts the host's `/usr/bin` directory as a read-only volume at `/host-bin`.

Inside the pod, write a script that calculates the SHA256 hash of the following files and stores the results in a file at `/tmp/verified-hashes.txt` within the pod:
- /host-bin/kubectl
- /host-bin/kubelet

Use the command format: `sha256sum [file] >> /tmp/verified-hashes.txt`

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

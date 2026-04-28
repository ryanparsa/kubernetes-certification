# Question 49

> **Solve this question on:** `cka-lab-49`

Create a new StorageClass named `fast-local` with the following specifications:

- Provisioner: `rancher.io/local-path`
- VolumeBindingMode: `WaitForFirstConsumer`
- Set it as the `default` StorageClass

Note: Ensure any existing default StorageClass is no longer marked as default.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

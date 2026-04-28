# Question 2

Install the MinIO Operator using Helm in *Namespace* `minio`. Then configure and create the *Tenant* CRD:

> **Solve this question on:** the "cka-lab-2" kind cluster

1. Create *Namespace* `minio`
2. Install Helm chart `minio/operator` into the new *Namespace*. The Helm Release should be called `minio-operator`
3. Update the *Tenant* resource in `cka/2/lab/minio-tenant.yaml` to include `enableSFTP: true` under `features`
4. Create the *Tenant* resource from `cka/2/lab/minio-tenant.yaml`

> [!NOTE]
> It is not required for MinIO to run properly. Installing the Helm Chart and the *Tenant* resource as requested is enough

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

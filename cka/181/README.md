# Question 181

> **Solve this question on:** `ssh cka458`

Install the MinIO Operator using Helm in *Namespace* `minio`. Then configure and create the *Tenant* CRD:

1. Create *Namespace* `minio`

1. Install Helm chart `minio/operator` into the new *Namespace*. The Helm Release should be called `minio-operator`.

1. Update the *Tenant* resource in `/opt/course/2/minio-tenant.yaml` to include `enableSFTP: true` under `features`

1. Create the *Tenant* resource from `/opt/course/2/minio-tenant.yaml`

> [i] It is not required for MinIO to run properly. Installing the Helm Chart and the Tenant resource as requested is enough.

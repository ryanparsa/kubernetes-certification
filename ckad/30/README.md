# Question 30

> **Solve this question on:** `ckad-lab-30`

To support a custom backup solution, you need to extend the Kubernetes API.

Create a CustomResourceDefinition (CRD) named `backups.data.example.com` that defines a new resource type `Backup` in API group `data.example.com` with version `v1alpha1`.

This custom resource should include a schema that validates two required fields: `spec.source` (a string representing the source data location) and `spec.destination` (a string representing where backups should be stored).

Configure appropriate additional fields like shortNames, scope, and descriptions to make this CRD user-friendly.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`

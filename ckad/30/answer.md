## Answer

**Reference:** https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/

### Create the CRD

```yaml
# lab/backup-crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.data.example.com
spec:
  group: data.example.com
  names:
    kind: Backup
    listKind: BackupList
    plural: backups
    singular: backup
    shortNames:
    - bkp
  scope: Namespaced
  versions:
  - name: v1alpha1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            description: BackupSpec defines the desired state of Backup
            properties:
              source:
                type: string
                description: Source data location
              destination:
                type: string
                description: Destination where backups should be stored
            required: ["source", "destination"]
```

```bash
kubectl apply -f lab/backup-crd.yaml
```

### Verify

```bash
kubectl get crd backups.data.example.com
kubectl describe crd backups.data.example.com
```

## Checklist (Score: 0/2)

- [ ] CRD `backups.data.example.com` exists with API group `data.example.com` and version `v1alpha1`
- [ ] CRD schema includes required fields `spec.source` and `spec.destination` of type string

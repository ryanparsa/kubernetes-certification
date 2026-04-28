## Answer

**Reference:** https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/

### Create the CRD

```yaml
# lab/operator-crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: operators.stable.example.com
spec:
  group: stable.example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              email:
                type: string
              name:
                type: string
              age:
                type: integer
  scope: Namespaced
  names:
    plural: operators
    singular: operator
    shortNames:
    - op
    kind: Operator
```

```bash
kubectl apply -f lab/operator-crd.yaml
kubectl get crd operators.stable.example.com
# Wait for the CRD to be established
kubectl wait crd/operators.stable.example.com --for=condition=Established --timeout=30s
```

### Create the Operator custom resource

```yaml
# lab/operator-sample.yaml
apiVersion: stable.example.com/v1
kind: Operator
metadata:
  name: operator-sample
  namespace: default
spec:
  email: operator-sample@stable.example.com
  name: operator sample
  age: 30
```

```bash
kubectl apply -f lab/operator-sample.yaml
kubectl get operator operator-sample
```

### List using all three forms

```bash
# Plural
kubectl get operators

# Singular
kubectl get operator

# Short name
kubectl get op
```

All three commands should return the `operator-sample` resource.

## Checklist (Score: 0/3)

- [ ] CRD `operators.stable.example.com` created and in `Established` condition
- [ ] Custom resource `operator-sample` created with correct `email`, `name`, and `age` fields
- [ ] Resource listable via plural (`operators`), singular (`operator`), and short name (`op`)

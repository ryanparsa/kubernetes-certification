## Answer

**Reference:** https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/

### Create the CRD

```yaml
# lab/54-crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: applications.training.ckad.io
spec:
  group: training.ckad.io
  names:
    kind: Application
    plural: applications
    singular: application
    shortNames:
    - app
  scope: Namespaced
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
            required: ["image", "replicas"]
            properties:
              image:
                type: string
              replicas:
                type: integer
                minimum: 1
```

```bash
kubectl apply -f lab/54-crd.yaml
```

### Create the namespace and custom resource

```bash
kubectl create namespace crd-demo
```

```yaml
# lab/54-cr.yaml
apiVersion: training.ckad.io/v1
kind: Application
metadata:
  name: my-app
  namespace: crd-demo
spec:
  image: nginx:1.19.0
  replicas: 3
```

```bash
kubectl apply -f lab/54-cr.yaml
```

### Verify

```bash
kubectl get crd applications.training.ckad.io
kubectl get application -n crd-demo
kubectl get application my-app -n crd-demo -o yaml
```

## Checklist (Score: 0/5)

- [ ] Namespace `crd-demo` exists
- [ ] CRD `applications.training.ckad.io` is created with group `training.ckad.io`, kind `Application`, scope `Namespaced`
- [ ] Custom resource `my-app` is created in namespace `crd-demo`
- [ ] Custom resource has field `spec.image: nginx:1.19.0`
- [ ] Custom resource has field `spec.replicas: 3`

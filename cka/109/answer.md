## Answer

**Reference:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Create the ServiceAccount

```bash
# kubectl -n project-hamster create serviceaccount processor
apiVersion: v1
kind: ServiceAccount
metadata:
  name: processor
  namespace: project-hamster
```

### Create the Role

```bash
# kubectl -n project-hamster create role processor --verb=create --resource=secrets,configmaps
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: processor
  namespace: project-hamster
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["create"]
```

### Create the RoleBinding

```bash
# kubectl -n project-hamster create rolebinding processor --role=processor --serviceaccount=project-hamster:processor
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: processor
  namespace: project-hamster
subjects:
- kind: ServiceAccount
  name: processor
  namespace: project-hamster
roleRef:
  kind: Role
  name: processor
  apiGroup: rbac.authorization.k8s.io
```

## Checklist (Score: 0/6)

- [ ] *ServiceAccount* `processor` created in *Namespace* `project-hamster`
- [ ] *Role* `processor` created in *Namespace* `project-hamster`
- [ ] *RoleBinding* `processor` created in *Namespace* `project-hamster`
- [ ] *Role* allows `create` on *Secrets*
- [ ] *Role* allows `create` on *ConfigMaps*
- [ ] *RoleBinding* correctly binds the *ServiceAccount* to the *Role*

# Question 10 | RBAC ServiceAccount Role RoleBinding

> **Solve this question on:** the "cka-lab-10" kind cluster

Create a new *ServiceAccount* `processor` in *Namespace* `project-hamster`. Create a *Role* and *RoleBinding*, both named `processor` as well. These should allow the new *ServiceAccount* to only create *Secrets* and *ConfigMaps* in that *Namespace*.

## Answer

### Explore the current state

First, we check if the *Namespace* exists:

```bash
kubectl get ns project-hamster
```

### Solution

We first create the *ServiceAccount*:

```bash
kubectl -n project-hamster create sa processor
```

For the *Role* we can first view examples:

```bash
kubectl -n project-hamster create role -h
```

So we execute:

```bash
kubectl -n project-hamster create role processor --verb=create --resource=secret,configmap
```

Which will create a *Role* like:

```yaml
# cka/10/course/10.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: processor
  namespace: project-hamster
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  - configmaps
  verbs:
  - create
```

Now we bind the *Role* to the *ServiceAccount*:

```bash
kubectl -n project-hamster create rolebinding processor --role processor --serviceaccount project-hamster:processor
```

This will create a *RoleBinding* like:

```yaml
# cka/10/course/10.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: processor
  namespace: project-hamster
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: processor
subjects:
- kind: ServiceAccount
  name: processor
  namespace: project-hamster
```

### Verify

To test our RBAC setup we can use `kubectl auth can-i`:

```bash
kubectl -n project-hamster auth can-i create secret --as system:serviceaccount:project-hamster:processor
# yes

kubectl -n project-hamster auth can-i create configmap --as system:serviceaccount:project-hamster:processor
# yes

kubectl -n project-hamster auth can-i create pod --as system:serviceaccount:project-hamster:processor
# no

kubectl -n project-hamster auth can-i delete secret --as system:serviceaccount:project-hamster:processor
# no

kubectl -n project-hamster auth can-i get configmap --as system:serviceaccount:project-hamster:processor
# no
```

## Killer.sh Checklist (Score: 0/6)

- [ ] *ServiceAccount* `processor` exists in *Namespace* `project-hamster`
- [ ] *Role* `processor` exists in *Namespace* `project-hamster`
- [ ] *RoleBinding* `processor` exists and binds the *Role* to the *ServiceAccount*
- [ ] *ServiceAccount* can `create` *Secrets*
- [ ] *ServiceAccount* can `create` *ConfigMaps*
- [ ] *ServiceAccount* cannot perform other operations (e.g. delete *Secrets*, get *ConfigMaps*, create *Pods*)

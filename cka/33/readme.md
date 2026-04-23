# Question 33 | Namespaces and Api Resources

> **Solve this question on:** the "cka-lab-33" kind cluster

Write the names of all namespaced *Kubernetes* resources (like *Pod*, *Secret*, *ConfigMap*...) into `cka/33/course/resources.txt`.

Find the `project-*` *Namespace* with the highest number of *Roles* defined in it and write its name and amount of *Roles* into `cka/33/course/crowded-namespace.txt`.

## Answer

### Namespace and Namespaced Resources

We can get a list of all resources:

```bash
kubectl api-resources    # shows all

kubectl api-resources -h   # a bit of help is always good
```

So we write them into the requested location:

```bash
kubectl api-resources --namespaced -o name > cka/33/course/resources.txt
```

Which results in the file:

```bash
# cka/33/course/resources.txt
bindings
configmaps
endpoints
events
limitranges
persistentvolumeclaims
pods
podtemplates
replicationcontrollers
resourcequotas
secrets
serviceaccounts
services
controllerrevisions.apps
daemonsets.apps
deployments.apps
replicasets.apps
statefulsets.apps
localsubjectaccessreviews.authorization.k8s.io
horizontalpodautoscalers.autoscaling
cronjobs.batch
jobs.batch
leases.coordination.k8s.io
endpointslices.discovery.k8s.io
events.events.k8s.io
ingresses.networking.k8s.io
networkpolicies.networking.k8s.io
poddisruptionbudgets.policy
rolebindings.rbac.authorization.k8s.io
roles.rbac.authorization.k8s.io
csistoragecapacities.storage.k8s.io
```

### Namespace with most *Roles*

```bash
kubectl -n project-jinan get role --no-headers | wc -l
# 0

kubectl -n project-miami get role --no-headers | wc -l
# 300

kubectl -n project-melbourne get role --no-headers | wc -l
# 2

kubectl -n project-seoul get role --no-headers | wc -l
# 10

kubectl -n project-toronto get role --no-headers | wc -l
# 0
```

Finally we write the name and amount into the file:

```bash
# cka/33/course/crowded-namespace.txt
project-miami with 300 roles
```

## Checklist

- [ ] File `cka/33/course/resources.txt` contains namespaced resources
- [ ] File `cka/33/course/crowded-namespace.txt` contains the correct *Namespace* and amount of *Roles*

## Answer

### Namespace and Namespaces Resources

We can get a list of all resources:

```bash
kubectl api-resources    # shows all

kubectl api-resources -h   # a bit of help is always good
```

So we write them into the requested location:

```bash
kubectl api-resources --namespaced -o name > cka/33/lab/resources.txt
```

Which results in the file:

```bash
# cka/33/lab/resources.txt
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
No resources found in project-jinan namespace.
0

kubectl -n project-miami get role --no-headers | wc -l
300

kubectl -n project-melbourne get role --no-headers | wc -l
2

kubectl -n project-seoul get role --no-headers | wc -l
10

kubectl -n project-toronto get role --no-headers | wc -l
No resources found in project-toronto namespace.
0
```

Finally we write the name and amount into the file:

```bash
# cka/33/lab/crowded-namespace.txt
project-miami with 300 roles
```


## Killer.sh Checklist (Score: 0/2)

- [ ] File /opt/lab/16/resources.txt contains namespaced resources
- [ ] File /opt/lab/16/crowded-namespace.txt correct content

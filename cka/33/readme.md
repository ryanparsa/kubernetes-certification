# Question 16 | Namespaces and Api Resources

Solve this question on: `ssh cka3200`

Write the names of all namespaced Kubernetes resources (like *Pod*, *Secret*, *ConfigMap*...) into `/opt/course/16/resources.txt`.

Find the `project-*` *Namespace* with the highest number of `Roles` defined in it and write its name and amount of *Roles* into `/opt/course/16/crowded-namespace.txt`.

## Answer

### Namespace and Namespaces Resources

We can get a list of all resources:

```bash
k api-resources    # shows all

k api-resources -h   # a bit of help is always good
```

So we write them into the requested location:

```bash
➜ ssh cka3200

➜ candidate@cka3200:~$ k api-resources --namespaced -o name > /opt/course/16/resources.txt
```

Which results in the file:

```bash
# cka3200:/opt/course/16/resources.txt
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

### Namespace with most Roles

```bash
➜ candidate@cka3200:~$ k -n project-jinan get role --no-headers | wc -l
No resources found in project-jinan namespace.
0

➜ candidate@cka3200:~$ k -n project-miami get role --no-headers | wc -l
300

➜ candidate@cka3200:~$ k -n project-melbourne get role --no-headers | wc -l
2

➜ candidate@cka3200:~$ k -n project-seoul get role --no-headers | wc -l
10

➜ candidate@cka3200:~$ k -n project-toronto get role --no-headers | wc -l
No resources found in project-toronto namespace.
0
```

Finally we write the name and amount into the file:

```bash
# cka3200:/opt/course/16/crowded-namespace.txt
project-miami with 300 roles
```

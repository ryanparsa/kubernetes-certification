# Question 5 | Kustomize configure HPA Autoscaler

> **Solve this question on:** the "cka-lab-5" kind cluster

Previously the application `api-gateway` used some external autoscaler which should now be replaced with a *HorizontalPodAutoscaler* (*HPA*). The application has been deployed to *Namespaces* `api-gateway-staging` and `api-gateway-prod` like this:

```
kubectl kustomize cka/5/course/api-gateway/staging | kubectl apply -f -
kubectl kustomize cka/5/course/api-gateway/prod | kubectl apply -f -
```

Using the Kustomize config at `cka/5/course/api-gateway` do the following:

1. Remove the *ConfigMap* `horizontal-scaling-config` completely
2. Add *HPA* named `api-gateway` for the *Deployment* `api-gateway` with min `2` and max `4` replicas. It should scale at `50%` average CPU utilisation
3. In prod the *HPA* should have max `6` replicas
4. Apply your changes for staging and prod so they're reflected in the cluster

## Answer

Kustomize is a standalone tool to manage K8s Yaml files, but it also comes included with kubectl. The common idea is to have a base set of K8s Yaml and then override or extend it for different overlays, like here done for staging and prod:

```bash
cd cka/5/course/api-gateway

ls
base  prod  staging
```

### Investigate Base

Let's investigate the base first for better understanding:

```bash
kubectl kustomize cka/5/course/api-gateway/base
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
---
apiVersion: v1
data:
  horizontal-scaling: "70"
kind: ConfigMap
metadata:
  name: horizontal-scaling-config
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      id: api-gateway
  template:
    metadata:
      labels:
        id: api-gateway
    spec:
      containers:
      - image: httpd:2-alpine
        name: httpd
      serviceAccountName: api-gateway
```

Running `kubectl kustomize DIR` will build the whole Yaml based on whatever is defined in the `kustomization.yaml`.

In the case above we did build for the base directory, which produces Yaml that is not expected to be deployed just like that. The base has no namespace set — the staging and prod overlays use a *NamespaceTransformer* to inject the correct namespace.

But for debugging it can be useful to build the base Yaml.

### Investigate Staging

Now we look at the staging directory:

```bash
kubectl kustomize cka/5/course/api-gateway/staging
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
  namespace: api-gateway-staging
---
apiVersion: v1
data:
  horizontal-scaling: "60"
kind: ConfigMap
metadata:
  name: horizontal-scaling-config
  namespace: api-gateway-staging
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    env: staging
  name: api-gateway
  namespace: api-gateway-staging
spec:
  replicas: 1
  selector:
    matchLabels:
      id: api-gateway
  template:
    metadata:
      labels:
        id: api-gateway
    spec:
      containers:
      - image: httpd:2-alpine
        name: httpd
      serviceAccountName: api-gateway
```

We can see that all resources now have `namespace: api-gateway-staging`. Also staging seems to change the *ConfigMap* value to `horizontal-scaling: "60"`. And it adds the additional label `env: staging` to the *Deployment*. The rest is taken from base.

This all happens because of the *Kustomization* file:

```yaml
# cka/5/course/api-gateway/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../base

patches:
  - path: api-gateway.yaml

transformers:
  - |-
    apiVersion: builtin
    kind: NamespaceTransformer
    metadata:
      name: notImportantHere
      namespace: api-gateway-staging
```

- The `resources:` section is the directory on which everything will be based on
- The `patches:` section specifies Yaml files with alterations or additions applied on the base files
- The `transformers:` section in this case sets the *Namespace* for all resources

We should be able to build and deploy the staging *YAML*:

```bash
kubectl kustomize cka/5/course/api-gateway/staging | kubectl diff -f -

kubectl kustomize cka/5/course/api-gateway/staging | kubectl apply -f -
serviceaccount/api-gateway unchanged
configmap/horizontal-scaling-config unchanged
deployment.apps/api-gateway unchanged
```

Actually we see that no changes were performed, because everything is already deployed:

```bash
kubectl -n api-gateway-staging get deployment,configmap
NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/api-gateway   1/1     1            1           20m

NAME                               DATA   AGE
configmap/horizontal-scaling-config   1       20m
configmap/kube-root-ca.crt           1       21m
```

### Investigate Prod

Everything said about staging is also true about prod, there are just different values of resources changed. Hence we should also see that there are no changes to be applied:

```bash
kubectl kustomize cka/5/course/api-gateway/prod
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
  namespace: api-gateway-prod
...
```

We can see that now *Namespace* `api-gateway-prod` is being used.

```bash
kubectl kustomize cka/5/course/api-gateway/prod | kubectl diff -f -

kubectl kustomize cka/5/course/api-gateway/prod | kubectl apply -f -
serviceaccount/api-gateway unchanged
configmap/horizontal-scaling-config unchanged
deployment.apps/api-gateway unchanged
```

And everything seems to be up to date for prod as well.

### Step 1

We need to remove the *ConfigMap* from base, staging and prod because staging and prod both reference it as a patch. If we would only remove it from base we would run into an error when trying to build staging for example:

```bash
kubectl kustomize cka/5/course/api-gateway/staging
error: no resource matches strategic merge patch "ConfigMap.v1.[noGrp]/horizontal-scaling-config.[noNs]": no matches for Id ConfigMap.v1.[noGrp]/horizontal-scaling-config.[noNs]; failed to find unique target for patch ConfigMap.v1.[noGrp]/horizontal-scaling-config.[noNs]
```

So we edit files `cka/5/course/api-gateway/base/api-gateway.yaml`, `cka/5/course/api-gateway/staging/api-gateway.yaml` and `cka/5/course/api-gateway/prod/api-gateway.yaml` and remove the *ConfigMap*. Afterwards we should get no errors and *YAML* without that *ConfigMap*:

```bash
kubectl kustomize cka/5/course/api-gateway/staging
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
  namespace: api-gateway-staging
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    env: staging
  name: api-gateway
  namespace: api-gateway-staging
spec:
  replicas: 1
  selector:
    matchLabels:
      id: api-gateway
  template:
    metadata:
      labels:
        id: api-gateway
    spec:
      containers:
      - image: httpd:2-alpine
        name: httpd
      serviceAccountName: api-gateway

kubectl kustomize cka/5/course/api-gateway/prod
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
  namespace: api-gateway-prod
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    env: prod
  name: api-gateway
  namespace: api-gateway-prod
spec:
  replicas: 1
  ...
```

### Step 2

We're going to add the requested *HPA* into the base config file:

```yaml
# cka/5/course/api-gateway/base/api-gateway.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      id: api-gateway
  template:
    metadata:
      labels:
        id: api-gateway
    spec:
      serviceAccountName: api-gateway
      containers:
      - image: httpd:2-alpine
        name: httpd
        resources:
          requests:
            cpu: 100m
```

Notice that we don't specify a *Namespace* here as done also for the other resources. The *Namespace* will be set by staging and prod overlays automatically.

### Step 3

In prod the *HPA* should have max replicas set to `6` so we add this to the prod *patch*:

```yaml
# cka/5/course/api-gateway/prod/api-gateway.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
spec:
  maxReplicas: 6
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  labels:
    env: prod
```

With that change we should see that staging will have the *HPA* with `maxReplicas: 4` from base, whereas prod will have `maxReplicas: 6`:

```bash
kubectl kustomize cka/5/course/api-gateway/staging | grep maxReplicas -B5
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
  namespace: api-gateway-staging
spec:
  maxReplicas: 4

kubectl kustomize cka/5/course/api-gateway/prod | grep maxReplicas -B5
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway
  namespace: api-gateway-prod
spec:
  maxReplicas: 6
```

### Step 4

Finally we apply the changes, first staging:

```bash
kubectl kustomize cka/5/course/api-gateway/staging | kubectl diff -f -
diff -u -N /tmp/LIVE-3038173353/autoscaling.v2.HorizontalPodAutoscaler.api-gateway-staging.api-gateway /tmp/MERGED-332240272/autoscaling.v2.HorizontalPodAutoscaler.api-gateway-staging.api-gateway
--- /tmp/LIVE-3038173353/autoscaling.v2.HorizontalPodAutoscaler.api-gateway-staging.api-gateway 2024-12-23 16:21:47.771211074 +0000
+++ /tmp/MERGED-332240272/autoscaling.v2.HorizontalPodAutoscaler.api-gateway-staging.api-gateway       2024-12-23 16:21:47.772211169 +0000
@@ -0,0 +1,24 @@
+apiVersion: autoscaling/v2
+kind: HorizontalPodAutoscaler
+metadata:
+  creationTimestamp: "2024-12-23T16:21:47Z"
+  name: api-gateway
+  namespace: api-gateway-staging
+  uid: d846f349-e695-4538-b3f8-ba514fc02ea5
+spec:
+  maxReplicas: 4
+  metrics:
+  - resource:
+      name: cpu
+      target:
+        averageUtilization: 50
+        type: Utilization
+    type: Resource
+  minReplicas: 2
+  scaleTargetRef:
+    apiVersion: apps/v1
+    kind: Deployment
+    name: api-gateway
+status:
+  currentMetrics: null
+  desiredReplicas: 0

kubectl kustomize cka/5/course/api-gateway/staging | kubectl apply -f -
serviceaccount/api-gateway unchanged
deployment.apps/api-gateway unchanged
horizontalpodautoscaler.autoscaling/api-gateway created

kubectl kustomize cka/5/course/api-gateway/staging | kubectl diff -f -
```

And next for prod:

```bash
kubectl kustomize cka/5/course/api-gateway/prod | kubectl apply -f -
serviceaccount/api-gateway unchanged
deployment.apps/api-gateway unchanged
horizontalpodautoscaler.autoscaling/api-gateway created

kubectl kustomize cka/5/course/api-gateway/prod | kubectl diff -f -
```

We notice that the *HPA* was created as expected, but nothing was done with the *ConfigMap* that we removed from the *YAML* files earlier. We need to delete the remote *ConfigMaps* manually, why is explained in more detail at the end of this solution.

```bash
kubectl -n api-gateway-staging get configmap
NAME                        DATA   AGE
horizontal-scaling-config   1       61m
kube-root-ca.crt            1       61m

kubectl -n api-gateway-staging delete configmap horizontal-scaling-config
configmap "horizontal-scaling-config" deleted

kubectl -n api-gateway-prod get configmap
NAME                        DATA   AGE
horizontal-scaling-config   2       61m
kube-root-ca.crt            1       62m

kubectl -n api-gateway-prod delete configmap horizontal-scaling-config
configmap "horizontal-scaling-config" deleted

```

Done!

### Diff output after solution complete

After deleting the *ConfigMaps* manually we should not see any changes when running a diff. This is because the *ConfigMap* does not exist any longer in our *YAML* and we already applied all changes. But we might see something like this:

```bash
kubectl kustomize cka/5/course/api-gateway/prod | kubectl diff -f -
diff -u -N /tmp/LIVE-849078037/apps.v1.Deployment.api-gateway-prod.api-gateway /tmp/MERGED-2513424623/apps.v1.Deployment.api-gateway-prod.api-gateway
--- /tmp/LIVE-849078037/apps.v1.Deployment.api-gateway-prod.api-gateway 2024-12-23 16:37:44.763088538 +0000
+++ /tmp/MERGED-2513424623/apps.v1.Deployment.api-gateway-prod.api-gateway     2024-12-23 16:37:44.766088823 +0000
@@ -6,7 +6,7 @@
     kubectl.kubernetes.io/last-applied-configuration: |
       {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"env":"prod"},"name":"api-gateway","namespace":"api-gateway-prod"},"spec":{"replicas":1,"selector":{"matchLabels":{"id":"api-gateway"}},"template":{"metadata":{"labels":{"id":"api-gateway"}},"spec":{"containers":[{"image":"httpd:2-alpine","name":"httpd"}],"serviceAccountName":"api-gateway"}}}}
   creationTimestamp: "2024-12-23T15:34:06Z"
-  generation: 2
+  generation: 3
   labels:
     env: prod
   name: api-gateway
@@ -15,7 +15,7 @@
   uid: ca3b43c9-d33b-4bdc-98ae-172cd9ee8cdb
 spec:
   progressDeadlineSeconds: 600
-  replicas: 2
+  replicas: 1
   revisionHistoryLimit: 10
   selector:
     matchLabels:
```

Above we can see that we would change the replicas from 2 to 1. This is because the *HPA* already set the replicas to the `minReplicas` that we defined and it's different than the default `replicas:` of the *Deployment*:

```bash
kubectl -n api-gateway-prod get hpa
NAME          ...   MINPODS   MAXPODS   REPLICAS   AGE
api-gateway   ...   2         6         2          15m
```

This means each time we deploy our Kustomize built Yaml, the replicas that the *HPA* applied would be overwritten, which is not cool. It does not matter for the scoring of this question but to prevent this we could simply remove the `replicas:` setting from the *Deployment* in base, staging and prod.

### Kustomize / Helm and State

We had to delete the remote *ConfigMaps* manually. Kustomize won't delete remote resources if they only exist remote. This is because it does not keep any state and hence doesn't know which remote resources were created by Kustomize or by anything else.

Helm will remove remote resources if they only exist remote and if they were created by Helm. It can do this because it keeps a state (or release information) of all performed changes.

Both approaches have pros and cons:

- Kustomize is less complex by not having to manage state, but might need more manual work cleaning up
- Helm can keep better track of remote resources, but things can get complex and messy if there is a state error or mismatch. State changes (Helm actions) at the same time need to be prevented or accounted for

## Killer.sh Checklist (Score: 0/6)

- [ ] HPA `api-gateway` exists in namespace `api-gateway-staging` with `minReplicas: 2`
- [ ] HPA `api-gateway` in namespace `api-gateway-staging` has `maxReplicas: 4`
- [ ] HPA `api-gateway` in namespace `api-gateway-staging` targets 50% average CPU utilisation
- [ ] HPA `api-gateway` exists in namespace `api-gateway-prod` with `maxReplicas: 6`
- [ ] ConfigMap `horizontal-scaling-config` does not exist in namespace `api-gateway-staging`
- [ ] ConfigMap `horizontal-scaling-config` does not exist in namespace `api-gateway-prod`

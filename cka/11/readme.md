# Question 11 | DaemonSet on all Nodes

> **Solve this question on:** the "cka-lab-11" kind cluster

Use *Namespace* `project-tiger` for the following. Create a *DaemonSet* named `ds-important` with image `httpd:2-alpine` and labels `id=ds-important` and `uuid=18426a0b-5f59-4e10-923f-c0e078e82462`. The *Pods* it creates should request 10 millicore cpu and 10 mebibyte memory. The *Pods* of that *DaemonSet* should run on all *Nodes*, also *Controlplanes*.

## Answer

As of now we aren't able to create a *DaemonSet* directly using `kubectl`, so we create a *Deployment* and just change it up:

```bash
kubectl -n project-tiger create deployment --image=httpd:2-alpine ds-important --dry-run=client -o yaml > cka/11/course/11.yaml
```

Or we could search for a *DaemonSet* example yaml in the K8s docs and alter it to our needs.

We adjust the yaml to:

```yaml
# cka/11/course/11.yaml
apiVersion: apps/v1
kind: DaemonSet                               # change from Deployment to Daemonset
metadata:
  creationTimestamp: null
  labels:                                     # add
    id: ds-important                          # add
    uuid: 18426a0b-5f59-4e10-923f-c0e078e82462# add
  name: ds-important
  namespace: project-tiger                    # important
spec:
  #replicas: 1                                # remove
  selector:
    matchLabels:
      id: ds-important                        # add
      uuid: 18426a0b-5f59-4e10-923f-c0e078e82462# add
  #strategy: {}                               # remove
  template:
    metadata:
      creationTimestamp: null
      labels:
        id: ds-important                      # add
        uuid: 18426a0b-5f59-4e10-923f-c0e078e82462# add
    spec:
      containers:
      - image: httpd:2-alpine
        name: ds-important
        resources:
          requests:                           # add
            cpu: 10m                          # add
            memory: 10Mi                      # add
      tolerations:                            # add
      - effect: NoSchedule                    # add
        key: node-role.kubernetes.io/control-plane # add
#status: {}                                   # remove
```

It was requested that the *DaemonSet* runs on all *Nodes*, so we need to specify the toleration for this.

Let's give it a go:

```bash
kubectl create -f cka/11/course/11.yaml
daemonset.apps/ds-important created

kubectl -n project-tiger get ds
NAME           DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
ds-important   3         3         3       3            3           <none>          8s

kubectl -n project-tiger get pod -l id=ds-important -o wide
NAME                 READY   STATUS    ...   NODE                        ...
ds-important-26456   1/1     Running   ...   cka-lab-11-worker              ...
ds-important-wnt5p   1/1     Running   ...   cka-lab-11-control-plane       ...
ds-important-wrbjd   1/1     Running   ...   cka-lab-11-worker2             ...
```

Above we can see one *Pod* on each *Node*, including the *Controlplane* one.

## Killer.sh Checklist (Score: 0/9)

- [ ] DaemonSet `ds-important` exists in namespace `project-tiger`
- [ ] DaemonSet has label `id=ds-important`
- [ ] DaemonSet has label `uuid=18426a0b-5f59-4e10-923f-c0e078e82462`
- [ ] Pod template has label `id=ds-important`
- [ ] Pod template has label `uuid=18426a0b-5f59-4e10-923f-c0e078e82462`
- [ ] Container requests 10m CPU
- [ ] Container requests 10Mi memory
- [ ] DaemonSet has toleration for `node-role.kubernetes.io/control-plane:NoSchedule`
- [ ] DaemonSet runs on all nodes (desired == ready > 0)

# Question 11 | DaemonSet on all Nodes

Solve this question on: `ssh cka2556`

Use *Namespace* `project-tiger` for the following. Create a *DaemonSet* named `ds-important` with image `httpd:2-alpine` and labels `id=ds-important` and `uuid=18426a0b-5f59-4e10-923f-c0e078e82462`. The *Pods* it creates should request 10 millicore cpu and 10 mebibyte memory. The *Pods* of that *DaemonSet* should run on all nodes, also controlplanes.

## Answer

As of now we aren't able to create a *DaemonSet* directly using `kubectl`, so we create a *Deployment* and just change it up:

```bash
➜ ssh cka2556
➜ candidate@cka2556:~$ k -n project-tiger create deployment --image=httpd:2.4-alpine ds-important --dry-run=client -o yaml > 11.yaml
```

Or we could search for a *DaemonSet* example yaml in the K8s docs and alter it to our needs.

We adjust the yaml to:

```yaml
# cka2556:/home/candidate/11.yaml
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

It was requested that the *DaemonSet* runs on all nodes, so we need to specify the toleration for this.

Let's give it a go:

```bash
➜ candidate@cka2556:~$ k -f 11.yaml create
daemonset.apps/ds-important created

➜ candidate@cka2556:~$ k -n project-tiger get ds
NAME           DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
ds-important   3         3         3       3            3           <none>          8s

➜ candidate@cka2556:~$ k -n project-tiger get pod -l id=ds-important -o wide
NAME                 READY   STATUS    ...   NODE            ...
ds-important-26456   1/1     Running   ...   cka2556-node2   ...
ds-important-wnt5p   1/1     Running   ...   cka2556         ...
ds-important-wrbjd   1/1     Running   ...   cka2556-node1   ...
```

Above we can see one *Pod* on each node, including the controlplane one.

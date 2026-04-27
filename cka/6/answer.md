## Answer

```bash
vim cka/6/lab/6_pv.yaml
```

Find an example from https://kubernetes.io/docs and alter it:

```yaml
kind: PersistentVolume
apiVersion: v1
metadata:
 name: safari-pv
spec:
 storageClassName: ""
 capacity:
  storage: 2Gi
 accessModes:
  - ReadWriteOnce
 hostPath:
  path: "/Volumes/Data"
```

> ℹ️ Using the `hostPath` volume type presents many security risks, avoid if possible. Be aware that data stored in the hostPath directory will not be shared across nodes. The data available for a Pod depends on which node the Pod is scheduled.

Then create it:

```bash
k -f cka/6/lab/6_pv.yaml create
persistentvolume/safari-pv created
```

Next the *PersistentVolumeClaim*:

```bash
vim cka/6/lab/6_pvc.yaml
```

Find an example from the K8s Docs and alter it:

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: safari-pvc
  namespace: project-t230
spec:
  storageClassName: ""
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
     storage: 2Gi
```

Then create:

```bash
k -f cka/6/lab/6_pvc.yaml create
persistentvolumeclaim/safari-pvc created
```

And check that both have the status Bound:

```bash
k -n project-t230 get pv,pvc
NAME                         CAPACITY  ... STATUS   CLAIM                    ...
persistentvolume/safari-pv   2Gi       ... Bound    project-t230/safari-pvc ...

NAME                               STATUS   VOLUME      CAPACITY ...
persistentvolumeclaim/safari-pvc   Bound    safari-pv   2Gi      ...
```

Next we create a *Deployment* and mount that volume:

```bash
k -n project-t230 create deploy safari --image=httpd:2-alpine --dry-run=client -o yaml > cka/6/lab/6_dep.yaml

vim cka/6/lab/6_dep.yaml
```

Alter the yaml to mount the volume:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: safari
  name: safari
  namespace: project-t230
spec:
  replicas: 1
  selector:
    matchLabels:
      app: safari
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: safari
    spec:
      volumes:                                      # add
      - name: data                                  # add
        persistentVolumeClaim:                      # add
          claimName: safari-pvc                     # add
      containers:
      - image: httpd:2-alpine
        name: container
        volumeMounts:                               # add
        - name: data                                # add
          mountPath: /tmp/safari-data               # add
```

```bash
k -f cka/6/lab/6_dep.yaml create
deployment.apps/safari created
```

We can confirm it's mounting correctly:

```bash
k -n project-t230 describe pod safari-b499cc5b9-x7d7h | grep -A2 Mounts:
    Mounts:
      /tmp/safari-data from data (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xght8 (ro)
```

## Killer.sh Checklist (Score: 0/10)

- [ ] PersistentVolume `safari-pv` exists
- [ ] PV capacity is 2Gi
- [ ] PV accessMode is ReadWriteOnce
- [ ] PV hostPath is `/Volumes/Data`
- [ ] PV has no storageClassName
- [ ] PVC `safari-pvc` exists in Namespace `project-t230`
- [ ] PVC is Bound to the PV
- [ ] Deployment `safari` exists in Namespace `project-t230`
- [ ] Deployment uses image `httpd:2-alpine`
- [ ] Volume is mounted at `/tmp/safari-data`
# Question 6 | Storage, PV, PVC, Pod volume

> **Solve this question on:** `ssh cka7968`

Create a new *PersistentVolume* named `safari-pv`. It should have a capacity of *2Gi*, accessMode *ReadWriteOnce*, hostPath `/Volumes/Data` and no storageClassName defined.

Next create a new *PersistentVolumeClaim* in *Namespace* `project-t230` named `safari-pvc`. It should request *2Gi* storage, accessMode *ReadWriteOnce* and should not define a storageClassName. The *PVC* should bound to the *PV* correctly.

Finally create a new *Deployment* `safari` in *Namespace* `project-t230` which mounts that volume at `/tmp/safari-data`. The *Pods* of that *Deployment* should be of image `httpd:2-alpine`.

## Answer

```bash
➜ ssh cka7968

➜ candidate@cka7968:~$ vim 6_pv.yaml
```

Find an example from https://kubernetes.io/docs and alter it:

```yaml
# cka7968:/home/candidate/6_pv.yaml
kind: PersistentVolume
apiVersion: v1
metadata:
 name: safari-pv
spec:
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
➜ candidate@cka7968:~$ k -f 6_pv.yaml create
persistentvolume/safari-pv created
```

Next the *PersistentVolumeClaim*:

```bash
➜ candidate@cka7968:~ vim 6_pvc.yaml
```

Find an example from the K8s Docs and alter it:

```yaml
# cka7968:/home/candidate/6_pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: safari-pvc
  namespace: project-t230
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
     storage: 2Gi
```

Then create:

```bash
➜ candidate@cka7968:~$ k -f 6_pvc.yaml create
persistentvolumeclaim/safari-pvc created
```

And check that both have the status Bound:

```bash
➜ candidate@cka7968:~$ k -n project-t230 get pv,pvc
NAME                         CAPACITY  ... STATUS   CLAIM                    ...
persistentvolume/safari-pv   2Gi       ... Bound    project-t230/safari-pvc ...

NAME                               STATUS   VOLUME      CAPACITY ...
persistentvolumeclaim/safari-pvc   Bound    safari-pv   2Gi      ...
```

Next we create a *Deployment* and mount that volume:

```bash
➜ candidate@cka7968:~$ k -n project-t230 create deploy safari --image=httpd:2-alpine --dry-run=client -o yaml > 6_dep.yaml

➜ candidate@cka7968:~$ vim 6_dep.yaml
```

Alter the yaml to mount the volume:

```yaml
# cka7968:/home/candidate/6_dep.yaml
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
➜ candidate@cka7968:~$ k -f 6_dep.yaml create
deployment.apps/safari created
```

We can confirm it's mounting correctly:

```bash
➜ candidate@cka7968:~$ k -n project-t230 describe pod safari-b499cc5b9-x7d7h | grep -A2 Mounts:
    Mounts:
      /tmp/safari-data from data (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xght8 (ro)
```
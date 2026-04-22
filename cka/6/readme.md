# Question 6 | Storage, PV, PVC, Pod volume

> **Solve this question on:** `ssh cka7968`

Create a new *PersistentVolume* named `safari-pv`. It should have a capacity of *2Gi*, accessMode *ReadWriteOnce*, hostPath `/Volumes/Data` and no storageClassName defined.

Next create a new *PersistentVolumeClaim* in *Namespace* `project-t230` named `safari-pvc`. It should request *2Gi* storage, accessMode *ReadWriteOnce* and should not define a storageClassName. The *PVC* should bound to the *PV* correctly.

Finally create a new *Deployment* `safari` in *Namespace* `project-t230` which mounts that volume at `/tmp/safari-data`. The *Pods* of that *Deployment* should be of image `httpd:2-alpine`.

## Answer

```bash
➜ ssh cka7968
```

Let's start by creating the *PersistentVolume*:

```bash
➜ candidate@cka7968:~$ vim 6_pv.yaml
```

```yaml
# 6_pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: safari-pv
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /Volumes/Data
```

```bash
➜ candidate@cka7968:~$ k -f 6_pv.yaml apply
persistentvolume/safari-pv created

➜ candidate@cka7968:~$ k get pv
NAME        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
safari-pv   2Gi        RWO            Retain           Available                                   4s
```

Next we create the *PersistentVolumeClaim*:

```bash
➜ candidate@cka7968:~$ vim 6_pvc.yaml
```

```yaml
# 6_pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
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

```bash
➜ candidate@cka7968:~$ k -f 6_pvc.yaml apply
persistentvolumeclaim/safari-pvc created

➜ candidate@cka7968:~$ k -n project-t230 get pvc
NAME         STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
safari-pvc   Bound    safari-pv  2Gi        RWO                           2s

➜ candidate@cka7968:~$ k get pv
NAME        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS   REASON   AGE
safari-pv   2Gi        RWO            Retain           Bound    project-t230/safari-pvc                            22s
```

Great! The *PVC* is Bound to our *PV*. Finally we create the *Deployment* and mount the volume:

```bash
➜ candidate@cka7968:~$ k -n project-t230 create deployment safari --image=httpd:2-alpine --dry-run=client -o yaml > 6_dep.yaml

➜ candidate@cka7968:~$ vim 6_dep.yaml
```

```yaml
# 6_dep.yaml
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
        name: httpd
        volumeMounts:                               # add
        - name: data                                # add
          mountPath: /tmp/safari-data              # add
        resources: {}
status: {}
```

```bash
➜ candidate@cka7968:~$ k -f 6_dep.yaml apply
deployment.apps/safari created

➜ candidate@cka7968:~$ k -n project-t230 get pod
NAME                      READY   STATUS    RESTARTS   AGE
safari-57cbdfc69b-9p8z8   1/1     Running   0          33s
```

Let's check if the mounting works:

```bash
➜ candidate@cka7968:~$ k -n project-t230 exec safari-57cbdfc69b-9p8z8 -- df -h | grep safari
/dev/vdb                  2.0G   24K  1.9G   1% /tmp/safari-data

➜ candidate@cka7968:~$ k -n project-t230 exec safari-57cbdfc69b-9p8z8 -- mount | grep safari
/dev/vdb on /tmp/safari-data type ext4 (rw,relatime)
```

The volume is mounted! When using `hostPath`, it's very important to know that the directory `/Volumes/Data` has to exist on every Node where a *Pod* could be scheduled. Otherwise the *Pod* will stay in a `Pending` state. In a real world setup this could be implemented by a NFS mount for example.
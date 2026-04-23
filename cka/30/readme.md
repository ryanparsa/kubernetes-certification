# Question 30 | Multi Containers and Pod shared Volume

> **Solve this question on:** the "cka-lab-30" kind cluster

Create a *Pod* with multiple *Containers* named `multi-container-playground` in *Namespace* `default`:

- It should have a *Volume* attached and mounted into each *Container*. The *Volume* shouldn't be persisted or shared with other *Pods*
- *Container* `c1` with image `nginx:1-alpine` should have the name of the *Node* where its *Pod* is running on available as environment variable `MY_NODE_NAME`
- *Container* `c2` with image `busybox:1` should write the output of the `date` command every second in the shared *Volume* into file `date.log`. You can use `while true; do date >> /your/vol/path/date.log; sleep 1; done` for this.
- *Container* `c3` with image `busybox:1` should constantly write the content of file `date.log` from the shared *Volume* to stdout. You can use `tail -f /your/vol/path/date.log` for this.

> ℹ️ Check the logs of *Container* `c3` to confirm correct setup

## Answer

First we create the *Pod* template:

```bash
kubectl run multi-container-playground --image=nginx:1-alpine --dry-run=client -o yaml > cka/30/course/30.yaml
```

And add the other *Containers* and the commands they should execute:

```yaml
# cka/30/course/30.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-container-playground
  name: multi-container-playground
spec:
  containers:
  - image: nginx:1-alpine
    name: c1
    env:
    - name: MY_NODE_NAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
    volumeMounts:
    - name: vol
      mountPath: /vol
  - image: busybox:1
    name: c2
    command: ["sh", "-c", "while true; do date >> /vol/date.log; sleep 1; done"]
    volumeMounts:
    - name: vol
      mountPath: /vol
  - image: busybox:1
    name: c3
    command: ["sh", "-c", "tail -f /vol/date.log"]
    volumeMounts:
    - name: vol
      mountPath: /vol
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:
  - name: vol
    emptyDir: {}
```

Well, there was a lot requested here! We check if everything is good with the *Pod*:

```bash
kubectl create -f cka/30/course/30.yaml

kubectl get pod multi-container-playground
```

Now we check if *Container* `c1` has the requested *Node* name as env variable:

```bash
kubectl exec multi-container-playground -c c1 -- env | grep MY_NODE_NAME
```

And finally we check the logging, which means that *Container* `c2` correctly writes and *Container* `c3` correctly reads and outputs to stdout:

```bash
kubectl logs multi-container-playground -c c3
```

## Checklist

- [ ] *Pod* is running
- [ ] *Pod* has three *Containers*
- [ ] *Pod* has three *Ready* *Containers*
- [ ] *Container* `c1` has correct name
- [ ] *Container* `c1` has correct image
- [ ] *Container* `c1` has environment variable `MY_NODE_NAME`
- [ ] *Container* `c2` has correct name
- [ ] *Container* `c2` has correct image
- [ ] *Container* `c3` has correct name
- [ ] *Container* `c3` has correct image
- [ ] All *Containers* have *Volume* mounted

# Question 13 | Multi Containers and Pod shared Volume

Create a *Pod* with multiple containers named `multi-container-playground` in *Namespace* `default`:

- It should have a volume attached and mounted into each container. The volume shouldn't be persisted or shared with other *Pods*
- Container `c1` with image `nginx:1-alpine` should have the name of the node where its *Pod* is running on available as environment variable `MY_NODE_NAME`
- Container `c2` with image `busybox:1` should write the output of the `date` command every second in the shared volume into file `date.log`. You can use `while true; do date >> /your/vol/path/date.log; sleep 1; done` for this.
- Container `c3` with image `busybox:1` should constantly write the content of file `date.log` from the shared volume to stdout. You can use `tail -f /your/vol/path/date.log` for this.

> ℹ️ Check the logs of container `c3` to confirm correct setup

## Answer

First we create the *Pod* template:

```bash
k run multi-container-playground --image=nginx:1-alpine --dry-run=client -o yaml > 13.yaml
```

And add the other containers and the commands they should execute:

```yaml
# 13.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-container-playground
  name: multi-container-playground
spec:
  containers:
  - image: nginx:1-alpine
    name: c1                          # change
    resources: {}
    env:                              # add
    - name: MY_NODE_NAME              # add
      valueFrom:                      # add
        fieldRef:                     # add
          fieldPath: spec.nodeName    # add
    volumeMounts:                     # add
    - name: vol                       # add
      mountPath: /vol                 # add
  - image: busybox:1                  # add
    name: c2                          # add
    command: ["sh", "-c", "while true; do date >> /vol/date.log; sleep 1; done"]  # add
    volumeMounts:                     # add
    - name: vol                       # add
      mountPath: /vol                 # add
  - image: busybox:1                  # add
    name: c3                          # add
    command: ["sh", "-c", "tail -f /vol/date.log"]  # add
    volumeMounts:                     # add
    - name: vol                       # add
      mountPath: /vol                 # add
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:                            # add
  - name: vol                         # add
    emptyDir: {}                      # add
status: {}
```

Well, there was a lot requested here! We check if everything is good with the *Pod*:

```bash
k -f 13.yaml create
pod/multi-container-playground created

k get pod multi-container-playground
NAME                         READY   STATUS    RESTARTS   AGE
multi-container-playground   3/3     Running   0          47s
```

Now we check if container `c1` has the requested node name as env variable:

```bash
k exec multi-container-playground -c c1 -- env | grep MY
MY_NODE_NAME=cka-lab-control-plane
```

And finally we check the logging, which means that `c2` correctly writes and `c3` correctly reads and outputs to stdout:

```bash
k logs multi-container-playground -c c3
Tue Nov  5 13:41:33 UTC 2024
Tue Nov  5 13:41:34 UTC 2024
Tue Nov  5 13:41:35 UTC 2024
Tue Nov  5 13:41:36 UTC 2024
Tue Nov  5 13:41:37 UTC 2024
Tue Nov  5 13:41:38 UTC 2024
```

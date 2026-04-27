## Answer

First we create the *Pod* template:

```bash
kubectl run multi-container-playground --image=nginx:1-alpine --dry-run=client -o yaml > 30.yaml
```

And add the other *Containers* and the commands they should execute:

```yaml
# cka/30/lab/30.yaml
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
kubectl -f 30.yaml create
pod/multi-container-playground created

kubectl get pod multi-container-playground
NAME                         READY   STATUS    RESTARTS   AGE
multi-container-playground   3/3     Running   0          47s
```

Now we check if *Container* `c1` has the requested *Node* name as env variable:

```bash
kubectl exec multi-container-playground -c c1 -- env | grep MY
MY_NODE_NAME=cka-lab-30-control-plane
```

And finally we check the logging, which means that *Container* `c2` correctly writes and *Container* `c3` correctly reads and outputs to *stdout*:

```bash
kubectl logs multi-container-playground -c c3
Tue Nov  5 13:41:33 UTC 2024
Tue Nov  5 13:41:34 UTC 2024
Tue Nov  5 13:41:35 UTC 2024
Tue Nov  5 13:41:36 UTC 2024
Tue Nov  5 13:41:37 UTC 2024
Tue Nov  5 13:41:38 UTC 2024
```


## Checklist (Score: 0/11)

- [ ] Pod is running
- [ ] Pod has three containers
- [ ] Pod has three Ready containers
- [ ] Pod container 1 has correct name
- [ ] Pod container 1 has correct image
- [ ] Pod container 1 has env variable MY_NODE_NAME
- [ ] Pod container 2 has correct name
- [ ] Pod container 2 has correct image
- [ ] Pod container 3 has correct name
- [ ] Pod container 3 has correct image
- [ ] All Pod containers have volume mounted

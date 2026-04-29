## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/generated/kubectl_run/

### Create the Pod

```bash
kubectl run tigers-reunite -n project-tiger --image=httpd:2.4-alpine --labels "pod=container,container=pod"
```

### Find the Node

```bash
kubectl get pod tigers-reunite -n project-tiger -o wide
```

Output:
```
NAME             READY   STATUS    RESTARTS   AGE   IP           NODE               NOMINATED NODE   READINESS GATES
tigers-reunite   1/1     Running   0          10s   10.244.1.2   cka-lab-196-worker   <none>           <none>
```

The node is `cka-lab-196-worker`.

### Connect to the Node and find the Container

```bash
docker exec -it cka-lab-196-worker bash
```

Inside the node:

```bash
crictl ps --name tigers-reunite
```

Output:
```
CONTAINER           IMAGE               CREATED             STATE               NAME                ATTEMPT             POD ID              NAMESPACE
d5f3a6b7c8d9e       a7ccaadd632cf       30 seconds ago      Running             tigers-reunite      0                   e1f2a3b4c5d6e       project-tiger
```

### Get ID and runtimeType

```bash
crictl inspect d5f3a6b7c8d9e | grep runtimeType
```

Output:
```
    "runtimeType": "io.containerd.runc.v2",
```

Write to `lab/pod-container.txt`:
```
d5f3a6b7c8d9e io.containerd.runc.v2
```

### Get logs

```bash
crictl logs d5f3a6b7c8d9e
```

Write the output to `lab/container.log`.

## Checklist (Score: 5/5)

- [ ] Pod `tigers-reunite` created in namespace `project-tiger`
- [ ] Pod uses image `httpd:2.4-alpine`
- [ ] Pod has labels `pod=container` and `container=pod`
- [ ] File `lab/pod-container.txt` contains container ID and `runtimeType`
- [ ] File `lab/container.log` contains container logs

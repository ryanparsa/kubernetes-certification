# Question 2 | Create a Static Pod and Service

> **Solve this question on:** the "cka-lab-19" kind cluster

Create a *Static Pod* named `my-static-pod` in *Namespace* `default` on the *Node* `cka-lab-19-control-plane`. It should be of image `nginx:1-alpine` and have resource requests for `10m` CPU and `20Mi` memory.

Create a *NodePort Service* named `static-pod-service` which exposes that *Static Pod* on port `80`.

> [!NOTE]
> ℹ️ For verification check if the new *Service* has one *Endpoint*. In the kind lab you can access the *Node* `cka-lab-19-control-plane` with `docker exec -it cka-lab-19-control-plane bash`

## Answer

### Step 1

First we find the *Controlplane Node* and its internal IP:

```bash
kubectl get node -o wide
NAME                        STATUS   ROLES           AGE   VERSION   INTERNAL-IP
cka-lab-19-control-plane    Ready    control-plane   8d    v1.33.1   172.18.0.2
cka-lab-19-worker           Ready    <none>          8d    v1.33.1   172.18.0.3
```

### Step 2

Access the *Controlplane Node*:

```bash
docker exec -it cka-lab-19-control-plane bash
```

Now we navigate to the *Static Pod* manifests directory and create the manifest:

```bash
cd /etc/kubernetes/manifests/

# Create the Static Pod manifest
kubectl run my-static-pod --image=nginx:1-alpine -o yaml --dry-run=client > 19.yaml
```

Then edit the `19.yaml` to add the requested resource requests:

```yaml
# /etc/kubernetes/manifests/19.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: my-static-pod
  name: my-static-pod
spec:
  containers:
  - image: nginx:1-alpine
    name: my-static-pod
    resources:
      requests:
        cpu: 10m
        memory: 20Mi
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Exit the *Node* shell and verify the *Pod* is running (it will have the suffix `-cka-lab-19-control-plane`):

```bash
kubectl get pod -A | grep my-static
default       my-static-pod-cka-lab-19-control-plane   1/1     Running   0            20s
```

### Step 3

Now we expose that *Static Pod* by creating a *NodePort Service*:

```bash
kubectl expose pod my-static-pod-cka-lab-19-control-plane --name static-pod-service --type=NodePort --port 80
```

This will generate a *Service* manifest like:

```yaml
# cka/19/course/19.yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    run: my-static-pod
  name: static-pod-service
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: my-static-pod
  type: NodePort
status:
  loadBalancer: {}
```

Then we check the *Service* and *Endpoints*:

```bash
kubectl get svc,endpointslice -l run=my-static-pod
NAME                         TYPE       CLUSTER-IP      ...   PORT(S)        AGE
service/static-pod-service   NodePort   10.98.249.240   ...   80:32699/TCP   34s

NAME                       ADDRESSTYPE   PORTS   ENDPOINTS   AGE
static-pod-service-2h7cf   IPv4          80      10.32.0.4   34s
```

Also we should be able to access that Nginx container from inside the kind *Node* using the *NodePort*:

```bash
# Access from inside the control-plane container
docker exec -it cka-lab-19-control-plane curl 172.18.0.2:32699
...
```

## Checklist

- [ ] *Static Pod* `my-static-pod` exists on `cka-lab-19-control-plane`
- [ ] *Pod* has single *Container*
- [ ] *Container* has correct image `nginx:1-alpine`
- [ ] *Pod* has correct CPU resource requests
- [ ] *Pod* has correct memory resource requests
- [ ] *Service* `static-pod-service` is of type *NodePort*
- [ ] *Service* selector matches *Pod*

## Answer

**Reference:** <https://kubernetes.io/docs/concepts/services-networking/service/>

### ClusterIP Service

```bash
kubectl run nginx-clusterip --image=nginx --port=80 --expose
```

Verify:

```bash
kubectl get svc nginx-clusterip
# NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# nginx-clusterip   ClusterIP   10.x.x.x        <none>        80/TCP    5s
```

### NodePort Service for a Deployment

```bash
kubectl create deployment nginx-deployment --image=nginx --replicas=3
kubectl expose deployment nginx-deployment \
  --name=nginx-deployment-svc \
  --type=NodePort \
  --port=80 \
  --target-port=80 \
  --dry-run=client -o yaml > lab/nginx-deployment-svc.yaml
```

Edit `lab/nginx-deployment-svc.yaml` to add `nodePort: 30080`:

```yaml
# lab/nginx-deployment-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-deployment-svc
spec:
  type: NodePort
  selector:
    app: nginx-deployment
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

```bash
kubectl apply -f lab/nginx-deployment-svc.yaml
```

Verify:

```bash
kubectl get svc nginx-deployment-svc
# NAME                   TYPE       CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
# nginx-deployment-svc   NodePort   10.x.x.x     <none>        80:30080/TCP   5s
```

## Checklist (Score: 0/5)

- [ ] Pod `nginx-clusterip` is running
- [ ] Service `nginx-clusterip` of type `ClusterIP` exposes port `80`
- [ ] Deployment `nginx-deployment` has 3 running replicas
- [ ] Service `nginx-deployment-svc` of type `NodePort` exposes port `80`
- [ ] `nginx-deployment-svc` uses `nodePort: 30080`

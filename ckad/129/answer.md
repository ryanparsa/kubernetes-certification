## Answer

**Reference:** <https://kubernetes.io/docs/concepts/services-networking/service/>

### Create the Pod

```bash
kubectl run project-plt-6cc-api \
  --image=nginx:1.17.3-alpine \
  --port=3333 \
  -n pluto
```

### Create the ClusterIP Service

```bash
kubectl expose pod project-plt-6cc-api \
  --name=project-plt-6cc-svc \
  --port=3333 \
  --target-port=3333 \
  -n pluto
```

### Test the Service from within the cluster

```bash
# Test via Service name
kubectl run test --image=busybox:1.31.0 -it --rm --restart=Never -n pluto -- \
  wget -O- project-plt-6cc-svc:3333 > /opt/course/10/service_test.html

# Test via ClusterIP
CLUSTER_IP=$(kubectl get svc project-plt-6cc-svc -n pluto -o jsonpath='{.spec.clusterIP}')
kubectl run test2 --image=busybox:1.31.0 -it --rm --restart=Never -n pluto -- \
  wget -O- $CLUSTER_IP:3333 > /opt/course/10/service_test2.html
```

## Checklist (Score: 0/5)

- [ ] Pod `project-plt-6cc-api` running in Namespace `pluto` with image `nginx:1.17.3-alpine`
- [ ] Container named `project-plt-6cc-api` listening on port 3333
- [ ] ClusterIP Service `project-plt-6cc-svc` exposing port 3333
- [ ] `/opt/course/10/service_test.html` contains curl/wget result via Service name
- [ ] `/opt/course/10/service_test2.html` contains curl/wget result via ClusterIP

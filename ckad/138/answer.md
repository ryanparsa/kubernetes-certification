## Answer

**Reference:** <https://kubernetes.io/docs/concepts/services-networking/service/>

### Test the Service

```bash
kubectl run test --image=busybox:1.31.0 -it --rm --restart=Never -n saturn -- \
  wget -O- saturn-2cc-runner:8080
```

### Find which node the Pod is running on

```bash
kubectl get pods -n saturn -o wide
# Note the NODE column

kubectl get pods -n saturn -o jsonpath='{.items[0].spec.nodeName}'
```

### Write node name to file

```bash
kubectl get pods -n saturn -o jsonpath='{.items[0].spec.nodeName}' \
  > /opt/course/19/pod-on-node.txt

cat /opt/course/19/pod-on-node.txt
```

## Checklist (Score: 0/3)

- [ ] Deployment `saturn-2cc-runner` and Service exist in Namespace `saturn`
- [ ] Service responds on port 8080 from within the cluster
- [ ] Node name written to `/opt/course/19/pod-on-node.txt`

## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/pods/>

### Create the Pod

```bash
kubectl run pod1 --image=httpd:2.4.41-alpine --port=80
```

### Expose as NodePort Service

```bash
kubectl expose pod pod1 --name=pod1-svc --type=NodePort --port=80
echo "kubectl expose pod pod1 --name=pod1-svc --type=NodePort --port=80" > /opt/course/2/pod1-svc.sh
```

### Verify

```bash
kubectl get pod pod1
kubectl get svc pod1-svc
```

## Checklist (Score: 0/3)

- [ ] Pod `pod1` running with image `httpd:2.4.41-alpine` and container named `pod1`
- [ ] Service `pod1-svc` of type `NodePort` exposing port 80
- [ ] Command written to `/opt/course/2/pod1-svc.sh`

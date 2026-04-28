## Answer

**Reference:** <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/>

### List Deployments in both Namespaces

```bash
kubectl get deployment -n project-tiger > /opt/course/20/deployments.txt
kubectl get deployment -n project-snake >> /opt/course/20/deployments.txt
cat /opt/course/20/deployments.txt
```

### List Pods with label app=runner across all Namespaces

```bash
kubectl get pods --all-namespaces -l app=runner > /opt/course/20/pods.txt
cat /opt/course/20/pods.txt
```

## Checklist (Score: 0/2)

- [ ] `/opt/course/20/deployments.txt` contains deployment list from both Namespaces
- [ ] `/opt/course/20/pods.txt` contains all Pods with label `app=runner` across all Namespaces

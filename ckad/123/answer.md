## Answer

**Reference:** <https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/>

### List images with crictl

```bash
crictl images > /opt/course/4/images
cat /opt/course/4/images
```

### Remove nginx images

```bash
crictl images | grep nginx
crictl rmi <image-id>
```

### Remove untagged image

```bash
crictl images | grep "<none>"
crictl rmi <image-id>
```

### Verify

```bash
crictl images | grep nginx     # should return nothing
crictl images | grep "<none>"  # should return nothing
```

## Checklist (Score: 0/3)

- [ ] Image list written to `/opt/course/4/images`
- [ ] All `nginx` images removed from the node
- [ ] Untagged (`<none>`) image removed from the node

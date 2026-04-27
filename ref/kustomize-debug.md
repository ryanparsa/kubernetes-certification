# Debugging Tips

```bash
# Build and validate without applying
kubectl kustomize staging

# Common error: patch target not found in base
# → The resource referenced by the patch doesn't exist in resources
# Fix: make sure the resource is in base/ and patch metadata.name matches exactly

# Check what a full build produces for an overlay
kubectl kustomize prod | grep -A 5 "kind: HorizontalPodAutoscaler"

# Validate with dry-run
kubectl kustomize prod | kubectl apply --dry-run=client -f -

# Diff against live cluster
kubectl kustomize prod | kubectl diff -f -
```

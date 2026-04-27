# Image Overrides

Change image names and tags without editing deployment YAML:

```yaml
images:
  - name: my-app              # matches .spec.containers[*].image by name
    newTag: v2.1.0
  - name: nginx
    newName: registry.example.com/nginx
    newTag: 1.25-alpine
```

---


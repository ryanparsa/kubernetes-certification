## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/quick-reference/#output-format

### Create the namespace

```bash
kubectl create namespace custom-columns-demo
```

### Output all pods with custom columns (single image)

```bash
kubectl get pods -A \
  -o custom-columns="POD:.metadata.name,NAMESPACE:.metadata.namespace,IMAGE:.spec.containers[0].image" \
  > /tmp/pod-images.txt

cat /tmp/pod-images.txt
```

### Output all pods with all container images (multi-container aware)

```bash
kubectl get pods -A -o json \
  | jq -r '.items[] | .metadata.name + "," + .metadata.namespace + "," + (.spec.containers | map(.image) | join(","))' \
  > /tmp/all-container-images.txt

cat /tmp/all-container-images.txt
```

Alternatively using jsonpath:

```bash
kubectl get pods -A \
  -o jsonpath="{range .items[*]}{.metadata.name},{.metadata.namespace},{range .spec.containers[*]}{.image}{','}{end}{'\n'}{end}" \
  > /tmp/all-container-images.txt
```

### Verify

```bash
wc -l /tmp/pod-images.txt
wc -l /tmp/all-container-images.txt
```

## Checklist (Score: 0/2)

- [ ] `/tmp/pod-images.txt` exists with correct format (pod name, namespace, primary container image)
- [ ] `/tmp/all-container-images.txt` exists with multi-container details (pod name, namespace, all images comma-separated)

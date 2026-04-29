## Answer

**Reference:** <https://kubernetes.io/docs/reference/kubectl/cheatsheet/>

### 1. Extract all pod names

```bash
kubectl get pods -A -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' > /opt/course/1/pods.txt
```

### 2. Extract all container image names

```bash
kubectl get pods -A -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u > /opt/course/1/containers.txt
```

### 3. Extract current context name

```bash
kubectl config current-context > /opt/course/1/context
```

### 4. Extract and decode user certificate

```bash
kubectl config view --raw -o jsonpath='{.users[?(@.name=="accounts-432")].user.client-certificate-data}' | base64 -d > /opt/course/1/cert
```

## Checklist (Score: 0/4)

- [ ] All pod names from all namespaces are written to `/opt/course/1/pods.txt`
- [ ] All deduplicated container image names from all namespaces are written to `/opt/course/1/containers.txt`
- [ ] Current context name is written to `/opt/course/1/context`
- [ ] Decoded client certificate for user `accounts-432` is written to `/opt/course/1/cert`

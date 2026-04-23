# Question 9 | Contact K8s Api from inside Pod

> **Solve this question on:** the "cka-lab-9" kind cluster

There is a *ServiceAccount* `secret-reader` in *Namespace* `project-swan`. Create a *Pod* of image `nginx:1-alpine` named `api-contact` which uses this *ServiceAccount*.

Exec into the *Pod* and use `curl` to manually query all *Secrets* from the *Kubernetes* *API*.

Write the result into file `cka/9/course/result.json`.

## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/access-api-from-pod

You can find information in the *Kubernetes* documentation by searching for "curl api" for example.

### Create Pod which uses ServiceAccount

First we create the *Pod*:

```bash
kubectl run api-contact --image=nginx:1-alpine --dry-run=client -o yaml > cka/9/course/9.yaml
```

Update the manifest to add the `serviceAccountName` and *Namespace*:

```yaml
# cka/9/course/9.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: api-contact
  name: api-contact
  namespace: project-swan
spec:
  serviceAccountName: secret-reader
  containers:
  - image: nginx:1-alpine
    name: api-contact
```

Apply it:

```bash
kubectl apply -f cka/9/course/9.yaml
```

### Contact K8s Api from inside Pod

Once in the *Container* we can connect to the *Kubernetes* *API* using `curl`, it's usually available via the *Service* named `kubernetes` in *Namespace* `default`. Because of *Kubernetes* internal DNS resolution we can use the url `kubernetes.default`.

Otherwise we can find the *Kubernetes* *API* IP via environment variables inside the *Pod*, simply run `env`.

So we can try to contact the *Kubernetes* *API*:

```bash
kubectl -n project-swan exec api-contact -it -- sh

curl https://kubernetes.default
# This will fail because of an untrusted certificate

curl -k https://kubernetes.default
# This will show 403 Forbidden because we are not passing authorization information
```

### Use ServiceAccount Token to authenticate

We find the token at `/var/run/secrets/kubernetes.io/serviceaccount/token`.

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
```

Now we're able to list all *Secrets* as the *Pod*'s *ServiceAccount* `secret-reader`.

For troubleshooting we could also check if the *ServiceAccount* is actually able to list *Secrets*:

```bash
kubectl auth can-i list secrets --as system:serviceaccount:project-swan:secret-reader
```

### Store result at requested location

We write the full result into `cka/9/course/result.json`:

```bash
# Inside the pod
curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}" > result.json

# Exit the pod
exit

# Copy the file to the host
kubectl -n project-swan exec api-contact -- cat result.json > cka/9/course/result.json
```

### Connect via HTTPS with correct CA

To connect without `curl -k` we can specify the *CertificateAuthority* (CA):

```bash
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

curl --cacert ${CACERT} https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
```

## Checklist (Score: 0/4)

- [ ] *Pod* `api-contact` exists in *Namespace* `project-swan`
- [ ] *Pod* uses *ServiceAccount* `secret-reader`
- [ ] *Pod* is Running
- [ ] `course/result.json` exists and contains a `SecretList`

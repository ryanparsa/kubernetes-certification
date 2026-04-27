## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/access-api-from-pod

You can find information in the K8s Docs by searching for "curl api" for example.

### Create Pod which uses ServiceAccount

First we create the *Pod*:

```bash
kubectl run api-contact --image=nginx:1-alpine --dry-run=client -o yaml > 9.yaml

vim 9.yaml
```

Add the serviceAccountName and *Namespace*:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: api-contact
  name: api-contact
  namespace: project-swan             # add
spec:
  serviceAccountName: secret-reader   # add
  containers:
  - image: nginx:1-alpine
    name: api-contact
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Create it:

```bash
kubectl -f 9.yaml apply
pod/api-contact created
```

### Contact K8s Api from inside Pod

Once in the container we can connect to the K8s Api using `curl`, it's usually available via the *Service* named `kubernetes` in *Namespace* `default`. Because of K8s internal DNS resolution we can use the url `kubernetes.default`.

> ℹ️ Otherwise we can find the K8s Api IP via environment variables inside the *Pod*, simply run `env`

So we can try to contact the K8s Api:

```bash
kubectl -n project-swan exec api-contact -it -- sh

curl https://kubernetes.default
curl: (60) SSL peer certificate or SSH remote key was not OK
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the webpage mentioned above.

curl -k https://kubernetes.default
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}

curl -k https://kubernetes.default/api/v1/secrets
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "secrets is forbidden: User \"system:anonymous\" cannot list resource \"secrets\" in API group \"\" at the cluster scope",
  "reason": "Forbidden",
  "details": {
    "kind": "secrets"
  },
  "code": 403
}
```

The first command fails because of an untrusted certificate, but we can ignore this with `-k` for this scenario. We explain at the end how we can add the correct certificate instead of having to use the insecure `-k` option.

The last command shows 403 forbidden, this is because we are not passing any authorisation information. For the K8s Api we are connecting as `system:anonymous`, which should not have permission to perform the query. We want to change this and connect using the Pod's ServiceAccount named `secret-reader`.

### Use ServiceAccount Token to authenticate

We find the token at `/var/run/secrets/kubernetes.io/serviceaccount`, so we do:

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
{
  "kind": "SecretList",
  "apiVersion": "v1",
  "metadata": {
    "resourceVersion": "4881"
  },
  "items": [
    {
...
    {
      "metadata": {
        "name": "read-me",
        "namespace": "project-swan",
...
```

Now we're able to list all Secrets as the Pod's ServiceAccount `secret-reader`.

For troubleshooting we could also check if the ServiceAccount is actually able to list Secrets:

```bash
kubectl auth can-i get secret --as system:serviceaccount:project-swan:secret-reader
yes
```

### Store result at requested location

We write the full result into `lab/result.json`:

```
{
  "kind": "SecretList",
  "apiVersion": "v1",
  "metadata": {
    "resourceVersion": "4881"
  },
  "items": [
    {
...
    {
      "metadata": {
        "name": "read-me",
        "namespace": "project-swan",
        ...
      },
      "data": {
        "token": "ZjMyMDEzOTYtZjVkOC00NTg0LWE2ZjEtNmYyZGZkYjM4NzVl"
      },
      "type": "Opaque"
    }
  ]
}
...
```

The easiest way would probably be to copy and paste the result manually. But if it's too long or not possible we could also do:

```bash
curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}" > result.json

exit

kubectl -n project-swan exec api-contact -it -- cat result.json > lab/result.json
```

### Connect via HTTPS with correct CA

To connect without `curl -k` we can specify the CertificateAuthority (CA):

```bash
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

curl --cacert ${CACERT} https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
```

## Killer.sh Checklist (Score: 0/4)

- [ ] Pod `api-contact` exists in Namespace `project-swan`
- [ ] Pod uses ServiceAccount `secret-reader`
- [ ] Pod is Running
- [ ] `lab/result.json` exists and contains a `SecretList`
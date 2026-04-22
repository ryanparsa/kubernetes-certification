# Question 9 | Contact K8s Api from inside Pod

> **Solve this question on:** `ssh cka9412`

There is *ServiceAccount* `secret-reader` in *Namespace* `project-swan`. Create a *Pod* of image `nginx:1-alpine` named `api-contact` which uses this *ServiceAccount*.

Exec into the *Pod* and use `curl` to manually query all *Secrets* from the Kubernetes Api.

Write the result into file `/opt/course/9/result.json`.

## Answer

**Reference:** https://kubernetes.io/docs/tasks/run-application/access-api-from-pod

You can find information in the K8s Docs by searching for "curl api" for example.

### Create Pod which uses ServiceAccount

First we create the *Pod*:

```bash
➜ ssh cka9412

➜ candidate@cka9412:~$ k run api-contact --image=nginx:1-alpine --dry-run=client -o yaml > 9.yaml

➜ candidate@cka9412:~$ vim 9.yaml
```

Add the serviceAccountName and *Namespace*:

```yaml
# cka9412:/home/candidate/9.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: api-contact
  name: api-contact
  namespace: project-swan         # add
spec:
  serviceAccountName: secret-reader # add
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
➜ candidate@cka9412:~$ k -f 9.yaml apply
pod/api-contact created
```

### Contact K8s Api from inside Pod

Once in the container we can connect to the K8s Api using `curl`, it's usually available via the *Service* named `kubernetes` in *Namespace* `default`. Because of K8s internal DNS resolution we can use the url `kubernetes.default`.

> ℹ️ Otherwise we can find the K8s Api IP via environment variables inside the *Pod*, simply run `env`

So we can try to contact the K8s Api:

```bash
➜ candidate@cka9412:~$ k -n project-swan exec api-contact -it -- sh

➜ / # curl https://kubernetes.default
curl: (60) SSL peer certificate or SSH remote key was not OK
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the webpage mentioned above.

➜ / # curl -k https://kubernetes.default
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

➜ / # curl -k https://kubernetes.default/api/v1/secrets
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

We see that we need to authenticate. For this we can use the Service Account token mounted into every Pod by default at `/var/run/secrets/kubernetes.io/serviceaccount`. Let's check what's available:

```bash
➜ / # find /var/run/secrets/kubernetes.io/serviceaccount
/var/run/secrets/kubernetes.io/serviceaccount
/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
/var/run/secrets/kubernetes.io/serviceaccount/namespace
/var/run/secrets/kubernetes.io/serviceaccount/token

➜ / # cat /var/run/secrets/kubernetes.io/serviceaccount/token
# returns service account token

➜ / # cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
# returns the ca certificate

➜ / # cat /var/run/secrets/kubernetes.io/serviceaccount/namespace
# returns project-swan
```

Let's store the token in an environment variable and use it to authenticate our request:

```bash
➜ / # TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

➜ / # curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
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
        "uid": "e2e45842-688b-5057-af4e-6431f04cc0d6",
        "resourceVersion": "4881",
        "creationTimestamp": "2024-12-28T13:11:21Z"
      },
      "data": {
        "secret": "SGFsdCBjb21iaW5lZCB3aXRoIGFuIGVuZXJneS4uLg=="
      },
      "type": "Opaque"
    }
  ]
}
```

Great! We can access the secrets. Now let's save this result to the requested location. We need to save the result both inside the pod and then copy it to the host:

```bash
➜ / # curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}" > result.json

➜ / # exit

➜ candidate@cka9412:~$ k -n project-swan exec api-contact -it -- cat result.json > /opt/course/9/result.json
```

### Connect via HTTPS with correct CA

To connect without `curl -k` we can specify the CertificateAuthority (CA):

```bash
➜ / # CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

➜ / # curl --cacert ${CACERT} https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"
```

This approach uses the proper CA certificate instead of ignoring SSL verification with `-k`.
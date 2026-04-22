# Question 1 | Contexts

You're asked to extract the following information out of kubeconfig file `cka/1/course/kubeconfig`:

1. Write all kubeconfig context names into `cka/1/course/contexts`, one per line
2. Write the name of the current context into `cka/1/course/current-context`
3. Write the client-certificate of user `account-0027` base64-decoded into `cka/1/course/cert`

## Answer

All that's asked for here could be extracted by manually reading the kubeconfig file. But we're going to use kubectl for it.

### Step 1

First we get all context names:

```bash
kubectl --kubeconfig cka/1/course/kubeconfig config get-contexts
CURRENT   NAME            CLUSTER     AUTHINFO               NAMESPACE
          cluster-admin   kubernetes  admin@internal         
          cluster-w100    kubernetes  account-0027@internal  
*         cluster-w200    kubernetes  account-0028@internal  

kubectl --kubeconfig cka/1/course/kubeconfig config get-contexts -oname
cluster-admin
cluster-w100
cluster-w200

kubectl --kubeconfig cka/1/course/kubeconfig config get-contexts -oname > cka/1/course/contexts
```

This will result in:

```
# cka/1/course/contexts
cluster-admin
cluster-w100
cluster-w200
```

We could also do extractions using jsonpath:

```bash
kubectl --kubeconfig cka/1/course/kubeconfig config view -o yaml

kubectl --kubeconfig cka/1/course/kubeconfig config view -o jsonpath="{.contexts[*].name}"
```

But it would probably be overkill for this task.

### Step 2

Now we query the current context:

```bash
kubectl --kubeconfig cka/1/course/kubeconfig config current-context
cluster-w200

kubectl --kubeconfig cka/1/course/kubeconfig config current-context > cka/1/course/current-context
```

Which will result in:

```
# cka/1/course/current-context
cluster-w200
```

### Step 3

And finally we extract the certificate and write it base64 decoded into the required location:

```bash
kubectl --kubeconfig cka/1/course/kubeconfig config view -o yaml --raw
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tC...
    server: https://10.30.110.30:6443
  name: cluster1
contexts:
- context:
    cluster: kubernetes
    user: admin@internal
  name: cluster-admin
- context:
    cluster: kubernetes
    user: account-0027@internal
  name: cluster-w100
- context:
    cluster: kubernetes
    user: account-0028@internal
  name: cluster-w200
current-context: cluster-w200
kind: Config
preferences: {}
users:
- name: account-0027@internal
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN2RENDQWFRQ0ZIWWRqU1pGS0N5VUNSMUIybmFYQ2cvVWpTSExNQTBHQ1NxR1NJYjNEUUVCQ3dVQU1CVXgK...
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVk...
...
```

Instead of using `--raw` to see the sensitive certificate information, we could also simply open the kubeconfig file in an editor. No matter how, we copy the whole value of `client-certificate-data` and base64 decode it:

```bash
echo LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN2RE... | base64 -d > cka/1/course/cert
```

Or if we like it automated:

```bash
kubectl --kubeconfig cka/1/course/kubeconfig config view --raw -ojsonpath="{.users[?(@.name=='account-0027@internal')].user.client-certificate-data}" | base64 -d > cka/1/course/cert
```

Which will result in:

```
# cka/1/course/cert
-----BEGIN CERTIFICATE-----
MIICvDCCAaQCFHYdjSZFKCyUCR1B2naXCg/UjSHLMA0GCSqGSIb3DQEBCwUAMBUx
EzARBgNVBAMTCmt1YmVybmV0ZXMwHhcNMjQxMDI4MTkwOTUwWhcNMjYwMzEyMTkw
OTUwWjAgMR4wHAYDVQQDDBVhY2NvdW50LTAwMjdAaW50ZXJuYWwwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQDpUsQDDEW+48AvZmKbKS2wmsZa0gy+kzii
cZDpZg8mgO+50jNnHQ4ICqAjG3fFHmPnbuj0sZGXf+ym0J2dVL9jwGSt5NVoLrjj
TwlBG63+k4jRBxLBv6479iPXXk0giP38TAoS//dtJ+O8isbRMnlb9aI5L2JYxHfN
VL2qrF9arLf1DN+h0havFxn9noJ/iZx/qb/FHgeZqnTf7zR6OouRuWHG523jnTqA
06K+g4k2o6hg3u7JM/cNbHFM7S2qSBDkS266JJtvMtC+cpsmg/eUnDhA21tTa4vg
lbpw6vxnJcwMt4n0KaAeS0j4L3OC869alpy1jvI3ATjFjuckLESLAgMBAAEwDQYJ
KoZIhvcNAQELBQADggEBADQQLGYZoUSrbpgFV69sHvMuoxn2YUt1B5FBmQrxwOli
dem936q2ZLMr34rQ5rC1uTQDraWXa44yHmVZ07tdINkV2voIexHjX91gVC+LirQq
IKGxiok9CKLE7NReF63pp/7BNe7/P6cORh0O2EDM4TgHXLpXrt7tdPEXwvrN1tMQ
z5av9Po5Td4Vf0paODtlahwhIZ6K7ctgVGT1KdQln1qXDb/Vwq3VyYBAJKlmOu9l
bj3nmvc7D99e9p4y4GFCkAlbxv9TD0T4yvYgVFtRTVbGAkmazwUHrfcQnRTVfKoz
SfsYRy6L1RKxjwh74KnhKJz+09JqXpr7MVdQgjh0Rdw=
-----END CERTIFICATE-----
```

Task completed.

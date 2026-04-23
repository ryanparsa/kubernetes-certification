# Question 11 | Create Secret and mount into Pod

> **Solve this question on:** the "cka-lab-28" kind cluster

Create *Namespace* `secret` and implement the following in it:

- Create *Pod* `secret-pod` with image `busybox:1`. It should be kept running by executing `sleep 1d` or something similar
- Create the existing *Secret* `cka/28/course/secret1.yaml` and mount it readonly into the *Pod* at `/tmp/secret1`
- Create a new *Secret* called `secret2` which should contain `user=user1` and `pass=1234`. These entries should be available inside the *Pod*'s container as environment variables `APP_USER` and `APP_PASS`

## Answer

First we create the *Namespace*:

```bash
kubectl create ns secret
```

### Secret 1

To create the existing *Secret* we need to adjust the *Namespace* for it:

```bash
cp cka/28/course/secret1.yaml cka/28/course/11_secret1.yaml
```

Update the `namespace` field in `cka/28/course/11_secret1.yaml`:

```yaml
# cka/28/course/11_secret1.yaml
apiVersion: v1
data:
  halt: IyEgL2Jpbi9zaAo...
kind: Secret
metadata:
  name: secret1
  namespace: secret
```

```bash
kubectl create -f cka/28/course/11_secret1.yaml
```

### Secret 2

Next we create the second *Secret*:

```bash
kubectl -n secret create secret generic secret2 --from-literal=user=user1 --from-literal=pass=1234
```

### Pod

Now we create the *Pod* template:

```bash
kubectl -n secret run secret-pod --image=busybox:1 --dry-run=client -o yaml -- sh -c "sleep 1d" > cka/28/course/11.yaml
```

Then make the necessary changes:

```yaml
# cka/28/course/11.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: secret-pod
  name: secret-pod
  namespace: secret
spec:
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox:1
    name: secret-pod
    env:
    - name: APP_USER
      valueFrom:
        secretKeyRef:
          name: secret2
          key: user
    - name: APP_PASS
      valueFrom:
        secretKeyRef:
          name: secret2
          key: pass
    volumeMounts:
    - name: secret1
      mountPath: /tmp/secret1
      readOnly: true
  volumes:
  - name: secret1
    secret:
      secretName: secret1
```

And execute:

```bash
kubectl create -f cka/28/course/11.yaml
```

### Verify

```bash
kubectl -n secret exec secret-pod -- env | grep APP
# APP_PASS=1234
# APP_USER=user1

kubectl -n secret exec secret-pod -- find /tmp/secret1
# /tmp/secret1
# /tmp/secret1/..data
# /tmp/secret1/halt
# ...

kubectl -n secret exec secret-pod -- cat /tmp/secret1/halt
```


## Checklist (Score: 0/7)

- [ ] *Secret* `secret1` exists
- [ ] *Secret* `secret2` exists
- [ ] *Pod* `secret-pod` exists
- [ ] *Pod* has single container
- [ ] *Pod* container has correct image `busybox:1`
- [ ] *Pod* mounts `secret1` readonly at `/tmp/secret1`
- [ ] *Pod* has `secret2` values as environment variables `APP_USER` and `APP_PASS`

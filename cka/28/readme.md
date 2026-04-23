# Question 11 | Create Secret and mount into Pod

> **Solve this question on:** the "cka-lab" kind cluster

Create *Namespace* `secret` and implement the following in it:

- Create *Pod* `secret-pod` with image `busybox:1`. It should be kept running by executing `sleep 1d` or something similar
- Create the existing *Secret* `cka/28/course/secret1.yaml` and mount it readonly into the *Pod* at `/tmp/secret1`
- Create a new *Secret* called `secret2` which should contain `user=user1` and `pass=1234`. These entries should be available inside the *Pod*'s container as environment variables `APP_USER` and `APP_PASS`

## Answer

First we create the *Namespace*:

```bash
kubectl create ns secret
namespace/secret created
```

### Secret 1

To create the existing *Secret* we need to adjust the *Namespace* for it:

```bash
cp cka/28/course/secret1.yaml 11_secret1.yaml
```

```yaml
# 11_secret1.yaml
apiVersion: v1
data:
  halt: IyEgL2Jpbi9zaAo...
kind: Secret
metadata:
  creationTimestamp: null
  name: secret1
  namespace: secret           # UPDATE
```

```bash
kubectl -n secret create -f 11_secret1.yaml
secret/secret1 created
```

### Secret 2

Next we create the second *Secret*:

```bash
kubectl -n secret create secret generic secret2 --from-literal=user=user1 --from-literal=pass=1234
secret/secret2 created
```

### Pod

Now we create the *Pod* template:

```bash
kubectl -n secret run secret-pod --image=busybox:1 --dry-run=client -o yaml -- sh -c "sleep 1d" > 11.yaml
```

Then make the necessary changes:

```yaml
# 11.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-pod
  name: secret-pod
  namespace: secret                       # important if not automatically added
spec:
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox:1
    name: secret-pod
    resources: {}
    env:                                  # add
    - name: APP_USER                      # add
      valueFrom:                          # add
        secretKeyRef:                     # add
          name: secret2                   # add
          key: user                       # add
    - name: APP_PASS                      # add
      valueFrom:                          # add
        secretKeyRef:                     # add
          name: secret2                   # add
          key: pass                       # add
    volumeMounts:                         # add
    - name: secret1                       # add
      mountPath: /tmp/secret1             # add
      readOnly: true                      # add
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:                                # add
  - name: secret1                         # add
    secret:                               # add
      secretName: secret1                 # add
status: {}
```

And execute:

```bash
kubectl -n secret create -f 11.yaml
pod/secret-pod created
```

Finally we verify:

```bash
kubectl -n secret exec secret-pod -- env | grep APP
APP_PASS=1234
APP_USER=user1

kubectl -n secret exec secret-pod -- find /tmp/secret1
/tmp/secret1
/tmp/secret1/..data
/tmp/secret1/halt
/tmp/secret1/..2019_12_08_12_15_39.463036797
/tmp/secret1/..2019_12_08_12_15_39.463036797/halt

kubectl -n secret exec secret-pod -- cat /tmp/secret1/halt
#! /bin/sh
### BEGIN INIT INFO
# Provides:          halt
# Required-Start:
# Required-Stop:
# Default-Start:
# Default-Stop:      0
# Short-Description: Execute the halt command.
# Description:
...
```


## Killer.sh Checklist (Score: 0/7)

- [ ] Secret secret1 exists
- [ ] Secret secret2 exists
- [ ] Pod exists
- [ ] Pod has single container
- [ ] Pod container has correct image
- [ ] Pod mounts secret1 readonly
- [ ] Pod has secret2 env variables

# Question 33 | Update CoreDNS Configuration

> **Solve this question on:** the "cka-lab-33" kind cluster

The CoreDNS configuration in the cluster needs to be updated:

1. Make a backup of the existing configuration YAML and store it at `cka/33/course/coredns_backup.yaml`. You should be able to fast recover from the backup.
2. Update the CoreDNS configuration in the cluster so that DNS resolution for `SERVICE.NAMESPACE.custom-domain` will work exactly like and in addition to `SERVICE.NAMESPACE.cluster.local`.

Test your configuration for example from a *Pod* with `busybox:1` image. These commands should result in an IP address:

```
nslookup kubernetes.default.svc.cluster.local
nslookup kubernetes.default.svc.custom-domain
```

## Answer

We have a look at the CoreDNS *Pods*:

```bash
kubectl -n kube-system get deploy,pod
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/coredns          2/2     2            2           42h
...

NAME                                  READY   STATUS    RESTARTS      AGE
pod/coredns-74f75f8b69-c4z47          1/1     Running   0             42h
pod/coredns-74f75f8b69-wsnfr          1/1     Running   0             42h
...
```

It looks like CoreDNS is running as a *Deployment* with two replicas.

### Step 1

CoreDNS uses a *ConfigMap* by default when installed via Kubeadm. Creating a backup is always a good idea before performing sensitive changes:

```bash
kubectl -n kube-system get cm
NAME                                                   DATA   AGE
coredns                                                1      42h
...

kubectl -n kube-system get cm coredns -oyaml > cka/33/course/coredns_backup.yaml
```

The current configuration looks like this:

```yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30 {
           disable success cluster.local
           disable denial cluster.local
        }
        loop
        reload
        loadbalance
    }
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
...
```

### Step 2

We update the config:

```bash
kubectl -n kube-system edit cm coredns
```

```yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes custom-domain cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30 {
           disable success cluster.local
           disable denial cluster.local
        }
        loop
        reload
        loadbalance
    }
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
...
```

Note that we added `custom-domain` in the same line where `cluster.local` is already defined.

Now we need to restart the *Deployment*:

```bash
kubectl -n kube-system rollout restart deploy coredns
deployment.apps/coredns restarted

kubectl -n kube-system get pod
NAME                              READY   STATUS    RESTARTS      AGE
coredns-77d6976b98-jkvqn          1/1     Running   0             13s
coredns-77d6976b98-zdxw8          1/1     Running   0             13s
...
```

We should see both *Pods* restarted and running without errors, this is only the case if there are no syntax errors in the CoreDNS config.

To test the updated configuration we create a *Pod*, image `busybox:1` contains `nslookup` already:

```bash
kubectl run bb --image=busybox:1 -- sh -c 'sleep 1d'

kubectl exec -it bb -- sh

nslookup kubernetes.default.svc.custom-domain
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.custom-domain
Address: 10.96.0.1

nslookup kubernetes.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1
```

We see that now `kubernetes.default.svc.custom-domain` and `kubernetes.default.svc.cluster.local` resolve to IP address `10.96.0.1`. Which is the Kubernetes *Service* in the *default* *Namespace*:

```bash
kubectl -n default get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   43h
```

### Recover from backup

If we messed something up we could do:

```bash
kubectl -n kube-system delete cm coredns
kubectl -n kube-system apply -f cka/33/course/coredns_backup.yaml
kubectl -n kube-system rollout restart deploy coredns
```

## Checklist (Score: 0/2)

- [ ] Backup file `cka/33/course/coredns_backup.yaml` exists
- [ ] CoreDNS configuration updated with `custom-domain`

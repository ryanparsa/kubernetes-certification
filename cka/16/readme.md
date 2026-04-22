# Question 16 | Update CoreDNS Configuration

> **Solve this question on:** `ssh cka5774`

The CoreDNS configuration in the cluster needs to be updated:

1. Make a backup of the existing configuration Yaml and store it at `/opt/course/16/coredns_backup.yaml`. You should be able to fast recover from the backup
2. Update the CoreDNS configuration in the cluster so that DNS resolution for `SERVICE.NAMESPACE.custom-domain` will work exactly like and in addition to `SERVICE.NAMESPACE.cluster.local`

Test your configuration for example from a Pod with `busybox:1` image. These commands should result in an IP address:

```
nslookup kubernetes.default.svc.cluster.local
nslookup kubernetes.default.svc.custom-domain
```

## Answer

We have a look at the CoreDNS Pods:

```bash
➜ ssh cka5774

➜ candidate@cka5774:~$ k -n kube-system get deploy,pod
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/coredns          2/2     2            2           42h
...

NAME                                  READY   STATUS    RESTARTS      AGE
pod/coredns-74f75f8b69-c4z47          1/1     Running   0             42h
pod/coredns-74f75f8b69-wsnfr          1/1     Running   0             42h
...
```

It looks like CoreDNS is running as a Deployment with two replicas.

### Step 1

CoreDNS uses a ConfigMap by default when installed via Kubeadm. Creating a backup is always a good idea before performing sensitive changes:

```bash
➜ candidate@cka5774:~$ k -n kube-system get cm
NAME                                                   DATA   AGE
coredns                                                1      42h
...

➜ candidate@cka5774:~$ k -n kube-system get cm coredns -oyaml > /opt/course/16/coredns_backup.yaml
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
➜ candidate@cka5774:~$ k -n kube-system edit cm coredns
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
  creationTimestamp: "2024-12-26T20:35:11Z"
  name: coredns
  namespace: kube-system
  resourceVersion: "262"
  uid: c76d208f-1bc8-4c0f-a8e8-a8bfa440870e
```

Note that we added `custom-domain` in the same line where `cluster.local` is already defined.

Now we need to restart the Deployment:

```bash
➜ candidate@cka5774:~$ k -n kube-system rollout restart deploy coredns
deployment.apps/coredns restarted

➜ candidate@cka5774:~$ k -n kube-system get pod
NAME                              READY   STATUS    RESTARTS      AGE
coredns-77d6976b98-jkvqn          1/1     Running   0             13s
coredns-77d6976b98-zdxw8          1/1     Running   0             13s
...
```

We should see both Pods restarted and running without errors, this is only the case if there are no syntax errors in the CoreDNS config.

To test the updated configuration we create a Pod, image `busybox:1` contains `nslookup` already:

```bash
➜ candidate@cka5774:~$ k run bb --image=busybox:1 -- sh -c 'sleep 1d'

➜ candidate@cka5774:~$ k exec -it bb -- sh

➜ / # nslookup kubernetes.default.svc.custom-domain
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.custom-domain
Address: 10.96.0.1

➜ / # nslookup kubernetes.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1
```

We see that now `kubernetes.default.svc.custom-domain` and `kubernetes.default.svc.cluster.local` resolve to IP address `10.96.0.1`. Which is the Kubernetes Service in the default Namespace:

```bash
➜ candidate@cka5774:~$ k -n default get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   43h
```

This Service is often used from Pods that need to communicate with the K8s Api, like operators.

### Recover from backup

If we messed something up we could do:

```bash
➜ candidate@cka5774:~$ k diff -f /opt/course/16/coredns_backup.yaml 
diff -u -N /tmp/LIVE-591628213/v1.ConfigMap.kube-system.coredns /tmp/MERGED-4230802928/v1.ConfigMap.kube-system.coredns
--- /tmp/LIVE-591628213/v1.ConfigMap.kube-system.coredns        2024-12-28 16:14:03.158949709 +0000
+++ /tmp/MERGED-4230802928/v1.ConfigMap.kube-system.coredns     2024-12-28 16:14:03.159949781 +0000
@@ -7,7 +7,7 @@
            lameduck 5s
         }
         ready
-        kubernetes custom-domain cluster.local in-addr.arpa ip6.arpa {
+        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
            ttl 30
            
➜ candidate@cka5774:~$ k delete -f /opt/course/16/coredns_backup.yaml 
configmap "coredns" deleted

➜ candidate@cka5774:~$ k apply -f /opt/course/16/coredns_backup.yaml 
configmap/coredns created

➜ candidate@cka5774:~$ k -n kube-system rollout restart deploy coredns
deployment.apps/coredns restarted

➜ candidate@cka5774:~$ k -n kube-system get pod
NAME                              READY   STATUS    RESTARTS      AGE
coredns-79f94f8fc8-h8z7t          1/1     Running   0             11s
coredns-79f94f8fc8-tj7hg          1/1     Running   0             10s
...
```

But this only works if a backup is available!

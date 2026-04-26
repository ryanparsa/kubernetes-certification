# Question 4

> **Solve this question on:** the "cka-lab-21" kind cluster

Do the following in *Namespace* `default`:

1. Create a *Pod* named `ready-if-service-ready` of image `nginx:1-alpine`
2. Configure a *LivenessProbe* which simply executes command `true`
3. Configure a *ReadinessProbe* which does check if the url `http://service-am-i-ready:80` is reachable, you can use `wget -T2 -O- http://service-am-i-ready:80` for this
4. Start the *Pod* and confirm it isn't ready because of the *ReadinessProbe*.

Then:

1. Create a second *Pod* named `am-i-ready` of image `nginx:1-alpine` with label `id: cross-server-ready`
2. The already existing *Service* `service-am-i-ready` should now have that second *Pod* as *Endpoint*
3. Now the first *Pod* should be in ready state, check that

## Answer

It's a bit of an anti-pattern for one *Pod* to check another *Pod* for being ready using probes, hence the normally available `readinessProbe.httpGet` doesn't work for absolute remote urls. Still the workaround requested in this task should show how probes and *Pod*<->*Service* communication works.

First we create the first *Pod*:

```bash
kubectl run ready-if-service-ready --image=nginx:1-alpine --dry-run=client -o yaml > cka/21/course/4_pod1.yaml
```

Next perform the necessary additions manually:

```yaml
# cka/21/course/4_pod1.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: ready-if-service-ready
  name: ready-if-service-ready
spec:
  containers:
  - image: nginx:1-alpine
    name: ready-if-service-ready
    resources: {}
    livenessProbe:                                      # add from here
      exec:
        command:
        - 'true'
    readinessProbe:
      exec:
        command:
        - sh
        - -c
        - 'wget -T2 -O- http://service-am-i-ready:80'   # to here
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Then create the *Pod* and confirm it's in a non-ready state:

```bash
kubectl create -f cka/21/course/4_pod1.yaml
pod/ready-if-service-ready created

kubectl get pod ready-if-service-ready
NAME                     READY   STATUS    RESTARTS   AGE
ready-if-service-ready   0/1     Running   0          8s
```

We can also check the reason for this using `describe`:

```bash
kubectl describe pod ready-if-service-ready
...
  Warning  Unhealthy  7s (x4 over 23s)  kubelet            Readiness probe failed: command timed out: "sh -c wget -T2 -O- http://service-am-i-ready:80" timed out after 1s
```

Now we create the second *Pod*:

```bash
kubectl run am-i-ready --image=nginx:1-alpine --labels="id=cross-server-ready"
pod/am-i-ready created
```

The already existing *Service* `service-am-i-ready` should now have an *Endpoint*:

```bash
kubectl describe svc service-am-i-ready
Name:                     service-am-i-ready
Namespace:                default
Labels:                   id=cross-server-ready
Annotations:              <none>
Selector:                 id=cross-server-ready
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.108.19.XXX
IPs:                      10.108.19.XXX
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
Endpoints:                10.44.0.XXX:80
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>

kubectl get endpointslice
NAME                       ADDRESSTYPE   PORTS   ENDPOINTS    AGE
service-am-i-ready-XXXXX   IPv4          80      10.44.0.XXX  6d19h
```

Which will result in our first *Pod* being ready, just give it a minute for the *Readiness* probe to check again:

```bash
kubectl get pod ready-if-service-ready
NAME                     READY   STATUS    RESTARTS   AGE
ready-if-service-ready   1/1     Running   0          2m10s
```

Look at these Pods working together!


## Checklist (Score: 11/11)

- [ ] Pod1 is running
- [ ] Pod1 has single container
- [ ] Pod1 container is Ready
- [ ] Pod1 container has correct image
- [ ] Pod1 container has LivenessProbe
- [ ] Pod1 container has ReadinessProbe
- [ ] Pod2 is running
- [ ] Pod2 has correct label
- [ ] Pod2 has single container
- [ ] Pod2 container is Ready
- [ ] Pod2 container has correct image

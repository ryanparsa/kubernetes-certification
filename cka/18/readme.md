# Question 1 | DNS / FQDN / Headless Service

Solve this question on: `ssh cka6016`

The *Deployment* `controller` in *Namespace* `lima-control` communicates with various cluster internal endpoints by using their DNS FQDN values.

Update the *ConfigMap* used by the *Deployment* with the correct FQDN values for:

1. `DNS_1`: *Service* `kubernetes` in *Namespace* `default`
2. `DNS_2`: Headless *Service* `department` in *Namespace* `lima-workload`
3. `DNS_3`: *Pod* `section100` in *Namespace* `lima-workload`. It should work even if the *Pod* IP changes
4. `DNS_4`: A *Pod* with IP `1.2.3.4` in *Namespace* `kube-system`

Ensure the *Deployment* works with the updated values.

> [!NOTE]
> ℹ️ You can use `nslookup` or `dig` inside a *Pod* of the `controller` *Deployment*

## Answer:

For this question we need to understand how cluster internal DNS works in Kubernetes. The most common use is `SERVICE.NAMESPACE.svc.cluster.local` which will resolve to the IP address of the Kubernetes *Service*. Note that we're asked to specify the FQDNs here so short values like `SERVICE.NAMESPACE` are not possible even if they would work.

Let's exec into the *Pod* for testing:

```bash
➜ ssh cka6016

➜ candidate@cka6016:~$ k -n lima-control get pod
NAME                        READY   STATUS    RESTARTS   AGE
controller-586d6657-gdmch   1/1     Running   0          11m
controller-586d6657-lvdtd   1/1     Running   0          11m

➜ candidate@cka6016:~$ k -n lima-control exec -it controller-586d6657-gdmch -- sh

➜ / # nslookup google.com
Server:         10.96.0.10
Address:        10.96.0.10:53

Non-authoritative answer:
Name:   google.com
Address: 142.250.185.238

Non-authoritative answer:
Name:   google.com
Address: 2a00:1450:4001:82f::200e

➜ / # nslookup non-exist.some.google.com
Server:         10.96.0.10
Address:        10.96.0.10:53

** server can't find non-exist.some.google.com: NXDOMAIN

** server can't find non-exist.some.google.com: NXDOMAIN
```

We can perform DNS queries using `nslookup` and see if they resolve into an IP address.

### Step 1

By default there is the `kubernetes` *Service* in `default` *Namespace* which can be used to access the K8s Api:

```bash
➜ / # nslookup kubernetes.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1
```

And we already have the value for `DNS_1` which is `kubernetes.default.svc.cluster.local`, that was the easy one.

### Step 2

The next one is similar:

```bash
➜ / # nslookup department.lima-workload.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   department.lima-workload.svc.cluster.local
Address: 10.32.0.2
Name:   department.lima-workload.svc.cluster.local
Address: 10.32.0.9
```

The value for `DNS_2` is `department.lima-workload.svc.cluster.local`. It is the same structure as before but what's interesting here is that we get two IP addresses. These are the IP addresses of the *Pods* behind that *Service*.

This is the case because the *Service* is headless and doesn't have its own IP address, but it still has *Endpoints* and points properly to *Pods*:

```bash
➜ candidate@cka6016:~$ k -n lima-workload get svc
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
department   ClusterIP   None           <none>        80/TCP    2m19s
section      ClusterIP   10.99.121.17   <none>        80/TCP    2m18s

➜ candidate@cka6016:~$ k -n lima-workload get endpointslice
NAME               ADDRESSTYPE   PORTS   ENDPOINTS                   AGE
department-wqvvq   IPv4          80      10.32.0.2:80,10.32.0.9:80   2m19s
section-dtt9s      IPv4          80      10.32.0.10:80,10.32.0.3:80  2m19s
```

This means the decision which *Pod* IP to contact is now in the hands of the application which performed the DNS query of the headless *Service*.

### Step 3

Now things start to get spicy, because we can do this:

```bash
➜ / # nslookup section100.section.lima-workload.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   section100.section.lima-workload.svc.cluster.local
Address: 10.32.0.10

➜ / # nslookup section200.section.lima-workload.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   section200.section.lima-workload.svc.cluster.local
Address: 10.32.0.3
```

Hence the value for `DNS_3` is `section100.section.lima-workload.svc.cluster.local`.

But this is **only possible** because the *Pods* behind the *Service* specify hostname and subdomain like this:

```yaml
# kubectl -n lima-workload edit pod section100
apiVersion: v1
kind: Pod
metadata:
  name: section100
  namespace: lima-workload
  labels:
    name: section
spec:
  hostname: section100  # set hostname
  subdomain: section    # set subdomain to same name as service
  containers:
    - image: httpd:2-alpine
      name: pod
...
```

### Step 4

It's possible to resolve a FQDN like `IP.NAMESPACE.pod.cluster.local` into an IP address:

```bash
➜ / # nslookup 1-2-3-4.kube-system.pod.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   1-2-3-4.kube-system.pod.cluster.local
Address: 1.2.3.4
```

This is possible even without a *Pod* having to exist with that IP address in that *Namespace*.

We set `DNS_4` to `1-2-3-4.kube-system.pod.cluster.local`.

### Solution

We should update the *ConfigMap*:

```bash
➜ candidate@cka6016:~$ $ k -n lima-control get cm                
NAME               DATA   AGE
control-config     4      10m

➜ candidate@cka6016:~$ k -n lima-control edit cm control-config
```

```yaml
apiVersion: v1
data:
  DNS_1: kubernetes.default.svc.cluster.local                  # UPDATE
  DNS_2: department.lima-workload.svc.cluster.local            # UPDATE
  DNS_3: section100.section.lima-workload.svc.cluster.local    # UPDATE
  DNS_4: 1-2-3-4.kube-system.pod.cluster.local                 # UPDATE
kind: ConfigMap
metadata:
  name: control-config
  namespace: lima-control
...
```

And restart the *Deployment*:

```bash
➜ candidate@cka6016:~$ kubectl -n lima-control rollout restart deploy controller
deployment.apps/controller restarted
```

And the *Pod* logs also look happy now:

```bash
➜ candidate@cka6016:~$ k -n lima-control logs -f controller-54b5b69d7d-mgng2

+ nslookup kubernetes.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1


+ nslookup department.lima-workload.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   department.lima-workload.svc.cluster.local
Address: 10.32.0.2
Name:   department.lima-workload.svc.cluster.local
Address: 10.32.0.9


+ nslookup section100.section.lima-workload.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   section100.section.lima-workload.svc.cluster.local
Address: 10.32.0.10


+ nslookup 1-2-3-4.kube-system.pod.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10:53

Name:   1-2-3-4.kube-system.pod.cluster.local
Address: 1.2.3.4
```

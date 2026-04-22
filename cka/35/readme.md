# Preview Question 1 | ETCD Information

Solve this question on: `ssh cka9412`

The cluster admin asked you to find out the following information about etcd running on `cka9412`:

- Server private key location
- Server certificate expiration date
- Is client certificate authentication enabled

Write these information into `/opt/course/p1/etcd-info.txt`

## Answer

### Find out etcd information

Let's check the nodes:

```bash
➜ ssh cka9412
➜ candidate@cka9412:~$ k get node
NAME            STATUS   ROLES           AGE   VERSION
cka9412         Ready    control-plane   9d    v1.35.2
cka9412-node1   Ready    <none>          9d    v1.35.2
```

First we check how etcd is setup in this cluster:

```bash
➜ candidate@cka9412:~$ sudo -i
➜ root@cka9412:~# k -n kube-system get pod
NAME                              READY   STATUS    RESTARTS   AGE
coredns-6f4c58b94d-djpgr          1/1     Running   0          8d
coredns-6f4c58b94d-ds6ch          1/1     Running   0          8d
etcd-cka9412                      1/1     Running   0          9d
kube-apiserver-cka9412            1/1     Running   0          9d
kube-controller-manager-cka9412   1/1     Running   0          9d
kube-proxy-7zhtk                  1/1     Running   0          9d
kube-proxy-nbzrt                  1/1     Running   0          9d
kube-scheduler-cka9412            1/1     Running   0          9d
weave-net-h7n8j                   2/2     Running   1 (9d ago) 9d
weave-net-rbhgl                   2/2     Running   1 (9d ago) 9d
```

We see it's running as a *Pod*, more specific a static *Pod*. So we check for the default kubelet directory for static manifests:

```bash
➜ root@cka9412:~# find /etc/kubernetes/manifests/
/etc/kubernetes/manifests/
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/etcd.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml

➜ root@cka9412:~# vim /etc/kubernetes/manifests/etcd.yaml
```

So we look at the yaml and the parameters with which etcd is started:

```yaml
# cka9412:/etc/kubernetes/manifests/etcd.yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubeadm.kubernetes.io/etcd.advertise-client-urls: https://192.168.100.21:2379
  creationTimestamp: null
  labels:
    component: etcd
    tier: control-plane
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.100.21:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt            # server certificate
    - --client-cert-auth=true                                    # enabled
    - --data-dir=/var/lib/etcd
    - --experimental-initial-corrupt-check=true
    - --experimental-watch-progress-notify-interval=5s
    - --initial-advertise-peer-urls=https://192.168.100.21:2380
    - --initial-cluster=cka9412=https://192.168.100.21:2380
    - --key-file=/etc/kubernetes/pki/etcd/server.key             # server private key
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.100.21:2379
    - --listen-metrics-urls=http://127.0.0.1:2381
    - --listen-peer-urls=https://192.168.100.21:2380
    - --name=cka9412
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    image: registry.k8s.io/etcd:3.5.15-0
    imagePullPolicy: IfNotPresent
...
```

We see that client authentication is enabled and also the requested path to the server private key, now let's find out the expiration of the server certificate:

```bash
➜ root@cka9412:~# openssl x509  -noout -text -in /etc/kubernetes/pki/etcd/server.crt | grep Validity -A2
        Validity
            Not Before: Oct 29 14:14:27 2024 GMT
            Not After : Oct 29 14:19:27 2025 GMT
```

There we have it. Let's write the information into the requested file:

```text
# /opt/course/p1/etcd-info.txt
Server private key location: /etc/kubernetes/pki/etcd/server.key
Server certificate expiration date: Oct 29 14:19:29 2025 GMT
Is client certificate authentication enabled: yes
```

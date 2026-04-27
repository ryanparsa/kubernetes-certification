## Answer

### Find out etcd information

Let's check the *Nodes*:

```bash
kubectl get node
NAME                        STATUS   ROLES           AGE   VERSION
cka-lab-control-plane       Ready    control-plane   9d    v1.35.2
```

First we check how etcd is setup in this cluster.

```bash
kubectl -n kube-system get pod
NAME                                          READY   STATUS    RESTARTS   AGE
coredns-6f4c58b94d-djpgr                      1/1     Running   0          8d
coredns-6f4c58b94d-ds6ch                      1/1     Running   0          8d
etcd-cka-lab-control-plane                    1/1     Running   0          9d
kube-apiserver-cka-lab-control-plane          1/1     Running   0          9d
kube-controller-manager-cka-lab-control-plane 1/1     Running   0          9d
kube-proxy-7zhtk                              1/1     Running   0          9d
kube-scheduler-cka-lab-control-plane          1/1     Running   0          9d
```

We see it's running as a *Pod*, more specific a static *Pod*. So we check for the default kubelet directory for static manifests:

```bash
find /etc/kubernetes/manifests/
/etc/kubernetes/manifests/
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/etcd.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml

cat /etc/kubernetes/manifests/etcd.yaml
```

So we look at the yaml and the parameters with which etcd is started:

```yaml
# /etc/kubernetes/manifests/etcd.yaml
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
    - --initial-cluster=cka-lab-control-plane=https://192.168.100.21:2380
    - --key-file=/etc/kubernetes/pki/etcd/server.key             # server private key
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.100.21:2379
    - --listen-metrics-urls=http://127.0.0.1:2381
    - --listen-peer-urls=https://192.168.100.21:2380
    - --name=cka-lab-control-plane
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
openssl x509  -noout -text -in /etc/kubernetes/pki/etcd/server.crt | grep Validity -A2
        Validity
            Not Before: Oct 29 14:14:27 2024 GMT
            Not After : Oct 29 14:19:27 2025 GMT
```

There we have it. Let's write the information into the requested file:

```text
# cka/35/lab/etcd-info.txt
Server private key location: /etc/kubernetes/pki/etcd/server.key
Server certificate expiration date: Oct 29 14:19:29 2025 GMT
Is client certificate authentication enabled: yes
```

## Killer.sh Checklist (Score: 0/3)

- [ ] Server private key location correctly identified
- [ ] Server certificate expiration date correctly identified
- [ ] Client certificate authentication status correctly identified

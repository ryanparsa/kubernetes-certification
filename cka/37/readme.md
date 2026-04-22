# Preview Question 3 | Change Service CIDR

> **Solve this question on:** `ssh cka9412`

1.  Create a *Pod* named `check-ip` in *Namespace* `default` using image `httpd:2-alpine`
2.  Expose it on port `80` as a ClusterIP *Service* named `check-ip-service`. Remember/output the IP of that *Service*
3.  Change the Service CIDR to `11.96.0.0/12` for the cluster
4.  Create a second *Service* named `check-ip-service2` pointing to the same *Pod*

> ℹ️ The second *Service* should get an IP address from the new CIDR range

## Answer

Let's create the *Pod* and expose it:

```bash
➜ ssh cka9412
➜ candidate@cka9412:~$ k run check-ip --image=httpd:2-alpine
pod/check-ip created

➜ candidate@cka9412:~$ k expose pod check-ip --name check-ip-service --port 80
```

And check the *Service* IP:

```bash
➜ candidate@cka9412:~$ k get svc
NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
check-ip-service   ClusterIP   10.97.6.41   <none>        80/TCP    3s
kubernetes         ClusterIP   10.96.0.1    <none>        443/TCP   32d
```

Now we change the *Service* CIDR in the kube-apiserver manifest:

```bash
➜ candidate@cka9412:~$ sudo -i
➜ root@cka9412:~# vim /etc/kubernetes/manifests/kube-apiserver.yaml
```

```yaml
# cka9412:/etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=192.168.100.21
...
    - --service-account-key-file=/etc/kubernetes/pki/sa.pub
    - --service-cluster-ip-range=11.96.0.0/12                     # change
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
...
```

We wait for the kube-apiserver to be restarted, which can take a minute:

```bash
➜ root@cka9412:~# watch crictl ps

➜ root@cka9412:~# kubectl -n kube-system get pod | grep api
kube-apiserver-cka9412            1/1     Running   0             20s
```

Now we do the same for the controller manager:

```bash
➜ root@cka9412:~# vim /etc/kubernetes/manifests/kube-controller-manager.yaml
```

```yaml
# cka9412:/etc/kubernetes/manifests/kube-controller-manager.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-controller-manager
    tier: control-plane
  name: kube-controller-manager
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-controller-manager
    - --allocate-node-cidrs=true
    - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --bind-address=127.0.0.1
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --cluster-cidr=10.244.0.0/16
    - --cluster-name=kubernetes
    - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
    - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
    - --controllers=*,bootstrapsigner,tokencleaner
    - --kubeconfig=/etc/kubernetes/controller-manager.conf
    - --leader-elect=true
    - --node-cidr-mask-size=24
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --root-ca-file=/etc/kubernetes/pki/ca.crt
    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=11.96.0.0/12                     # change
    - --use-service-account-credentials=true
```

We wait for the kube-controller-manager to be restarted, which can take a minute:

```bash
➜ root@cka9412:~# watch crictl ps

➜ root@cka9412:~# kubectl -n kube-system get pod | grep controller
kube-controller-manager-cka9412   1/1     Running   0               39s
```

Finally we need to create an additional `ServiceCIDR` resource:

```bash
➜ root@cka9412:~# k get servicecidr
NAME         CIDRS          AGE
kubernetes   10.96.0.0/12   32d

➜ root@cka9412:~# cat <<'EOF' | k apply -f -
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata:
  name: svc-cidr-new
spec:
  cidrs:
  - 11.96.0.0/12
EOF
servicecidr.networking.k8s.io/svc-cidr-new created

➜ root@cka9412:~# k get servicecidr
NAME           CIDRS          AGE
kubernetes     10.96.0.0/12   32d
svc-cidr-new   11.96.0.0/12   4s
```

We also need to delete the old `ServiceCIDR` resource:

```bash
➜ root@cka9412:~# k delete servicecidr kubernetes
servicecidr.networking.k8s.io "kubernetes" deleted
^C

➜ root@cka9412:~# k get servicecidr
NAME           CIDRS          AGE
kubernetes     10.96.0.0/12   32d
svc-cidr-new   11.96.0.0/12   5m14s

➜ root@cka9412:~# k get servicecidr kubernetes -oyaml
```

```yaml
# kubectl get servicecidr kubernetes -oyaml
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata:
  creationTimestamp: "2025-09-18T15:04:19Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2025-10-21T08:45:18Z"      # delete initiated
...
spec:
  cidrs:
  - 10.96.0.0/12
status:
  conditions:
  - lastTransitionTime: "2025-10-21T08:45:18Z"
    message: There are still IPAddresses referencing the ServiceCIDR, please remove
      them or create a new ServiceCIDR
    reason: Terminating                          # delete initiated
    status: "False"
    type: Ready
```

The deleted *ServiceCIDR* will remain in a terminating state till no more *Services* exist that use that CIDR.

Let's query our *Service* again:

```bash
➜ root@cka9412:~$ k get svc
NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
check-ip-service   ClusterIP   10.97.6.41   <none>        80/TCP    7m14s
kubernetes         ClusterIP   10.96.0.1    <none>        443/TCP   32d
```

Nothing will change for existing *Services*. Now we create the new one:

```bash
➜ root@cka9412:~$ k expose pod check-ip --name check-ip-service2 --port 80
```

And check again:

```bash
➜ root@cka9412:~# k get svc
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
check-ip-service    ClusterIP   10.97.6.41      <none>        80/TCP    7m24s
check-ip-service2   ClusterIP   11.108.174.69   <none>        80/TCP    2s
kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP   32d
```

There we go, the new *Service* got an IP of the updated range assigned.

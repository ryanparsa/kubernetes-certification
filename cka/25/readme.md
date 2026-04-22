# Question 8 | Get Controlplane Information

> **Solve this question on:** `ssh cka8448`

Check how the controlplane components kubelet, kube-apiserver, kube-scheduler, kube-controller-manager and etcd are started/installed on the controlplane node.

Also find out the name of the DNS application and how it's started/installed in the cluster.

Write your findings into file `/opt/course/8/controlplane-components.txt`. The file should be structured like:

```
# /opt/course/8/controlplane-components.txt
kubelet: [TYPE]
kube-apiserver: [TYPE]
kube-scheduler: [TYPE]
kube-controller-manager: [TYPE]
etcd: [TYPE]
dns: [TYPE] [NAME]
```

Choices of `[TYPE]` are: `not-installed`, `process`, `static-pod`, `pod`

## Answer

We could start by finding processes of the requested components, especially the kubelet at first:

```bash
➜ ssh cka8448

➜ candidate@cka8448:~$ sudo -i

➜ root@cka8448:~# ps aux | grep kubelet
```

We can see which components are controlled via systemd looking at `/usr/lib/systemd` directory:

```bash
➜ root@cka8448:~# find /usr/lib/systemd | grep kube
/usr/lib/systemd/user/podman-kube@.service
/usr/lib/systemd/system/kubelet.service.d
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
/usr/lib/systemd/system/kubelet.service
/usr/lib/systemd/system/podman-kube@.service

➜ root@cka8448:~# service kubelet status
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
    Drop-In: /usr/lib/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: active (running) since Sun 2024-12-08 16:10:53 UTC; 1h 6min ago
       Docs: https://kubernetes.io/docs/
   Main PID: 7355 (kubelet)
      Tasks: 11 (limit: 1317)
     Memory: 69.0M (peak: 75.9M)
        CPU: 1min 58.582s
     CGroup: /system.slice/kubelet.service
             └─7355 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet>
...

➜ root@cka8448:~# find /usr/lib/systemd | grep etcd
```

This shows kubelet is controlled via systemd, but no other service named `kube` nor `etcd`. It seems that this cluster has been setup using kubeadm, so we check in the default manifests directory:

```bash
➜ root@cka8448:~# find /etc/kubernetes/manifests/
/etc/kubernetes/manifests/
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/etcd.yaml
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml
```

The kubelet could also have a different manifests directory specified via a KubeletConfiguration, but the one above is the default one.

This means the main 4 controlplane services are setup as static Pods. Actually, let's check all Pods running in the `kube-system` Namespace:

```bash
➜ root@cka8448:~# k -n kube-system get pod -o wide
NAME                              ...   NODE      
coredns-6f8b9d9f4b-8z7rb          ...   cka8448   
coredns-6f8b9d9f4b-fg7bt          ...   cka8448   
etcd-cka8448                      ...   cka8448   
kube-apiserver-cka8448            ...   cka8448   
kube-controller-manager-cka8448   ...   cka8448   
kube-proxy-dvv7m                  ...   cka8448   
kube-scheduler-cka8448            ...   cka8448   
weave-net-gjrxh                   ...   cka8448    
```

Above we see the 4 static pods, with `-cka8448` as suffix.

We also see that the dns application seems to be coredns, but how is it controlled?

```bash
➜ root@cka8448$ kubectl -n kube-system get ds
NAME         DESIRED   ...   NODE SELECTOR            AGE
kube-proxy   1         ...   kubernetes.io/os=linux   67m
weave-net    1         ...   <none>                   67m

➜ root@cka8448$ k -n kube-system get deploy
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
coredns   2/2     2            2           68m
```

Seems like coredns is controlled via a Deployment. We combine our findings in the requested file:

```
# /opt/course/8/controlplane-components.txt
kubelet: process
kube-apiserver: static-pod
kube-scheduler: static-pod
kube-controller-manager: static-pod
etcd: static-pod
dns: pod coredns
```

You should be comfortable investigating a running cluster, know different methods on how a cluster and its services can be setup and be able to troubleshoot and find error sources.

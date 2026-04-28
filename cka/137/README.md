# Question 137

> **Solve this question on:** `ssh cluster1-controlplane1`

SSH into the controlplane node. Check how the controlplane components (`kubelet`, `kube-apiserver`, `kube-scheduler`, `kube-controller-manager`, `etcd`) are started/installed. Also find out the name of the DNS application and how it's started/installed in the cluster.

Write your findings into `/opt/course/8/master-components.txt` structured like:

```
#apiserver: [TYPE]
#scheduler: [TYPE]
#controller-manager: [TYPE]
#etcd: [TYPE]
#dns: [TYPE] [NAME]
```

Choices of `[TYPE]` are: `not-installed`, `process`, `static-pod`, `pod`.

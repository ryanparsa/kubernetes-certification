# Question 107

> **Solve this question on:** `ssh cluster1-master1`

SSH into the master node. Check how the master components (`kubelet`, `kube-apiserver`, `kube-scheduler`, `kube-controller-manager`, `etcd`) are started/installed on the master node. Also find out the name of the DNS application and how it's started/installed.

Write your findings into `/opt/course/8/master-components.txt` structured like:

```
#apiserver: [TYPE]
#scheduler: [TYPE]
#controller-manager: [TYPE]
#etcd: [TYPE]
#dns: [TYPE] [NAME]
```

Choices of `[TYPE]` are: `not-installed`, `process`, `static-pod`, `pod`.

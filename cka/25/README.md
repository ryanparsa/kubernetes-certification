# Question 25

Check how the *Controlplane Nodes* components *Kubelet*, *Kube-apiserver*, *Kube-scheduler*, *Kube-controller-manager* and *Etcd* are started/installed on the *Controlplane Nodes*.

Also find out the name of the DNS application and how it's started/installed in the cluster.

Write your findings into file `cka/25/lab/controlplane-components.txt`. The file should be structured like:

```
# cka/25/lab/controlplane-components.txt
kubelet: [TYPE]
kube-apiserver: [TYPE]
kube-scheduler: [TYPE]
kube-controller-manager: [TYPE]
etcd: [TYPE]
dns: [TYPE] [NAME]
```

Choices of `[TYPE]` are: `not-installed`, `process`, `static-pod`, `pod`

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

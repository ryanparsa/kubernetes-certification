# Role in Kubernetes

etcd is the **single source of truth** for all cluster state. Every object the API
server creates, updates, or deletes is persisted to etcd.

```
kubectl → kube-apiserver → etcd
                     ↑
kube-scheduler, controller-manager, kubelet all watch etcd via the API server
(they never connect to etcd directly)
```

Only the **kube-apiserver** talks to etcd. All other components communicate with etcd
indirectly through the API server.

### What is stored in etcd

- All Kubernetes objects: Pods, Deployments, Services, ConfigMaps, Secrets, RBAC objects
- Cluster configuration: Namespaces, ResourceQuotas, LimitRanges, StorageClasses
- Lease objects used for leader election (controller-manager, scheduler)
- Node heartbeat leases

---


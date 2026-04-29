# CKA - Certified Kubernetes Administrator

## Exam Overview

| | |
|---|---|
| **Format** | Performance-based (hands-on CLI tasks) |
| **Duration** | 2 hours |
| **Passing score** | 66% |
| **Cost** | $395 USD (includes one free retake) |
| **Validity** | 3 years |
| **Allowed docs** | kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs, github.com/kubernetes |
| **Official curriculum** | https://github.com/cncf/curriculum |

## Domains & Weights

| Domain | Weight |
|---|---|
| Cluster Architecture, Installation & Configuration | 25% |
| Workloads & Scheduling | 15% |
| Services & Networking | 20% |
| Storage | 10% |
| Troubleshooting | 30% |

## Domain Topics

### Cluster Architecture, Installation & Configuration (25%)
- kubeadm init: `--pod-network-cidr`, `--apiserver-advertise-address`, `--config` file
- kubeadm join: worker nodes, control plane nodes, token creation
- kubeadm upgrade: plan -> apply -> node upgrade sequence
- kubeadm reset
- RBAC: ClusterRole, ClusterRoleBinding, Role, RoleBinding
- ServiceAccount permissions across namespaces; `kubectl auth can-i --as`
- kubeconfig: clusters, users, contexts; `kubectl config use-context`
- etcdctl snapshot save / restore; `--endpoints`, `--cacert`, `--cert`, `--key`
- Restoring etcd to a new data directory; updating the static pod manifest
- Certificate management: `kubeadm certs check-expiration`, `kubeadm certs renew`
- `openssl x509 -in / -text / -noout`; `/etc/kubernetes/pki/` structure

### Workloads & Scheduling (15%)
- Deployments: rolling update (`maxSurge`, `maxUnavailable`), rollback, pause/resume
- DaemonSet, StatefulSet, Job, CronJob - choosing the right workload
- ConfigMap and Secret: creation, env injection, volume mount
- Resource requests and limits; how requests drive scheduling decisions
- nodeSelector: key/value label matching
- Node affinity: `requiredDuringScheduling` vs `preferred`; `matchExpressions` operators
- Pod affinity / anti-affinity: `topologyKey`
- Taints: `kubectl taint nodes`, effects (`NoSchedule` / `PreferNoSchedule` / `NoExecute`)
- Tolerations: `key`, `operator` (`Equal` / `Exists`), `effect`, `value`
- PriorityClass: `globalDefault`, `value`, `preemptionPolicy`
- Static pod manifests in `/etc/kubernetes/manifests/`

### Services & Networking (20%)
- Services: ClusterIP, NodePort, LoadBalancer - `spec.selector`, `targetPort` int vs string
- Ingress: rules, `pathType` (`Exact` / `Prefix`), `ingressClassName`
- NetworkPolicy: `podSelector`, `namespaceSelector`, `ipBlock`, ingress/egress, `ports[].protocol` uppercase
- DNS: `<service>.<namespace>.svc.cluster.local`; `resolv.conf` in pods; `ndots`
- CNI plugin location: `/etc/cni/net.d/`, `/opt/cni/bin/`
- kube-proxy ConfigMap, mode (`iptables` vs `ipvs`)
- CoreDNS ConfigMap, Corefile syntax, restarting CoreDNS pods

### Storage (10%)
- PersistentVolume: `capacity`, `accessModes` (`ReadWriteOnce` / `ReadOnlyMany` / `ReadWriteMany`), reclaim policy
- PersistentVolumeClaim: `storageClassName`, `accessModes` array, `resources.requests.storage`
- StorageClass: `provisioner`, `reclaimPolicy`, `volumeBindingMode`
- Dynamic provisioning vs static binding
- Volume types: `emptyDir`, `hostPath`, `configMap`, `secret`, `persistentVolumeClaim`
- `kubectl get pv / pvc` - Bound vs Pending, capacity, access modes

### Troubleshooting (30%)
- kubelet: `/var/lib/kubelet/config.yaml`; `systemctl status/restart/daemon-reload kubelet`
- `journalctl -u kubelet -f`
- Control plane as static pods: kube-apiserver, kube-scheduler, kube-controller-manager
- Broken flags, wrong paths, missing or expired certs
- `crictl ps` / `crictl logs` for container-level debugging when kubectl is unavailable
- Node conditions, `kubectl cordon / drain / uncordon`; `--ignore-daemonsets`, `--delete-emptydir-data`
- Application failures: image pull, probes, RBAC, volume mounts, OOMKilled
- Networking failures: selector mismatch, empty Endpoints, NetworkPolicy blocking traffic

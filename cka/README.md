# CKA - Certified Kubernetes Administrator

## Exam Overview

| | |
|---|---|
| **Format** | Performance-based (hands-on CLI tasks) |
| **Duration** | 2 hours |
| **Passing score** | 66% |
| **Cost** | $395 USD (includes one free retake) |
| **Validity** | 2 years |
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


## Labs Mapping
| Lab | Topics |
|---|---|
| [1](1/README.md) | Certificate, Namespace, context, kubeconfig, kubectl |
| [2](2/README.md) | DNS, Job, Labels, Namespace, Pod, Requests, Resources, Secret, describe, helm, kubectl |
| [3](3/README.md) | Labels, Namespace, Pod, Replica, Resources, StatefulSet |
| [4](4/README.md) | CPU, Deployment, Limits, Memory, Namespace, Pod, Requests, Resources, Service, describe, kubectl, top |
| [5](5/README.md) | CPU, Deployment, HPA, Labels, Metrics, Namespace, Requests, Resources, Selector, ServiceAccount, helm, kubectl, kustomize |
| [6](6/README.md) | Deployment, Labels, Namespace, Node, PV, PVC, Pod, Requests, Resources, Selector, ServiceAccount, Volume, describe, hostPath |
| [7](7/README.md) | CPU, Memory, Metrics, Node, Pod, kubectl, metrics-server, top |
| [8](8/README.md) | Node, Service, kubeadm, kubectl, kubelet |
| [9](9/README.md) | Certificate, DNS, Fix, Labels, Namespace, Pod, Resources, Secret, Service, ServiceAccount, kubectl |
| [10](10/README.md) | ClusterRole, ClusterRoleBinding, Namespace, Pod, RBAC, Resources, Role, RoleBinding, Secret, ServiceAccount, kubectl |
| [11](11/README.md) | CPU, DaemonSet, Deployment, Labels, Memory, Namespace, Node, Pod, Requests, Resources, Role, Selector, Toleration, kubectl |
| [12](12/README.md) | Affinity, DaemonSet, Deployment, Labels, Namespace, Node, Pod, Resources, Role, Scheduling, Selector, Taint, describe, kubectl |
| [13](13/README.md) | Gateway API, Ingress, Namespace, Node, NodePort, Requests, Resources, Service, ingress, kubectl |
| [14](14/README.md) | Certificate, etcd, kube-apiserver, kubeadm, kubelet, openssl |
| [15](15/README.md) | Labels, Namespace, NetworkPolicy, Pod, Secret, describe, egress, kubectl |
| [16](16/README.md) | Backup, ClusterIP, CoreDNS, DNS, Deployment, Namespace, Pod, Service, kubeadm, kubectl |
| [17](17/README.md) | Labels, Log, Namespace, Node, Pod, containerd, crictl, kubectl |
| [18](18/README.md) | ClusterIP, DNS, Deployment, Labels, Namespace, Pod, Service, kubectl |
| [19](19/README.md) | CPU, Endpoint, Labels, LoadBalancer, Memory, Namespace, Node, NodePort, Pod, Requests, Resources, Selector, Service, Static Pod, kubectl |
| [20](20/README.md) | Certificate, Node, kube-apiserver, kubeadm, kubelet, openssl |
| [21](21/README.md) | Affinity, ClusterIP, Endpoint, Events, Labels, Namespace, Pod, Probes, Resources, Selector, Service, describe, kubectl, kubelet |
| [22](22/README.md) | CoreDNS, Namespace, Pod, etcd, kube-apiserver, kube-controller-manager, kube-proxy, kube-scheduler, kubectl |
| [23](23/README.md) | CPU, Endpoint, Fix, Job, Log, Memory, Namespace, Node, Pod, Service, containerd, crictl, etcd, journalctl, kube-apiserver, kube-controller-manager, kube-scheduler, kubeadm, kubeconfig, kubectl, kubelet, systemd |
| [24](24/README.md) | Backup, CoreDNS, Endpoint, Labels, Memory, Metrics, Namespace, Node, Pod, Resources, Restore, Snapshot, crictl, etcd, hostPath, kube-apiserver, kube-controller-manager, kube-proxy, kube-scheduler, kubectl |
| [25](25/README.md) | CPU, CoreDNS, DNS, Deployment, Memory, Namespace, Node, Pod, Selector, Service, Troubleshoot, etcd, kube-apiserver, kube-controller-manager, kube-proxy, kube-scheduler, kubeadm, kubeconfig, kubectl, kubelet, systemd |
| [26](26/README.md) | Affinity, Labels, Log, Namespace, Node, Pod, Resources, ServiceAccount, kube-scheduler, kubectl |
| [27](27/README.md) | Backup, Job, Namespace, Node, PV, PVC, Pod, Provisioner, Requests, Resources, StorageClass, Volume, VolumeBindingMode, emptyDir, kubectl |
| [28](28/README.md) | Labels, Namespace, Pod, Resources, Secret, kubectl |
| [29](29/README.md) | Affinity, Labels, Namespace, Node, Pod, Resources, Role, Taint, Toleration, describe, kubectl, nodeSelector |
| [30](30/README.md) | Labels, Log, Multi-container, Namespace, Node, Pod, Resources, Volume, emptyDir, kubectl |
| [31](31/README.md) | CNI, Node, Service, kube-apiserver, kubectl |
| [32](32/README.md) | DaemonSet, Events, Log, Namespace, Node, Pod, containerd, crictl, kube-proxy, kubectl |
| [33](33/README.md) | Events, Namespace, Pod, RBAC, Resources, Role, Secret, kubectl |
| [34](34/README.md) | Deployment, Namespace, Pod, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl, kustomize |
| [35](35/README.md) | Certificate, CoreDNS, Labels, Metrics, Namespace, Node, Pod, Snapshot, etcd, kube-apiserver, kube-controller-manager, kube-proxy, kube-scheduler, kubeadm, kubectl, kubelet, openssl |
| [36](36/README.md) | ClusterIP, Namespace, Node, Pod, Service, crictl, kube-apiserver, kube-proxy, kubectl |
| [37](37/README.md) | ClusterIP, Namespace, Node, Pod, Resources, Service, kube-apiserver, kube-controller-manager, kubectl |
| [38](38/README.md) | Labels, Namespace, Pod, kubectl |
| [39](39/README.md) | Node, Pod, Static Pod, kubectl, kubelet |
| [40](40/README.md) | Namespace, PVC, Provisioner, Requests, Resources, StorageClass, kubectl |
| [41](41/README.md) | Log, Multi-container, Namespace, Pod, Volume, emptyDir, kubectl |
| [42](42/README.md) | Namespace, Pod, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl |
| [43](43/README.md) | Ingress, Labels, Namespace, NetworkPolicy, Role, describe, ingress, kubectl |
| [44](44/README.md) | Affinity, Deployment, Labels, Namespace, NodePort, Pod, Selector, Service, kubectl |
| [45](45/README.md) | CPU, Limits, Memory, Namespace, Pod, Requests, Resources, describe, kubectl |
| [46](46/README.md) | Namespace, Pod, Volume, kubectl |
| [47](47/README.md) | Namespace, Pod, Probes, describe, kubectl |
| [48](48/README.md) | Namespace, PVC, Pod, Requests, Resources, StorageClass, Volume, kubectl |
| [49](49/README.md) | Provisioner, StorageClass, VolumeBindingMode, kubectl |
| [50](50/README.md) | Affinity, Namespace, Node, PV, PVC, Pod, Requests, Resources, hostPath, kubectl |
| [51](51/README.md) | CPU, Deployment, HPA, Labels, Limits, Memory, Namespace, Pod, Requests, Resources, Selector, kubectl |
| [52](52/README.md) | Affinity, Deployment, Labels, Namespace, Node, Pod, Scheduling, Selector, kubectl, nodeSelector |
| [53](53/README.md) | Capabilities, Labels, Namespace, PSA, Pod, Pod Security, Seccomp, SecurityContext, Volume, allowPrivilegeEscalation, context, emptyDir, kubectl, runAsNonRoot |
| [54](54/README.md) | Deployment, Labels, Namespace, Node, Scheduling, Selector, Taint, Toleration, kubectl |
| [55](55/README.md) | ClusterIP, Labels, Namespace, Pod, Requests, Resources, Selector, Service, StatefulSet, StorageClass, Volume, kubectl |
| [56](56/README.md) | ClusterIP, DNS, Debug, Deployment, Labels, Namespace, Pod, Selector, Service, kubectl |
| [57](57/README.md) | DNS, Deployment, Labels, Namespace, Pod, Selector, Service, kubectl |
| [58](58/README.md) | Deployment, Namespace, NodePort, Replica, Service, helm, kubectl |
| [59](59/README.md) | Deployment, Labels, Namespace, Resources, Selector, Volume, kubectl, kustomize |
| [60](60/README.md) | Deployment, Gateway API, Labels, Namespace, Resources, Selector, Service, kubectl |
| [61](61/README.md) | CPU, Deployment, Labels, LimitRange, Limits, Memory, Namespace, ResourceQuota, Resources, Selector, describe, kubectl |
| [62](62/README.md) | CPU, Deployment, HPA, Labels, Limits, Memory, Metrics, Namespace, Pod, Requests, Resources, Selector, kubectl, metrics-server |
| [63](63/README.md) | Namespace, Pod, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl |
| [64](64/README.md) | Deployment, Ingress, Labels, Namespace, NetworkPolicy, Pod, Selector, egress, ingress, kubectl |
| [65](65/README.md) | Deployment, Labels, Namespace, Selector, Upgrade, kubectl |
| [66](66/README.md) | Affinity, Labels, Namespace, Node, Pod, PriorityClass, Scheduling, kubectl |
| [67](67/README.md) | Debug, Deployment, Fix, Labels, Limits, Memory, Namespace, Pod, Resources, Selector, Troubleshoot, describe, kubectl |
| [68](68/README.md) | Deployment, Namespace, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl |
| [69](69/README.md) | ClusterIP, Ingress, Labels, Namespace, NetworkPolicy, Pod, Service, ingress, kubectl |
| [70](70/README.md) | PV, PVC, Pod, Requests, Resources, StorageClass, Volume, hostPath, kubectl |
| [71](71/README.md) | DaemonSet, Deployment, Labels, Node, Pod, Scheduling, Selector, Taint, kubectl |
| [72](72/README.md) | Namespace, Node, Pod, Scheduling, kubectl |
| [80](80/README.md) | Certificate, Pod, context |
| [81](81/README.md) | ClusterRole, ClusterRoleBinding, Namespace, RBAC, Resources, ServiceAccount, context, kubeconfig, kubectl |
| [84](84/README.md) | CPU, Deployment, HPA, Metrics, Namespace, Pod, kubectl |
| [85](85/README.md) | Namespace, PV, PVC, Pod |
| [86](86/README.md) | CPU, Metrics, Node, Pod, kubectl, metrics-server, top |
| [93](93/README.md) | Certificate, etcd, kubeadm, kubelet, openssl |
| [94](94/README.md) | Ingress, Namespace, NetworkPolicy, Pod, Service, egress, ingress |
| [95](95/README.md) | Backup, CoreDNS, DNS, Deployment, Node, kubectl |
| [96](96/README.md) | Labels, Namespace, Node, Pod, containerd |
| [100](100/README.md) | context, kubectl |
| [102](102/README.md) | Namespace, Replica, Resources, StatefulSet, kubectl |
| [105](105/README.md) | Deployment, Namespace, PV, PVC, Pod, Volume, context, hostPath, kubectl |
| [106](106/README.md) | CPU, Job, Memory, Metrics, Node, Pod, Resources, context, kubectl, metrics-server |
| [108](108/README.md) | Node, Pod, Scheduling, kube-scheduler, kubectl |
| [109](109/README.md) | Namespace, RBAC, Resources, Role, RoleBinding, ServiceAccount, kubectl |
| [112](112/README.md) | Log, Multi-container, Namespace, Node, Pod, Volume, context, kubectl |
| [113](113/README.md) | CNI, Node, Service, context, kubectl |
| [114](114/README.md) | Events, Log, Pod, containerd, context, kube-proxy, kubectl |
| [115](115/README.md) | Namespace, Pod, Resources, context, kubectl |
| [116](116/README.md) | Log, Namespace, Node, Pod, containerd, context, kubectl |
| [117](117/README.md) | Fix, Node, Pod, context, kubectl, kubelet |
| [118](118/README.md) | Namespace, Pod, Secret, context, kubectl |
| [119](119/README.md) | Node, context, kubeadm, kubectl |
| [120](120/README.md) | CPU, Memory, Namespace, NodePort, Pod, Requests, Service, Static Pod, context, kubectl |
| [121](121/README.md) | Certificate, kube-apiserver, kubeadm, openssl |
| [122](122/README.md) | Certificate, Node, context, kube-apiserver, kubeadm, kubectl, kubelet |
| [123](123/README.md) | Namespace, NetworkPolicy, Pod, context, kubectl |
| [124](124/README.md) | Backup, Node, Pod, Restore, etcd |
| [130](130/README.md) | context, kubectl |
| [132](132/README.md) | Namespace, Replica, Resources, context, kubectl |
| [133](133/README.md) | Namespace, Pod, Service, context, kubectl |
| [136](136/README.md) | Metrics, Node, Pod, context, kubectl, metrics-server |
| [137](137/README.md) | DNS, Node, Pod, etcd, kube-apiserver, kube-controller-manager, kube-scheduler, kubelet |
| [138](138/README.md) | Node, Pod, kube-scheduler |
| [139](139/README.md) | Namespace, Role, RoleBinding, ServiceAccount, context, kubectl |
| [140](140/README.md) | CPU, DaemonSet, Labels, Memory, Namespace, context, kubectl |
| [141](141/README.md) | DaemonSet, Deployment, Namespace, Node, Pod, context, kubectl |
| [142](142/README.md) | Log, Multi-container, Namespace, Node, Pod, Volume, context, kubectl |
| [143](143/README.md) | CNI, Node, Service, context, kubectl |
| [144](144/README.md) | Events, Log, Pod, containerd, context, kube-proxy, kubectl |
| [148](148/README.md) | Fix, Namespace, Pod, Secret, context, kubectl, kubelet |
| [149](149/README.md) | Node, context, kubeadm, kubectl |
| [150](150/README.md) | CPU, Memory, Namespace, NodePort, Pod, Requests, Service, Static Pod, context, kubectl |
| [151](151/README.md) | Certificate, kube-apiserver, kubeadm, openssl |
| [153](153/README.md) | Namespace, NetworkPolicy, Pod, context, kubectl |
| [154](154/README.md) | Backup, Node, Pod, Restore, etcd |
| [180](180/README.md) | context, kubeconfig |
| [181](181/README.md) | Namespace, helm |
| [182](182/README.md) | Namespace, Replica, Resources |
| [183](183/README.md) | CPU, Memory, Namespace, Pod, Resources |
| [184](184/README.md) | CPU, Deployment, HPA, kustomize |
| [185](185/README.md) | Deployment, Namespace, PV, PVC, Volume, hostPath |
| [186](186/README.md) | Metrics, Node, Pod, kubectl, metrics-server |
| [188](188/README.md) | Namespace, Pod, Secret, ServiceAccount |
| [192](192/README.md) | Gateway API, Ingress, Namespace, ingress |
| [196](196/README.md) | Labels, Log, Namespace, Node, Pod, containerd, crictl, kubectl |

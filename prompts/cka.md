Topic scope: CKA-specific. Combine with base.md for a full session.

COVERAGE — rotate through all areas:

Cluster setup & configuration
- kubeadm init: --pod-network-cidr, --apiserver-advertise-address, --config file
- kubeadm join: worker nodes, control plane nodes, token creation
- kubeadm upgrade: plan, apply, node upgrade sequence
- kubeadm reset

etcd
- etcdctl snapshot save / restore
- --endpoints, --cacert, --cert, --key flags
- Restoring to a new data directory, updating etcd static pod manifest

Certificate management
- kubeadm certs check-expiration
- kubeadm certs renew
- openssl x509 -in / -text / -noout
- /etc/kubernetes/pki/ structure and file purposes

Node management
- kubectl cordon / drain / uncordon
- --ignore-daemonsets, --delete-emptydir-data
- Node conditions, taints added automatically by drain

Kubelet
- /var/lib/kubelet/config.yaml
- systemctl status / restart / daemon-reload kubelet
- journalctl -u kubelet -f
- Static pod manifests in /etc/kubernetes/manifests/

Control plane troubleshooting
- kube-apiserver, kube-scheduler, kube-controller-manager as static pods
- Broken flags, wrong paths, missing or expired certs
- crictl ps / crictl logs for container-level debugging when kubectl is unavailable

RBAC (admin level)
- ClusterRole, ClusterRoleBinding
- ServiceAccount permissions across namespaces
- kubectl auth can-i --as system:serviceaccount:<ns>:<name>

Networking (admin level)
- CNI plugin location: /etc/cni/net.d/, /opt/cni/bin/
- kube-proxy ConfigMap, mode (iptables vs ipvs)
- CoreDNS ConfigMap, Corefile syntax, restarting CoreDNS pods

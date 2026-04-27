# Certificate File Map

| File                                           | Used by                   | Purpose                           |
|------------------------------------------------|---------------------------|-----------------------------------|
| `/etc/kubernetes/pki/ca.crt`                   | all components            | cluster CA — validates everything |
| `/etc/kubernetes/pki/ca.key`                   | controller-manager        | signs kubelet client certs        |
| `/etc/kubernetes/pki/apiserver.crt`            | kube-apiserver            | TLS serving cert                  |
| `/etc/kubernetes/pki/apiserver-kubelet-client.crt` | kube-apiserver        | client cert to kubelets           |
| `/etc/kubernetes/pki/apiserver-etcd-client.crt`| kube-apiserver            | client cert to etcd               |
| `/etc/kubernetes/pki/sa.pub`                   | kube-apiserver            | verifies ServiceAccount JWTs      |
| `/etc/kubernetes/pki/sa.key`                   | kube-controller-manager   | signs ServiceAccount JWTs         |
| `/etc/kubernetes/pki/etcd/ca.crt`              | etcd, apiserver           | etcd CA                           |
| `/etc/kubernetes/pki/etcd/server.crt`          | etcd                      | etcd TLS serving cert             |
| `/etc/kubernetes/pki/etcd/peer.crt`            | etcd                      | etcd peer communication cert      |
| `/etc/kubernetes/pki/front-proxy-ca.crt`       | kube-apiserver            | aggregation layer CA              |
| `/etc/kubernetes/pki/front-proxy-client.crt`   | kube-apiserver            | aggregation layer client cert     |

---


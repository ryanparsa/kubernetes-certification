# Why Unique Certs for Kubelets? (Node Restriction)

The `NodeRestriction` Admission Controller prevents a compromised node from accessing data belonging to other nodes. This security is based on the **Common Name (CN)** inside each Kubelet's client certificate (e.g., `system:node:worker-1`).

> **Security Warning:** If Kubelet client certificates are shared across nodes, hacking one node effectively grants access to the data of all nodes sharing that identity.
> 

---


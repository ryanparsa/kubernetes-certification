RBAC roles should specify apiGroups correctly (empty string for core API, "apps" for deployments).
Always verify that a ServiceAccount has the exact permissions required and no more (least privilege).
Testing RBAC often requires using `kubectl auth can-i ... --as system:serviceaccount:<namespace>:<name>`.
When using kind in restricted environments, ensure `networking.ipFamily: ipv4` is set in kind-config.yaml to avoid IPv6 related iptables issues.

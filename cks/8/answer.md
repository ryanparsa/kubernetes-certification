## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Get the API server ClusterIP

```bash
API_SERVER_IP=$(kubectl get svc kubernetes -n default -o jsonpath='{.spec.clusterIP}')
echo "API Server IP: $API_SERVER_IP"
```

### Create the NetworkPolicy and pods

```yaml
# lab/api-restrict-policy.yaml
# 1. Deny egress to API server for all pods by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-server-policy
  namespace: api-restrict
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - <API_SERVER_IP>/32  # replace with actual IP
---
# 2. Allow egress to API server for admin pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-admin-api-egress
  namespace: api-restrict
spec:
  podSelector:
    matchLabels:
      role: admin
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: <API_SERVER_IP>/32  # replace with actual IP
    ports:
    - protocol: TCP
      port: 443
---
apiVersion: v1
kind: Pod
metadata:
  name: admin-pod
  namespace: api-restrict
  labels:
    role: admin
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
---
apiVersion: v1
kind: Pod
metadata:
  name: restricted-pod
  namespace: api-restrict
  labels:
    role: restricted
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
```

Apply substituting the real API server IP:

```bash
sed "s|<API_SERVER_IP>|$API_SERVER_IP|g" lab/api-restrict-policy.yaml | kubectl apply -f -
kubectl wait pod admin-pod restricted-pod -n api-restrict --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get networkpolicy -n api-restrict
kubectl get pods -n api-restrict --show-labels
```

## Checklist (Score: 0/5)

- [ ] NetworkPolicy `api-server-policy` exists in namespace `api-restrict`
- [ ] Default policy denies all egress to the Kubernetes API server IP
- [ ] NetworkPolicy (or second policy) allows `role=admin` pods to reach API server
- [ ] Pod `admin-pod` exists with label `role=admin`
- [ ] Pod `restricted-pod` exists with label `role=restricted`

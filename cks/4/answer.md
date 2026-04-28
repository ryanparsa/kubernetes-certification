## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Create the NetworkPolicy to block metadata access

The metadata endpoint `169.254.169.254` is used by cloud providers to supply instance credentials and configuration to workloads. Blocking it prevents pods from escalating privileges via the IMDS (Instance Metadata Service).

```yaml
# lab/block-metadata.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-metadata
  namespace: metadata-protect
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
```

```bash
kubectl apply -f lab/block-metadata.yaml
```

### Create the test pod

```yaml
# lab/test-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  namespace: metadata-protect
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
```

```bash
kubectl apply -f lab/test-pod.yaml
kubectl wait pod test-pod -n metadata-protect --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get networkpolicy block-metadata -n metadata-protect
kubectl get pod test-pod -n metadata-protect
```

## Checklist (Score: 0/5)

- [ ] NetworkPolicy `block-metadata` exists in namespace `metadata-protect`
- [ ] NetworkPolicy applies to all pods (`podSelector: {}`)
- [ ] NetworkPolicy blocks egress to `169.254.169.254/32`
- [ ] NetworkPolicy allows all other egress traffic
- [ ] Pod `test-pod` exists and is running in namespace `metadata-protect`

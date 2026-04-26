# Preview Question 3 | Change Service CIDR

> **Solve this question on:** the "cka-lab-37" kind cluster

1.  Create a *Pod* named `check-ip` in *Namespace* `default` using image `httpd:2-alpine`
2.  Expose it on port `80` as a ClusterIP *Service* named `check-ip-service`. Remember/output the IP of that *Service*
3.  Change the Service CIDR to `11.96.0.0/12` for the cluster
4.  Create a second *Service* named `check-ip-service2` pointing to the same *Pod*

> ℹ️ The second *Service* should get an IP address from the new CIDR range

## Answer

### Create the Pod and initial Service

```bash
kubectl run check-ip --image=httpd:2-alpine
kubectl expose pod check-ip --name check-ip-service --port 80
```

Check the *Service* IP:

```bash
kubectl get svc check-ip-service
```

### Change Service CIDR

Connect to the control-plane *Node*:

```bash
docker exec -it cka-lab-37-control-plane bash
```

Edit the `kube-apiserver` manifest:

```bash
vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

Update the `--service-cluster-ip-range` flag:

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
...
    - --service-cluster-ip-range=11.96.0.0/12
...
```

Edit the `kube-controller-manager` manifest:

```bash
vi /etc/kubernetes/manifests/kube-controller-manager.yaml
```

Update the `--service-cluster-ip-range` flag:

```yaml
# /etc/kubernetes/manifests/kube-controller-manager.yaml
...
    - --service-cluster-ip-range=11.96.0.0/12
...
```

Wait for the components to restart.

### Update ServiceCIDR resources

Create a new *ServiceCIDR*:

```yaml
# cka/37/course/svc-cidr-new.yaml
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata:
  name: svc-cidr-new
spec:
  cidrs:
  - 11.96.0.0/12
```

```bash
kubectl apply -f cka/37/course/svc-cidr-new.yaml
```

Delete the old *ServiceCIDR*:

```bash
kubectl delete servicecidr kubernetes
```

### Verify with new Service

```bash
kubectl expose pod check-ip --name check-ip-service2 --port 80
kubectl get svc check-ip-service2
```

The new *Service* should have an IP in the `11.96.0.0/12` range.

## Killer.sh Checklist (Score: 0/7)

- [ ] *Pod* `check-ip` exists in `default` *Namespace* with image `httpd:2-alpine`
- [ ] *Service* `check-ip-service` exists and has an IP in the `10.96.0.0/12` range
- [ ] `kube-apiserver` manifest has `--service-cluster-ip-range=11.96.0.0/12`
- [ ] `kube-controller-manager` manifest has `--service-cluster-ip-range=11.96.0.0/12`
- [ ] *ServiceCIDR* `svc-cidr-new` exists with range `11.96.0.0/12`
- [ ] *ServiceCIDR* `kubernetes` is deleted (or in terminating state)
- [ ] *Service* `check-ip-service2` exists and has an IP in the `11.96.0.0/12` range

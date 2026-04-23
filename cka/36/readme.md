# Question 36 | Kube-Proxy iptables

> **Solve this question on:** the "cka-lab-36" kind cluster

You're asked to confirm that kube-proxy is running correctly. For this perform the following in *Namespace* `project-hamster`:

1.  Create *Pod* `p2-pod` with image `nginx:1-alpine`
2.  Create *Service* `p2-service` which exposes the *Pod* internally in the cluster on port `3000->80`
3.  Write the iptables rules of the control-plane node belonging to the created *Service* `p2-service` into file `cka/36/course/iptables.txt`
4.  Delete the *Service* and confirm that the iptables rules are gone again

## Answer

### Step 1: Create the *Pod*

First we create the *Pod*:

```bash
kubectl -n project-hamster run p2-pod --image=nginx:1-alpine
```

### Step 2: Create the *Service*

Next we create the *Service*:

```bash
kubectl -n project-hamster expose pod p2-pod --name p2-service --port 3000 --target-port 80

kubectl -n project-hamster get pod,svc
```

### (Optional) Confirm kube-proxy is running and is using iptables

The idea here is to find the kube-proxy container and check its logs:

```bash
docker exec cka-lab-36-control-plane crictl ps | grep kube-proxy

docker exec cka-lab-36-control-plane crictl logs <CONTAINER_ID>
```

### Step 3: Check kube-proxy is creating iptables rules

Now we check the iptables rules on the node and write them to the file:

```bash
docker exec cka-lab-36-control-plane iptables-save | grep p2-service > cka/36/course/iptables.txt
```

### Delete the *Service* and confirm iptables rules are gone

Delete the *Service* and confirm the iptables rules are gone:

```bash
kubectl -n project-hamster delete svc p2-service

docker exec cka-lab-36-control-plane iptables-save | grep p2-service
```

## Killer.sh Checklist (Score: 0/4)

- [ ] *Pod* `p2-pod` is running in `project-hamster` with image `nginx:1-alpine`
- [ ] *Service* `p2-service` is created and exposes port `3000`
- [ ] File `cka/36/course/iptables.txt` exists and contains iptables rules for `p2-service`
- [ ] *Service* `p2-service` is deleted at the end

## Answer

**Reference:** <https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/>

### Solution

Create the output directory and run the two one-liner commands:

```bash
mkdir -p /opt/course/7

kubectl top pod --all-namespaces --sort-by=name --containers > /opt/course/7/pods.txt

kubectl top node --sort-by=cpu > /opt/course/7/nodes.txt
```

### Verify

```bash
cat /opt/course/7/pods.txt
# NAMESPACE     POD                                      NAME                      CPU(cores)   MEMORY(bytes)
# kube-system   coredns-7d89d9b6f8-abc                  coredns                   3m           22Mi
# kube-system   etcd-cka-lab-72-control-plane            etcd                      25m          54Mi
# ...

cat /opt/course/7/nodes.txt
# NAME                       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# cka-lab-72-control-plane   104m         10%    1121Mi          60%
```

## Checklist (Score: 0/5)

- [ ] `/opt/course/7/pods.txt` exists and is not empty
- [ ] `pods.txt` covers all namespaces (`--all-namespaces`)
- [ ] `pods.txt` includes per-container usage (`--containers`)
- [ ] `pods.txt` pod names are sorted alphabetically
- [ ] `/opt/course/7/nodes.txt` exists and is not empty

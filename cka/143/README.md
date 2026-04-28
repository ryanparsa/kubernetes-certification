# Question 143

> **Solve this question on:** `kubectl config use-context k8s-c1-H`

You're asked to find out the following information about the cluster and write it into `/opt/course/14/cluster-info`:

1. How many controlplane nodes are available?
2. How many worker nodes are available?
3. What is the Service CIDR?
4. Which Networking (or CNI Plugin) is configured and where is its config file?
5. Which suffix will static pods have that run on `cluster1`?

Structure the file like:

```
#1: [controlplane node count]
#2: [worker node count]
#3: [service CIDR]
#4: [CNI name], /[path/to/cni/config]
#5: [suffix]
```

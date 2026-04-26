# Question 7

> **Solve this question on:** the "cka-lab-7" kind cluster

The metrics-server has been installed in the cluster. Write two bash scripts which use `kubectl`:

1. Script `cka/7/course/node.sh` should show resource usage of nodes
2. Script `cka/7/course/pod.sh` should show resource usage of Pods and their containers

## Answer

The command we need to use here is top:

```bash
kubectl top -h
Display resource (CPU/memory) usage.

 The top command allows you to see the resource consumption for nodes or pods.

 This command requires Metrics Server to be correctly configured and working on the server.

Available Commands:
  node        Display resource (CPU/memory) usage of nodes
  pod         Display resource (CPU/memory) usage of pods

Usage:
  kubectl top [flags] [options]

Use "kubectl top <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
```

We see that the metrics server provides information about resource usage:

```bash
kubectl top node
NAME                    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
cka-lab-control-plane   104m         10%    1121Mi          60%
```

We create the first file, ensure to **not** use aliases but instead the full command names:

```bash
# cka/7/course/node.sh
kubectl top node
```

For the second file we might need to check the docs again:

```bash
kubectl top pod -h
Display resource (CPU/memory) usage of pods.
...
  --containers=false:
      If present, print usage of containers within a pod.
...
```

With this we can finish this task:

```bash
# cka/7/course/pod.sh
kubectl top pod --containers=true
```

## Killer.sh Checklist (Score: 0/2)

- [ ] `course/node.sh` contains `kubectl top node`
- [ ] `course/pod.sh` contains `kubectl top pod --containers=true`
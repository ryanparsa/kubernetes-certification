# Question 7 | Node and Pod Resource Usage

> **Solve this question on:** `ssh cka5774`

The metrics-server has been installed in the cluster. Write two bash scripts which use `kubectl`:

1. Script `/opt/course/7/node.sh` should show resource usage of nodes
2. Script `/opt/course/7/pod.sh` should show resource usage of Pods and their containers

## Answer

The command we need to use here is top:

```bash
ssh cka5774
```

```bash
candidate@cka5774:~$ k top -h
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
candidate@cka5774:~$ k top node
NAME          CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
cka5774       104m         10%    1121Mi          60%       
```

We create the first file, ensure to **not** use aliases but instead the full command names:

```bash
# cka5774:/opt/course/7/node.sh
kubectl top node
```

For the second file we might need to check the docs again:

```bash
candidate@cka5774:~$ k top pod -h
Display resource (CPU/memory) usage of pods.
...
  --containers=false:
      If present, print usage of containers within a pod.
...
```

With this we can finish this task:

```bash
# cka5774:/opt/course/7/pod.sh
kubectl top pod --containers=true
```
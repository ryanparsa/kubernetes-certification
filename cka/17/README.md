# Question 17

> **Solve this question on:** the "cka-lab-17" kind cluster

In *Namespace* `project-tiger` create a *Pod* named `tigers-reunite` of image `httpd:2-alpine` with labels `pod=container` and `container=pod`. Find out on which *Node* the *Pod* is scheduled. Connect to that *Node* and find the containerd container belonging to that *Pod*.

Using command `crictl`:

- Write the ID of the container and the `info.runtimeType` into `cka/17/course/pod-container.txt`
- Write the logs of the container into `cka/17/course/pod-container.log`

> [!NOTE]
> You can connect to a worker node using `docker exec -it cka-lab-17-worker bash` from your local machine

## Answer

> [!NOTE]
> In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

First we create the *Pod*:

```bash
kubectl -n project-tiger run tigers-reunite --image=httpd:2-alpine --labels "pod=container,container=pod"
pod/tigers-reunite created
```

Next we find out the *Node* it's scheduled on:

```bash
kubectl -n project-tiger get pod -o wide
NAME                                   READY   ...   NODE
tigers-for-rent-web-57558cfbf8-4tldr   1/1     ...   cka-lab-17-worker
tigers-for-rent-web-57558cfbf8-5pz4z   1/1     ...   cka-lab-17-control-plane
tigers-reunite                         1/1     ...   cka-lab-17-worker
```

Here it's `cka-lab-17-worker` so we exec into that *Node* and check the container info:

```bash
docker exec -it cka-lab-17-worker bash

crictl ps | grep tigers-reunite
ba62e5d465ff0   a7ccaadd632cf   2 minutes ago   Running   tigers-reunite   ...
```

### Step 1

Having the container we can `crictl inspect` it for the `runtimeType`:

```bash
crictl inspect ba62e5d465ff0 | grep runtimeType
    "runtimeType": "io.containerd.runc.v2",
```

Now we create the requested file:

```
# cka/17/course/pod-container.txt
ba62e5d465ff0 io.containerd.runc.v2
```

### Step 2

Finally we query the container logs:

```bash
crictl logs ba62e5d465ff0
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.29. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.29. Set the 'ServerName' directive globally to suppress this message
[Tue Oct 29 15:12:57.211347 2024] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.62 (Unix) configured -- resuming normal operations
[Tue Oct 29 15:12:57.211841 2024] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
```

Here we run `crictl logs` on the worker node and copy the content manually, that works if it's not a lot of logs. Otherwise we could redirect the logs into a file inside the container node and copy it out via `docker cp`.

The file should look like this:

```
# cka/17/course/pod-container.log
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.37. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.37. Set the 'ServerName' directive globally to suppress this message
[Mon Sep 13 13:32:18.555280 2021] [mpm_event:notice] [pid 1:tid 139929534545224] AH00489: Apache/2.4.41 (Unix) configured -- resuming normal operations
[Mon Sep 13 13:32:18.555610 2021] [core:notice] [pid 1:tid 139929534545224] AH00094: Command line: 'httpd -D FOREGROUND'
```

## Checklist (Score: 0/4)

- [ ] Pod `tigers-reunite` created with correct image and labels in `project-tiger` namespace
- [ ] `cka/17/course/pod-container.txt` contains correct container ID and runtimeType
- [ ] `cka/17/course/pod-container.log` contains container logs
- [ ] Pod is scheduled and running

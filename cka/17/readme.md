# Question 17 | Find Container of Pod and check info

Solve this question on: `ssh cka2556`

In Namespace `project-tiger` create a Pod named `tigers-reunite` of image `httpd:2-alpine` with labels `pod=container` and `container=pod`. Find out on which node the Pod is scheduled. Ssh into that node and find the containerd container belonging to that Pod.

Using command `crictl`:

- Write the ID of the container and the `info.runtimeType` into `/opt/course/17/pod-container.txt`
- Write the logs of the container into `/opt/course/17/pod-container.log`

> [!NOTE]
> You can connect to a worker node using `ssh cka2556-node1` or `ssh cka2556-node2` from `cka2556`

## Answer

> [!NOTE]
> In this environment `crictl` can be used for container management. In the real exam this could also be `docker`. Both commands can be used with the same arguments.

First we create the Pod:

```bash
➜ ssh cka2556

➜ candidate@cka2556:~$ k -n project-tiger run tigers-reunite --image=httpd:2-alpine --labels "pod=container,container=pod"
pod/tigers-reunite created
```

Next we find out the node it's scheduled on:

```bash
➜ candidate@cka2556:~$ k -n project-tiger get pod -o wide
NAME                                   READY   ...   NODE
tigers-for-rent-web-57558cfbf8-4tldr   1/1     ...   cka2556-node1
tigers-for-rent-web-57558cfbf8-5pz4z   1/1     ...   cka2556-node2
tigers-reunite                         1/1     ...   cka2556-node1
```

Here it's `cka2556-node1` so we ssh into that node and check the container info:

```bash
➜ candidate@cka2556:~$ ssh cka2556-node1

➜ candidate@cka2556-node1:~$ sudo -i

➜ root@cka2556-node1:~# crictl ps | grep tigers-reunite
ba62e5d465ff0   a7ccaadd632cf   2 minutes ago   Running   tigers-reunite   ...
```

### Step 1

Having the container we can `crictl inspect` it for the `runtimeType`:

```bash
➜ root@cka2556-node1:~# crictl inspect ba62e5d465ff0 | grep runtimeType
    "runtimeType": "io.containerd.runc.v2",
```

Now we create the requested file on `cka2556`:

```
# cka2556:/opt/course/17/pod-container.txt
ba62e5d465ff0 io.containerd.runc.v2
```

### Step 2

Finally we query the container logs:

```bash
➜ root@cka2556-node1:~# crictl logs ba62e5d465ff0
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.29. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.29. Set the 'ServerName' directive globally to suppress this message
[Tue Oct 29 15:12:57.211347 2024] [mpm_event:notice] [pid 1:tid 1] AH00489: Apache/2.4.62 (Unix) configured -- resuming normal operations
[Tue Oct 29 15:12:57.211841 2024] [core:notice] [pid 1:tid 1] AH00094: Command line: 'httpd -D FOREGROUND'
```

Here we run `crictl logs` on the worker node and copy the content manually, that works if it's not a lot of logs. Otherwise we could write the logs into a file on `cka2556-node1` and download the file via `scp` from `cka2556`.

The file should look like this:

```
# cka2556:/opt/course/17/pod-container.log
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.37. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.44.0.37. Set the 'ServerName' directive globally to suppress this message
[Mon Sep 13 13:32:18.555280 2021] [mpm_event:notice] [pid 1:tid 139929534545224] AH00489: Apache/2.4.41 (Unix) configured -- resuming normal operations
[Mon Sep 13 13:32:18.555610 2021] [core:notice] [pid 1:tid 139929534545224] AH00094: Command line: 'httpd -D FOREGROUND'
```

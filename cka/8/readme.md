# Question 8 | Update Kubernetes Version and join cluster

> **Solve this question on:** `ssh cka3962`

Your coworker notified you that node `cka3962-node1` is running an older Kubernetes version and is not even part of the cluster yet.

1. Update the node's Kubernetes to the exact version of the controlplane
2. Add the node to the cluster using kubeadm

> ℹ️ You can connect to the worker node using `ssh cka3962-node1` from `cka3962`

## Answer

### Update Kubernetes to controlplane version

Search in the docs for [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade):

```bash
➜ ssh cka3962
```

```bash
➜ candidate@cka3962:~$ k get node
NAME      STATUS   ROLES           AGE    VERSION
cka3962   Ready    control-plane   4h7m   v1.35.2
```

The controlplane node seems to be running Kubernetes 1.35.2.

```bash
➜ ssh cka3962-node1
```

```bash
➜ candidate@cka3962-node1:~$ sudo -i
```

```bash
➜ root@cka3962-node1:~# kubectl version
Client Version: v1.34.5
Kustomize Version: v5.7.1
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

```bash
➜ root@cka3962-node1:~# kubelet --version
Kubernetes v1.34.5
```

```bash
➜ root@cka3962-node1:~# kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"35", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.35.2", GitCommit:"fdc9d74cbf2da6754ebf81d56f80ae2948cd6425", GitTreeState:"clean", BuildDate:"2026-02-26T20:04:53Z", GoVersion:"go1.25.7", Compiler:"gc", Platform:"linux/amd64"}
```

Above we can see that kubeadm is already installed in the exact needed version, otherwise we would need to install it using `apt install kubeadm=1.35.2-1.1`.

With the correct kubeadm version we can continue:

```bash
➜ root@cka3962-node1:~# kubeadm upgrade node
error: couldn't create a Kubernetes client from file "/etc/kubernetes/kubelet.conf": failed to load admin kubeconfig: open /etc/kubernetes/kubelet.conf: no such file or directory
To see the stack trace of this error execute with --v=5 or higher
```

This is usually the proper command to upgrade a worker node. But as mentioned in the question description, this node is not yet part of the cluster. Hence there is nothing to update. We'll add the node to the cluster later using kubeadm join. For now we can continue with updating kubelet and kubectl:

```bash
➜ root@cka3962-node1:~# apt update
Hit:1 https://prod-cdn.packages.k8s.io/repositories/isv:/kubernetes:/core:/stable:/v1.34/deb  InRelease
Hit:2 https://prod-cdn.packages.k8s.io/repositories/isv:/kubernetes:/core:/stable:/v1.35/deb  InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
2 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

```bash
➜ root@cka3962-node1:~# apt show kubectl -a | grep 1.35
Version: 1.35.2-1.1
APT-Sources: https://pkgs.k8s.io/core:/stable:/v1.35/deb  Packages
Version: 1.35.1-1.1
APT-Sources: https://pkgs.k8s.io/core:/stable:/v1.35/deb  Packages
Version: 1.35.0-1.1
APT-Sources: https://pkgs.k8s.io/core:/stable:/v1.35/deb  Packages
```

```bash
➜ root@cka3962-node1:~# apt install kubectl=1.35.2-1.1 kubelet=1.35.2-1.1
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libevent-core-2.1-7t64 libjq1 libonig5 pastebinit python3-newt run-one squashfs-tools
Use 'apt autoremove' to remove them.
The following packages will be upgraded:
  kubectl kubelet
2 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Need to get 24.4 MB of archives.
After this operation, 49.2 kB of additional disk space will be used.
Get:1 https://pkgs.k8s.io/core:/stable:/v1.35/deb  kubectl 1.35.2-1.1 [11.2 MB]
Get:2 https://pkgs.k8s.io/core:/stable:/v1.35/deb  kubelet 1.35.2-1.1 [13.2 MB]
Fetched 24.4 MB in 1s (30.3 MB/s)
(Reading database ... 113742 files and directories currently installed.)
Preparing to unpack .../kubectl_1.35.2-1.1_amd64.deb ...
Unpacking kubectl (1.35.2-1.1) over (1.34.5-1.1) ...
Preparing to unpack .../kubelet_1.35.2-1.1_amd64.deb ...
Unpacking kubelet (1.35.2-1.1) over (1.34.5-1.1) ...
Setting up kubelet (1.35.2-1.1) ...
Setting up kubectl (1.35.2-1.1) ...
Scanning processes...
Scanning linux images...

Running kernel seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
```

```bash
➜ root@cka3962-node1:~# kubelet --version
Kubernetes v1.35.2
```

Now that we're up to date with kubeadm, kubectl and kubelet we can restart the kubelet:

```bash
➜ root@cka3962-node1:~# service kubelet restart
```

```bash
➜ root@cka3962-node1:~# service kubelet status
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
    Drop-In: /usr/lib/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: activating (auto-restart) (Result: exit-code) since Fri 2026-02-27 14:37:29 UTC; 5s ago
       Docs: https://kubernetes.io/docs/
    Process: 14101 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_AR>
   Main PID: 14101 (code=exited, status=1/FAILURE)
      CPU: 105ms
```

This is expected because the worker node hasn't joined the cluster yet, so no kubelet configuration exists. Let's join the node to the cluster.

### Join using kubeadm

```bash
➜ exit
```

```bash
➜ candidate@cka3962:~$ sudo -i
```

```bash
➜ root@cka3962:~# kubeadm token create --print-join-command
kubeadm join 192.168.100.31:6443 --token xpexct.yefojay1ejbq8akx --discovery-token-ca-cert-hash sha256:e2e45842688b5057af4e6431f04cc0d6aa3c0a1a11769a69fd28b6972b886e77
```

```bash
➜ root@cka3962:~# kubeadm token list
TOKEN                     TTL         EXPIRES                ...
3g4c7h.s0cz1hsinq6tfm4d   <forever>   <never>               ...
4olh95.0rj602m58qtqz0xp   19h         2026-02-28T10:27:35Z  ...
xpexct.yefojay1ejbq8akx   23h         2026-02-28T14:38:57Z  ...
```

We see the expiration of 23h for our token, we could adjust this by passing the ttl argument.

Next we connect again to `cka3962-node1` and simply execute the join command from above:

```bash
➜ ssh cka3962-node1
```

```bash
➜ root@cka3962-node1:~# kubeadm join 192.168.100.31:6443 --token xpexct.yefojay1ejbq8akx --discovery-token-ca-cert-hash sha256:e2e45842688b5057af4e6431f04cc0d6aa3c0a1a11769a69fd28b6972b886e77
[preflight] Running pre-flight checks
        [WARNING ContainerRuntimeVersion]: You must update your container runtime to a version that supports the CRI method RuntimeConfig. Falling back to using cgroupDriver from kubelet config will be removed in 1.36. For more information, see https://git.k8s.io/enhancements/keps/sig-node/4033-group-driver-detection-over-cri
[preflight] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
[preflight] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/instance-config.yaml"
[patches] Applied patch of type "application/strategic-merge-patch+json" to target "kubeletconfiguration"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 1.02973788s
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

```bash
➜ root@cka3962-node1:~# service kubelet status
● kubelet.service - kubelet: The Kubernetes Node Agent
     Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
    Drop-In: /usr/lib/systemd/system/kubelet.service.d
             └─10-kubeadm.conf
     Active: active (running) since Fri 2026-02-27 14:39:57 UTC; 4s ago
       Docs: https://kubernetes.io/docs/
   Main PID: 14321 (kubelet)
      Tasks: 10 (limit: 1113)
     Memory: 22.1M (peak: 22.6M)
        CPU: 1.542s
     CGroup: /system.slice/kubelet.service
             └─14321 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernete>

Feb 27 14:39:57 cka3962-node1 kubelet[14321]: I0227 14:39:57.979055   14321 kuberuntime_manager.go:263] "Container runtime netw>
Feb 27 14:39:58 cka3962-node1 kubelet[14321]: I0227 14:39:58.001189   14321 kubelet.go:2424] "Started kubelet"
Feb 27 14:40:01 cka3962-node1 kubelet[14321]: I0227 14:40:01.222198   14321 reconciler_common.go:251] "operationExecutor.VerifyCont>
...
```

> ℹ️ If you have troubles with `kubeadm join` you might need to run `kubeadm reset` before

Finally we check the node status:

```bash
➜ exit
```

```bash
➜ root@cka3962:~# k get node
NAME             STATUS     ROLES           AGE     VERSION
cka3962          Ready      control-plane   4h13m   v1.35.2
cka3962-node1    NotReady   <none>          24s     v1.35.2
```

Give it a bit of time till the node is ready.

```bash
➜ root@cka3962:~# k get node
NAME             STATUS   ROLES           AGE     VERSION
cka3962          Ready    control-plane   4h13m   v1.35.2
cka3962-node1    Ready    <none>          34s     v1.35.2
```

We see `cka3962-node1` is now available and up to date.

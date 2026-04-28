# Question 87

> **Solve this question on:** `cka-lab-cp` (control plane VM)

Your coworker notified you that node `cka-lab-worker` is running an older Kubernetes version and is not part of the cluster yet. Add the node to the cluster and ensure it runs the same Kubernetes version as the control plane.

1. Check the current Kubernetes version on the control plane

1. Upgrade the worker node to match the control plane version using `kubeadm`

1. Confirm the node has joined the cluster and is `Ready`

# Question 81

> **Solve this question on:** the `cka-lab` kind cluster

You're asked to perform the following in *Namespace* `app`:

1. Create a *ClusterRole* named `app-reader` that allows `get`, `list`, and `watch` on *Pods* and *Deployments*

1. Create a *ClusterRoleBinding* named `app-reader` that binds the *ClusterRole* to *ServiceAccount* `app-reader` in *Namespace* `app`

1. Configure a new kubeconfig context pointing to the cluster but using the `app` *Namespace* by default

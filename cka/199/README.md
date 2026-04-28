# Question 199

> **Solve this question on:** `ssh cka412`

Create a *Pod* named `check-ip` in *Namespace* `default` using image `httpd:2.4-alpine`.

1. Expose it on port `80` as a *ClusterIP* *Service* named `check-ip-service`. Note the IP address of that *Service*.

1. Change the *Service* CIDR to `11.96.0.0/12` for the cluster.

1. Create a second *Service* named `check-ip-service2` pointing to the same *Pod*.

1. Confirm the second *Service* gets an IP address from the new CIDR range `11.96.0.0/12`.

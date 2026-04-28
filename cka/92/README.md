# Question 92

> **Solve this question on:** the `cka-lab` kind cluster

The team from Project r500 wants to replace their *Ingress* (`networking.k8s.io`) with a *Gateway API* (`gateway.networking.k8s.io`) solution.

Implement the following in *Namespace* `project-r500`:

1. Create an `HTTPRoute` resource that replaces the existing *Ingress* and routes traffic to the same backend service

1. Delete the old *Ingress* once the *HTTPRoute* is in place

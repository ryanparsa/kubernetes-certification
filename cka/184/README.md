# Question 184

> **Solve this question on:** `ssh cka4774`

Previously the application `api-gateway` used an external autoscaler which should now be replaced with a *HorizontalPodAutoscaler* (*HPA*). The application has been deployed using Kustomize configs at `/opt/course/5/api-gateway/staging` and `/opt/course/5/api-gateway/prod`.

Using the Kustomize config at `/opt/course/5/api-gateway`, do the following:

1. Remove the *ConfigMap* `horizontal-scaling-config` completely

1. Add an *HPA* named `api-gateway` for the *Deployment* `api-gateway` with minimum `2` and maximum `6` replicas, scaling at `78%` average CPU utilisation

Apply the changes to both `staging` and `prod` namespaces and confirm they're correct.

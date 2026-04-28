# Question 84

> **Solve this question on:** the `cka-lab` kind cluster

Previously the application `api-gateway` used an external autoscaler which should now be replaced with a *HorizontalPodAutoscaler* (*HPA*). The application is deployed to *Namespaces* `api-gateway-staging` and `api-gateway-prod`.

Do the following:

1. Remove the `ConfigMap` named `api-gateway-autoscaler` and set the `replicas` of the *Deployment* `api-gateway` to `0` in **both** namespaces

1. Create a *HorizontalPodAutoscaler* named `gateway` in **both** namespaces for the `api-gateway` *Deployment*, with:
   - Minimum replicas: `2`
   - Maximum replicas: `3`
   - Target CPU utilization: `50%`

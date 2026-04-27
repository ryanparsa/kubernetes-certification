# Question 5

> **Solve this question on:** the "cka-lab-5" kind cluster

Previously the application `api-gateway` used some external autoscaler which should now be replaced with a *HorizontalPodAutoscaler* (*HPA*). The application has been deployed to *Namespaces* `api-gateway-staging` and `api-gateway-prod` like this:

```
kubectl kustomize cka/5/lab/api-gateway/staging | kubectl apply -f -
kubectl kustomize cka/5/lab/api-gateway/prod | kubectl apply -f -
```

Using the Kustomize config at `cka/5/lab/api-gateway` do the following:

1. Remove the *ConfigMap* `horizontal-scaling-config` completely
2. Add *HPA* named `api-gateway` for the *Deployment* `api-gateway` with min `2` and max `4` replicas. It should scale at `50%` average CPU utilisation
3. In prod the *HPA* should have max `6` replicas
4. Apply your changes for staging and prod so they're reflected in the cluster

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

# Question 34

> **Solve this question on:** the "cka-lab-34" kind cluster

There is Kustomize config available at `cka/34/lab/operator`. It installs an operator which works with different *CRDs*. It has been deployed like this:

```bash
kubectl kustomize cka/34/lab/operator/prod | kubectl apply -f -
```

Perform the following changes in the Kustomize base config:

1. The operator needs to `list` certain *CRDs*. Check the logs to find out which ones and adjust the permissions for *Role* `operator-role`
2. Add a new *Student* resource called `student4` with any name and description

Deploy your Kustomize config changes to prod.

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`

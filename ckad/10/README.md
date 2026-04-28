# Question 10

> **Solve this question on:** `ckad-lab-10`

Perform the following resource management tasks:

1. Create a namespace `quota-ns`. Create a ResourceQuota named `ns-quota` in `quota-ns` with the following limits:
   - `requests.cpu: 1`
   - `requests.memory: 500Mi`
   - `limits.cpu: 2`
   - `limits.memory: 1Gi`
   - `pods: 4`

2. Create a LimitRange named `container-limits` in `quota-ns` with default container values:
   - `defaultRequest.cpu: 100m`, `defaultRequest.memory: 64Mi`
   - `default.cpu: 200m`, `default.memory: 128Mi`

3. Create a pod named `resource-pod` with image `nginx` in `quota-ns` with **explicit** resource requests (`cpu: 250m`, `memory: 128Mi`) and limits (`cpu: 500m`, `memory: 256Mi`).

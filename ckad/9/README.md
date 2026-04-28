# Question 9

> **Solve this question on:** `ckad-lab-9`

Perform the following security-related tasks:

1. Create a namespace called `secure`. Create a ServiceAccount named `app-sa` in namespace `secure`.

2. Create a pod named `secure-pod` with image `nginx` in namespace `secure` with the following security configuration:
   - Uses ServiceAccount `app-sa`
   - Runs as user ID `1000` (pod-level `runAsUser`)
   - Container has capability `NET_ADMIN` added
   - Container has `allowPrivilegeEscalation: false`

Verify the pod is running and confirm the security context is applied correctly.

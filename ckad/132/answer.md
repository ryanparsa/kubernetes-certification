## Answer

**Reference:** <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>

```yaml
# lab/pod-13.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-13
  namespace: default
spec:
  containers:
  - name: pod-13
    image: busybox:1.31.0
    command: ["sh", "-c", "sleep 9999"]
    livenessProbe:
      exec:
        command: ["true"]
    readinessProbe:
      exec:
        command: ["sh", "-c", "wget -T2 -O- http://service-13"]
      initialDelaySeconds: 15
      periodSeconds: 5
```

```bash
kubectl apply -f lab/pod-13.yaml
kubectl get pod pod-13
kubectl describe pod pod-13 | grep -A10 "Liveness\|Readiness"
```

## Checklist (Score: 0/4)

- [ ] Pod `pod-13` running in Namespace `default` with image `busybox:1.31.0`
- [ ] `livenessProbe` configured to run `true`
- [ ] `readinessProbe` checks `http://service-13` with `wget -T2 -O-`
- [ ] `readinessProbe` has `initialDelaySeconds: 15` and `periodSeconds: 5`

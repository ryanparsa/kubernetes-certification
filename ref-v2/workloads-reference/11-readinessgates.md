# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 11. readinessGates

`readinessGates` let external controllers block a pod from becoming `Ready` by requiring
custom `PodCondition` entries to be `True` before the pod is considered ready. This is
commonly used by load-balancer controllers and service meshes.

Without a readiness gate, a pod becomes `Ready` as soon as all containers pass their
`readinessProbe`. With a readiness gate, the pod also waits for the named condition to
be set to `True` by an external controller.

### How it works

1. Pod spec declares a `readinessGate` with a `conditionType` name.
2. An external controller (e.g. a load-balancer controller) watches pods.
3. The controller sets that `PodCondition` to `True` once its own check passes
   (e.g. the pod has been registered in the load-balancer target group).
4. Only then does the pod transition to `Ready = True`.

### Spec example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
spec:
  readinessGates:
  - conditionType: "target-health.elbv2.k8s.aws/tg-abc123"   # custom condition name
  containers:
  - name: app
    image: nginx:1.25
    readinessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Inspecting readiness conditions

```bash
# View all pod conditions (including custom gates)
kubectl get pod my-pod -o jsonpath='{.status.conditions}' | jq .

# Example output — pod waits for the custom condition:
# [
#   {"type":"Initialized","status":"True"},
#   {"type":"Ready","status":"False"},           ← still False
#   {"type":"ContainersReady","status":"True"},
#   {"type":"PodScheduled","status":"True"},
#   {"type":"target-health.elbv2.k8s.aws/tg-abc123","status":"False"}  ← gate not met
# ]

# After the external controller sets the condition to True:
# {"type":"target-health.elbv2.k8s.aws/tg-abc123","status":"True"}
# → pod.status.conditions[?type=="Ready"].status becomes "True"

# Check if the ready gate is blocking readiness
kubectl describe pod my-pod | grep -A 10 "Conditions:"
```

### Patching a readiness gate condition (simulating what a controller does)

```bash
# External controller sets the custom condition via status patch
kubectl patch pod my-pod --subresource=status --type=json \
  -p='[{"op":"add","path":"/status/conditions/-","value":
    {"type":"target-health.elbv2.k8s.aws/tg-abc123",
     "status":"True",
     "lastTransitionTime":"2025-01-01T00:00:00Z"}}]'
```

> `readinessGates` are distinct from `readinessProbe`. The probe is evaluated by kubelet
> inside the container; the gate is a pod-level condition set by an external entity.

---

# Hints — Task 29

## Hint 1
`kubectl -n web describe pod <name>` — look at the Events section.
What is the liveness probe trying to connect to?

## Hint 2
Compare `containerPort` in the Deployment spec against `livenessProbe.httpGet.port`.
They don't match — one is `3000`, the other is `8080`.

## Hint 3
The liveness probe must target the port the container actually listens on.
Exit code `137` means the kubelet killed the container after 3 consecutive probe failures.

## Solution

```bash
kubectl -n web patch deployment api-server --type=json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/livenessProbe/httpGet/port","value":3000}]'

kubectl -n web rollout status deployment/api-server
```

**Reflex:** Restarts + never Ready + Exit 137 = liveness probe killing the container.
Always check `Events` in `kubectl describe pod` first.

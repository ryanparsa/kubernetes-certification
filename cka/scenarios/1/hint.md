# Hints — Task 1

## Hint 1
`kubectl -n troubleshoot get pods` — what status are they in?
`kubectl -n troubleshoot logs <pod> --previous` — what does the container print before it dies?

## Hint 2
The container's `command` field is `sh -c "echo starting; exit 7"` — it exits non-zero on purpose.
You need a command that **stays running**.

## Hint 3
`kubectl -n troubleshoot edit deployment crashy` and replace the command, e.g.:
```yaml
command: ["sh","-c","while true; do echo alive; sleep 30; done"]
```
or simply remove the `command` field so busybox runs its default.

## Solution

```bash
kubectl -n troubleshoot patch deployment crashy --type=json -p='[
  {"op":"replace","path":"/spec/template/spec/containers/0/command","value":["sh","-c","sleep infinity"]}
]'
kubectl -n troubleshoot rollout status deployment/crashy
```

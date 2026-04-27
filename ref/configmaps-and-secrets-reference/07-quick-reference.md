# ConfigMaps and Secrets Reference — 7. Quick Reference

> Part of [ConfigMaps and Secrets Reference](../ConfigMaps and Secrets Reference.md)


| Task | ConfigMap | Secret |
|---|---|---|
| Create from literals | `kubectl create configmap cm --from-literal=k=v` | `kubectl create secret generic s --from-literal=k=v` |
| Create from file | `kubectl create configmap cm --from-file=file` | `kubectl create secret generic s --from-file=file` |
| Inject all keys as env vars | `envFrom.configMapRef` | `envFrom.secretRef` |
| Inject single key as env var | `env[].valueFrom.configMapKeyRef` | `env[].valueFrom.secretKeyRef` |
| Mount as files | `volumes[].configMap` | `volumes[].secret` |
| Decode value | — | `kubectl get secret ... -o jsonpath='{.data.KEY}' \| base64 --decode` |

> **Important:** Pods do **not** automatically pick up ConfigMap or Secret changes
> when using `envFrom`/`env`. The pod must be restarted. Volume-mounted files update
> automatically (with a short kubelet sync delay).

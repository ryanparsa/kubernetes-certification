# Kubernetes Troubleshooting Reference

[← Back to index](../README.md)

---

## 6. Cluster Event Logging

```bash
# All events in a namespace (sorted by time)
kubectl get events -n <ns> --sort-by='.lastTimestamp'

# All events cluster-wide
kubectl get events -A --sort-by='.lastTimestamp'

# Watch events live
kubectl get events -n <ns> -w

# Only Warning events
kubectl get events -n <ns> --field-selector type=Warning

# Events for a specific object
kubectl get events -n <ns> \
  --field-selector involvedObject.name=<pod-name>

# Events for a specific kind (Pod, Node, etc.)
kubectl get events -A \
  --field-selector involvedObject.kind=Node

# Get reason from events
kubectl get events -n <ns> -o json | \
  jq '.items[] | {name:.involvedObject.name, reason:.reason, message:.message}'
```

### API server audit log

The API server can write a structured audit log for every request. Requires:
1. An **audit policy** file that defines which requests to log and at what detail level.
2. API server flags that point to the policy file and set the log destination.

#### Audit levels

| Level | What is recorded |
|---|---|
| `None` | Do not log this event |
| `Metadata` | Request metadata only (user, verb, resource, namespace, timestamp) — no request/response body |
| `Request` | Metadata + request body |
| `RequestResponse` | Metadata + request body + response body (most verbose) |

#### Audit stages

| Stage | When it fires |
|---|---|
| `RequestReceived` | As soon as the API server receives the request, before routing |
| `ResponseStarted` | After response headers are sent but before the response body (long-running requests: watches) |
| `ResponseComplete` | After the response body is fully sent |
| `Panic` | When the API server panics while handling a request |

#### Audit policy YAML

Rules are evaluated top-to-bottom; the first matching rule wins.

```yaml
# /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
# Rules are evaluated in order; first match wins
rules:
  # Do not log read-only requests to certain non-resource URLs
  - level: None
    nonResourceURLs:
    - /healthz
    - /readyz
    - /livez

  # Do not log watch calls from the system:nodes group
  - level: None
    userGroups: ["system:nodes"]
    verbs: ["watch"]

  # Log metadata-only for read requests on secrets and configmaps
  - level: Metadata
    resources:
    - group: ""
      resources: ["secrets", "configmaps"]
    verbs: ["get", "list", "watch"]

  # Log full request+response for writes to secrets
  - level: RequestResponse
    resources:
    - group: ""
      resources: ["secrets"]
    verbs: ["create", "update", "patch", "delete"]

  # Default: log metadata for everything else
  - level: Metadata
```

#### Enabling audit logging on the API server

Edit `/etc/kubernetes/manifests/kube-apiserver.yaml` and add flags + volume mounts:

```yaml
spec:
  containers:
  - name: kube-apiserver
    command:
    - kube-apiserver
    # ... existing flags ...
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-log-maxsize=100          # rotate at 100 MB
    - --audit-log-maxbackup=5          # keep 5 rotated files
    - --audit-log-maxage=30            # delete files older than 30 days
    volumeMounts:
    - name: audit-policy
      mountPath: /etc/kubernetes/audit-policy.yaml
      readOnly: true
    - name: audit-log
      mountPath: /var/log/kubernetes
  volumes:
  - name: audit-policy
    hostPath:
      path: /etc/kubernetes/audit-policy.yaml
      type: File
  - name: audit-log
    hostPath:
      path: /var/log/kubernetes
      type: DirectoryOrCreate
```

```bash
# Verify flags are present after saving the manifest (kubelet auto-restarts the static pod)
grep audit /etc/kubernetes/manifests/kube-apiserver.yaml

# Tail the audit log (jq makes it readable)
tail -f /var/log/kubernetes/audit.log | jq .

# Find which user deleted a secret
cat /var/log/kubernetes/audit.log | \
  jq 'select(.verb=="delete" and .objectRef.resource=="secrets") |
      {user:.user.username, ns:.objectRef.namespace, name:.objectRef.name}'
```

---

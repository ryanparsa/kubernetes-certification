# Kubernetes Storage Reference

[← Back to index](../README.md)

---

## 4. Volume Types

### emptyDir

Temporary scratch space shared between containers in the same Pod. Deleted when the pod
is removed. Survives container restarts.

```yaml
volumes:
- name: shared-data
  emptyDir: {}
  # emptyDir:
  #   medium: Memory   # RAM-backed tmpfs
  #   sizeLimit: 128Mi
```

### hostPath

Mounts a directory from the **node's** filesystem. Data persists as long as the node
exists but is NOT portable across nodes.

```yaml
volumes:
- name: host-log
  hostPath:
    path: /var/log/myapp
    type: DirectoryOrCreate   # Directory | File | Socket | CharDevice | BlockDevice
```

> ⚠️ Security risk: gives pod access to node filesystem. Avoid in production.

### configMap

Mount a ConfigMap as files.

```yaml
volumes:
- name: config
  configMap:
    name: my-config
    items:
    - key: app.properties
      path: application.properties   # filename inside the mount
```

### secret

Mount a Secret as files. Files are base64-decoded automatically.

```yaml
volumes:
- name: tls-certs
  secret:
    secretName: my-tls
    defaultMode: 0400    # restrict permissions
```

### projected

Combines multiple sources (serviceAccountToken, configMap, secret, downwardAPI) into
a single mount point.

```yaml
volumes:
- name: token-and-ca
  projected:
    sources:
    - serviceAccountToken:
        path: token
        expirationSeconds: 3600
        audience: api
    - configMap:
        name: kube-root-ca.crt
        items:
        - key: ca.crt
          path: ca.crt
    - downwardAPI:
        items:
        - path: namespace
          fieldRef:
            fieldPath: metadata.namespace
```

> This is the default volume injected into every pod at
> `/var/run/secrets/kubernetes.io/serviceaccount/`.

### nfs

```yaml
volumes:
- name: nfs-vol
  nfs:
    server: nfs-server.example.com
    path: /exports/mydata
    readOnly: false
```

---

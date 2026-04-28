## Answer

**Reference:** https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/

### Confirm the current environment variable

```bash
kubectl describe deployment nginx-deployment -n set-env-namespace | grep -i env -A 2
```

Expected output:

```console
    Environment:
      TIER:  web
```

### Update the environment variable

```bash
kubectl set env deployment/nginx-deployment TIER=app -n set-env-namespace
```

### Verify the change

```bash
kubectl describe deployment nginx-deployment -n set-env-namespace | grep -i env -A 2
kubectl rollout status deployment/nginx-deployment -n set-env-namespace
```

Expected output after update:

```console
    Environment:
      TIER:  app
```

## Checklist (Score: 0/2)

- [ ] Deployment `nginx-deployment` exists in `set-env-namespace` with env var `TIER`
- [ ] Environment variable `TIER` updated from `web` to `app`

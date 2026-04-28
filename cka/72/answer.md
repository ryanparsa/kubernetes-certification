## Answer

**Reference:** https://gateway-api.sigs.k8s.io/guides/http-routing/

### Create HTTPRoute

```bash
kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: traffic-director
  namespace: project-r500
spec:
  parentRefs:
  - name: main
    namespace: project-r500
  hostnames:
  - "72.gateway"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /desktop
    backendRefs:
    - name: web-desktop
      port: 80
  - matches:
    - path:
        type: PathPrefix
        value: /mobile
    backendRefs:
    - name: web-mobile
      port: 80
  - matches:
    - path:
        type: PathPrefix
        value: /api/route
      headers:
      - name: User-Agent
        value: mobile
    filters:
    - type: RequestRedirect
      requestRedirect:
        path:
          type: ReplaceFullPath
          value: /mobile
        statusCode: 302
EOF
```

## Checklist (Score: 0/3)

- [ ] HTTPRoute `traffic-director` exists in namespace `project-r500`
- [ ] HTTPRoute replicates routes `/desktop` and `/mobile` from Ingress
- [ ] HTTPRoute redirects `/api/route` to `/mobile` when `User-Agent` is `mobile`

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

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

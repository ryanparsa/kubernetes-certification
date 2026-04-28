#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBECONFIG_FILE="$SCRIPT_DIR/../lab/kubeconfig.yaml"
if [ -f "$KUBECONFIG_FILE" ]; then
  export KUBECONFIG="$KUBECONFIG_FILE"
fi

kubectl apply -f - <<EOF
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.data.example.com
spec:
  group: data.example.com
  names:
    kind: Backup
    listKind: BackupList
    plural: backups
    singular: backup
    shortNames:
    - bkp
  scope: Namespaced
  versions:
  - name: v1alpha1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            description: BackupSpec defines the desired state of Backup
            properties:
              source:
                type: string
                description: Source data location
              destination:
                type: string
                description: Destination where backups should be stored
            required: ["source", "destination"]
EOF

kubectl wait crd backups.data.example.com --for=condition=Established --timeout=60s

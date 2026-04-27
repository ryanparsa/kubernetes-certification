#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/../lab/kubeconfig.yaml"

# 1. Adjust RBAC in base/rbac.yaml
cat <<EOF > "$SCRIPT_DIR/../lab/operator/base/rbac.yaml"
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: operator-role
  namespace: default
rules:
- apiGroups:
  - education.killer.sh
  resources:
  - students
  - classes
  verbs:
  - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: operator-rolebinding
  namespace: default
subjects:
  - kind: ServiceAccount
    name: operator
    namespace: default
roleRef:
  kind: Role
  name: operator-role
  apiGroup: rbac.authorization.k8s.io
EOF

# 2. Add new Student resource in base/students.yaml
cat <<EOF >> "$SCRIPT_DIR/../lab/operator/base/students.yaml"
---
apiVersion: education.killer.sh/v1
kind: Student
metadata:
  name: student4
spec:
  name: Some Name
  description: Some Description
EOF

# 3. Apply the kustomize config changes to prod
kubectl kustomize "$SCRIPT_DIR/../lab/operator/prod" | kubectl apply -f -

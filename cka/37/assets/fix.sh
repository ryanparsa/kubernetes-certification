#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export KUBECONFIG="$SCRIPT_DIR/kubeconfig.yaml"

# 1. Create the Pod and initial Service
kubectl run check-ip --image=httpd:2-alpine
kubectl expose pod check-ip --name check-ip-service --port 80

# 2. Change Service CIDR
# Update kube-apiserver
docker exec cka-lab-37-control-plane sed -i 's/--service-cluster-ip-range=[^ ]*/--service-cluster-ip-range=11.96.0.0\/12/' /etc/kubernetes/manifests/kube-apiserver.yaml

# Update kube-controller-manager
docker exec cka-lab-37-control-plane sed -i 's/--service-cluster-ip-range=[^ ]*/--service-cluster-ip-range=11.96.0.0\/12/' /etc/kubernetes/manifests/kube-controller-manager.yaml

# Wait for components to restart
# Usually we would wait for the pods to be ready, but here we'll just wait a bit or use a more robust check
echo "Waiting for control plane components to restart..."
sleep 30

# 3. Update ServiceCIDR resources
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata:
  name: svc-cidr-new
spec:
  cidrs:
  - 11.96.0.0/12
EOF

kubectl delete servicecidr kubernetes --ignore-not-found

# 4. Create second Service
kubectl expose pod check-ip --name check-ip-service2 --port 80

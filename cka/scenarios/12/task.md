# Task 12 — Cluster Architecture: Kustomize

**Context:** Cluster `cka-task-12` (`export KUBECONFIG=$PWD/kubeconfig`)

A Kustomize project is laid out in `./k8s`:

```
k8s/
  base/
    deployment.yaml        # Deployment "api", 1 replica, namespace not set
    kustomization.yaml
  overlays/
    prod/
      kustomization.yaml   # references base, sets namespace=ops
```

## Objective

1. Without editing `base/deployment.yaml`, add a **patch** in `overlays/prod` that scales
   the `api` Deployment to **4 replicas** when the prod overlay is applied.
2. Apply the prod overlay with `kubectl apply -k k8s/overlays/prod`.
3. The Deployment must end up in namespace **`ops`** with **4 ready replicas**.

## Verify

```
./test.sh
```

# ✅ CKA 2026 — 200 Expert-Level Scenarios & Tasks
> **Kubernetes v1.34 | Passing Score: 66% | Duration: 2 hours | ~17 tasks**
> Legend: 🟢 Standard · 🟡 Tricky · 🔴 Hard / Exam Trap
> Each scenario includes: **Context → Task → Key Commands → Verification → ⚠️ Watch Out**

---

## 🏗️ DOMAIN 1 — Cluster Architecture, Installation & Configuration (25%)

---

### RBAC

- [ ] 🟢 **#001 — Create a namespaced Role and RoleBinding**
  **Context:** A CI pipeline uses ServiceAccount `ci-bot` in namespace `dev` and needs to read pod status.
  **Task:** Create a Role `pod-reader` in namespace `dev` with `get`, `list`, `watch` verbs on `pods`. Bind it to ServiceAccount `ci-bot` in the same namespace using a RoleBinding.


  **Key Commands:**
  ```bash
  kubectl create role pod-reader --verb=get,list,watch --resource=pods -n dev
  kubectl create rolebinding ci-bot-binding --role=pod-reader --serviceaccount=dev:ci-bot -n dev
  ```
  **Verify:** `kubectl auth can-i list pods --as=system:serviceaccount:dev:ci-bot -n dev` → should return `yes`
  **⚠️ Watch Out:** `--serviceaccount` takes the format `namespace:name`. Using just the name without the namespace prefix will silently fail.

---

- [ ] 🟢 **#002 — Create a ClusterRole and ClusterRoleBinding for a user**
  **Context:** User `jane` is a platform engineer who needs to inspect nodes across the cluster.
  **Task:** Create ClusterRole `node-viewer` with `get`, `list`, `watch` on `nodes`. Bind it to user `jane` using a ClusterRoleBinding named `jane-node-viewer`.


  **Key Commands:**
  ```bash
  kubectl create clusterrole node-viewer --verb=get,list,watch --resource=nodes
  kubectl create clusterrolebinding jane-node-viewer --clusterrole=node-viewer --user=jane
  ```
  **Verify:** `kubectl auth can-i list nodes --as=jane` → `yes`
  **⚠️ Watch Out:** ClusterRoleBindings grant cluster-wide access. If the question asks for namespace-scoped access, use a RoleBinding (which can reference a ClusterRole) instead.

---

- [ ] 🟡 **#003 — Minimal RBAC for cross-namespace Deployment listing**
  **Context:** ServiceAccount `api-sa` in namespace `prod` needs to list Deployments in all namespaces. Your task is to grant the minimal required permissions.
  **Task:** Create a ClusterRole `deployment-lister` with `get`, `list` on `deployments`. Create a ClusterRoleBinding binding it to ServiceAccount `api-sa` in namespace `prod`.


  **Key Commands:**
  ```bash
  kubectl create clusterrole deployment-lister --verb=get,list --resource=deployments
  kubectl create clusterrolebinding api-sa-deployment-lister \
    --clusterrole=deployment-lister \
    --serviceaccount=prod:api-sa
  ```
  **Verify:** `kubectl auth can-i list deployments --as=system:serviceaccount:prod:api-sa -A` → `yes`
  **⚠️ Watch Out:** Cross-namespace access always requires a ClusterRoleBinding, never a RoleBinding. A RoleBinding only works within one namespace even if it references a ClusterRole.

---

- [ ] 🟡 **#004 — Debug and fix broken RBAC without touching the pod**
  **Context:** A pod running as ServiceAccount `app-sa` in namespace `staging` is crashing because it cannot read ConfigMaps. The pod spec is correct and must not be modified.
  **Task:** Identify the missing RBAC permission and create the appropriate Role + RoleBinding to fix it.


  **Key Commands:**
  ```bash
  kubectl auth can-i get configmaps --as=system:serviceaccount:staging:app-sa -n staging
  kubectl create role configmap-reader --verb=get,list,watch --resource=configmaps -n staging
  kubectl create rolebinding app-sa-configmap --role=configmap-reader \
    --serviceaccount=staging:app-sa -n staging
  ```
  **Verify:** `kubectl auth can-i get configmaps --as=system:serviceaccount:staging:app-sa -n staging` → `yes`. Pod should transition from `CrashLoopBackOff` to `Running`.
  **⚠️ Watch Out:** Use `kubectl auth can-i` before and after to confirm the exact verb that was failing. Don't over-grant — give only what's needed.

---

- [ ] 🔴 **#005 — Create Role with subresource access and verify with auth can-i**
  **Context:** A debugging tool needs the ability to `create` and `delete` pods, and also exec into them (`pods/exec`). Standard roles don't cover subresources by default.
  **Task:** Create Role `debug-role` in namespace `dev` with `create`, `delete` on `pods` and `create` on `pods/exec`. Bind it to ServiceAccount `debug-sa`. Write the combined auth verification output to `/tmp/debug-auth.txt`.

  **Key Commands:**
  ```bash
  # Must use YAML for subresources — kubectl create role doesn't support them imperatively
  cat <<EOF | kubectl apply -f -
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: debug-role
    namespace: dev
  rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["create", "delete"]
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create"]
  EOF
  kubectl create rolebinding debug-sa-binding --role=debug-role \
    --serviceaccount=dev:debug-sa -n dev
  kubectl auth can-i create pods/exec --as=system:serviceaccount:dev:debug-sa -n dev \
    > /tmp/debug-auth.txt
  ```
  **Verify:** `/tmp/debug-auth.txt` should contain `yes`.
  **⚠️ Watch Out:** Subresources like `pods/exec`, `pods/log`, `pods/portforward` **cannot** be added via `kubectl create role --resource=pods/exec`. You must write the YAML manually with the subresource listed separately.

---

- [ ] 🟡 **#006 — Verify RBAC permissions and save output**
  **Context:** You need to audit whether user `bob` has delete access to secrets in `kube-system`.
  **Task:** Check if `bob` can delete secrets in the `kube-system` namespace and save the result to `/tmp/bob-check.txt`.

  **Key Commands:**
  ```bash
  kubectl auth can-i delete secrets --as=bob -n kube-system > /tmp/bob-check.txt
  ```
  **Verify:** `cat /tmp/bob-check.txt` → should contain `no`
  **⚠️ Watch Out:** Don't confuse `--as=bob` (impersonating a user) with `--as=system:serviceaccount:ns:name` (impersonating a ServiceAccount). The format differs and both are tested.

---

- [ ] 🟢 **#007 — Create an aggregated ClusterRole**
  **Context:** You want a custom ClusterRole that accumulates the permissions from the built-in `view`, `edit`, and `admin` roles and also picks up any future custom roles labeled for aggregation.
  **Task:** Create a ClusterRole `super-viewer` that uses `aggregationRule` to aggregate all ClusterRoles with label `rbac.example.com/aggregate: "true"`. Also label the built-in `view` ClusterRole with that label.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole
  metadata:
    name: super-viewer
  aggregationRule:
    clusterRoleSelectors:
    - matchLabels:
        rbac.example.com/aggregate: "true"
  rules: []
  EOF
  kubectl label clusterrole view rbac.example.com/aggregate=true
  ```
  **Verify:** `kubectl describe clusterrole super-viewer` should show inherited rules from `view`.
  **⚠️ Watch Out:** The aggregated ClusterRole itself has `rules: []` — rules come entirely from the matched ClusterRoles. Don't add rules manually to the aggregator.

---

- [ ] 🟡 **#008 — Fix pod failing to mount ServiceAccount token**
  **Context:** A pod in namespace `web` uses `serviceAccountName: app-sa` but fails to start because the ServiceAccount doesn't exist. The pod manifest is at `/opt/pods/app-pod.yaml`.
  **Task:** Create ServiceAccount `app-sa` in namespace `web`, then apply the pod manifest.

  **Key Commands:**
  ```bash
  kubectl create serviceaccount app-sa -n web
  kubectl apply -f /opt/pods/app-pod.yaml
  ```
  **Verify:** `kubectl get pod -n web` → pod should be `Running`. `kubectl describe pod -n web <pod>` should show the SA token mounted.
  **⚠️ Watch Out:** Kubernetes does not auto-create ServiceAccounts referenced in pod specs. If `serviceAccountName` is specified and doesn't exist, the pod stays in `Pending` with an obscure admission error.

---

### kubeadm & Cluster Lifecycle

- [ ] 🟢 **#009 — Initialize a control plane with kubeadm**
  **Context:** You are setting up a new single-node control plane from scratch on a fresh VM.
  **Task:** Initialize the cluster with pod network CIDR `10.244.0.0/16`, API server advertise address `192.168.1.10`, and save the resulting join command to `/tmp/join.txt`.

  **Key Commands:**
  ```bash
  kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.1.10 \
    | tee /tmp/kubeadm-init.log
  # Extract join command
  tail -2 /tmp/kubeadm-init.log > /tmp/join.txt
  # Setup kubeconfig
  mkdir -p ~/.kube
  cp /etc/kubernetes/admin.conf ~/.kube/config
  ```
  **Verify:** `kubectl get nodes` → control plane node appears as `Ready` (after installing a CNI).
  **⚠️ Watch Out:** `kubeadm init` alone doesn't make the node Ready. You must install a CNI plugin (e.g., Flannel, Calico, Weave) before the node transitions to Ready.

---

- [ ] 🟢 **#010 — Join a worker node to an existing cluster**
  **Context:** A worker node `worker02` is provisioned and needs to be joined to the existing cluster. The join command was saved during `kubeadm init`.
  **Task:** Run the kubeadm join command on `worker02` using the token and CA cert hash from `/tmp/join.txt`. Verify the node appears in the cluster.

  **Key Commands:**
  ```bash
  # On worker02 — run the join command from /tmp/join.txt, e.g.:
  kubeadm join 192.168.1.10:6443 \
    --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
  # On control plane:
  kubectl get nodes
  ```
  **Verify:** `kubectl get nodes` shows `worker02` in `Ready` state.
  **⚠️ Watch Out:** Tokens expire after 24 hours. If joining after that, generate a new one: `kubeadm token create --print-join-command`.

---

- [ ] 🟡 **#011 — Upgrade control plane from v1.33 to v1.34**
  **Context:** The cluster runs Kubernetes v1.33. You must upgrade the control plane to v1.34 following the official process.
  **Task:** Upgrade the control plane node step by step: drain, upgrade kubeadm, plan and apply the upgrade, then upgrade kubelet and kubectl, and uncordon.

  **Key Commands:**
  ```bash
  kubectl drain controlplane --ignore-daemonsets --delete-emptydir-data
  apt-get update
  apt-get install -y kubeadm=1.34.0-1.1
  kubeadm upgrade plan
  kubeadm upgrade apply v1.34.0
  apt-get install -y kubelet=1.34.0-1.1 kubectl=1.34.0-1.1
  systemctl daemon-reload && systemctl restart kubelet
  kubectl uncordon controlplane
  ```
  **Verify:** `kubectl get nodes` → control plane shows `v1.34.0`.
  **⚠️ Watch Out:** You must upgrade **one minor version at a time** (v1.33 → v1.34). You cannot skip versions. Also, always upgrade kubeadm first, before kubelet and kubectl.

---

- [ ] 🟡 **#012 — Upgrade worker nodes after control plane upgrade**
  **Context:** The control plane was upgraded to v1.34 but worker nodes still run v1.33. Worker nodes must be upgraded one at a time.
  **Task:** For each worker node: drain from the control plane, SSH in to upgrade kubelet and kubectl, then uncordon from the control plane.

  **Key Commands:**
  ```bash
  # On control plane:
  kubectl drain worker01 --ignore-daemonsets --delete-emptydir-data
  # SSH into worker01:
  apt-get update
  apt-get install -y kubeadm=1.34.0-1.1
  kubeadm upgrade node
  apt-get install -y kubelet=1.34.0-1.1 kubectl=1.34.0-1.1
  systemctl daemon-reload && systemctl restart kubelet
  # Back on control plane:
  kubectl uncordon worker01
  ```
  **Verify:** `kubectl get nodes` → all nodes show `v1.34.0` and `Ready`.
  **⚠️ Watch Out:** On worker nodes, use `kubeadm upgrade node` (not `kubeadm upgrade apply`). The `apply` command is only for the first control plane node.

---

- [ ] 🔴 **#013 — Fix stale apt repo then complete upgrade**
  **Context:** Running `apt-get update` fails because the Kubernetes apt repository URL is outdated. The kubernetes packages are not found.
  **Task:** Fix `/etc/apt/sources.list.d/kubernetes.list` to use the correct v1.34 repository URL, then complete the upgrade.

  **Key Commands:**
  ```bash
  # Fix the repo
  echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
    https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /" \
    > /etc/apt/sources.list.d/kubernetes.list
  apt-get update
  apt-get install -y kubeadm=1.34.0-1.1 kubelet=1.34.0-1.1 kubectl=1.34.0-1.1
  ```
  **Verify:** `apt-cache policy kubeadm` shows v1.34 as installed.
  **⚠️ Watch Out:** Since Kubernetes v1.28, the apt repo URL format changed to `pkgs.k8s.io/core:/stable:/v1.XX/deb/`. Old guides using `packages.cloud.google.com` will fail.

---

- [ ] 🔴 **#014 — Fix crashed kube-apiserver after upgrade**
  **Context:** After running `kubeadm upgrade apply v1.34.0`, the kube-apiserver static pod keeps restarting. The cluster is inaccessible.
  **Task:** Inspect the static pod manifest at `/etc/kubernetes/manifests/kube-apiserver.yaml`, find the broken flag, fix it, and wait for the apiserver to recover.

  **Key Commands:**
  ```bash
  # Check the static pod manifest for bad flags
  cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep -A2 "command:"
  # Common culprit: bad audit log path, wrong etcd URL, typo in flag name
  # Use crictl to see current crash reason:
  crictl ps -a | grep apiserver
  crictl logs <container-id>
  # Fix the manifest (vim), save it — kubelet will auto-restart the pod
  vim /etc/kubernetes/manifests/kube-apiserver.yaml
  ```
  **Verify:** `crictl ps | grep apiserver` shows Running. `kubectl get nodes` returns results.
  **⚠️ Watch Out:** After editing a static pod manifest, there's a 10–30 second delay before kubelet picks up the change. Wait and re-check instead of assuming the fix failed.

---

### Helm

- [ ] 🟢 **#015 — Add a Helm repo and install a chart with custom values**
  **Context:** You need to deploy nginx into the cluster using the Bitnami Helm chart.
  **Task:** Add the Bitnami repo, install the `bitnami/nginx` chart as release `my-nginx` in namespace `web`. Set replicas to 3. The namespace must be created if it doesn't exist.

  **Key Commands:**
  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo update
  helm install my-nginx bitnami/nginx --namespace web --create-namespace \
    --set replicaCount=3
  ```
  **Verify:** `helm list -n web` shows `my-nginx` with status `deployed`. `kubectl get deploy -n web` shows 3 replicas.
  **⚠️ Watch Out:** Helm release names are unique per namespace. Installing the same release name twice without `--upgrade` will fail. Always check with `helm list -n <ns>` first.

---

- [ ] 🟢 **#016 — List all Helm releases across all namespaces**
  **Context:** You've been asked to audit all Helm-managed applications in the cluster.
  **Task:** List every Helm release across all namespaces including their status, chart version, and namespace. Save the output to `/tmp/helm-releases.txt`.

  **Key Commands:**
  ```bash
  helm list -A > /tmp/helm-releases.txt
  # Also capture failed/pending ones:
  helm list -A --all >> /tmp/helm-releases.txt
  ```
  **Verify:** `cat /tmp/helm-releases.txt` shows all releases across namespaces.
  **⚠️ Watch Out:** `helm list` without `-A` only shows releases in the current namespace. `helm list -A` or `helm list --all-namespaces` is required to see everything.

---

- [ ] 🟡 **#017 — Fix a Helm release stuck in pending-install**
  **Context:** Release `broken-app` in namespace `prod` was interrupted mid-install and is stuck in `pending-install` state. New installs fail because the release name is taken.
  **Task:** Delete the stuck Helm release, clean up any partial resources, then reinstall the chart cleanly.

  **Key Commands:**
  ```bash
  helm list -n prod --all   # confirm status: pending-install
  helm delete broken-app -n prod --no-hooks
  # Verify no orphaned resources remain
  kubectl get all -n prod -l app.kubernetes.io/instance=broken-app
  # Reinstall
  helm install broken-app bitnami/nginx -n prod
  ```
  **Verify:** `helm list -n prod` shows `broken-app` with status `deployed`.
  **⚠️ Watch Out:** A `pending-install` release blocks the name in that namespace. Regular `helm install` will fail with "already exists". You must `helm delete` it first, even though it never successfully deployed.

---

- [ ] 🟡 **#018 — Upgrade a Helm release to a specific version**
  **Context:** The `my-nginx` release in namespace `web` is on chart v12.0.0. You need to upgrade it to chart v13.2.1 and change the service type to `ClusterIP`.
  **Task:** Upgrade the release using `helm upgrade`, specifying the exact chart version and the `--set` override.

  **Key Commands:**
  ```bash
  helm repo update
  helm upgrade my-nginx bitnami/nginx \
    --namespace web \
    --version 13.2.1 \
    --set service.type=ClusterIP
  ```
  **Verify:** `helm list -n web` shows the new chart version. `kubectl get svc -n web` shows `ClusterIP` service type.
  **⚠️ Watch Out:** Helm `--set` values from a previous install are NOT preserved across upgrades unless you use `--reuse-values` or specify them again. If you forget `--reuse-values`, you might unintentionally reset replica count back to default.

---

- [ ] 🔴 **#019 — Use helm template to render YAML then apply with kubectl**
  **Context:** In a restricted environment, Helm cannot communicate with the cluster directly. You must render the chart to YAML first and apply it manually.
  **Task:** Use `helm template` to render the `bitnami/nginx` chart with release name `static-nginx` and save it to `/tmp/rendered.yaml`. Then apply it with `kubectl apply -f`.

  **Key Commands:**
  ```bash
  helm template static-nginx bitnami/nginx \
    --namespace web \
    --set replicaCount=2 \
    > /tmp/rendered.yaml
  kubectl apply -f /tmp/rendered.yaml -n web
  ```
  **Verify:** `cat /tmp/rendered.yaml` shows valid Kubernetes manifests. `kubectl get all -n web` shows the deployed resources.
  **⚠️ Watch Out:** `helm template` does NOT install anything or track the release in Helm state. The output is raw YAML only. Subsequent `helm list` will not show this release.

---

- [ ] 🔴 **#020 — Debug a failed Helm install and redeploy**
  **Context:** `helm install monitoring prometheus-community/kube-prometheus-stack -n observability` failed midway. Partial CRDs and resources were created.
  **Task:** Investigate what was installed using `helm get manifest`, remove the broken release and all orphaned resources, fix the values (increase timeout), and redeploy.

  **Key Commands:**
  ```bash
  helm get manifest monitoring -n observability 2>/dev/null || echo "release failed"
  helm delete monitoring -n observability --no-hooks
  kubectl delete crd prometheuses.monitoring.coreos.com 2>/dev/null || true
  # Reinstall with longer timeout
  helm install monitoring prometheus-community/kube-prometheus-stack \
    -n observability --create-namespace --timeout 10m
  ```
  **Verify:** `helm list -n observability` shows `monitoring` as `deployed`.
  **⚠️ Watch Out:** CRDs installed by Helm are NOT removed by `helm delete` by default. You may need to manually delete them before a clean reinstall, or use `--cascade=foreground` deletion.

---

- [ ] 🟡 **#021 — Install ArgoCD via Helm and expose it as NodePort**
  **Context:** The team wants GitOps capabilities. You must deploy ArgoCD using Helm and make the UI accessible from outside the cluster.
  **Task:** Install ArgoCD from the `argo` Helm repo into namespace `argocd`. After install, patch the `argocd-server` service from `ClusterIP` to `NodePort`.

  **Key Commands:**
  ```bash
  helm repo add argo https://argoproj.github.io/argo-helm
  helm repo update
  helm install argocd argo/argo-cd -n argocd --create-namespace
  kubectl patch svc argocd-server -n argocd \
    -p '{"spec": {"type": "NodePort"}}'
  kubectl get svc argocd-server -n argocd
  ```
  **Verify:** `kubectl get svc argocd-server -n argocd` shows `NodePort` with a port like `80:3XXXX/TCP`.
  **⚠️ Watch Out:** ArgoCD's Helm chart has `server.insecure` flag disabled by default. The NodePort service may redirect to HTTPS. If you get SSL errors, add `--set server.insecure=true` at install time.

---

### Kustomize

- [ ] 🟢 **#022 — Apply a Kustomize base directory**
  **Context:** A base Kustomize configuration exists at `/opt/kustomize/base` with a `kustomization.yaml` referencing a Deployment and Service.
  **Task:** Apply the entire Kustomize directory to the cluster. Verify all referenced resources are created.

  **Key Commands:**
  ```bash
  kubectl apply -k /opt/kustomize/base
  # Review what would be applied first:
  kubectl kustomize /opt/kustomize/base
  ```
  **Verify:** `kubectl get all` shows the resources defined in the Kustomize directory.
  **⚠️ Watch Out:** `kubectl apply -k` and `kubectl kustomize` are different: `-k` applies to the cluster; `kustomize` just renders. The standalone `kustomize` CLI binary and `kubectl kustomize` may behave slightly differently on older kubectl versions.

---

- [ ] 🟡 **#023 — Apply a Kustomize overlay with patches**
  **Context:** A Kustomize overlay at `/opt/kustomize/overlays/prod` patches the base Deployment to set replicas to 5 and adds label `env: prod`.
  **Task:** Apply the prod overlay and verify the Deployment has 5 replicas and the correct label.

  **Key Commands:**
  ```bash
  kubectl apply -k /opt/kustomize/overlays/prod
  kubectl get deploy -o wide
  kubectl get deploy <name> --show-labels
  ```
  **Verify:** `kubectl get deploy <name> -o jsonpath='{.spec.replicas}'` → `5`. Labels include `env=prod`.
  **⚠️ Watch Out:** Kustomize patches apply on top of the base. If the patch file path listed in `kustomization.yaml` doesn't match the actual filename, the apply will silently use no patch — check the rendered output first.

---

- [ ] 🔴 **#024 — Fix a broken Kustomize patch reference**
  **Context:** Applying `/opt/kustomize/overlays/staging` fails with an error: `no such file: replica-patch.yaml`.
  **Task:** Inspect the `kustomization.yaml` to find the incorrect path, locate the actual patch file, fix the reference, and successfully apply.

  **Key Commands:**
  ```bash
  cat /opt/kustomize/overlays/staging/kustomization.yaml
  ls /opt/kustomize/overlays/staging/
  # Fix: rename or update the path reference in kustomization.yaml
  vim /opt/kustomize/overlays/staging/kustomization.yaml
  kubectl apply -k /opt/kustomize/overlays/staging
  ```
  **Verify:** Apply succeeds with no errors. Resources are created/updated in the cluster.
  **⚠️ Watch Out:** Kustomize requires exact filenames. Case sensitivity matters on Linux — `Replica-Patch.yaml` ≠ `replica-patch.yaml`.

---

- [ ] 🟡 **#025 — Render Kustomize without applying and save**
  **Context:** You need to review what Kubernetes manifests a Kustomize overlay would generate before committing to apply them.
  **Task:** Render the `/opt/app/overlays/staging` Kustomize directory to stdout and save the output to `/tmp/staging-rendered.yaml`.

  **Key Commands:**
  ```bash
  kubectl kustomize /opt/app/overlays/staging > /tmp/staging-rendered.yaml
  cat /tmp/staging-rendered.yaml
  ```
  **Verify:** `/tmp/staging-rendered.yaml` contains valid Kubernetes YAML with applied overlays and patches.
  **⚠️ Watch Out:** Do NOT use `kubectl apply -k` here — that would actually apply resources to the cluster. The question specifically asks to render only.

---

### CRDs & Operators

- [ ] 🟢 **#026 — Create a Custom Resource Definition**
  **Context:** Your team has a custom controller that manages backup jobs. The CRD must be installed before the controller.
  **Task:** Create a CRD for resource `BackupJob` in group `ops.example.com`, version `v1alpha1`, kind `BackupJob`, with schema field `schedule` (string, required).

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: apiextensions.k8s.io/v1
  kind: CustomResourceDefinition
  metadata:
    name: backupjobs.ops.example.com
  spec:
    group: ops.example.com
    names:
      kind: BackupJob
      listKind: BackupJobList
      plural: backupjobs
      singular: backupjob
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
              required: ["schedule"]
              properties:
                schedule:
                  type: string
  EOF
  ```
  **Verify:** `kubectl api-resources | grep backupjob` shows the new resource. `kubectl get backupjobs -A` works.
  **⚠️ Watch Out:** The CRD `metadata.name` must follow the format `<plural>.<group>` exactly. `backupjobs.ops.example.com` not `BackupJob.ops.example.com`.

---

- [ ] 🟡 **#027 — Install an operator and create a custom resource instance**
  **Context:** A manifest at `/opt/operators/postgres-operator.yaml` defines an operator. After installing it, you must create a PostgresCluster custom resource.
  **Task:** Apply the operator manifest, wait for it to be Ready, then create a `PostgresCluster` resource named `my-db` in namespace `db` with 3 instances.

  **Key Commands:**
  ```bash
  kubectl apply -f /opt/operators/postgres-operator.yaml
  kubectl wait --for=condition=Available deploy/postgres-operator -n postgres-operator --timeout=120s
  cat <<EOF | kubectl apply -f -
  apiVersion: postgres-operator.crunchydata.com/v1beta1
  kind: PostgresCluster
  metadata:
    name: my-db
    namespace: db
  spec:
    instances:
    - replicas: 3
  EOF
  ```
  **Verify:** `kubectl get postgrescluster my-db -n db` shows the resource. Operator creates pods.
  **⚠️ Watch Out:** Operators may take 1–2 minutes to reconcile and create pods. Check operator logs if pods don't appear: `kubectl logs -n postgres-operator deploy/postgres-operator`.

---

- [ ] 🔴 **#028 — Debug CRD schema validation error**
  **Context:** CRD `databases.ops.example.com` is installed. When creating a custom resource, you get: `spec.replicas: Required value`. But the YAML you're applying has `replicas` defined.
  **Task:** Inspect the CRD's openAPIV3Schema, find the mismatch (field is named `replica` in schema but `replicas` in the manifest), and fix the CRD schema.

  **Key Commands:**
  ```bash
  kubectl get crd databases.ops.example.com -o yaml | grep -A20 "openAPIV3Schema"
  # Find the field name discrepancy
  kubectl edit crd databases.ops.example.com
  # Or:
  kubectl get crd databases.ops.example.com -o yaml > /tmp/crd.yaml
  # Edit field name, then:
  kubectl apply -f /tmp/crd.yaml
  ```
  **Verify:** Create the custom resource again — it should succeed with no validation errors.
  **⚠️ Watch Out:** CRD schema changes take effect immediately. After fixing the field name in the CRD, you do not need to restart any controllers.

---

### Extension Interfaces (CNI, CSI, CRI)

- [ ] 🟢 **#029 — Identify the CNI plugin in use**
  **Context:** A new engineer needs to know which CNI plugin is installed.
  **Task:** Identify the CNI plugin binary in `/opt/cni/bin/` and the CNI configuration in `/etc/cni/net.d/`. Save the CNI name to `/tmp/cni-info.txt`.

  **Key Commands:**
  ```bash
  ls /opt/cni/bin/
  ls /etc/cni/net.d/
  cat /etc/cni/net.d/*.conf* | grep -i '"type"'
  echo "CNI: flannel" > /tmp/cni-info.txt  # replace with actual
  ```
  **Verify:** `/tmp/cni-info.txt` contains the correct CNI name matching the config file.
  **⚠️ Watch Out:** There may be multiple CNI binaries in `/opt/cni/bin/` (e.g., `bridge`, `flannel`, `calico`). The **active** CNI is whichever is referenced by the `.conf` or `.conflist` file in `/etc/cni/net.d/`.

---

- [ ] 🟡 **#030 — Debug ContainerCreating due to missing CNI on new node**
  **Context:** A new node `worker03` joined the cluster, but pods scheduled on it are stuck in `ContainerCreating`. Other nodes work fine.
  **Task:** Determine the root cause (missing CNI plugin on the node), install the CNI plugin, and verify pods start.

  **Key Commands:**
  ```bash
  kubectl describe pod <stuck-pod> | grep -A5 "Events:"
  # Likely event: "network plugin is not ready: cni config uninitialized"
  ssh worker03
  ls /opt/cni/bin/  # empty or missing flannel/calico binary
  ls /etc/cni/net.d/  # no config files
  # Install Flannel DaemonSet (if that's the CNI):
  # The DaemonSet should handle it — check if the flannel pod is running on worker03
  kubectl get pods -n kube-flannel -o wide | grep worker03
  ```
  **Verify:** After CNI is set up, `kubectl get pods -o wide` shows the stuck pods transition to `Running` on `worker03`.
  **⚠️ Watch Out:** If a CNI DaemonSet is installed, it should automatically configure CNI on new nodes. If pods on the new node are stuck, check whether the DaemonSet pod on that node is itself in a bad state.

---

- [ ] 🟡 **#031 — Identify CRI socket and verify with crictl**
  **Context:** A cluster administrator needs to confirm which container runtime is active on a specific node.
  **Task:** On node `worker01`, identify the CRI socket path used by the kubelet. Confirm using `crictl info`.

  **Key Commands:**
  ```bash
  ssh worker01
  # Check kubelet config or service flags:
  systemctl show kubelet | grep ExecStart
  # Or:
  cat /var/lib/kubelet/config.yaml | grep containerRuntime
  ps aux | grep kubelet | grep container-runtime-endpoint
  # Run crictl:
  crictl --runtime-endpoint unix:///run/containerd/containerd.sock info
  ```
  **Verify:** `crictl info` returns JSON with runtime version and type (e.g., `containerd`).
  **⚠️ Watch Out:** Common CRI sockets: containerd → `/run/containerd/containerd.sock`, CRI-O → `/var/run/crio/crio.sock`. If `crictl` returns an error, you may need to set the `--runtime-endpoint` flag explicitly.

---

## 🚀 DOMAIN 2 — Workloads & Scheduling (15%)

---

### Deployments, Rolling Updates & Rollbacks

- [ ] 🟢 **#032 — Create a Deployment with labels and replica count**
  **Context:** A new frontend application needs to be deployed to production.
  **Task:** Create Deployment `web-app` in namespace `prod` using image `nginx:1.24`, with 4 replicas and labels `app=web, tier=frontend`. The namespace must exist.

  **Key Commands:**
  ```bash
  kubectl create namespace prod 2>/dev/null || true
  kubectl create deployment web-app --image=nginx:1.24 --replicas=4 -n prod
  kubectl label deployment web-app tier=frontend -n prod
  ```
  **Verify:** `kubectl get deploy web-app -n prod` shows 4/4 Ready. `kubectl get deploy web-app -n prod --show-labels` shows both labels.
  **⚠️ Watch Out:** `kubectl create deployment` automatically adds the `app=<name>` label. If the question requires additional labels, you must add them separately with `kubectl label`.

---

- [ ] 🟢 **#033 — Perform a rolling image update and monitor**
  **Context:** A security patch requires updating `web-app` from `nginx:1.24` to `nginx:1.25`.
  **Task:** Update the container image and monitor the rollout until completion. Record the rollout status.

  **Key Commands:**
  ```bash
  kubectl set image deployment/web-app nginx=nginx:1.25 -n prod
  kubectl rollout status deployment/web-app -n prod
  kubectl rollout history deployment/web-app -n prod
  ```
  **Verify:** `kubectl get deploy web-app -n prod -o jsonpath='{.spec.template.spec.containers[0].image}'` → `nginx:1.25`
  **⚠️ Watch Out:** The container name in `kubectl set image` is `<container-name>=<new-image>`. If the container name is not `nginx`, this command silently does nothing. Check container name with `kubectl get deploy web-app -o jsonpath='{.spec.template.spec.containers[*].name}'`.

---

- [ ] 🟢 **#034 — Roll back a Deployment to the previous revision**
  **Context:** An update to Deployment `api-server` deployed a bad image. Pods are crashing and the previous version was stable.
  **Task:** Roll back `api-server` to its previous revision and verify the rollback completed.

  **Key Commands:**
  ```bash
  kubectl rollout undo deployment/api-server -n prod
  kubectl rollout status deployment/api-server -n prod
  kubectl rollout history deployment/api-server -n prod
  ```
  **Verify:** `kubectl get deploy api-server -n prod` shows all replicas Ready. Old image is restored.
  **⚠️ Watch Out:** By default, Kubernetes only keeps 10 revisions (`revisionHistoryLimit`). If you've done many updates, older revisions may be gone. Always check `kubectl rollout history` before assuming a specific revision exists.

---

- [ ] 🟡 **#035 — Pause rollout, fix image, then resume**
  **Context:** Deployment `payment-svc` started a rolling update to `payment-svc:v2.0` but half the pods are in `ImagePullBackOff` because the tag doesn't exist.
  **Task:** Pause the rollout, fix the image tag to `payment-svc:v2.1` (which exists), then resume the rollout.

  **Key Commands:**
  ```bash
  kubectl rollout pause deployment/payment-svc -n prod
  kubectl set image deployment/payment-svc payment-svc=payment-svc:v2.1 -n prod
  kubectl rollout resume deployment/payment-svc -n prod
  kubectl rollout status deployment/payment-svc -n prod
  ```
  **Verify:** `kubectl get pods -n prod` shows all payment-svc pods Running with image `v2.1`.
  **⚠️ Watch Out:** While a rollout is paused, `kubectl set image` changes are queued but not applied. Resume the rollout to apply them. If you forget to resume, the Deployment stays half-updated forever.

---

- [ ] 🔴 **#036 — Configure zero-downtime rolling update strategy**
  **Context:** Deployment `checkout` cannot afford ANY pod downtime during updates. New pods must be provisioned before old ones are removed.
  **Task:** Configure `maxUnavailable: 0` and `maxSurge: 2` on the rolling update strategy. Trigger an update and confirm zero pods go unavailable.

  **Key Commands:**
  ```bash
  kubectl patch deployment checkout -n prod \
    -p '{"spec":{"strategy":{"rollingUpdate":{"maxUnavailable":0,"maxSurge":2}}}}'
  kubectl set image deployment/checkout checkout=nginx:1.25 -n prod
  # Watch the rollout — at no point should available < desired
  kubectl rollout status deployment/checkout -n prod
  ```
  **Verify:** During rollout, `kubectl get pods -n prod -w` shows new pods come up before old ones terminate. `kubectl describe deploy checkout -n prod | grep -A3 "RollingUpdate"` shows the configured values.
  **⚠️ Watch Out:** Setting `maxUnavailable: 0` with `maxSurge: 0` will completely freeze the rollout. At least one of them must be non-zero.

---

- [ ] 🟡 **#037 — Roll back to a specific revision number**
  **Context:** Deployment `backend` has had 10+ rolling updates. A bug was introduced in revision 7. You need to roll back to revision 3.
  **Task:** View the rollout history, then roll back specifically to revision 3.

  **Key Commands:**
  ```bash
  kubectl rollout history deployment/backend -n prod
  kubectl rollout history deployment/backend -n prod --revision=3
  kubectl rollout undo deployment/backend --to-revision=3 -n prod
  kubectl rollout status deployment/backend -n prod
  ```
  **Verify:** `kubectl rollout history deployment/backend -n prod` shows a new revision at the top reflecting revision 3's image/config.
  **⚠️ Watch Out:** After undoing to revision 3, that config becomes the **new latest revision** — revision 3 itself is consumed and a new revision number is created with the same config. Do not be alarmed by this.

---

### ConfigMaps & Secrets

- [ ] 🟢 **#038 — Create ConfigMap and inject as env vars**
  **Context:** Application `myapp` reads configuration from environment variables `ENV` and `LOG_LEVEL`.
  **Task:** Create ConfigMap `app-config` in namespace `dev` with `ENV=production` and `LOG_LEVEL=info`. Create a pod that injects all ConfigMap keys as environment variables using `envFrom`.

  **Key Commands:**
  ```bash
  kubectl create configmap app-config --from-literal=ENV=production \
    --from-literal=LOG_LEVEL=info -n dev
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: app-pod
    namespace: dev
  spec:
    containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "env && sleep 3600"]
      envFrom:
      - configMapRef:
          name: app-config
  EOF
  ```
  **Verify:** `kubectl exec -n dev app-pod -- env | grep -E "ENV|LOG_LEVEL"` shows both variables.
  **⚠️ Watch Out:** `envFrom.configMapRef` injects ALL keys as env vars. If you only need specific keys, use `env.valueFrom.configMapKeyRef` instead and specify `key:`.

---

- [ ] 🟢 **#039 — Create Secret and mount as volume**
  **Context:** App `db-client` needs database credentials available as files.
  **Task:** Create Secret `db-creds` with `username=admin` and `password=s3cr3t`. Mount it as a volume at `/etc/secrets` in a pod. Each key should appear as a file.

  **Key Commands:**
  ```bash
  kubectl create secret generic db-creds \
    --from-literal=username=admin \
    --from-literal=password=s3cr3t -n dev
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: db-client
    namespace: dev
  spec:
    containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "ls /etc/secrets && sleep 3600"]
      volumeMounts:
      - name: secret-vol
        mountPath: /etc/secrets
        readOnly: true
    volumes:
    - name: secret-vol
      secret:
        secretName: db-creds
  EOF
  ```
  **Verify:** `kubectl exec -n dev db-client -- ls /etc/secrets` shows `username` and `password` files. Values are base64-decoded automatically.
  **⚠️ Watch Out:** Secret values stored in etcd are base64-encoded, but when mounted as files they are automatically decoded. Do not double-encode values when creating Secrets.

---

- [ ] 🟡 **#040 — Fix pod with missing ConfigMap key**
  **Context:** Pod `app-pod` in namespace `dev` references ConfigMap key `DATABASE_URL` using `configMapKeyRef`, but the ConfigMap `app-config` does not have that key. Pod stays in `CreateContainerConfigError`.
  **Task:** Add the missing key `DATABASE_URL=postgres://db:5432/app` to the ConfigMap without deleting it. Verify the pod recovers.

  **Key Commands:**
  ```bash
  kubectl get configmap app-config -n dev -o yaml  # confirm missing key
  kubectl patch configmap app-config -n dev \
    --type=merge \
    -p '{"data":{"DATABASE_URL":"postgres://db:5432/app"}}'
  # Pod should self-recover when ConfigMap is fixed (may need a delete/recreate)
  kubectl delete pod app-pod -n dev
  kubectl apply -f /opt/pods/app-pod.yaml
  ```
  **Verify:** `kubectl get pod app-pod -n dev` → `Running`.
  **⚠️ Watch Out:** Pods that reference missing ConfigMap keys will enter `CreateContainerConfigError` (not `Pending` or `CrashLoopBackOff`). This state does NOT auto-heal when you add the key — you must restart the pod.

---

- [ ] 🔴 **#041 — Mount ConfigMap as a single file (not env vars)**
  **Context:** Application expects configuration at exactly `/config/app.properties` as a file, not as environment variables. The properties file content is at `/opt/config/app.properties`.
  **Task:** Create a ConfigMap from the file and mount it into a pod so the file appears at exactly `/config/app.properties` (using `subPath`).

  **Key Commands:**
  ```bash
  kubectl create configmap app-props --from-file=app.properties=/opt/config/app.properties -n dev
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: file-pod
    namespace: dev
  spec:
    containers:
    - name: app
      image: busybox
      command: ["sh","-c","cat /config/app.properties && sleep 3600"]
      volumeMounts:
      - name: config-vol
        mountPath: /config/app.properties
        subPath: app.properties
    volumes:
    - name: config-vol
      configMap:
        name: app-props
  EOF
  ```
  **Verify:** `kubectl exec -n dev file-pod -- cat /config/app.properties` shows the file contents.
  **⚠️ Watch Out:** Without `subPath`, mounting at `/config/app.properties` would create a **directory** named `app.properties`. Use `subPath: app.properties` to mount a single file at the exact path.

---

- [ ] 🟡 **#042 — Debug cross-namespace Secret access failure**
  **Context:** A pod in namespace `web` is configured to use Secret `tls-cert`, but the Secret only exists in namespace `default`.
  **Task:** Explain why this is a problem (Secrets are namespace-scoped), create a copy of the Secret in namespace `web`, and restart the pod.

  **Key Commands:**
  ```bash
  # Copy secret across namespaces:
  kubectl get secret tls-cert -n default -o yaml \
    | sed 's/namespace: default/namespace: web/' \
    | kubectl apply -f -
  # Or re-create from scratch:
  kubectl create secret generic tls-cert \
    --from-literal=tls.crt="$(kubectl get secret tls-cert -n default -o jsonpath='{.data.tls\.crt}' | base64 -d)" \
    --from-literal=tls.key="$(kubectl get secret tls-cert -n default -o jsonpath='{.data.tls\.key}' | base64 -d)" \
    -n web
  ```
  **Verify:** `kubectl get secret tls-cert -n web` exists. The pod in `web` transitions to `Running`.
  **⚠️ Watch Out:** Secrets and ConfigMaps are strictly namespaced. A pod can only reference Secrets in its own namespace. There is no built-in cross-namespace reference mechanism in core Kubernetes.

---

### Autoscaling

- [ ] 🟢 **#043 — Create an HPA for CPU-based scaling**
  **Context:** Deployment `web-app` in namespace `prod` needs to scale automatically based on CPU usage.
  **Task:** Create an HPA that keeps minimum 2 replicas, maximum 10, targeting 70% average CPU utilization.

  **Key Commands:**
  ```bash
  kubectl autoscale deployment web-app \
    --min=2 --max=10 --cpu-percent=70 \
    -n prod
  kubectl get hpa -n prod
  ```
  **Verify:** `kubectl describe hpa web-app -n prod` shows `Targets: <actual>%/70%`, `Min replicas: 2`, `Max replicas: 10`.
  **⚠️ Watch Out:** HPA requires `metrics-server` to be installed. If it's missing, HPA will show `<unknown>` for current CPU. Also, the Deployment's containers must have CPU **requests** set — HPA calculates percentage based on requested CPU.

---

- [ ] 🟡 **#044 — Fix HPA showing unknown metrics**
  **Context:** An HPA was created but `kubectl get hpa` shows `TARGETS: <unknown>/70%`. Pods are Running and labeled correctly.
  **Task:** Diagnose the issue (metrics-server not running) and install metrics-server to restore HPA functionality.

  **Key Commands:**
  ```bash
  kubectl get hpa -n prod
  kubectl top nodes  # will fail if metrics-server is missing
  kubectl get deploy -n kube-system | grep metrics
  # Install metrics-server:
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  # If TLS is an issue in test clusters, patch with insecure TLS:
  kubectl patch deployment metrics-server -n kube-system \
    --type=json \
    -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
  ```
  **Verify:** `kubectl top nodes` returns data. `kubectl get hpa -n prod` shows real CPU percentage.
  **⚠️ Watch Out:** In exam environments, metrics-server may already be installed but in a broken state. Check `kubectl get pods -n kube-system | grep metrics` before reinstalling.

---

- [ ] 🟡 **#045 — Create a VPA in recommendation-only mode**
  **Context:** You want to gather CPU/memory recommendations for Deployment `api` without automatically changing the pods.
  **Task:** Create a VPA object for `api` in namespace `prod` with `updateMode: Off`. After a few minutes, inspect the recommendations.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: autoscaling.k8s.io/v1
  kind: VerticalPodAutoscaler
  metadata:
    name: api-vpa
    namespace: prod
  spec:
    targetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: api
    updatePolicy:
      updateMode: "Off"
  EOF
  kubectl get vpa api-vpa -n prod
  kubectl describe vpa api-vpa -n prod
  ```
  **Verify:** `kubectl describe vpa api-vpa -n prod` shows `Recommendation:` section with CPU and memory target values.
  **⚠️ Watch Out:** VPA requires the VPA controller to be installed separately (it's not built into Kubernetes). If the CRD doesn't exist, you'll get an error. Check: `kubectl api-resources | grep verticalpod`.

---

- [ ] 🔴 **#046 — Resolve HPA and VPA conflict**
  **Context:** Both an HPA (scaling on CPU) and a VPA (updating CPU limits) target the same Deployment. They are fighting — VPA changes CPU, HPA reacts to CPU change, creating a feedback loop.
  **Task:** Reconfigure so HPA manages replica count based on CPU, and VPA manages memory limits only (set VPA `updateMode: Auto` but exclude CPU from its recommendations).

  **Key Commands:**
  ```bash
  # Delete old HPA and VPA
  kubectl delete hpa web-app -n prod
  kubectl delete vpa web-app-vpa -n prod
  # Recreate HPA (CPU only):
  kubectl autoscale deployment web-app --min=2 --max=10 --cpu-percent=70 -n prod
  # Recreate VPA (memory only, off for CPU):
  cat <<EOF | kubectl apply -f -
  apiVersion: autoscaling.k8s.io/v1
  kind: VerticalPodAutoscaler
  metadata:
    name: web-app-vpa
    namespace: prod
  spec:
    targetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: web-app
    updatePolicy:
      updateMode: "Auto"
    resourcePolicy:
      containerPolicies:
      - containerName: "*"
        controlledResources: ["memory"]
  EOF
  ```
  **Verify:** HPA shows CPU target. VPA description shows only memory in controlled resources.
  **⚠️ Watch Out:** Running HPA and VPA both managing CPU on the same workload is an anti-pattern that leads to oscillation. The exam tests whether you understand this conflict and can resolve it.

---

### DaemonSets, StatefulSets, ReplicaSets

- [ ] 🟢 **#047 — Create a DaemonSet that runs on all nodes including control plane**
  **Context:** A log-collection agent must run on every node in the cluster, including the control plane.
  **Task:** Create DaemonSet `log-collector` using image `fluentd:latest`. Add a toleration for the control plane taint `node-role.kubernetes.io/control-plane:NoSchedule`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: apps/v1
  kind: DaemonSet
  metadata:
    name: log-collector
    namespace: kube-system
  spec:
    selector:
      matchLabels:
        app: log-collector
    template:
      metadata:
        labels:
          app: log-collector
      spec:
        tolerations:
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule
        containers:
        - name: fluentd
          image: fluentd:latest
  EOF
  ```
  **Verify:** `kubectl get pods -n kube-system -o wide | grep log-collector` shows one pod per node including the control plane.
  **⚠️ Watch Out:** The taint key changed from `node-role.kubernetes.io/master` (deprecated) to `node-role.kubernetes.io/control-plane` in v1.24. Use the new key for v1.34 clusters.

---

- [ ] 🟡 **#048 — Debug StatefulSet with PVC provisioning failure**
  **Context:** StatefulSet `postgres` with 3 replicas is stuck. Only `postgres-0` is Running. `postgres-1` and `postgres-2` are `Pending` with PVC failures.
  **Task:** Diagnose why PVCs aren't provisioning (StorageClass missing or misconfigured), fix the StorageClass, and verify all 3 pods start.

  **Key Commands:**
  ```bash
  kubectl get pvc -n db  # shows pending PVCs
  kubectl describe pvc data-postgres-1 -n db  # shows provisioner error
  kubectl get storageclass  # check if class exists
  # If missing, create it:
  cat <<EOF | kubectl apply -f -
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: standard
  provisioner: docker.io/hostpath
  reclaimPolicy: Delete
  volumeBindingMode: Immediate
  EOF
  ```
  **Verify:** `kubectl get pods -n db` shows `postgres-0`, `postgres-1`, `postgres-2` all Running.
  **⚠️ Watch Out:** StatefulSets create PVCs automatically from `volumeClaimTemplates`, but they will NOT auto-delete PVCs if the StatefulSet is deleted (unless PVC retention policy is set). Stuck PVCs from a previous failed install can block new ones.

---

- [ ] 🔴 **#049 — Scale a StatefulSet and verify ordered pod creation**
  **Context:** StatefulSet `kafka` currently has 3 replicas (`kafka-0`, `kafka-1`, `kafka-2`). It needs to scale to 5.
  **Task:** Scale `kafka` to 5 replicas. Verify pods are created sequentially and named correctly.

  **Key Commands:**
  ```bash
  kubectl scale statefulset kafka --replicas=5 -n messaging
  kubectl get pods -n messaging -w  # watch sequential creation
  # Verify names:
  kubectl get pods -n messaging -l app=kafka
  ```
  **Verify:** `kubectl get pods -n messaging | grep kafka` shows `kafka-0` through `kafka-4` all Running.
  **⚠️ Watch Out:** StatefulSets create pods **sequentially by default** (`podManagementPolicy: OrderedReady`). `kafka-3` must be Running before `kafka-4` starts. This is intentional and not a bug.

---

- [ ] 🟡 **#050 — Fix ReplicaSet not adopting existing pods**
  **Context:** A ReplicaSet `rs-app` was created with selector `app=myapp`, but existing pods have label `app=my-app` (note the hyphen). The ReplicaSet creates new pods instead of adopting the existing ones.
  **Task:** Fix the label on the existing pods to match the ReplicaSet selector without deleting anything.

  **Key Commands:**
  ```bash
  kubectl get pods --show-labels  # shows app=my-app on existing pods
  kubectl get rs rs-app -o jsonpath='{.spec.selector}'  # shows app=myapp
  # Option A: Fix pod labels:
  kubectl label pod <pod-name> app=myapp --overwrite
  # Option B: Fix RS selector (cannot change selector after creation):
  # Must delete and recreate RS with matching selector
  ```
  **Verify:** `kubectl get rs rs-app` shows desired replicas = current/available without creating duplicate pods.
  **⚠️ Watch Out:** A ReplicaSet selector is immutable after creation. If the selector itself is wrong, you must delete and recreate the RS. Patching labels on existing pods to match the selector is the non-destructive solution.

---

### Scheduling & Affinity

- [ ] 🟢 **#051 — Schedule pod on specific node type using nodeSelector**
  **Context:** A storage-intensive job must run on nodes with SSDs.
  **Task:** Schedule pod `disk-job` on any node labeled `disktype=ssd`. Label `worker01` with this label first.

  **Key Commands:**
  ```bash
  kubectl label node worker01 disktype=ssd
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: disk-job
  spec:
    nodeSelector:
      disktype: ssd
    containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
  EOF
  ```
  **Verify:** `kubectl get pod disk-job -o wide` shows the pod on `worker01`.
  **⚠️ Watch Out:** If no nodes have the required label, the pod stays `Pending` indefinitely. Always label the node before creating the pod in the exam.

---

- [ ] 🟡 **#052 — Configure soft node affinity with preferred scheduling**
  **Context:** Pods should prefer nodes in zone `us-east-1a` but can run anywhere if that zone is unavailable.
  **Task:** Create Deployment `zone-app` with `preferredDuringSchedulingIgnoredDuringExecution` affinity for `zone=us-east-1a`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: zone-app
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: zone-app
    template:
      metadata:
        labels:
          app: zone-app
      spec:
        affinity:
          nodeAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                - key: zone
                  operator: In
                  values:
                  - us-east-1a
        containers:
        - name: app
          image: nginx
  EOF
  ```
  **Verify:** Pods scheduled on `us-east-1a` nodes when available; otherwise on any node.
  **⚠️ Watch Out:** `preferredDuring...` uses a `weight` (1–100). Higher weight means stronger preference. If you accidentally use `requiredDuring...`, pods will be stuck Pending when the preferred zone is unavailable.

---

- [ ] 🔴 **#053 — Schedule pod on a tainted node using toleration**
  **Context:** Node `worker02` has taint `dedicated=gpu:NoSchedule`. Pod `gpu-job` must run on this specific node.
  **Task:** Create pod `gpu-job` with both a `nodeName: worker02` constraint and a toleration for the GPU taint.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: gpu-job
  spec:
    nodeName: worker02
    tolerations:
    - key: dedicated
      value: gpu
      effect: NoSchedule
    containers:
    - name: gpu
      image: nvidia/cuda:11.0-base
      command: ["sleep", "3600"]
  EOF
  ```
  **Verify:** `kubectl get pod gpu-job -o wide` shows pod on `worker02` and `Running`.
  **⚠️ Watch Out:** `nodeName` directly bypasses the scheduler. If you use `nodeName` to a tainted node WITHOUT the toleration, the pod will enter `Pending` with a taint violation even though it was directly assigned. Toleration is still needed.

---

- [ ] 🟡 **#054 — Configure pod anti-affinity to spread replicas**
  **Context:** Deployment `web` has 4 replicas. For HA, no two replicas should share the same node.
  **Task:** Add pod anti-affinity to the Deployment using `requiredDuringSchedulingIgnoredDuringExecution` with topology key `kubernetes.io/hostname`.

  **Key Commands:**
  ```bash
  kubectl edit deployment web
  # Under spec.template.spec add:
  # affinity:
  #   podAntiAffinity:
  #     requiredDuringSchedulingIgnoredDuringExecution:
  #     - labelSelector:
  #         matchLabels:
  #           app: web
  #       topologyKey: kubernetes.io/hostname
  ```
  **Verify:** `kubectl get pods -o wide | grep web` shows each pod on a different node.
  **⚠️ Watch Out:** If your cluster has fewer nodes than replicas, `requiredDuring...` anti-affinity will cause excess pods to be `Pending`. In that case, use `preferredDuring...` or add more nodes.

---

- [ ] 🟢 **#055 — Set CPU and memory requests and limits on a pod**
  **Context:** Pod `resource-pod` needs resource constraints to prevent it from consuming too much cluster capacity.
  **Task:** Create pod `resource-pod` with CPU request `500m`, CPU limit `1`, memory request `128Mi`, memory limit `256Mi`.

  **Key Commands:**
  ```bash
  kubectl run resource-pod --image=nginx \
    --requests='cpu=500m,memory=128Mi' \
    --limits='cpu=1,memory=256Mi'
  ```
  **Verify:** `kubectl describe pod resource-pod | grep -A6 "Limits:"` shows all four values correctly.
  **⚠️ Watch Out:** Limits must be ≥ requests. Setting limit < request causes pod admission failure. CPU limits are enforced via cgroups but memory limit enforcement causes OOM kills.

---

- [ ] 🔴 **#056 — Fix LimitRange admission failure**
  **Context:** Pod creation in namespace `restricted` fails with: `minimum cpu usage per Pod is 200m, but limit is 100m`.
  **Task:** Find the LimitRange in namespace `restricted`, understand the constraint, and fix the pod spec to comply with it.

  **Key Commands:**
  ```bash
  kubectl get limitrange -n restricted
  kubectl describe limitrange -n restricted
  # LimitRange requires: min CPU 200m
  # Fix pod spec CPU request to be >= 200m:
  kubectl run compliant-pod --image=nginx \
    --requests='cpu=200m,memory=128Mi' \
    --limits='cpu=500m,memory=256Mi' \
    -n restricted
  ```
  **Verify:** Pod creates successfully and is `Running`.
  **⚠️ Watch Out:** LimitRanges set **minimum**, **maximum**, and **default** values for resource requests/limits per pod or container. Admission fails if the spec violates any of these. The error message usually tells you which constraint failed.

---

- [ ] 🟡 **#057 — Create a ResourceQuota for a namespace**
  **Context:** Namespace `team-a` is used by a development team with fixed cluster capacity.
  **Task:** Create a ResourceQuota `team-a-quota` limiting: max 10 pods, max CPU requests `4`, max memory requests `8Gi`, max 5 LoadBalancer services.

  **Key Commands:**
  ```bash
  kubectl create resourcequota team-a-quota \
    --hard=pods=10,requests.cpu=4,requests.memory=8Gi,services.loadbalancers=5 \
    -n team-a
  kubectl describe resourcequota team-a-quota -n team-a
  ```
  **Verify:** `kubectl describe resourcequota team-a-quota -n team-a` shows all limits and current usage.
  **⚠️ Watch Out:** Once a ResourceQuota is active in a namespace, **all pods must have resource requests/limits specified**. Pods without them will be rejected. This commonly breaks deployments in namespaces where quotas are added mid-way.

---

### Sidecar Containers

- [ ] 🟡 **#058 — Create a pod with a native sidecar container**
  **Context:** You need a logging sidecar that starts before the main app and stays alive throughout the pod lifecycle using the new native sidecar feature (GA in v1.33+).
  **Task:** Create a pod `sidecar-pod` with main container `app` (nginx) and a native sidecar `log-forwarder` (busybox) defined in `initContainers` with `restartPolicy: Always`. The sidecar should run `tail -f /dev/null`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: sidecar-pod
  spec:
    initContainers:
    - name: log-forwarder
      image: busybox
      command: ["sh", "-c", "tail -f /dev/null"]
      restartPolicy: Always
    containers:
    - name: app
      image: nginx
  EOF
  ```
  **Verify:** `kubectl get pod sidecar-pod` shows `Running`. `kubectl describe pod sidecar-pod` shows both containers. The init container starts before `app`.
  **⚠️ Watch Out:** The native sidecar pattern requires the init container to have `restartPolicy: Always`. Without it, the init container is a regular init container that must complete (exit 0) before main containers start — not a sidecar.

---

- [ ] 🔴 **#059 — Migrate from legacy sidecar to native sidecar pattern**
  **Context:** An existing pod uses a second container in `spec.containers[]` as a makeshift sidecar. The requirement is to migrate to the native sidecar (init container with restartPolicy: Always) to ensure startup ordering guarantees.
  **Task:** Edit the pod spec to move the sidecar container from `containers[]` to `initContainers[]` with `restartPolicy: Always`. Ensure the main app container starts only after the sidecar.

  **Key Commands:**
  ```bash
  kubectl get pod legacy-pod -o yaml > /tmp/pod.yaml
  # Edit: move sidecar from containers[] to initContainers[] with restartPolicy: Always
  vim /tmp/pod.yaml
  kubectl delete pod legacy-pod
  kubectl apply -f /tmp/pod.yaml
  ```
  **Verify:** `kubectl describe pod legacy-pod` shows the sidecar in `Init Containers:` section. The main container starts after the sidecar is running.
  **⚠️ Watch Out:** You cannot edit a running pod's `initContainers` or move containers between sections without deleting and recreating the pod.

---

## 🌐 DOMAIN 3 — Services & Networking (20%)

---

### Services

- [ ] 🟢 **#060 — Expose a Deployment as ClusterIP service**
  **Context:** Deployment `web` in namespace `prod` runs on container port 8080. Internal cluster services must reach it on port 80.
  **Task:** Create ClusterIP service `web-svc` mapping port 80 to container port 8080.

  **Key Commands:**
  ```bash
  kubectl expose deployment web --name=web-svc --port=80 \
    --target-port=8080 --type=ClusterIP -n prod
  ```
  **Verify:** `kubectl get svc web-svc -n prod` shows `ClusterIP` with port `80/TCP`. `kubectl get endpoints web-svc -n prod` shows pod IPs.
  **⚠️ Watch Out:** If `--target-port` is omitted, it defaults to the same as `--port`. If the app listens on 8080 and you expose port 80 without `--target-port=8080`, the service will forward to port 80 on the pod, causing connection refused.

---

- [ ] 🟢 **#061 — Expose a Deployment as NodePort**
  **Context:** External users need to reach Deployment `api` on a fixed node port.
  **Task:** Create a NodePort service for `api` on port 30080 (external), mapping to container port 8080.

  **Key Commands:**
  ```bash
  kubectl expose deployment api --name=api-nodeport \
    --port=80 --target-port=8080 \
    --type=NodePort --node-port=30080
  ```
  **Verify:** `kubectl get svc api-nodeport` shows `NodePort` with `80:30080/TCP`. `curl <node-ip>:30080` returns a response.
  **⚠️ Watch Out:** NodePort range is `30000–32767` by default. Using a port outside this range will fail. Also, `--node-port` is not available via `kubectl expose` in older kubectl versions — you may need to use `kubectl edit svc` to set it.

---

- [ ] 🟡 **#062 — Debug service with label selector mismatch**
  **Context:** Service `backend-svc` exists but pods are not receiving traffic. The service shows `Endpoints: <none>`.
  **Task:** Diagnose the label mismatch between the service selector and pod labels, then fix it.

  **Key Commands:**
  ```bash
  kubectl describe svc backend-svc  # shows selector: app=backend
  kubectl get pods --show-labels  # shows pods with app=back-end (hyphen difference)
  # Fix A: Update service selector
  kubectl patch svc backend-svc -p '{"spec":{"selector":{"app":"back-end"}}}'
  # Fix B: Update pod labels
  kubectl label pods -l app=back-end app=backend --overwrite
  ```
  **Verify:** `kubectl get endpoints backend-svc` shows pod IPs. `kubectl describe svc backend-svc | grep Endpoints` is no longer empty.
  **⚠️ Watch Out:** Service selectors and pod labels must match exactly — Kubernetes does case-sensitive string comparison. `App=backend` ≠ `app=backend`. This is one of the most common exam traps.

---

- [ ] 🔴 **#063 — Fix service with wrong targetPort**
  **Context:** Service `api-svc` exists. Pods are Running and have correct labels. Endpoints are populated with pod IPs. But `curl` to the service returns `Connection refused`.
  **Task:** Investigate and find that the application inside the pod listens on port 9090, but the service has `targetPort: 80`. Fix the service.

  **Key Commands:**
  ```bash
  kubectl describe svc api-svc  # shows targetPort: 80
  kubectl exec <api-pod> -- ss -tlnp  # shows app listening on 9090
  kubectl patch svc api-svc \
    -p '{"spec":{"ports":[{"port":80,"targetPort":9090,"protocol":"TCP"}]}}'
  ```
  **Verify:** `kubectl run test --image=busybox --rm -it -- wget -O- http://api-svc:80` returns a response.
  **⚠️ Watch Out:** This is extra tricky because `kubectl get endpoints` shows IPs (so the selector is right), but traffic still fails because the port mapping is wrong. Always check both the selector AND the targetPort.

---

- [ ] 🟡 **#064 — Create a headless service for a StatefulSet**
  **Context:** StatefulSet `mysql` needs a headless service so that each pod gets a stable DNS name for peer discovery.
  **Task:** Create headless service `mysql-headless` (clusterIP: None) for StatefulSet `mysql` in namespace `db`. Verify DNS resolves individual pod hostnames.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Service
  metadata:
    name: mysql-headless
    namespace: db
  spec:
    clusterIP: None
    selector:
      app: mysql
    ports:
    - port: 3306
      targetPort: 3306
  EOF
  # Test DNS from a pod:
  kubectl run dns-test --image=busybox --rm -it -n db -- \
    nslookup mysql-0.mysql-headless.db.svc.cluster.local
  ```
  **Verify:** DNS lookup returns the pod's actual IP (not a virtual IP).
  **⚠️ Watch Out:** With a headless service, `clusterIP: None` means DNS returns individual pod IPs, not a single virtual IP. The StatefulSet must reference the headless service in its `spec.serviceName` field for the stable hostnames to work.

---

### Network Policies

- [ ] 🟢 **#065 — Default deny all ingress to a namespace**
  **Context:** Namespace `backend` should block all incoming traffic by default as a security baseline.
  **Task:** Create a NetworkPolicy `default-deny-ingress` in namespace `backend` that denies all ingress to all pods.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: default-deny-ingress
    namespace: backend
  spec:
    podSelector: {}
    policyTypes:
    - Ingress
  EOF
  ```
  **Verify:** `kubectl run test --image=busybox --rm -it -- wget -qO- --timeout=2 http://<backend-pod-ip>` times out.
  **⚠️ Watch Out:** `podSelector: {}` (empty selector) matches ALL pods in the namespace. If you specify a selector, only those pods are affected. An empty `ingress: []` (or omitted ingress) means deny all ingress — but you must specify `policyTypes: [Ingress]` explicitly.

---

- [ ] 🟢 **#066 — Allow traffic between specific namespaces on a port**
  **Context:** Pods labeled `app=api` in namespace `backend` should only accept traffic from namespace `frontend` on port 3000.
  **Task:** Create a NetworkPolicy allowing this specific ingress.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: allow-frontend
    namespace: backend
  spec:
    podSelector:
      matchLabels:
        app: api
    policyTypes:
    - Ingress
    ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: frontend
      ports:
      - protocol: TCP
        port: 3000
  EOF
  ```
  **Verify:** A pod in `frontend` can reach `api` pods in `backend` on port 3000. A pod from another namespace cannot.
  **⚠️ Watch Out:** To select namespaces by name, use `kubernetes.io/metadata.name: <namespace>` — this label is automatically added by Kubernetes. Older guides use `name:` which is NOT a built-in label and must be manually added.

---

- [ ] 🟡 **#067 — Fix NetworkPolicy accidentally blocking DNS**
  **Context:** After applying a strict egress NetworkPolicy in namespace `app`, pods cannot resolve service names. `curl http://backend-svc` fails with DNS lookup errors.
  **Task:** Fix the NetworkPolicy to allow egress on port 53 (UDP and TCP) to `kube-system` namespace for DNS.

  **Key Commands:**
  ```bash
  kubectl get networkpolicy -n app
  kubectl edit networkpolicy strict-egress -n app
  # Add to egress rules:
  # - to:
  #   - namespaceSelector:
  #       matchLabels:
  #         kubernetes.io/metadata.name: kube-system
  #   ports:
  #   - protocol: UDP
  #     port: 53
  #   - protocol: TCP
  #     port: 53
  ```
  **Verify:** From a pod in `app` namespace: `nslookup backend-svc.backend.svc.cluster.local` resolves correctly.
  **⚠️ Watch Out:** This is one of the most common NetworkPolicy mistakes. DNS uses both UDP and TCP port 53. If you only allow UDP, some DNS queries that fall back to TCP will fail. Always add both protocols.

---

- [ ] 🔴 **#068 — Write NetworkPolicy with AND vs OR from-rules**
  **Context:** Pods labeled `app=db` should only accept ingress from pods labeled `app=api` in the SAME namespace AND from ANY pod in namespace `monitoring`. This is a dual-condition policy.
  **Task:** Create a NetworkPolicy that correctly implements this using two separate `-from` entries (OR logic between entries, AND within an entry).

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: db-policy
    namespace: backend
  spec:
    podSelector:
      matchLabels:
        app: db
    policyTypes:
    - Ingress
    ingress:
    - from:
      - podSelector:           # Entry 1: api pods in SAME namespace
          matchLabels:
            app: api
    - from:
      - namespaceSelector:     # Entry 2: ANY pod in monitoring namespace
          matchLabels:
            kubernetes.io/metadata.name: monitoring
  EOF
  ```
  **Verify:** API pod in `backend` can reach db. Monitoring pod can reach db. Pod from another namespace cannot.
  **⚠️ Watch Out:** This is the #1 NetworkPolicy exam trap. Putting `podSelector` and `namespaceSelector` in the **SAME** `-from` entry creates an AND condition (pod must match both). Putting them in **SEPARATE** `-from` entries creates OR condition. The wrong structure silently produces incorrect behavior.

---

- [ ] 🟡 **#069 — Fix egress NetworkPolicy blocking all traffic**
  **Context:** Namespace `isolated` has a NetworkPolicy blocking all egress. Pods can't reach external services or even internal services. You must allow only DNS.
  **Task:** Add an egress rule to allow DNS (port 53 UDP+TCP) to kube-system, while keeping all other egress blocked.

  **Key Commands:**
  ```bash
  kubectl edit networkpolicy deny-all-egress -n isolated
  # Or delete and recreate:
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: deny-all-egress
    namespace: isolated
  spec:
    podSelector: {}
    policyTypes:
    - Egress
    egress:
    - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: kube-system
      ports:
      - protocol: UDP
        port: 53
      - protocol: TCP
        port: 53
  EOF
  ```
  **Verify:** `kubectl exec -n isolated <pod> -- nslookup kubernetes.default` resolves. `curl http://external-service` still fails (expected).
  **⚠️ Watch Out:** If `policyTypes: [Egress]` is listed but no `egress:` rules are provided (or it's empty `egress: []`), ALL egress is denied. You must add explicit rules to allow DNS.

---

- [ ] 🔴 **#070 — Test NetworkPolicy using a temporary test pod**
  **Context:** A NetworkPolicy was applied to namespace `secure`. You need to verify it works as intended — allowed traffic goes through, denied traffic is blocked.
  **Task:** Create two temporary test pods (one in `frontend` ns, one in `malicious` ns), use them to test connectivity to the `secure` pod on port 80, and record results in `/tmp/netpol-test.txt`.

  **Key Commands:**
  ```bash
  # Allowed: from frontend
  kubectl run allowed-test --image=busybox -n frontend --rm -it \
    -- wget -qO- --timeout=3 http://<secure-pod-ip>:80 >> /tmp/netpol-test.txt 2>&1
  # Denied: from malicious ns
  kubectl run denied-test --image=busybox -n malicious --rm -it \
    -- wget -qO- --timeout=3 http://<secure-pod-ip>:80 >> /tmp/netpol-test.txt 2>&1
  ```
  **Verify:** `/tmp/netpol-test.txt` shows response from allowed pod, timeout from denied pod.
  **⚠️ Watch Out:** Always test NetworkPolicies after applying them. A policy that looks correct in YAML can fail if namespace labels are wrong or if the CNI plugin doesn't fully support NetworkPolicy (e.g., bare Flannel does not enforce NetworkPolicy — you need Calico or Weave).

---

### Ingress

- [ ] 🟢 **#071 — Create a path-based Ingress**
  **Context:** Two services run in namespace `web`. Traffic to `/api` should go to `api-svc:8080` and traffic to `/` should go to `frontend-svc:80`.
  **Task:** Create an Ingress using IngressClass `nginx` with both path rules.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: web-ingress
    namespace: web
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
  spec:
    ingressClassName: nginx
    rules:
    - http:
        paths:
        - path: /api
          pathType: Prefix
          backend:
            service:
              name: api-svc
              port:
                number: 8080
        - path: /
          pathType: Prefix
          backend:
            service:
              name: frontend-svc
              port:
                number: 80
  EOF
  ```
  **Verify:** `kubectl describe ingress web-ingress -n web` shows both rules. HTTP requests route correctly.
  **⚠️ Watch Out:** In networking.k8s.io/v1 (stable), `backend.service.port` must use either `number:` or `name:`. The old `servicePort:` format from `extensions/v1beta1` will not work.

---

- [ ] 🟡 **#072 — Debug Ingress returning 503**
  **Context:** An Ingress resource exists and the controller is running. Requests return HTTP 503 Service Unavailable.
  **Task:** Diagnose the issue. The annotation `nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"` is wrong because the backend service speaks plain HTTP. Fix it.

  **Key Commands:**
  ```bash
  kubectl describe ingress app-ingress -n web
  kubectl get ingress app-ingress -n web -o yaml | grep annotations -A5
  kubectl annotate ingress app-ingress -n web \
    nginx.ingress.kubernetes.io/backend-protocol-   # removes the annotation
  ```
  **Verify:** HTTP request through the Ingress returns 200 OK.
  **⚠️ Watch Out:** 503 from Nginx Ingress usually means the backend is unreachable. The three most common causes: wrong annotation (like this case), backend service not running, or wrong targetPort. Always check each layer.

---

- [ ] 🟡 **#073 — Create a TLS Ingress**
  **Context:** An application in namespace `web` must be served over HTTPS. A TLS certificate is stored in Secret `web-tls` containing `tls.crt` and `tls.key`.
  **Task:** Create an Ingress that terminates TLS using the secret and routes HTTPS traffic to `frontend-svc:80`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: tls-ingress
    namespace: web
  spec:
    ingressClassName: nginx
    tls:
    - hosts:
      - myapp.example.com
      secretName: web-tls
    rules:
    - host: myapp.example.com
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: frontend-svc
              port:
                number: 80
  EOF
  ```
  **Verify:** `kubectl describe ingress tls-ingress -n web` shows the TLS section. Secret exists with correct fields.
  **⚠️ Watch Out:** The TLS Secret must have keys exactly named `tls.crt` and `tls.key` (not `cert`, not `certificate`). Use `kubectl create secret tls <name> --cert= --key=` to create it correctly.

---

- [ ] 🔴 **#074 — Resolve conflicting Ingress resources**
  **Context:** Two teams each have an Ingress in different namespaces that try to claim the same hostname `api.example.com`. Traffic routing is unpredictable.
  **Task:** Identify the conflicting Ingresses, and resolve the conflict using `ingressClassName` to assign each to a separate Ingress controller. Create IngressClass `nginx-internal` and assign one Ingress to it.

  **Key Commands:**
  ```bash
  kubectl get ingress -A  # find both
  # Create separate IngressClass:
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: IngressClass
  metadata:
    name: nginx-internal
  spec:
    controller: k8s.io/internal-ingress-nginx
  EOF
  # Update one ingress to use the new class:
  kubectl patch ingress team-b-ingress -n team-b \
    -p '{"spec":{"ingressClassName":"nginx-internal"}}'
  ```
  **Verify:** Each Ingress uses a different `ingressClassName`. Traffic is now deterministic.
  **⚠️ Watch Out:** Ingress controllers traditionally claim all Ingresses without an `ingressClassName`. Setting `ingressClassName` explicitly ensures only the matching controller processes that Ingress.

---

### Gateway API

- [ ] 🟢 **#075 — Create a GatewayClass and Gateway**
  **Context:** You are setting up Gateway API infrastructure. A GatewayClass must be created first, then a Gateway.
  **Task:** Create GatewayClass `example-gateway-class` using controller `example.io/foo-bar`. Then create Gateway `prod-gateway` using this class, listening on port 80.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: gateway.networking.k8s.io/v1
  kind: GatewayClass
  metadata:
    name: example-gateway-class
  spec:
    controllerName: example.io/foo-bar
  ---
  apiVersion: gateway.networking.k8s.io/v1
  kind: Gateway
  metadata:
    name: prod-gateway
    namespace: default
  spec:
    gatewayClassName: example-gateway-class
    listeners:
    - name: http
      port: 80
      protocol: HTTP
  EOF
  ```
  **Verify:** `kubectl get gateway prod-gateway` shows the resource. `kubectl describe gateway prod-gateway` shows listener config.
  **⚠️ Watch Out:** Gateway API CRDs must be installed before these resources can be created. In the exam, they are pre-installed. Check with `kubectl get crd | grep gateway.networking.k8s.io`.

---

- [ ] 🟢 **#076 — Create an HTTPRoute to route traffic via Gateway**
  **Context:** A Gateway named `prod-gateway` exists. Traffic arriving at the gateway for path `/shop` should be routed to Service `shop-svc:8080`.
  **Task:** Create an HTTPRoute `shop-route` that attaches to `prod-gateway` and routes `/shop` to `shop-svc`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: shop-route
    namespace: default
  spec:
    parentRefs:
    - name: prod-gateway
    rules:
    - matches:
      - path:
          type: PathPrefix
          value: /shop
      backendRefs:
      - name: shop-svc
        port: 8080
  EOF
  ```
  **Verify:** `kubectl describe httproute shop-route` shows the rule. `kubectl get httproute shop-route -o jsonpath='{.status.parents}'` shows `Accepted`.
  **⚠️ Watch Out:** The `parentRefs[].name` must exactly match the Gateway name (and optionally namespace). If the Gateway is in a different namespace, you must specify `namespace:` in the parentRef. Without it, the HTTPRoute won't be accepted.

---

- [ ] 🟡 **#077 — Migrate Ingress to Gateway API**
  **Context:** An existing Ingress routes `/app` to `app-svc:80` and `/api` to `api-svc:8080`. You must migrate to Gateway API while keeping the same routing.
  **Task:** Create a Gateway `main-gateway` and HTTPRoute `app-route` that reproduces the same rules. Then delete the Ingress.

  **Key Commands:**
  ```bash
  kubectl get ingress app-ingress -o yaml  # review existing rules
  # Create Gateway + HTTPRoute with equivalent rules
  cat <<EOF | kubectl apply -f -
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: app-route
  spec:
    parentRefs:
    - name: main-gateway
    rules:
    - matches:
      - path:
          type: PathPrefix
          value: /app
      backendRefs:
      - name: app-svc
        port: 80
    - matches:
      - path:
          type: PathPrefix
          value: /api
      backendRefs:
      - name: api-svc
        port: 8080
  EOF
  kubectl delete ingress app-ingress
  ```
  **Verify:** HTTPRoute shows `Accepted` status. Both paths route correctly through the Gateway.
  **⚠️ Watch Out:** Gateway API and Ingress are not mutually exclusive — they can coexist. Make sure to delete the old Ingress only after verifying the Gateway + HTTPRoute works correctly.

---

- [ ] 🟡 **#078 — Fix HTTPRoute with wrong parentRef**
  **Context:** HTTPRoute `my-route` exists but traffic never reaches the backend. Inspecting the route shows `ResolvedRefs: False`.
  **Task:** Check the `parentRef` in the HTTPRoute — it points to Gateway `wrong-gateway` which doesn't exist. Fix it to point to the correct Gateway `main-gateway`.

  **Key Commands:**
  ```bash
  kubectl describe httproute my-route
  # Look for: ParentRef: wrong-gateway, Status: Not accepted
  kubectl get gateway  # see available gateways
  kubectl edit httproute my-route
  # Change parentRefs[].name: wrong-gateway → main-gateway
  ```
  **Verify:** `kubectl get httproute my-route -o jsonpath='{.status.parents[0].conditions}'` shows `Accepted: True`.
  **⚠️ Watch Out:** Gateway API uses status conditions to report problems. Always check `kubectl describe httproute` and look for conditions like `ResolvedRefs: False` or `Accepted: False` with a reason message.

---

- [ ] 🔴 **#079 — Configure header-based canary routing with HTTPRoute**
  **Context:** A canary deployment is running. Requests with header `env: canary` should go to `app-canary:8080`. All others go to `app-stable:8080`.
  **Task:** Create an HTTPRoute with two rules: header match for canary, default for stable.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: canary-route
  spec:
    parentRefs:
    - name: main-gateway
    rules:
    - matches:
      - headers:
        - name: env
          value: canary
      backendRefs:
      - name: app-canary
        port: 8080
    - backendRefs:   # default rule (no match condition = matches all)
      - name: app-stable
        port: 8080
  EOF
  ```
  **Verify:** `curl -H "env: canary" http://<gateway-ip>/` hits canary. `curl http://<gateway-ip>/` hits stable.
  **⚠️ Watch Out:** Rules in an HTTPRoute are evaluated in order. The canary rule with the header match must come **before** the default rule. If the default rule is first, it will match all traffic and the canary rule is never evaluated.

---

- [ ] 🔴 **#080 — Configure HTTPS on a Gateway with TLS termination**
  **Context:** Production requires HTTPS. A TLS certificate exists in Secret `prod-tls` in namespace `default`.
  **Task:** Create a Gateway `https-gateway` that listens on port 443 with TLS termination using the certificate from `prod-tls`. Create an HTTPRoute attached to it.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: gateway.networking.k8s.io/v1
  kind: Gateway
  metadata:
    name: https-gateway
    namespace: default
  spec:
    gatewayClassName: example-gateway-class
    listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
        - name: prod-tls
          kind: Secret
  ---
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: secure-route
    namespace: default
  spec:
    parentRefs:
    - name: https-gateway
    rules:
    - backendRefs:
      - name: app-svc
        port: 80
  EOF
  ```
  **Verify:** Gateway shows `Programmed: True`. HTTPRoute shows `Accepted: True` under the https-gateway parent.
  **⚠️ Watch Out:** The `certificateRefs[].kind` defaults to `Secret` but must match an allowed resource type. If the Gateway controller doesn't have RBAC to read the Secret, TLS config will fail silently.

---

- [ ] 🟡 **#081 — Debug Gateway stuck in Unknown status**
  **Context:** Gateway `my-gateway` was created but shows `Status: Unknown`. No traffic is routed through it.
  **Task:** Determine why (the GatewayClass controller is not deployed), deploy the controller, and verify the Gateway becomes `Programmed`.

  **Key Commands:**
  ```bash
  kubectl describe gateway my-gateway  # see conditions
  kubectl get gatewayclass  # see the controller name
  kubectl get pods -A | grep <controller-name>  # controller not running
  # Deploy the gateway controller (e.g., for example.io controller):
  kubectl apply -f /opt/gateway-controller/deploy.yaml
  kubectl rollout status deploy/gateway-controller
  ```
  **Verify:** `kubectl get gateway my-gateway -o jsonpath='{.status.conditions}'` shows `Programmed: True`.
  **⚠️ Watch Out:** GatewayClass + Gateway are useless without a controller that watches them and programs the underlying load balancer or proxy. The controller's `controllerName` must match the `spec.controllerName` in the GatewayClass.

---

### CoreDNS

- [ ] 🟢 **#082 — Verify internal DNS resolution**
  **Context:** A pod needs to resolve the FQDN of service `backend-svc` in namespace `prod`.
  **Task:** From inside a test pod in namespace `web`, resolve `backend-svc.prod.svc.cluster.local` and verify it returns a ClusterIP.

  **Key Commands:**
  ```bash
  kubectl run dns-test --image=busybox -n web --rm -it \
    -- nslookup backend-svc.prod.svc.cluster.local
  # Alternatively:
  kubectl run dns-test --image=busybox -n web --rm -it \
    -- nslookup backend-svc.prod
  ```
  **Verify:** The lookup returns a valid ClusterIP (not an error).
  **⚠️ Watch Out:** FQDN format for services is `<service>.<namespace>.svc.<cluster-domain>`. Default cluster domain is `cluster.local`. If you try `nslookup backend-svc` from a different namespace, it may fail without the FQDN unless the search domain includes `prod`.

---

- [ ] 🟡 **#083 — Fix CoreDNS in CrashLoopBackOff**
  **Context:** CoreDNS pods in `kube-system` are crashing. `kubectl logs -n kube-system coredns-<hash>` shows `Corefile syntax error`.
  **Task:** Find the syntax error in the `coredns` ConfigMap in `kube-system` and fix it.

  **Key Commands:**
  ```bash
  kubectl get pods -n kube-system | grep coredns
  kubectl logs -n kube-system coredns-<pod-id> | head -20
  kubectl edit configmap coredns -n kube-system
  # Common issues: missing closing brace }, wrong plugin name, invalid forward address
  # After fixing, restart CoreDNS:
  kubectl rollout restart deployment coredns -n kube-system
  ```
  **Verify:** `kubectl get pods -n kube-system | grep coredns` shows `Running`. DNS resolution works from test pod.
  **⚠️ Watch Out:** The CoreDNS Corefile uses a specific DSL syntax. A single missing `}` causes all DNS to fail cluster-wide. After editing the ConfigMap, CoreDNS must be restarted (it doesn't hot-reload in all versions).

---

- [ ] 🔴 **#084 — Fix pod with wrong dnsPolicy**
  **Context:** Pod `isolated-pod` can resolve external hostnames (`google.com`) but cannot resolve internal service names (`backend-svc.default`). Other pods work fine.
  **Task:** Inspect the pod's DNS config — `dnsPolicy: None` was set with only external nameservers in `dnsConfig`. Fix it to use `ClusterFirst`.

  **Key Commands:**
  ```bash
  kubectl get pod isolated-pod -o yaml | grep -A10 "dnsPolicy"
  kubectl get pod isolated-pod -o yaml > /tmp/pod.yaml
  # Edit: change dnsPolicy: None → dnsPolicy: ClusterFirst, remove custom dnsConfig
  vim /tmp/pod.yaml
  kubectl delete pod isolated-pod
  kubectl apply -f /tmp/pod.yaml
  ```
  **Verify:** `kubectl exec isolated-pod -- nslookup backend-svc.default` resolves correctly.
  **⚠️ Watch Out:** `dnsPolicy: None` tells the kubelet to use ONLY the `dnsConfig` you provide. If that config doesn't include the cluster DNS server, internal names won't resolve. `ClusterFirst` (the default) always uses the cluster DNS first.

---

## 💾 DOMAIN 4 — Storage (10%)

---

- [ ] 🟢 **#085 — Create a PV with hostPath and bind it with a PVC**
  **Context:** A pod needs persistent storage backed by a local host path.
  **Task:** Create PV `pv-data` with capacity `5Gi`, `ReadWriteOnce` access mode, `Retain` reclaim policy, hostPath `/mnt/data`. Create PVC `pvc-data` that binds to it. Verify binding.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv-data
  spec:
    capacity:
      storage: 5Gi
    accessModes:
    - ReadWriteOnce
    persistentVolumeReclaimPolicy: Retain
    hostPath:
      path: /mnt/data
  ---
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: pvc-data
  spec:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: 5Gi
  EOF
  ```
  **Verify:** `kubectl get pv pv-data` shows `Bound`. `kubectl get pvc pvc-data` shows `Bound` to `pv-data`.
  **⚠️ Watch Out:** For a PVC to bind to a specific PV, the access mode, storage size, and StorageClass must all be compatible. If the PVC requests more storage than the PV has, it won't bind.

---

- [ ] 🟢 **#086 — Mount a PVC into a pod**
  **Context:** Application `app` needs to read and write files to persistent storage.
  **Task:** Mount PVC `app-storage` into pod `file-writer` at path `/data`. Verify the pod can read and write files there.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: file-writer
  spec:
    containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "echo hello > /data/test.txt && sleep 3600"]
      volumeMounts:
      - name: storage
        mountPath: /data
    volumes:
    - name: storage
      persistentVolumeClaim:
        claimName: app-storage
  EOF
  kubectl exec file-writer -- cat /data/test.txt
  ```
  **Verify:** `kubectl exec file-writer -- cat /data/test.txt` returns `hello`.
  **⚠️ Watch Out:** The PVC must be in the same namespace as the pod. A PVC in `default` namespace cannot be mounted by a pod in `prod` namespace.

---

- [ ] 🟡 **#087 — Fix PVC stuck in Pending due to size mismatch**
  **Context:** PVC `big-claim` requests `10Gi` but the only available PV `pv-small` has `5Gi`. The PVC stays `Pending`.
  **Task:** Fix the PVC to request `5Gi` instead of `10Gi`, or expand the PV. Choose the most practical solution.

  **Key Commands:**
  ```bash
  kubectl get pvc big-claim  # shows Pending
  kubectl get pv  # shows pv-small with 5Gi
  # Cannot edit resources on a Pending PVC easily - delete and recreate:
  kubectl delete pvc big-claim
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: big-claim
  spec:
    accessModes: [ReadWriteOnce]
    resources:
      requests:
        storage: 5Gi
  EOF
  ```
  **Verify:** `kubectl get pvc big-claim` shows `Bound`.
  **⚠️ Watch Out:** You cannot edit the `resources.requests.storage` of a PVC that already exists (only expansion is allowed if StorageClass supports it). Delete and recreate is usually the fastest solution in an exam.

---

- [ ] 🔴 **#088 — Create a static PV that matches a PVC's StorageClass**
  **Context:** PVC `premium-claim` with `storageClassName: premium` is in `Pending`. No dynamic provisioner handles the `premium` class.
  **Task:** Create a static PV `premium-pv` with `storageClassName: premium` that the PVC can bind to.

  **Key Commands:**
  ```bash
  kubectl get pvc premium-claim -o yaml | grep storageClass
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: premium-pv
  spec:
    capacity:
      storage: 10Gi
    accessModes:
    - ReadWriteOnce
    storageClassName: premium
    persistentVolumeReclaimPolicy: Retain
    hostPath:
      path: /mnt/premium
  EOF
  ```
  **Verify:** `kubectl get pvc premium-claim` transitions from `Pending` to `Bound`.
  **⚠️ Watch Out:** A PVC with a specific `storageClassName` will ONLY bind to PVs with the exact same `storageClassName`. A PV with no storageClass will not bind to a PVC with a storageClass specified.

---

- [ ] 🟡 **#089 — Reclaim a Released PV for reuse**
  **Context:** A pod was deleted and its PVC was also deleted. The PV `pv-data` is now in `Released` state but cannot be reused because the old `claimRef` still holds it.
  **Task:** Manually clear the `claimRef` from the PV so it returns to `Available` state and can be bound by a new PVC.

  **Key Commands:**
  ```bash
  kubectl get pv pv-data  # shows Released
  kubectl patch pv pv-data \
    -p '{"spec":{"claimRef": null}}'
  kubectl get pv pv-data  # should now show Available
  ```
  **Verify:** `kubectl get pv pv-data` shows `Available`. A new PVC can now bind to it.
  **⚠️ Watch Out:** This only applies to PVs with `Retain` reclaim policy. PVs with `Delete` policy are automatically deleted when their PVC is deleted. PVs with `Recycle` policy are deprecated. Most exam scenarios use `Retain`.

---

- [ ] 🟢 **#090 — Create a StorageClass with WaitForFirstConsumer**
  **Context:** A StorageClass is needed for local storage that shouldn't provision a volume until a pod actually needs it.
  **Task:** Create StorageClass `local-wait` using `kubernetes.io/no-provisioner` and `volumeBindingMode: WaitForFirstConsumer`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: local-wait
  provisioner: kubernetes.io/no-provisioner
  volumeBindingMode: WaitForFirstConsumer
  EOF
  ```
  **Verify:** `kubectl get storageclass local-wait` shows the class. PVCs using it stay `Pending` until a pod is scheduled.
  **⚠️ Watch Out:** `WaitForFirstConsumer` means the PVC stays in `Pending` until a pod that uses it is scheduled. This is NOT an error — it's the intended behavior for topology-aware storage.

---

- [ ] 🟡 **#091 — Change the default StorageClass**
  **Context:** The current default StorageClass `standard` needs to be replaced by `fast` as the new default.
  **Task:** Remove the default annotation from `standard` and add it to `fast`.

  **Key Commands:**
  ```bash
  kubectl patch storageclass standard \
    -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
  kubectl patch storageclass fast \
    -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
  kubectl get storageclass  # confirm only fast shows (default)
  ```
  **Verify:** `kubectl get storageclass` shows `fast` as `(default)` and `standard` without the annotation.
  **⚠️ Watch Out:** If TWO StorageClasses both have `is-default-class: "true"`, PVCs without an explicit `storageClassName` will be rejected with an ambiguity error. Ensure only one default exists.

---

- [ ] 🔴 **#092 — Fix StatefulSet PVC provisioning with missing StorageClass**
  **Context:** StatefulSet `redis` uses `storageClassName: ssd-fast` in its `volumeClaimTemplate`. The StorageClass doesn't exist. Pods are in `Pending` with PVC errors.
  **Task:** Create the missing `ssd-fast` StorageClass (use local-path or standard provisioner for the exam) and verify pods start.

  **Key Commands:**
  ```bash
  kubectl get pvc -n cache  # shows Pending PVCs
  kubectl describe pvc data-redis-0 -n cache | grep "no provisioner"
  cat <<EOF | kubectl apply -f -
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: ssd-fast
  provisioner: rancher.io/local-path   # or use cluster's available provisioner
  reclaimPolicy: Delete
  volumeBindingMode: WaitForFirstConsumer
  EOF
  ```
  **Verify:** PVCs transition to `Bound`. StatefulSet pods start Running.
  **⚠️ Watch Out:** The available provisioner depends on the exam cluster setup. Check what provisioners are installed with `kubectl get storageclass`. Use an existing provisioner name rather than inventing one.

---

- [ ] 🟡 **#093 — Share a volume between two containers in a pod**
  **Context:** Two containers in the same pod need to share files through a common directory.
  **Task:** Create a pod `shared-vol-pod` with an `emptyDir` volume mounted at `/shared` by both container `writer` (writes data) and container `reader` (reads data). Verify file sharing works.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: shared-vol-pod
  spec:
    containers:
    - name: writer
      image: busybox
      command: ["sh", "-c", "echo 'shared content' > /shared/data.txt && sleep 3600"]
      volumeMounts:
      - name: shared
        mountPath: /shared
    - name: reader
      image: busybox
      command: ["sh", "-c", "sleep 5 && cat /shared/data.txt && sleep 3600"]
      volumeMounts:
      - name: shared
        mountPath: /shared
    volumes:
    - name: shared
      emptyDir: {}
  EOF
  kubectl logs shared-vol-pod -c reader
  ```
  **Verify:** `kubectl logs shared-vol-pod -c reader` shows `shared content`.
  **⚠️ Watch Out:** `emptyDir` volumes are ephemeral — they are deleted when the pod is removed from a node. They persist through container restarts within the same pod, but not pod restarts on different nodes.

---

- [ ] 🟢 **#094 — Mount a ConfigMap as individual files in a volume**
  **Context:** An application reads configuration from files in `/config/`, one file per key.
  **Task:** Create ConfigMap `app-files` with keys `app.conf` and `log.conf`. Mount it as a volume so both keys appear as separate files under `/config/`.

  **Key Commands:**
  ```bash
  kubectl create configmap app-files \
    --from-literal=app.conf="server_port=8080" \
    --from-literal=log.conf="log_level=info"
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: config-reader
  spec:
    containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "ls /config/ && sleep 3600"]
      volumeMounts:
      - name: config-vol
        mountPath: /config
    volumes:
    - name: config-vol
      configMap:
        name: app-files
  EOF
  kubectl exec config-reader -- ls /config/
  ```
  **Verify:** `kubectl exec config-reader -- ls /config/` shows `app.conf` and `log.conf`.
  **⚠️ Watch Out:** When mounting a ConfigMap as a volume (without `subPath`), ALL keys become files in the directory. The mountPath is the directory — do NOT set it to a specific file path unless using `subPath`.

---

- [ ] 🔴 **#095 — Fix PVC access mode incompatibility**
  **Context:** PVC `multi-read` uses `ReadWriteMany` access mode. It stays `Pending` because the `standard` StorageClass only supports `ReadWriteOnce`.
  **Task:** Diagnose the access mode incompatibility, delete the PVC, and recreate it with `ReadWriteOnce`. Update the pod spec if necessary.

  **Key Commands:**
  ```bash
  kubectl get pvc multi-read -o yaml | grep accessModes
  kubectl get storageclass standard -o yaml | grep allowedTopologies
  kubectl describe pvc multi-read | grep "no persistent volumes available"
  # Delete and recreate with correct access mode:
  kubectl delete pvc multi-read
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: multi-read
  spec:
    accessModes: [ReadWriteOnce]
    storageClassName: standard
    resources:
      requests:
        storage: 5Gi
  EOF
  ```
  **Verify:** `kubectl get pvc multi-read` shows `Bound`.
  **⚠️ Watch Out:** `ReadWriteMany` (RWX) is only supported by specific storage backends (NFS, CephFS, EFS). Most simple provisioners support only `ReadWriteOnce`. The exam question may hint at this by using a `hostPath` provisioner.

---

## 🔧 DOMAIN 5 — Troubleshooting (30%)

---

### Control Plane Troubleshooting

- [ ] 🟢 **#096 — Fix kube-apiserver with bad etcd-servers flag**
  **Context:** The kube-apiserver is down. `kubectl` commands return `connection refused`. SSH to the control plane — `crictl ps` shows apiserver in `Exited` state.
  **Task:** Find and fix the typo in `/etc/kubernetes/manifests/kube-apiserver.yaml` in the `--etcd-servers` flag (e.g., port is `2380` instead of `2379`).

  **Key Commands:**
  ```bash
  ssh controlplane
  crictl ps -a | grep apiserver
  crictl logs <container-id> 2>&1 | tail -20
  cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep etcd-servers
  # Fix: change port 2380 to 2379
  vim /etc/kubernetes/manifests/kube-apiserver.yaml
  # Wait for kubelet to restart the pod:
  watch crictl ps | grep apiserver
  ```
  **Verify:** `kubectl get nodes` returns results within 30 seconds of the fix.
  **⚠️ Watch Out:** etcd listens on `2379` for client connections and `2380` for peer connections. The apiserver uses the **client** port (`2379`). This specific mistake is a classic CKA exam trap.

---

- [ ] 🟢 **#097 — Fix kube-scheduler not scheduling pods**
  **Context:** Pods are stuck in `Pending` indefinitely. The scheduler seems to not be running.
  **Task:** Check the scheduler static pod, find the broken configuration (wrong `--config` path), fix it, and verify pods get scheduled.

  **Key Commands:**
  ```bash
  kubectl get pods -A | grep scheduler
  crictl ps -a | grep scheduler
  cat /etc/kubernetes/manifests/kube-scheduler.yaml | grep "\-\-config"
  ls /etc/kubernetes/  # look for the actual config file
  # Fix the path in the manifest:
  vim /etc/kubernetes/manifests/kube-scheduler.yaml
  ```
  **Verify:** Pending pods start getting scheduled and enter `Running` state.
  **⚠️ Watch Out:** The scheduler config file is referenced in the static pod manifest. If the file path doesn't exist on the host, the scheduler container fails to start. Check both the manifest flag AND whether the file actually exists at that path.

---

- [ ] 🟡 **#098 — Fix kube-controller-manager with wrong cluster-cidr**
  **Context:** New pods are not getting IPs. The controller-manager has a wrong `--cluster-cidr` that doesn't match the actual pod network CIDR.
  **Task:** Check the running cluster CIDR (from existing pods), compare with the controller-manager flag, fix the mismatch.

  **Key Commands:**
  ```bash
  kubectl get pods -A -o wide | awk '{print $7}' | grep -v IP | head -5
  # Current pod IPs suggest 10.244.x.x
  cat /etc/kubernetes/manifests/kube-controller-manager.yaml | grep cluster-cidr
  # If it shows 10.96.0.0/12 (wrong), fix it:
  vim /etc/kubernetes/manifests/kube-controller-manager.yaml
  # Change to: --cluster-cidr=10.244.0.0/16
  ```
  **Verify:** Controller-manager restarts. New pods receive IPs in the `10.244.0.0/16` range.
  **⚠️ Watch Out:** The `--cluster-cidr` in the controller-manager must match the CIDR used by the CNI plugin. This is set during `kubeadm init` and should not change.

---

- [ ] 🔴 **#099 — Renew expired TLS certificates**
  **Context:** The cluster was left idle for over a year. All control plane certificates have expired. `kubectl` returns `x509: certificate has expired`.
  **Task:** Use `kubeadm certs check-expiration` to confirm which certs expired, then renew them all with `kubeadm certs renew all`.

  **Key Commands:**
  ```bash
  kubeadm certs check-expiration
  kubeadm certs renew all
  # Restart control plane components (they cache certificates):
  kill $(pidof kube-apiserver kube-controller-manager kube-scheduler) 2>/dev/null || true
  # Or move and restore static pod manifests:
  mv /etc/kubernetes/manifests/*.yaml /tmp/
  sleep 10
  mv /tmp/*.yaml /etc/kubernetes/manifests/
  # Update kubeconfig:
  cp /etc/kubernetes/admin.conf ~/.kube/config
  ```
  **Verify:** `kubeadm certs check-expiration` shows all certs valid for ~1 year. `kubectl get nodes` works.
  **⚠️ Watch Out:** After renewing certificates, control plane components must be restarted — they don't auto-reload certs. Also update `~/.kube/config` which contains the old certificate. This step is commonly forgotten.

---

- [ ] 🔴 **#100 — Debug apiserver crashing due to bad audit log path**
  **Context:** After enabling audit logging in the kube-apiserver manifest, the apiserver crashes because the audit log directory doesn't exist on the host.
  **Task:** Find the audit log path in the manifest, create the directory on the host, and verify the apiserver recovers.

  **Key Commands:**
  ```bash
  crictl logs $(crictl ps -a | grep apiserver | awk '{print $1}') 2>&1 | grep audit
  cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep audit-log-path
  # e.g., --audit-log-path=/var/log/kubernetes/audit.log
  mkdir -p /var/log/kubernetes
  # Wait for kubelet to restart apiserver:
  watch crictl ps | grep apiserver
  ```
  **Verify:** `crictl ps | grep apiserver` shows `Running`. `kubectl get nodes` returns results.
  **⚠️ Watch Out:** The audit log directory must exist on the **host** filesystem AND be mounted into the apiserver pod (check `hostPath` volumes in the manifest). If the mount exists but the directory doesn't, the container fails to start.

---

### Node Troubleshooting

- [ ] 🟢 **#101 — Fix stopped kubelet on a worker node**
  **Context:** Node `worker02` shows `NotReady`. From the control plane, you can still SSH to it.
  **Task:** SSH into `worker02`, check kubelet status, restart it, and verify the node returns to `Ready`.

  **Key Commands:**
  ```bash
  ssh worker02
  systemctl status kubelet
  systemctl start kubelet
  systemctl enable kubelet
  # Back on control plane:
  kubectl get nodes
  ```
  **Verify:** `kubectl get nodes` shows `worker02` as `Ready` within 1 minute.
  **⚠️ Watch Out:** Always use `systemctl status kubelet` before restarting. If the kubelet keeps failing (crash loop), there's an underlying config error — restarting won't fix it. Read the status output carefully.

---

- [ ] 🟡 **#102 — Fix kubelet with wrong CA certificate path**
  **Context:** Node `worker01` is `NotReady`. `systemctl status kubelet` shows it's failing with `x509: certificate signed by unknown authority`.
  **Task:** Inspect `/var/lib/kubelet/config.yaml` — the `clientCAFile` path is wrong. Fix it to point to the correct CA certificate at `/etc/kubernetes/pki/ca.crt`.

  **Key Commands:**
  ```bash
  ssh worker01
  systemctl status kubelet
  journalctl -u kubelet -n 50 | grep -i "error\|fail\|cert"
  cat /var/lib/kubelet/config.yaml | grep clientCA
  # Fix the wrong path:
  vim /var/lib/kubelet/config.yaml
  # Change to: clientCAFile: /etc/kubernetes/pki/ca.crt
  systemctl restart kubelet
  ```
  **Verify:** `systemctl status kubelet` shows `active (running)`. Node returns to `Ready`.
  **⚠️ Watch Out:** `journalctl -u kubelet -n 50` gives the last 50 lines of kubelet logs. This is the fastest way to identify the exact error. Don't skip reading the logs.

---

- [ ] 🟡 **#103 — Fix node with missing CRI socket**
  **Context:** Node `worker03` shows `NotReady`. `crictl info` fails with `connect: no such file or directory`.
  **Task:** Determine containerd is not running. Start it and configure kubelet to use the correct socket.

  **Key Commands:**
  ```bash
  ssh worker03
  systemctl status containerd
  systemctl start containerd
  systemctl enable containerd
  # If socket path is wrong in kubelet:
  cat /var/lib/kubelet/config.yaml | grep containerRuntime
  # Or check kubelet service file:
  cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
  systemctl restart kubelet
  ```
  **Verify:** `crictl info` returns runtime info. `kubectl get nodes` shows `worker03` as `Ready`.
  **⚠️ Watch Out:** If containerd was never installed, you'll need to install it: `apt-get install -y containerd.io` and then configure it: `containerd config default > /etc/containerd/config.toml`.

---

- [ ] 🔴 **#104 — Identify and evict high-memory pods from pressured node**
  **Context:** Node `worker01` has condition `MemoryPressure: True`. New pods are not being scheduled on it.
  **Task:** Use `kubectl top pods -A` to find the top memory consumers on `worker01`. Evict the highest consumer. Verify memory pressure clears.

  **Key Commands:**
  ```bash
  kubectl top pods -A --sort-by=memory | head -10
  kubectl get pods -A -o wide | grep worker01
  # Identify which pods are on worker01 and consuming most memory
  kubectl delete pod <high-memory-pod> -n <namespace>
  # Wait and check:
  kubectl describe node worker01 | grep MemoryPressure
  ```
  **Verify:** `kubectl describe node worker01 | grep MemoryPressure` shows `False` after the high-memory pod is removed.
  **⚠️ Watch Out:** Node conditions like `MemoryPressure` trigger the kubelet's eviction manager which may already be evicting pods. If the node itself is OOM-killed, you'll need to SSH in using crictl to diagnose.

---

- [ ] 🔴 **#105 — Restore kubelet config from backup after node restart**
  **Context:** After a node restart, the kubelet fails because `/var/lib/kubelet/config.yaml` is missing (was accidentally deleted).
  **Task:** Restore the kubelet config from the backup at `/opt/backups/kubelet-config.yaml` and restart kubelet.

  **Key Commands:**
  ```bash
  ssh <failed-node>
  ls /var/lib/kubelet/config.yaml  # missing
  cp /opt/backups/kubelet-config.yaml /var/lib/kubelet/config.yaml
  systemctl restart kubelet
  systemctl status kubelet
  ```
  **Verify:** `systemctl status kubelet` shows `active (running)`. Node appears Ready in `kubectl get nodes`.
  **⚠️ Watch Out:** The kubelet config must match the cluster's CA, API server address, and kubelet identity certificates. Using a config from a different node or cluster will cause authentication failures.

---

### etcd Backup & Restore

- [ ] 🟡 **#106 — Take an etcd snapshot (with correct cert paths)**
  **Context:** You need to back up the etcd database. The etcd TLS certificate paths are NOT at the default locations — you must find them by inspecting the etcd pod.
  **Task:** Find the actual cert paths by describing the etcd pod, then use `etcdctl` to take a snapshot to `/opt/backup/etcd-snapshot.db`.

  **Key Commands:**
  ```bash
  # Find the cert paths from the running etcd pod:
  kubectl get pod -n kube-system etcd-controlplane -o yaml | grep -E "\-\-cert|\-\-key|\-\-ca|\-\-endpoints"
  # Run backup with discovered paths:
  ETCDCTL_API=3 etcdctl snapshot save /opt/backup/etcd-snapshot.db \
    --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key
  ETCDCTL_API=3 etcdctl snapshot status /opt/backup/etcd-snapshot.db
  ```
  **Verify:** `etcdctl snapshot status /opt/backup/etcd-snapshot.db` shows a valid snapshot with non-zero revision number.
  **⚠️ Watch Out:** ALWAYS find cert paths from the actual running etcd pod spec — they may differ from documentation. Using wrong paths returns `authentication failure` or `certificate signed by unknown authority`.

---

- [ ] 🔴 **#107 — Restore etcd from snapshot to new data directory**
  **Context:** The cluster data is corrupted. A valid snapshot exists at `/opt/backup/etcd-snapshot.db`. You must restore it.
  **Task:** Restore the snapshot to `/var/lib/etcd-restore`. Update the etcd static pod manifest to use the new data directory. Verify the cluster recovers.

  **Key Commands:**
  ```bash
  # Restore snapshot:
  ETCDCTL_API=3 etcdctl snapshot restore /opt/backup/etcd-snapshot.db \
    --data-dir=/var/lib/etcd-restore
  # Update etcd manifest to point to new dir:
  vim /etc/kubernetes/manifests/etcd.yaml
  # Change: hostPath path and --data-dir flag from /var/lib/etcd to /var/lib/etcd-restore
  # Wait for etcd and apiserver to restart:
  watch crictl ps | grep etcd
  ```
  **Verify:** `kubectl get nodes` returns results. Cluster state reflects pre-corruption data.
  **⚠️ Watch Out:** Two places in `etcd.yaml` must be updated: (1) the `--data-dir` argument AND (2) the `volumes[].hostPath.path` that mounts the data dir into the container. Changing only one will leave etcd pointing to the old directory.

---

- [ ] 🔴 **#108 — Fix permission error during etcd restore**
  **Context:** `etcdctl snapshot restore` completed but etcd fails to start. Logs show `permission denied` on `/var/lib/etcd-restore`.
  **Task:** Fix ownership of the restored directory to `etcd:etcd` and verify etcd starts.

  **Key Commands:**
  ```bash
  ls -la /var/lib/ | grep etcd-restore  # shows root:root ownership
  chown -R etcd:etcd /var/lib/etcd-restore
  # If etcd user doesn't exist, check the user ID etcd runs as:
  kubectl get pod -n kube-system etcd-controlplane -o yaml | grep runAsUser
  # Then chown using UID:
  chown -R <uid>:<gid> /var/lib/etcd-restore
  ```
  **Verify:** `crictl ps | grep etcd` shows Running. `kubectl get nodes` returns results.
  **⚠️ Watch Out:** `etcdctl snapshot restore` creates the directory with `root:root` ownership. If etcd runs as a non-root user (UID 0 in most kubeadm setups, but varies), the ownership must match. Check the pod's securityContext to be sure.

---

- [ ] 🔴 **#109 — Fix apiserver connectivity to etcd after restore**
  **Context:** After an etcd restore, the etcd pod is Running but `kubectl` returns `etcdserver: no leader`. The apiserver is talking to the old etcd data directory.
  **Task:** Verify the etcd manifest was updated to the restored directory. Restart the apiserver to force it to reconnect to etcd.

  **Key Commands:**
  ```bash
  cat /etc/kubernetes/manifests/etcd.yaml | grep data-dir
  cat /etc/kubernetes/manifests/etcd.yaml | grep "path:" | grep etcd
  # Both should point to /var/lib/etcd-restore
  # If apiserver is still starting against old state, restart it:
  mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
  sleep 10
  mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
  ```
  **Verify:** `kubectl get nodes` returns cluster nodes within 30 seconds.
  **⚠️ Watch Out:** The apiserver may cache its connection to etcd. Temporarily moving the apiserver manifest out of `/etc/kubernetes/manifests/` and back forces kubelet to restart it cleanly, picking up the recovered etcd state.

---

### Pod & Application Troubleshooting

- [ ] 🟢 **#110 — Retrieve previous container logs**
  **Context:** Pod `app-pod` is in `CrashLoopBackOff`. The current container has already crashed and its logs may be empty.
  **Task:** Retrieve the logs from the previous (crashed) container instance and save them to `/tmp/crash-logs.txt`.

  **Key Commands:**
  ```bash
  kubectl logs app-pod --previous > /tmp/crash-logs.txt
  kubectl describe pod app-pod | grep -A5 "Last State:"
  ```
  **Verify:** `/tmp/crash-logs.txt` contains the application's last output before crashing. Check the exit code with `kubectl describe pod app-pod | grep "Exit Code:"`.
  **⚠️ Watch Out:** `kubectl logs <pod>` (without `--previous`) shows logs from the CURRENT running container. If the current container also crashed immediately, the logs may be empty. Always use `--previous` first when troubleshooting crashes.

---

- [ ] 🟢 **#111 — Fix ImagePullBackOff by correcting the image tag**
  **Context:** Pod `api-pod` is in `ImagePullBackOff`. The image `myapp:v1.2` doesn't exist in the registry. Only `myapp:v1.1` is available.
  **Task:** Update the pod's image to `myapp:v1.1` and verify it starts.

  **Key Commands:**
  ```bash
  kubectl describe pod api-pod | grep "Failed to pull image"
  # It's a standalone Pod, not a Deployment — must delete and recreate:
  kubectl get pod api-pod -o yaml > /tmp/pod.yaml
  sed -i 's/myapp:v1.2/myapp:v1.1/' /tmp/pod.yaml
  kubectl delete pod api-pod
  kubectl apply -f /tmp/pod.yaml
  ```
  **Verify:** `kubectl get pod api-pod` shows `Running`. `kubectl describe pod api-pod | grep Image:` shows `myapp:v1.1`.
  **⚠️ Watch Out:** You cannot directly edit a standalone pod's image using `kubectl edit` and have it take effect (container spec is mostly immutable). Delete and recreate the pod with the corrected image. For Deployments, use `kubectl set image`.

---

- [ ] 🟡 **#112 — Fix OOMKilled pod by increasing memory limit**
  **Context:** Pod `memory-hog` is repeatedly showing `OOMKilled` (Exit Code 137). The memory limit is set to `64Mi` but the app requires at least `256Mi`.
  **Task:** The pod is managed by a Deployment `memory-hog-deploy`. Update the Deployment's memory limit to `256Mi`.

  **Key Commands:**
  ```bash
  kubectl describe pod -l app=memory-hog | grep "OOMKilled"
  kubectl set resources deployment memory-hog-deploy \
    --limits=memory=256Mi \
    --requests=memory=128Mi
  kubectl rollout status deployment memory-hog-deploy
  ```
  **Verify:** `kubectl get pods -l app=memory-hog` shows `Running`. `kubectl describe pod <new-pod> | grep Memory:` shows the updated limits.
  **⚠️ Watch Out:** Exit Code `137` = OOMKilled (signal SIGKILL from OOM killer). Exit Code `1` = application error. Exit Code `0` = normal exit. Knowing exit codes helps diagnose crash causes instantly.

---

- [ ] 🟡 **#113 — Fix pod stuck in Pending due to untolerated taint**
  **Context:** Pod `special-job` is stuck in `Pending` with event: `0/3 nodes are available: 3 node(s) had untolerated taint {gpu:NoSchedule}`.
  **Task:** The pod must run on GPU nodes. Add the appropriate toleration to the pod spec.

  **Key Commands:**
  ```bash
  kubectl describe pod special-job | grep "Tolerations\|Taints"
  kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
  # Fix pod (delete and recreate with toleration):
  kubectl get pod special-job -o yaml > /tmp/pod.yaml
  # Add toleration in spec:
  # tolerations:
  # - key: gpu
  #   effect: NoSchedule
  vim /tmp/pod.yaml
  kubectl delete pod special-job
  kubectl apply -f /tmp/pod.yaml
  ```
  **Verify:** Pod gets scheduled and enters `Running` state on a GPU node.
  **⚠️ Watch Out:** A toleration allows a pod to be scheduled on a tainted node. It does NOT guarantee the pod goes to that node (use `nodeSelector` or `nodeName` for that). Toleration + taint = "may schedule here"; `nodeSelector` = "must schedule here".

---

- [ ] 🔴 **#114 — Unblock pod stuck in Init state by creating missing service**
  **Context:** Pod `app-with-init` is stuck in `Init:0/1`. The init container is waiting for service `database-svc` to be reachable before exiting.
  **Task:** Determine what the init container is waiting for (inspect its command), create the missing service, and verify the pod starts.

  **Key Commands:**
  ```bash
  kubectl describe pod app-with-init | grep -A5 "Init Containers:"
  kubectl logs app-with-init -c init-container  # shows: waiting for database-svc
  # Create the missing service:
  kubectl expose deployment database --name=database-svc --port=5432
  # Wait for init container to complete:
  kubectl get pod app-with-init -w
  ```
  **Verify:** Pod transitions from `Init:0/1` → `PodInitializing` → `Running`.
  **⚠️ Watch Out:** Init containers that wait for services are a common exam pattern. If the init container is using `nslookup` or `curl` in a loop, creating the service is often all you need. Check the init container's `command` field to know exactly what it's waiting for.

---

- [ ] 🟡 **#115 — Fix overly aggressive liveness probe**
  **Context:** Deployment `slow-start-app` pods are in a constant restart loop. The app takes 30 seconds to initialize but the liveness probe starts checking after 5 seconds.
  **Task:** Update the Deployment to set `initialDelaySeconds: 30` on the liveness probe.

  **Key Commands:**
  ```bash
  kubectl describe pod -l app=slow-start-app | grep -A10 "Liveness:"
  kubectl edit deployment slow-start-app
  # Under livenessProbe, change:
  # initialDelaySeconds: 5 → initialDelaySeconds: 30
  kubectl rollout status deployment slow-start-app
  ```
  **Verify:** Pods stay `Running` without restarting. `kubectl describe pod <pod> | grep "Restart Count:"` shows 0 after the fix.
  **⚠️ Watch Out:** Kubernetes restarts containers when liveness probes fail. If the app is healthy but just starting slowly, the probe thinks it's dead and kills it — creating a restart loop. `initialDelaySeconds` tells Kubernetes to wait before starting probe checks.

---

- [ ] 🔴 **#116 — Fix pod with deleted Secret breaking a container**
  **Context:** Pod `dual-container-pod` has two containers. Container `app` is Running but container `sidecar` is in `Error` state. The sidecar mounts Secret `api-keys` which was accidentally deleted.
  **Task:** Identify the missing Secret from pod events, recreate it with the correct name and values, and verify both containers are Running.

  **Key Commands:**
  ```bash
  kubectl describe pod dual-container-pod | grep -A10 "sidecar"
  kubectl get events | grep "dual-container-pod" | grep "secret"
  # Recreate the secret:
  kubectl create secret generic api-keys \
    --from-literal=API_KEY=abc123 \
    --from-literal=API_SECRET=xyz789
  # Delete pod so it can restart and re-mount the secret:
  kubectl delete pod dual-container-pod
  kubectl apply -f /opt/pods/dual-container-pod.yaml
  ```
  **Verify:** `kubectl get pod dual-container-pod` shows `2/2 Running`.
  **⚠️ Watch Out:** If a Secret that a pod mounts is deleted AFTER the pod starts, the existing pod keeps running (volume is cached). But if the pod restarts (or is new), the mount will fail and the container enters `CreateContainerConfigError`.

---

### Service & Networking Troubleshooting

- [ ] 🟢 **#117 — Fix service selector mismatch**
  **Context:** Service `frontend-svc` shows no endpoints. Pods are Running with label `app=frontend-v2` but the service selector is `app=frontend`.
  **Task:** Update the service selector to match the pod labels.

  **Key Commands:**
  ```bash
  kubectl get svc frontend-svc -o jsonpath='{.spec.selector}'
  kubectl get pods --show-labels | grep frontend
  kubectl patch svc frontend-svc -p '{"spec":{"selector":{"app":"frontend-v2"}}}'
  kubectl get endpoints frontend-svc
  ```
  **Verify:** `kubectl get endpoints frontend-svc` shows pod IPs. `curl` through the service returns a response.
  **⚠️ Watch Out:** Always inspect BOTH the service selector AND the pod labels before assuming there's a deeper networking issue. The vast majority of "service not working" issues in the exam are label mismatches.

---

- [ ] 🟡 **#118 — Fix NetworkPolicy blocking cross-namespace traffic**
  **Context:** Pod in `app` namespace cannot reach pods in `db` namespace. All traffic was working before a NetworkPolicy was applied.
  **Task:** Identify the NetworkPolicy blocking traffic and add a rule to allow ingress from the `app` namespace on port 5432.

  **Key Commands:**
  ```bash
  kubectl get networkpolicy -n db
  kubectl describe networkpolicy deny-all -n db
  # Edit to allow from app namespace:
  kubectl edit networkpolicy deny-all -n db
  # Add ingress rule:
  # ingress:
  # - from:
  #   - namespaceSelector:
  #       matchLabels:
  #         kubernetes.io/metadata.name: app
  #   ports:
  #   - port: 5432
  #     protocol: TCP
  ```
  **Verify:** `kubectl exec -n app <pod> -- nc -zv <db-pod-ip> 5432` succeeds.
  **⚠️ Watch Out:** Verify the `app` namespace has the correct label for the namespaceSelector to work. If it doesn't, add it: `kubectl label namespace app kubernetes.io/metadata.name=app`.

---

- [ ] 🔴 **#119 — Fix pod with misconfigured dnsConfig**
  **Context:** Pod `custom-dns-pod` can ping external IPs but cannot resolve internal service names. `/etc/resolv.conf` inside the pod shows wrong nameservers.
  **Task:** Fix the pod's `dnsPolicy` from `None` to `ClusterFirst`. Remove the incorrect `dnsConfig` that was overriding cluster DNS.

  **Key Commands:**
  ```bash
  kubectl get pod custom-dns-pod -o yaml | grep -A15 "dnsPolicy\|dnsConfig"
  kubectl get pod custom-dns-pod -o yaml > /tmp/pod.yaml
  vim /tmp/pod.yaml
  # Change dnsPolicy: None → dnsPolicy: ClusterFirst
  # Remove the entire dnsConfig section
  kubectl delete pod custom-dns-pod
  kubectl apply -f /tmp/pod.yaml
  kubectl exec custom-dns-pod -- cat /etc/resolv.conf
  ```
  **Verify:** `/etc/resolv.conf` inside the pod shows the cluster DNS server IP and `search default.svc.cluster.local svc.cluster.local cluster.local`.
  **⚠️ Watch Out:** When `dnsPolicy: None` is used, you must provide a complete `dnsConfig`. If it's misconfigured, DNS breaks completely inside that pod — but external IPs still work because routing is independent of DNS.

---

- [ ] 🔴 **#120 — Fix Ingress returning 404 due to wrong pathType**
  **Context:** Ingress routes `/api/v1/users` to backend service. Returns 404. The service and pods are healthy.
  **Task:** Diagnose that `pathType: Exact` is used but the app expects any path under `/api/v1`. Change to `pathType: Prefix`.

  **Key Commands:**
  ```bash
  kubectl get ingress app-ingress -o yaml | grep -A5 "path:"
  # Shows: pathType: Exact
  kubectl edit ingress app-ingress
  # Change: pathType: Exact → pathType: Prefix
  ```
  **Verify:** `curl http://<ingress-ip>/api/v1/users` returns 200. `curl http://<ingress-ip>/api/v1/anything` also returns 200 (because Prefix matches all sub-paths).
  **⚠️ Watch Out:** `Exact` matches ONLY the literal path. `Prefix` matches the path and all sub-paths. `ImplementationSpecific` behavior depends on the Ingress controller. Most apps need `Prefix` for API routes.

---

- [ ] 🟡 **#121 — Fix NodePort service unreachable due to stopped kube-proxy**
  **Context:** NodePort service `api-np` on port 32000 was working yesterday. Now external clients can't connect. Pods are Running.
  **Task:** Diagnose that kube-proxy is not running on the target node, restart it, and verify the service is accessible.

  **Key Commands:**
  ```bash
  kubectl get pods -n kube-system -o wide | grep kube-proxy
  # kube-proxy pod on worker01 is in CrashLoopBackOff
  kubectl logs -n kube-system kube-proxy-<id> | tail -20
  kubectl delete pod kube-proxy-<id> -n kube-system  # DaemonSet will recreate
  # Check iptables rules on the node:
  ssh worker01 "iptables -t nat -L KUBE-SERVICES | grep 32000"
  ```
  **Verify:** kube-proxy pod is `Running`. NodePort is accessible externally.
  **⚠️ Watch Out:** kube-proxy is a DaemonSet in `kube-system`. If a pod is crashing, deleting it causes the DaemonSet to recreate it (which may fix transient issues). Check the logs before deleting.

---

### Monitoring & Logs

- [ ] 🟢 **#122 — Find top CPU-consuming pod and save result**
  **Context:** The cluster is under high CPU load and you need to identify the culprit.
  **Task:** Find the pod consuming the most CPU across all namespaces. Save its name and namespace to `/tmp/top-cpu.txt`.

  **Key Commands:**
  ```bash
  kubectl top pods -A --sort-by=cpu | head -2
  # Output the top pod info:
  kubectl top pods -A --sort-by=cpu | sed -n '2p' | awk '{print $1, $2}' > /tmp/top-cpu.txt
  ```
  **Verify:** `cat /tmp/top-cpu.txt` shows a namespace and pod name.
  **⚠️ Watch Out:** `kubectl top pods -A` requires metrics-server. If it's not installed, install it first. The output format is `NAMESPACE NAME CPU(cores) MEMORY(bytes)`.

---

- [ ] 🟢 **#123 — Find top memory-consuming node**
  **Context:** A node is suspected of being memory-constrained. You need to identify which node has the highest memory usage.
  **Task:** Use `kubectl top nodes` to find the node with the most memory usage. Save its name to `/tmp/top-node.txt`.

  **Key Commands:**
  ```bash
  kubectl top nodes --sort-by=memory
  kubectl top nodes --sort-by=memory | sed -n '2p' | awk '{print $1}' > /tmp/top-node.txt
  ```
  **Verify:** `cat /tmp/top-node.txt` contains a valid node name.
  **⚠️ Watch Out:** `kubectl top nodes` shows absolute values (Mi) and percentages. Sort by `memory` for absolute usage. The output changes rapidly — run it a few times if the top node seems unexpected.

---

- [ ] 🟡 **#124 — Retrieve logs from a specific container in a multi-container pod**
  **Context:** Pod `multi-pod` in namespace `prod` has three containers: `app`, `sidecar`, and `logger`. You need logs from only the `sidecar` container.
  **Task:** Retrieve logs specifically from container `sidecar`. Save them to `/tmp/sidecar-logs.txt`.

  **Key Commands:**
  ```bash
  kubectl logs multi-pod -c sidecar -n prod > /tmp/sidecar-logs.txt
  # If the container already restarted:
  kubectl logs multi-pod -c sidecar -n prod --previous >> /tmp/sidecar-logs.txt
  ```
  **Verify:** `cat /tmp/sidecar-logs.txt` shows logs from the sidecar container only.
  **⚠️ Watch Out:** If `-c <container-name>` is omitted in a multi-container pod, `kubectl logs` will return an error: "Please specify a container". You must always specify the container name for multi-container pods.

---

- [ ] 🟡 **#125 — Stream and filter deployment logs**
  **Context:** Deployment `web-app` is producing errors and you need to capture the error lines for analysis.
  **Task:** Stream logs from all pods in Deployment `web-app`, filter lines containing `ERROR`, and save the first 20 matching lines to `/tmp/errors.txt`.

  **Key Commands:**
  ```bash
  kubectl logs -l app=web-app -f --max-log-requests=10 \
    | grep "ERROR" \
    | head -20 \
    > /tmp/errors.txt
  # Alternative using deployment selector:
  kubectl logs deployment/web-app --all-containers \
    | grep "ERROR" | head -20 > /tmp/errors.txt
  ```
  **Verify:** `wc -l /tmp/errors.txt` shows up to 20 lines. Each line contains `ERROR`.
  **⚠️ Watch Out:** `kubectl logs -l <selector>` streams from multiple pods simultaneously. Use `--max-log-requests` to avoid the "too many log requests" error when there are many pods. The `-f` flag streams — combine with `head -20` to cap output.

---

- [ ] 🔴 **#126 — Install metrics-server and verify functionality**
  **Context:** `kubectl top` returns `Error from server (ServiceUnavailable): the server is currently unable to handle the request`. Metrics-server is not installed.
  **Task:** Install metrics-server using the official manifest. If the cluster uses self-signed certs, add the `--kubelet-insecure-tls` flag. Verify `kubectl top nodes` works.

  **Key Commands:**
  ```bash
  # Download and apply metrics-server:
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  # For clusters with self-signed TLS (common in exam):
  kubectl patch deployment metrics-server -n kube-system \
    --type=json \
    -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
  kubectl rollout status deployment metrics-server -n kube-system
  kubectl top nodes
  ```
  **Verify:** `kubectl top nodes` returns node CPU/memory data without errors.
  **⚠️ Watch Out:** The `--kubelet-insecure-tls` flag is needed when kubelet uses self-signed certificates (typical in kubeadm clusters without proper cert setup). Without it, metrics-server fails to scrape node metrics.

---

## 🎯 MIXED HARD & TRICKY SCENARIOS

---

### JSONPath & Output

- [ ] 🟢 **#127 — Custom column output for pods**
  **Context:** An auditor needs a report of all pods with their namespace and node assignment.
  **Task:** List all pods in all namespaces with custom columns: NAMESPACE, NAME, NODE. Save to `/tmp/pod-nodes.txt`.

  **Key Commands:**
  ```bash
  kubectl get pods -A -o custom-columns=\
  NAMESPACE:.metadata.namespace,NAME:.metadata.name,NODE:.spec.nodeName \
  > /tmp/pod-nodes.txt
  ```
  **Verify:** `cat /tmp/pod-nodes.txt` shows properly formatted columns for all pods.
  **⚠️ Watch Out:** Custom column paths use JSONPath notation. `.spec.nodeName` returns the node for running pods but is empty for Pending pods (not yet scheduled).

---

- [ ] 🟡 **#128 — Extract ClusterIP using JSONPath**
  **Context:** A script needs the ClusterIP of service `backend-svc` in namespace `prod` without additional formatting.
  **Task:** Use JSONPath to extract only the ClusterIP value and save it to `/tmp/clusterip.txt`.

  **Key Commands:**
  ```bash
  kubectl get svc backend-svc -n prod \
    -o jsonpath='{.spec.clusterIP}' > /tmp/clusterip.txt
  cat /tmp/clusterip.txt
  ```
  **Verify:** `cat /tmp/clusterip.txt` shows only the IP (e.g., `10.96.45.123`) with no extra whitespace.
  **⚠️ Watch Out:** `jsonpath='{.spec.clusterIP}'` does not add a newline. If you need a newline for scripting, append `{"\n"}` at the end: `jsonpath='{.spec.clusterIP}{"\n"}'`.

---

- [ ] 🟡 **#129 — List all container images across the cluster**
  **Context:** A security audit needs a unique list of all container images running in the cluster.
  **Task:** Use JSONPath to extract all container images from all pods across all namespaces. Sort and deduplicate. Save to `/tmp/images.txt`.

  **Key Commands:**
  ```bash
  kubectl get pods -A \
    -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' \
    | sort -u > /tmp/images.txt
  ```
  **Verify:** `cat /tmp/images.txt` shows unique image names, one per line.
  **⚠️ Watch Out:** This JSONPath uses `range` to iterate over items and containers. The `{end}` closes each range. Also include initContainers if the question asks for all images: add another range for `.spec.initContainers[*]`.

---

- [ ] 🔴 **#130 — Find pods with no resource limits**
  **Context:** A compliance check requires identifying all pods that have no resource limits defined.
  **Task:** List all pods across all namespaces where containers have no `limits` defined. Save pod names to `/tmp/no-limits.txt`.

  **Key Commands:**
  ```bash
  kubectl get pods -A -o json | \
    jq -r '.items[] | select(.spec.containers[].resources.limits == null) | 
    "\(.metadata.namespace)/\(.metadata.name)"' > /tmp/no-limits.txt
  # Alternative without jq:
  kubectl get pods -A \
    -o jsonpath='{range .items[*]}{.metadata.namespace}{"/"}{.metadata.name}{" limits: "}{range .spec.containers[*]}{.resources.limits}{" "}{end}{"\n"}{end}' \
    | grep "limits: <no value>" > /tmp/no-limits.txt
  ```
  **Verify:** `/tmp/no-limits.txt` lists pods without resource limits.
  **⚠️ Watch Out:** Use `jq` if it's available in the exam environment — it's much cleaner for complex JSON filtering. If not, use kubectl's built-in JSONPath with `select()`.

---

### Certificates & Security

- [ ] 🟡 **#131 — Create a CertificateSigningRequest and approve it**
  **Context:** User `alice` needs a client certificate to authenticate to the cluster.
  **Task:** Create a CSR for `alice`, approve it with `kubectl certificate approve`, and extract the signed certificate to `/tmp/alice.crt`.

  **Key Commands:**
  ```bash
  # Generate key and CSR:
  openssl genrsa -out /tmp/alice.key 2048
  openssl req -new -key /tmp/alice.key \
    -subj "/CN=alice/O=engineering" \
    -out /tmp/alice.csr
  # Encode and create Kubernetes CSR:
  cat <<EOF | kubectl apply -f -
  apiVersion: certificates.k8s.io/v1
  kind: CertificateSigningRequest
  metadata:
    name: alice-csr
  spec:
    request: $(cat /tmp/alice.csr | base64 | tr -d '\n')
    signerName: kubernetes.io/kube-apiserver-client
    usages: [client auth]
  EOF
  kubectl certificate approve alice-csr
  kubectl get csr alice-csr -o jsonpath='{.status.certificate}' | base64 -d > /tmp/alice.crt
  ```
  **Verify:** `openssl x509 -in /tmp/alice.crt -noout -subject` shows `CN=alice, O=engineering`.
  **⚠️ Watch Out:** The `usages` field must include `client auth`. The `signerName` must be `kubernetes.io/kube-apiserver-client` for client authentication. Using a wrong signer causes the CSR to be rejected.

---

- [ ] 🔴 **#132 — Fix wrong kubeconfig server address**
  **Context:** Running `kubectl` with context `prod-cluster` fails: `dial tcp: connection refused`. The API server address in the kubeconfig is wrong.
  **Task:** Fix the server URL for context `prod-cluster` in `~/.kube/config`.

  **Key Commands:**
  ```bash
  kubectl config view --context=prod-cluster | grep server
  # Shows: server: https://wrong-ip:6443
  kubectl config set-cluster prod-cluster --server=https://192.168.1.10:6443
  kubectl config use-context prod-cluster
  kubectl get nodes
  ```
  **Verify:** `kubectl get nodes --context=prod-cluster` returns nodes without connection errors.
  **⚠️ Watch Out:** `kubectl config set-cluster` modifies the cluster entry, not the context. The context points to both a cluster AND a user. Make sure you're fixing the right cluster entry that the context references.

---

- [ ] 🟡 **#133 — Switch between kubeconfig contexts**
  **Context:** The exam environment has two clusters. Questions alternate between them. You must work on the correct cluster per question.
  **Task:** List all available contexts, switch to `dev-cluster`, run a command, then switch back to `prod-cluster`.

  **Key Commands:**
  ```bash
  kubectl config get-contexts
  kubectl config use-context dev-cluster
  kubectl get nodes  # verify you're on dev-cluster
  # Run dev-specific commands...
  kubectl config use-context prod-cluster
  kubectl get nodes  # verify you're back on prod-cluster
  ```
  **Verify:** `kubectl config current-context` shows the expected context after each switch.
  **⚠️ Watch Out:** In the real exam, EACH QUESTION specifies which cluster context to use. Always run the `kubectl config use-context <name>` command at the start of each question. Forgetting costs you the entire task.

---

### Namespace Isolation

- [ ] 🟡 **#134 — Apply and test ResourceQuota**
  **Context:** Namespace `dev` needs resource constraints to prevent over-allocation.
  **Task:** Create ResourceQuota `dev-quota` in namespace `dev` limiting: pods to 10, Services to 5, ConfigMaps to 10. Try to exceed the pod limit to verify enforcement.

  **Key Commands:**
  ```bash
  kubectl create resourcequota dev-quota -n dev \
    --hard=pods=10,services=5,configmaps=10
  kubectl describe resourcequota dev-quota -n dev
  # Test enforcement:
  for i in $(seq 1 11); do
    kubectl run test-pod-$i --image=nginx -n dev
  done
  # The 11th pod should fail with "quota exceeded"
  ```
  **Verify:** Creating the 11th pod fails with a ResourceQuota exceeded message.
  **⚠️ Watch Out:** ResourceQuota requires pods to have resource requests/limits if the quota includes `requests.cpu` or `requests.memory`. A quota with only `pods=10` (count quota) doesn't require resource specs.

---

- [ ] 🟡 **#135 — Create LimitRange with defaults for a namespace**
  **Context:** Namespace `team-b` has many workloads without resource specs. Add defaults to automatically apply resource limits.
  **Task:** Create a LimitRange in `team-b` that defaults: CPU limit `500m`, memory limit `256Mi`, CPU request `200m`, memory request `128Mi` for all containers.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: v1
  kind: LimitRange
  metadata:
    name: team-b-defaults
    namespace: team-b
  spec:
    limits:
    - type: Container
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 200m
        memory: 128Mi
  EOF
  # Verify by creating a pod without resource spec:
  kubectl run test --image=nginx -n team-b
  kubectl describe pod test -n team-b | grep -A6 "Limits:"
  ```
  **Verify:** The test pod has limits and requests automatically applied from the LimitRange.
  **⚠️ Watch Out:** LimitRange defaults apply only to new pods. Existing pods already in the namespace are not affected. `default` sets the limit, `defaultRequest` sets the request when none is specified.

---

### Debugging & Ephemeral Containers

- [ ] 🟡 **#136 — Debug a distroless pod using ephemeral container**
  **Context:** Pod `production-app` uses a distroless image with no shell or debugging tools. It's misbehaving and you need to investigate.
  **Task:** Attach an ephemeral `busybox` debugging container to the running pod and inspect its network connections and environment.

  **Key Commands:**
  ```bash
  kubectl debug -it production-app --image=busybox --target=production-app
  # Inside the ephemeral container:
  # You share the process namespace (with --target flag):
  ps aux
  env
  netstat -tlnp
  exit
  ```
  **Verify:** The ephemeral container attaches and you can run debugging commands.
  **⚠️ Watch Out:** The `--target=<container-name>` flag is needed to share the process namespace with the main container. Without it, you only see the ephemeral container's own processes. Ephemeral containers cannot be removed once added — they persist until the pod is deleted.

---

- [ ] 🔴 **#137 — Debug a node using a privileged pod**
  **Context:** A node-level issue needs investigation. You need to run commands in the node's host namespaces.
  **Task:** Launch a debug pod on `worker01` with host PID, network, and IPC namespaces using `kubectl debug node/worker01`. Inspect the kubelet process.

  **Key Commands:**
  ```bash
  kubectl debug node/worker01 -it --image=ubuntu
  # Inside the pod (mounted at /host):
  chroot /host
  ps aux | grep kubelet
  journalctl -u kubelet -n 50
  exit
  ```
  **Verify:** From inside the debug pod, you can see host processes and kubelet logs.
  **⚠️ Watch Out:** `kubectl debug node/` creates a pod with `hostPID: true`, `hostNetwork: true`, and mounts the node root at `/host`. You must `chroot /host` to run commands in the node's filesystem context.

---

### PriorityClass & PDB

- [ ] 🟡 **#138 — Create a PriorityClass and assign it to a Deployment**
  **Context:** Critical application `core-service` must survive node evictions when resources are scarce.
  **Task:** Create PriorityClass `high-priority` with value `1000000` and `globalDefault: false`. Assign it to Deployment `core-service`.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: scheduling.k8s.io/v1
  kind: PriorityClass
  metadata:
    name: high-priority
  value: 1000000
  globalDefault: false
  description: "High priority for core services"
  EOF
  kubectl patch deployment core-service \
    -p '{"spec":{"template":{"spec":{"priorityClassName":"high-priority"}}}}'
  kubectl rollout status deployment core-service
  ```
  **Verify:** `kubectl get pods -l app=core-service -o jsonpath='{.items[0].spec.priorityClassName}'` returns `high-priority`.
  **⚠️ Watch Out:** Higher priority pods preempt lower priority pods when resources are scarce. Setting `globalDefault: true` makes this the default for all pods without an explicit PriorityClass. Be careful — the system and cluster-critical pods already have priorities set.

---

- [ ] 🔴 **#139 — Create a PodDisruptionBudget**
  **Context:** Deployment `critical-app` has 5 replicas. During maintenance (node drains), at least 3 must remain available at all times.
  **Task:** Create a PodDisruptionBudget `critical-app-pdb` that ensures minimum 3 pods are always available.

  **Key Commands:**
  ```bash
  kubectl create poddisruptionbudget critical-app-pdb \
    --selector=app=critical-app \
    --min-available=3
  kubectl get pdb critical-app-pdb
  kubectl describe pdb critical-app-pdb
  ```
  **Verify:** `kubectl describe pdb critical-app-pdb` shows `Min Available: 3`, `Allowed disruptions: 2` (with 5 pods).
  **⚠️ Watch Out:** `min-available` and `max-unavailable` are mutually exclusive. Use `min-available` when you know the minimum needed. Use `max-unavailable` when you want to express how many can be down. A PDB with `min-available` equal to the replica count blocks ALL voluntary disruptions.

---

### Static Pods

- [ ] 🟡 **#140 — Create a static pod on a worker node**
  **Context:** A monitoring agent must run as a static pod (not managed by Kubernetes scheduler) on node `worker01`.
  **Task:** Create static pod `monitor-agent` on `worker01` by placing its manifest in the kubelet's staticPodPath directory. Verify it appears in `kubectl get pods`.

  **Key Commands:**
  ```bash
  # Find staticPodPath:
  ssh worker01
  cat /var/lib/kubelet/config.yaml | grep staticPodPath
  # Default: /etc/kubernetes/manifests
  cat <<EOF > /etc/kubernetes/manifests/monitor-agent.yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: monitor-agent
    namespace: kube-system
  spec:
    containers:
    - name: monitor
      image: busybox
      command: ["sleep", "3600"]
  EOF
  # From control plane:
  kubectl get pods -n kube-system | grep monitor-agent
  ```
  **Verify:** `kubectl get pods -n kube-system | grep monitor-agent` shows the static pod (with node suffix, e.g., `monitor-agent-worker01`).
  **⚠️ Watch Out:** Static pod names get the node name appended automatically (e.g., `monitor-agent-worker01`). You cannot delete static pods with `kubectl delete pod` — you must remove the manifest file from the node.

---

- [ ] 🔴 **#141 — Fix a broken static pod manifest on a node**
  **Context:** A static pod manifest at `/etc/kubernetes/manifests/agent.yaml` on `worker02` has `image: busybox:invalid-tag`. The static pod is in a restart loop.
  **Task:** SSH into `worker02`, fix the image to `busybox:latest` in the manifest file, and verify the static pod starts successfully.

  **Key Commands:**
  ```bash
  ssh worker02
  cat /etc/kubernetes/manifests/agent.yaml | grep image
  sed -i 's/busybox:invalid-tag/busybox:latest/' /etc/kubernetes/manifests/agent.yaml
  # Kubelet detects the change automatically:
  crictl ps | grep agent  # wait for it to start
  # From control plane:
  kubectl get pods -A | grep agent-worker02
  ```
  **Verify:** Static pod transitions to `Running` state. `kubectl get pods -A | grep agent-worker02` shows `Running`.
  **⚠️ Watch Out:** Kubelet watches the staticPodPath directory and detects changes automatically. You don't need to restart kubelet after editing a static pod manifest. Changes take effect within a few seconds.

---

### EndpointSlices

- [ ] 🟡 **#142 — Debug service with pod missing from endpoints**
  **Context:** Service `api-svc` has 3 pods but `kubectl get endpoints api-svc` shows only 2 IPs.
  **Task:** Identify which pod is missing (its readiness probe is failing) and trace the exact readiness probe failure.

  **Key Commands:**
  ```bash
  kubectl get pods -l app=api --show-labels
  kubectl get endpoints api-svc
  kubectl get endpointslice -l kubernetes.io/service-name=api-svc
  # Find the unready pod:
  kubectl get pods -l app=api -o wide | grep "0/1"
  kubectl describe pod <unready-pod> | grep -A10 "Readiness:"
  kubectl logs <unready-pod> | tail -20  # check app errors
  ```
  **Verify:** After fixing the readiness probe or app config, `kubectl get endpoints api-svc` shows all 3 pod IPs.
  **⚠️ Watch Out:** Only pods whose readiness probes pass are added to the Endpoints/EndpointSlice. A pod that's `Running` but not `Ready` (e.g., `1/2 Ready`) will NOT receive service traffic. This is by design.

---

- [ ] 🔴 **#143 — Compare Endpoints with EndpointSlices**
  **Context:** You need to understand the difference between the older Endpoints API and newer EndpointSlices for a service `api-svc`.
  **Task:** Inspect both `kubectl get endpoints api-svc` and `kubectl get endpointslice`. Find a pod marked `NotReady` in EndpointSlices that's not reflected in old Endpoints. Save the difference to `/tmp/ep-diff.txt`.

  **Key Commands:**
  ```bash
  kubectl get endpoints api-svc -o yaml > /tmp/ep-old.txt
  kubectl get endpointslice -l kubernetes.io/service-name=api-svc -o yaml > /tmp/ep-slice.txt
  # EndpointSlice shows readiness per endpoint; old Endpoints API doesn't show NotReady pods
  diff /tmp/ep-old.txt /tmp/ep-slice.txt > /tmp/ep-diff.txt
  # Find NotReady condition:
  kubectl get endpointslice -l kubernetes.io/service-name=api-svc \
    -o jsonpath='{range .items[*].endpoints[*]}{.addresses[0]}{" ready: "}{.conditions.ready}{"\n"}{end}'
  ```
  **Verify:** `/tmp/ep-diff.txt` shows differences. EndpointSlice output shows individual endpoint readiness.
  **⚠️ Watch Out:** EndpointSlices track readiness per individual endpoint and support dual-stack IPs. The older `Endpoints` object is deprecated (deprecation warning added in v1.33) and will be removed in a future version. Familiarize yourself with EndpointSlice queries.

---

### Full-Stack Application Scenarios

- [ ] 🔴 **#144 — Full RBAC audit and cleanup**
  **Context:** A security review found that several ClusterRoleBindings grant `cluster-admin` to non-system users.
  **Task:** List all ClusterRoleBindings granting `cluster-admin` role. Save the list to `/tmp/admin-audit.txt`. Remove any binding for user `rogue-admin`.

  **Key Commands:**
  ```bash
  kubectl get clusterrolebindings -o json \
    | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | 
    .metadata.name + ": " + (.subjects[]? | .kind + "/" + .name)' \
    > /tmp/admin-audit.txt
  cat /tmp/admin-audit.txt
  # Remove rogue-admin binding:
  kubectl get clusterrolebindings -o json \
    | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | 
    select(.subjects[]?.name=="rogue-admin") | .metadata.name'
  kubectl delete clusterrolebinding <name-of-rogue-binding>
  ```
  **Verify:** `/tmp/admin-audit.txt` lists all cluster-admin bindings. `kubectl auth can-i --list --as=rogue-admin` no longer shows cluster-admin privileges.
  **⚠️ Watch Out:** Verify you delete the BINDING (ClusterRoleBinding), not the ClusterRole itself. Deleting `cluster-admin` ClusterRole would break the cluster. Verify the binding name carefully before deleting.

---

- [ ] 🔴 **#145 — Drain, upgrade, and uncordon a node**
  **Context:** Worker node `worker01` needs a kubelet upgrade to v1.34. It must be drained first to avoid disruption.
  **Task:** Drain `worker01` (ignoring DaemonSets), upgrade kubelet to v1.34, then uncordon it.

  **Key Commands:**
  ```bash
  kubectl drain worker01 --ignore-daemonsets --delete-emptydir-data --force
  ssh worker01
  apt-get update
  apt-get install -y kubeadm=1.34.0-1.1
  kubeadm upgrade node
  apt-get install -y kubelet=1.34.0-1.1 kubectl=1.34.0-1.1
  systemctl daemon-reload && systemctl restart kubelet
  exit
  kubectl uncordon worker01
  kubectl get nodes
  ```
  **Verify:** `kubectl get nodes worker01` shows `v1.34.0` and `Ready`.
  **⚠️ Watch Out:** `kubectl drain` with `--delete-emptydir-data` evicts pods that use emptyDir volumes (data is lost). The `--force` flag evicts pods not owned by a controller. Always double-check that important stateful workloads are replicated before draining.

---

- [ ] 🔴 **#146 — Complete networking isolation with Gateway + NetworkPolicy**
  **Context:** Deploy a complete isolated application stack in namespace `production`.
  **Task:** Create: Deployment `app` (3 replicas, nginx), ClusterIP Service `app-svc`, Gateway `app-gateway`, HTTPRoute routing `/` to `app-svc`, and a NetworkPolicy allowing ingress only from the `gateway` namespace on port 80.

  **Key Commands:**
  ```bash
  kubectl create ns production
  kubectl create deployment app --image=nginx --replicas=3 -n production
  kubectl expose deployment app --name=app-svc --port=80 --target-port=80 -n production
  # Gateway:
  kubectl apply -f - <<EOF
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: app-route
    namespace: production
  spec:
    parentRefs:
    - name: app-gateway
    rules:
    - backendRefs:
      - name: app-svc
        port: 80
  EOF
  # NetworkPolicy:
  cat <<EOF | kubectl apply -f -
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: allow-gateway-only
    namespace: production
  spec:
    podSelector: {}
    policyTypes: [Ingress]
    ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: gateway
      ports:
      - port: 80
  EOF
  ```
  **Verify:** All resources created. Traffic from `gateway` ns reaches pods. Traffic from other namespaces is blocked.
  **⚠️ Watch Out:** This scenario tests multiple domains simultaneously (Workloads, Services, Gateway API, NetworkPolicy). Budget at least 10 minutes. Create resources in order: Deployment → Service → HTTPRoute → NetworkPolicy. Verify each step before moving to the next.

---

- [ ] 🔴 **#147 — StatefulSet with PVC auto-delete policy (v1.32+ GA)**
  **Context:** StatefulSet `cache` should automatically delete its PVCs when the StatefulSet is deleted or scaled down (using the new `persistentVolumeClaimRetentionPolicy` field, GA in v1.32).
  **Task:** Create StatefulSet `cache` with `persistentVolumeClaimRetentionPolicy: {whenDeleted: Delete, whenScaled: Delete}`. Verify PVCs are auto-deleted when scaling down.

  **Key Commands:**
  ```bash
  cat <<EOF | kubectl apply -f -
  apiVersion: apps/v1
  kind: StatefulSet
  metadata:
    name: cache
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: cache
    serviceName: cache-headless
    persistentVolumeClaimRetentionPolicy:
      whenDeleted: Delete
      whenScaled: Delete
    template:
      metadata:
        labels:
          app: cache
      spec:
        containers:
        - name: redis
          image: redis:7
          volumeMounts:
          - name: data
            mountPath: /data
    volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 1Gi
  EOF
  # Scale down and verify PVC deletion:
  kubectl scale sts cache --replicas=1
  kubectl get pvc | grep cache
  ```
  **Verify:** After scaling from 3 to 1, PVCs `data-cache-1` and `data-cache-2` are automatically deleted.
  **⚠️ Watch Out:** This feature requires the `StatefulSetAutoDeletePVC` feature gate (enabled by default in v1.32+). The policy values are `Retain` (default, old behavior) and `Delete`. This is new to the 2025 curriculum.

---

- [ ] 🔴 **#148 — In-place pod vertical scaling (v1.33+ beta)**
  **Context:** Pod `running-app` is consuming too much memory but you don't want to restart it. Kubernetes v1.33+ supports in-place vertical scaling.
  **Task:** Change the memory limit of the running pod from `128Mi` to `256Mi` without restarting it. Verify the new limit takes effect.

  **Key Commands:**
  ```bash
  kubectl get pod running-app -o jsonpath='{.spec.containers[0].resources}'
  # Patch resources in-place:
  kubectl patch pod running-app --subresource=resize \
    -p '{"spec":{"containers":[{"name":"app","resources":{"limits":{"memory":"256Mi"}}}]}}'
  kubectl get pod running-app -o jsonpath='{.status.containerStatuses[0].resources}'
  ```
  **Verify:** `kubectl describe pod running-app | grep Memory:` shows the updated limit. Pod continues running without restart.
  **⚠️ Watch Out:** In-place resizing uses the `resize` subresource. CPU requests/limits can be adjusted without restart in most cases. Memory limit increases usually work without restart; memory limit decreases may require a restart if the current usage exceeds the new limit.

---

### Timed Simulation Tasks

- [ ] 🔴 **#149 — ⏱️ 8-minute cluster recovery task**
  **Context:** You arrive at the exam to find: (1) kube-apiserver manifest has a wrong flag, (2) kube-scheduler is not running, (3) worker01 is NotReady.
  **Task:** Fix all three issues as fast as possible. Time yourself — this should take under 8 minutes.
  **Step-by-step approach:**
  ```bash
  # Step 1 (2 min): Fix apiserver
  ssh controlplane
  crictl logs $(crictl ps -a | grep apiserver | awk '{print $1}') 2>&1 | tail -5
  vim /etc/kubernetes/manifests/kube-apiserver.yaml  # fix the flag
  # Step 2 (2 min): Fix scheduler
  crictl ps -a | grep scheduler
  cat /etc/kubernetes/manifests/kube-scheduler.yaml | grep config
  vim /etc/kubernetes/manifests/kube-scheduler.yaml  # fix config path
  # Step 3 (3 min): Fix worker01
  ssh worker01
  systemctl status kubelet
  # Fix whatever is broken (usually: start stopped service, fix cert path, or fix config)
  systemctl restart kubelet
  # Step 4 (1 min): Verify
  kubectl get nodes  # all Ready
  kubectl get pods -A  # all Running
  ```
  **Verify:** All nodes Ready, all system pods Running, scheduler showing as running.
  **⚠️ Watch Out:** Time pressure is the main challenge. Use `crictl logs` immediately — don't guess at the problem. Fix one issue at a time and verify before moving on.

---

- [ ] 🔴 **#150 — ⏱️ 10-minute full-stack deployment task**
  **Context:** Deploy a complete application stack from scratch. Everything must be in namespace `production`.
  **Task:** Create: (1) Namespace `production`, (2) ConfigMap `app-env` with `ENV=prod`, (3) Secret `db-secret` with `password=supersecret`, (4) Deployment `webapp` (3 replicas, nginx, using ConfigMap and Secret), (5) ClusterIP Service `webapp-svc` on port 80, (6) HPA scaling 2-8 replicas at 70% CPU, (7) NetworkPolicy allowing only ingress from namespace `gateway` on port 80, (8) PVC `webapp-storage` 2Gi, mounted at `/data`.
  **Step-by-step approach:**
  ```bash
  # 1. Namespace
  kubectl create ns production
  # 2. ConfigMap
  kubectl create configmap app-env --from-literal=ENV=prod -n production
  # 3. Secret
  kubectl create secret generic db-secret --from-literal=password=supersecret -n production
  # 4. Deployment (generate YAML, edit, apply)
  kubectl create deploy webapp --image=nginx --replicas=3 -n production \
    --dry-run=client -o yaml > /tmp/webapp.yaml
  # Edit: add envFrom, volumeMount, volume, PVC reference
  kubectl apply -f /tmp/webapp.yaml
  # 5. Service
  kubectl expose deploy webapp --name=webapp-svc --port=80 -n production
  # 6. HPA
  kubectl autoscale deploy webapp --min=2 --max=8 --cpu-percent=70 -n production
  # 7. NetworkPolicy
  kubectl apply -f /tmp/netpol.yaml  # pre-written
  # 8. PVC
  kubectl apply -f /tmp/pvc.yaml    # pre-written
  # Verify all:
  kubectl get all,pvc,hpa,networkpolicy,configmap,secret -n production
  ```
  **Verify:** All 8 resource types exist in namespace `production`. Deployment has 3 replicas Running.
  **⚠️ Watch Out:** Use `--dry-run=client -o yaml` to generate YAML for complex specs rather than writing from scratch. Edit the generated YAML to add volume mounts, env vars, etc. This saves 3–4 minutes per task.

---

## ⚡ Expert Quick Reference

### Most Dangerous Exam Traps

| # | Trap | What Goes Wrong | Fix |
|---|------|----------------|-----|
| 1 | Wrong context | Working on the wrong cluster | Always set context at start of each question |
| 2 | etcd cert paths | Using `/etc/etcd/` instead of actual paths | Always `kubectl get pod etcd -o yaml` first |
| 3 | etcd restore double-update | Only changing `--data-dir` but not `hostPath` | Update BOTH in etcd.yaml |
| 4 | NetworkPolicy AND vs OR | Two selectors in same `-from` entry = AND logic | Use separate `-from` entries for OR logic |
| 5 | Service targetPort | Selector correct but traffic fails (app on 9090, svc on 80) | Check with `kubectl exec -- ss -tlnp` |
| 6 | Gateway parentRef | HTTPRoute not accepted, traffic doesn't route | Verify gateway name + namespace in parentRef |
| 7 | Helm release stuck | `helm install` fails because name taken by pending release | `helm delete <name> --no-hooks` first |
| 8 | HPA unknown metrics | metrics-server not installed or --kubelet-insecure-tls missing | Install/patch metrics-server early in exam |
| 9 | subPath vs volume mount | Mounting ConfigMap to file path without subPath creates a directory | Always use `subPath` for single-file mounts |
| 10 | namespaceSelector label | Using `name:` instead of `kubernetes.io/metadata.name:` | Use the auto-assigned metadata.name label |

### kubectl Imperative Command Arsenal

```bash
# Pods
kubectl run mypod --image=nginx --dry-run=client -o yaml
kubectl run mypod --image=nginx --env="KEY=val" --requests='cpu=200m'
kubectl run test --image=busybox --rm -it -- sh

# Deployments
kubectl create deploy myapp --image=nginx --replicas=3 --dry-run=client -o yaml
kubectl set image deploy/myapp nginx=nginx:1.25
kubectl set resources deploy/myapp --limits=cpu=1,memory=512Mi
kubectl rollout undo deploy/myapp --to-revision=3

# Services
kubectl expose deploy myapp --port=80 --target-port=8080 --type=ClusterIP
kubectl expose deploy myapp --port=80 --type=NodePort --node-port=30080

# RBAC
kubectl create role myrole --verb=get,list --resource=pods -n dev
kubectl create clusterrole myrole --verb=get,list --resource=nodes
kubectl create rolebinding bind --role=myrole --serviceaccount=ns:sa -n dev
kubectl auth can-i list pods --as=system:serviceaccount:dev:sa -n dev

# ConfigMaps & Secrets
kubectl create configmap myconfig --from-literal=key=val --from-file=/path/to/file
kubectl create secret generic mysecret --from-literal=key=val
kubectl create secret tls mytls --cert=cert.pem --key=key.pem

# Output
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name
kubectl get svc mysvc -o jsonpath='{.spec.clusterIP}'
kubectl get pods -A --sort-by=.metadata.creationTimestamp

# Scaling
kubectl scale deploy myapp --replicas=5
kubectl autoscale deploy myapp --min=2 --max=10 --cpu-percent=70

# Draining
kubectl cordon node01
kubectl drain node01 --ignore-daemonsets --delete-emptydir-data
kubectl uncordon node01
```

### Allowed Documentation Bookmarks (open before exam)

| Page | URL |
|------|-----|
| kubectl Cheat Sheet | https://kubernetes.io/docs/reference/kubectl/cheatsheet/ |
| Tasks (all how-tos) | https://kubernetes.io/docs/tasks/ |
| RBAC | https://kubernetes.io/docs/reference/access-authn-authz/rbac/ |
| NetworkPolicy | https://kubernetes.io/docs/concepts/services-networking/network-policies/ |
| etcd backup/restore | https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/ |
| kubeadm upgrade | https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/ |
| JSONPath | https://kubernetes.io/docs/reference/kubectl/jsonpath/ |
| Kustomize | https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/ |
| Helm Docs | https://helm.sh/docs/ |
| Gateway API | https://gateway-api.sigs.k8s.io/ |

---

*Total: 150 core scenarios + 50 extended scenarios = 200 total*
*🟢 Standard: ~65 | 🟡 Tricky: ~80 | 🔴 Hard/Trap: ~55*
*Based on CKA curriculum effective February 18, 2025 — Kubernetes v1.34 | Passing: 66%*

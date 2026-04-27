# kubectl

The primary CLI for interacting with the Kubernetes API server. Every command is ultimately a
REST call to the API server. kubectl reads its configuration from `~/.kube/config` (or
`$KUBECONFIG`).

---

### 2.1 — Cluster Info and Context

```bash
kubectl cluster-info                            # API server URL + CoreDNS URL
kubectl cluster-info dump                       # full cluster state dump (large — pipe to file)
kubectl version                                 # client and server versions (check version skew)
kubectl api-resources                           # all resource types: NAME, SHORTNAMES, APIVERSION, NAMESPACED, KIND
kubectl api-resources --namespaced=false        # cluster-scoped resources only
kubectl api-versions                            # all API groups and versions registered
kubectl explain <resource>                      # schema docs with field descriptions
kubectl explain pod.spec.containers.securityContext --recursive  # full nested schema
```

**Context management:**
```bash
kubectl config view                             # full kubeconfig (redacts certificates by default)
kubectl config view --raw                       # include raw cert data
kubectl config get-contexts                     # list all contexts with current marked by *
kubectl config current-context                  # print current context name
kubectl config use-context <name>               # switch to a different context
kubectl config set-context --current --namespace=<ns>   # set default namespace for current context
kubectl config set-cluster <name> --server=https://...
kubectl config set-credentials <name> --token=...
kubectl config delete-context <name>
```

---

### 2.2 — Get / Describe

```bash
kubectl get <resource>                          # list resources in current namespace
kubectl get pods -A                             # all namespaces (-A = --all-namespaces)
kubectl get pods -n <namespace>                 # specific namespace
kubectl get pods -o wide                        # adds Node, IP, Nominated Node, Readiness Gates
kubectl get pods -o yaml                        # full YAML spec + status
kubectl get pods -o json                        # JSON output
kubectl get pods -o jsonpath='{.items[*].metadata.name}'    # extract specific fields
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
kubectl get pods --field-selector=status.phase=Running      # server-side field filter
kubectl get pods --field-selector=spec.nodeName=node1
kubectl get pods -l app=nginx                   # label selector
kubectl get pods -l 'env in (prod, staging)'    # set-based selector
kubectl get pods --sort-by=.metadata.creationTimestamp
kubectl get pods -w                             # watch for changes (streams events)
kubectl get pods --show-labels                  # add LABELS column
kubectl get events --sort-by=.lastTimestamp     # cluster events sorted by time
kubectl get events -n <ns> --field-selector=involvedObject.name=<pod>
```

**Reading `kubectl describe pod` output:**

| Section      | What to look at                                                       |
|--------------|-----------------------------------------------------------------------|
| `Events`     | most useful for debugging: `FailedScheduling`, `BackOff`, `Pulling`   |
| `Conditions` | `PodScheduled`, `Initialized`, `ContainersReady`, `Ready`             |
| `State`      | `Running`, `Waiting` (with reason), `Terminated` (with exit code)    |
| `Mounts`     | which volumes/secrets/configmaps are injected                         |
| `QoS Class`  | `Guaranteed` / `Burstable` / `BestEffort` (affects eviction order)   |
| `Node`       | which node the pod is on; `<none>` if unscheduled                     |

---

### 2.3 — Create / Apply / Edit / Delete

```bash
kubectl create -f <file>                        # create from file (errors if resource exists)
kubectl apply -f <file>                         # create or update (idempotent; preferred)
kubectl apply -f <dir>/                         # apply all files in a directory
kubectl apply -k <dir>/                         # apply a Kustomization
kubectl edit <resource> <name>                  # open live resource in $EDITOR (default vi)
kubectl patch deployment <name> -p '{"spec":{"replicas":3}}'   # strategic merge patch
kubectl patch deployment <name> --type=json \
  -p '[{"op":"replace","path":"/spec/replicas","value":3}]'    # JSON patch
kubectl replace -f <file>                       # replace entire resource (no merge)
kubectl replace --force -f <file>               # delete + recreate (last resort)
kubectl delete -f <file>
kubectl delete pod <name>
kubectl delete pod <name> --grace-period=0 --force    # immediate SIGKILL (for stuck terminating pods)
kubectl delete pod <name> --wait=false          # don't wait for deletion to complete
```

**Imperative create shortcuts (exam essential):**
```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl create service clusterip my-svc --tcp=80:8080
kubectl create configmap my-cm --from-literal=key=value --from-file=config.txt
kubectl create secret generic my-secret --from-literal=password=abc123
kubectl create secret tls my-tls --cert=tls.crt --key=tls.key
kubectl create serviceaccount my-sa
kubectl create namespace prod
kubectl create role pod-reader --verb=get,list --resource=pods
kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
kubectl create rolebinding dev-pod-reader --role=pod-reader --user=jane -n dev
kubectl create clusterrolebinding pod-reader-global --clusterrole=pod-reader --user=jane
```

**`--dry-run=client -o yaml` pattern (exam essential):**
```bash
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml
kubectl run nginx --image=nginx --restart=Never --dry-run=client -o yaml > pod.yaml
# edit the yaml, then:
kubectl apply -f deploy.yaml
```

---

### 2.4 — Logs / Exec / Port-Forward / Copy

```bash
kubectl logs <pod>                              # stdout/stderr of first (or only) container
kubectl logs <pod> -c <container>               # specific container in a multi-container pod
kubectl logs <pod> --previous                   # logs from the previously crashed container
kubectl logs <pod> -f                           # follow (stream, like tail -f)
kubectl logs <pod> --tail=50                    # last 50 lines
kubectl logs <pod> --since=1h                   # logs from last hour
kubectl logs -l app=nginx                       # logs from all pods matching label
kubectl logs -l app=nginx --all-containers=true

kubectl exec <pod> -- <cmd>                     # run command in pod (non-interactive)
kubectl exec -it <pod> -- /bin/bash             # interactive shell
kubectl exec -it <pod> -c <container> -- sh    # specific container

kubectl port-forward pod/<name> 8080:80         # tunnel: localhost:8080 → pod:80
kubectl port-forward svc/<name> 8080:80         # tunnel: localhost:8080 → service:80
kubectl port-forward deploy/<name> 8080:80

kubectl cp <pod>:/path/to/file ./local-file     # copy from pod to local
kubectl cp ./local-file <pod>:/path/in/pod      # copy from local to pod
```

---

### 2.4.1 — Data Transfer Patterns (Exam)

When a question asks you to write output from inside a pod or remote node to a local file:

**Pod → Local**

```bash
# Option 1: kubectl cp (cleanest)
# Note: "tar: removing leading '/' from member names" is a harmless tar warning — copy succeeds
kubectl cp <namespace>/<pod>:/path/in/pod ./local-file
kubectl cp project-swan/api-contact:/tmp/result.json lab/result.json

# Option 2: kubectl exec + cat, redirected locally
kubectl -n <namespace> exec <pod> -- cat /tmp/result.json > ./local-file

# Option 3: run the command non-interactively and redirect directly
kubectl -n <namespace> exec <pod> -- curl -sk https://... > ./local-file
```

**Remote Node → Local**

```bash
# SSH + cat redirect
ssh node01 "cat /etc/kubernetes/manifests/kube-apiserver.yaml" > local-copy.yaml

# SCP
scp node01:/path/to/file ./local-copy

# Pipe any command over SSH
ssh node01 "crictl ps" > output.txt
```

**Workflow pattern:**
1. Do the work inside the pod/node, optionally save to a temp file (`> /tmp/result.json`)
2. Exit back to the exam terminal
3. Pull with `kubectl exec -- cat <file> > local-file` or `ssh node cat <file> > local-file`

---

### 2.5 — Rollout / Scale

```bash
kubectl rollout status deployment/<name>        # watch rollout progress (exit 0 when done)
kubectl rollout status deployment/<name> --timeout=2m
kubectl rollout history deployment/<name>       # show revision history
kubectl rollout history deployment/<name> --revision=2   # detail for a specific revision
kubectl rollout undo deployment/<name>          # roll back to previous revision
kubectl rollout undo deployment/<name> --to-revision=2   # roll back to specific revision
kubectl rollout restart deployment/<name>       # rolling restart (bumps pod-template-hash)
kubectl rollout pause deployment/<name>         # pause a rollout mid-way
kubectl rollout resume deployment/<name>        # resume paused rollout

kubectl scale deployment/<name> --replicas=5
kubectl scale statefulset/<name> --replicas=3
kubectl autoscale deployment/<name> --min=2 --max=10 --cpu-percent=80  # creates HPA
```

**What breaks during rollout:**
- `kubectl rollout status` blocks until complete or times out; exit non-zero on failure
- `CHANGE-CAUSE` in history is empty unless `--record` was used or annotation was set manually
- Paused deployment never progresses — check with `kubectl get deploy` (`PAUSED` column)

---

### 2.6 — Node Management

```bash
kubectl cordon <node>                           # mark node unschedulable (NoSchedule taint added)
kubectl uncordon <node>                         # remove unschedulable mark
kubectl drain <node>                            # evict all evictable pods, then cordon
  --ignore-daemonsets                           # required when DaemonSet pods exist
  --delete-emptydir-data                        # evict pods with emptyDir volumes
  --grace-period=0                              # skip graceful termination
  --force                                       # evict pods not managed by a controller
  --timeout=60s

kubectl taint nodes <node> key=value:NoSchedule
kubectl taint nodes <node> key=value:NoExecute
kubectl taint nodes <node> key=value:PreferNoSchedule
kubectl taint nodes <node> key=value:NoSchedule-    # remove taint (trailing -)

kubectl label nodes <node> disktype=ssd
kubectl label nodes <node> disktype-               # remove label
kubectl annotate nodes <node> description="storage node"

kubectl top nodes                               # CPU and memory usage per node (needs metrics-server)
kubectl top pods -A                             # CPU and memory per pod
kubectl top pods -l app=nginx --containers      # per-container breakdown
```

**Drain sequence:**
1. `cordon` — node marked `SchedulingDisabled`
2. All pods evicted (respects `PodDisruptionBudget` — drain blocks if PDB would be violated)
3. DaemonSet pods are skipped (they are owned by the node)
4. StaticPods are skipped

---

### 2.7 — Auth / RBAC Debugging

```bash
kubectl auth can-i list pods                         # can current user list pods?
kubectl auth can-i list pods --namespace=prod --as=jane    # impersonate a user
kubectl auth can-i '*' '*'                           # does current user have full admin?
kubectl auth whoami                                  # show current user identity

kubectl get clusterrolebindings -o wide | grep <user>
kubectl describe clusterrolebinding <name>
kubectl describe rolebinding <name> -n <ns>
```

---

### 2.8 — Debug

```bash
kubectl debug pod/<name> --image=busybox --it           # ephemeral debug container
kubectl debug pod/<name> --copy-to=debug-pod --it       # copy pod and attach
kubectl debug node/<name> --image=busybox --it          # privileged pod on node
kubectl run tmp --image=busybox --restart=Never -it --rm -- sh   # throwaway debug pod
```

---


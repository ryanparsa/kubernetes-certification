# CKA Exam Practice Context

The following provides the specific grading rubrics and parameters for the Kubernetes Certified Administrator (CKA) simulation. Combine this with the base Terminal Simulation Prompt.

---

## QUICK REFERENCE

If you need a Kubernetes quick reference during the simulation, you can access the reference directory at:
`ref/`

If you need to search each time for a sample or more info, you can search in `ref/` and `cka/`. Use the `search-reference-material` and `search-k8s-docs` skills to find what you need.

---

## SCENARIO DESIGN RULES

- At session start, silently invent ONE broken scenario from the CKA syllabus.
- **ANTI-BIAS & REALISM:**
  - **Avoid Cliches:** Do not use `nginx`, `busybox`, or `redis` for every scenario. Invent realistic enterprise-like app names (e.g., `payment-gateway`, `auth-api`, `metrics-agent`).
  - **Add Noise:** Real clusters are not empty. Include unrelated pods, namespaces, or resources to distract the user. Emulate a failing resource in a different namespace that has nothing to do with the task to test their focus.
  - **SSH-Based Tasks:** The real exam requires SSHing to the correct node for every question. Every task MUST specify which node(s) to SSH to. Aliases and `.vimrc` settings do NOT survive SSH -- simulate this faithfully.
- Rotate through these scenario types across the session (highly realistic exam traps):

### Classic scenarios
  - Static pod syntax error in `/etc/kubernetes/manifests` causing kubelet to fail silently.
  - Missing or incorrect TLS cert paths in `/var/lib/kubelet/config.yaml` or `/etc/kubernetes/pki/`.
  - Ingress controller misconfigurations, missing IngressClass, or NetworkPolicy blocking namespace traffic.
  - Etcd snapshot / restore with specific required certs, keys, and endpoints.
  - Node taint / toleration mismatches preventing scheduling.
  - CoreDNS ConfigMap errors breaking service discovery.
  - Upgrading a kubeadm cluster (control plane or worker node).
  - RBAC permission gap (RoleBinding referencing a non-existent Role or missing a verb).
  - PersistentVolume / StorageClass misconfiguration (capacity mismatch or wrong accessModes).
  - Sidecar container failing due to a typo in a command argument or missing ConfigMap volume.
  - JSONPath / custom-columns / sort-by extraction queries.

### v1.35 new topics
  - **Helm/Kustomize:** `helm repo add` + `helm install` with flag overrides; `kubectl apply -k <dir>` for Kustomize overlays.
  - **Gateway API:** Provisioning a `Gateway` object with listeners + attaching an `HTTPRoute` for backend traffic distribution (replacing legacy Ingress patterns).
  - **Native Sidecar Containers:** Multi-container pods using `initContainers` with `restartPolicy: Always` -- the GA sidecar pattern in v1.35.

### Systemic trap scenarios (high-value exam gotchas)
  - **Static pod vs. systemd trap:** User runs `systemctl restart kube-apiserver` -> `Unit kube-apiserver.service not found`. Control plane components are static pods, not systemd units.
  - **etcdctl location trap:** User runs `etcdctl` from `dev` -> `command not found`. Must SSH to `controlplane`.
  - **etcd restore data-dir trap:** After `etcdctl snapshot restore --data-dir /var/lib/etcd-backup`, user must ALSO update `hostPath` in `/etc/kubernetes/manifests/etcd.yaml` to point to the new data directory.
  - **kubelet binary path corruption:** `ExecStart` in `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` changed to an invalid path (e.g., `/usr/local/bin/kubelet` instead of `/usr/bin/kubelet`) -> kubelet won't start. Diagnosed via `journalctl -u kubelet` or `whereis kubelet`.
  - **daemon-reload omission:** User edits kubelet drop-in file, runs `systemctl restart kubelet`, but forgets `systemctl daemon-reload` first -> old config persists.
  - **CNI missing/corrupt:** Files in `/etc/cni/net.d/` missing or renamed -> node stays `NotReady` despite kubelet running.
  - **SSH environment trap:** User defines `alias k=kubectl` or `export do="--dry-run=client -o yaml"` on `dev`, SSHes to `controlplane`, types `k get pods` -> `command not found`. Or edits YAML with vim using tabs (no `.vimrc`) -> YAML parse error.
  - **crictl debugging:** Use `crictl ps` and `crictl inspect <id>` on a cluster node to debug failing containers below the API layer.
  - **Certificate path mismatch:** API server or etcd cert/key paths in static pod manifest don't match actual files in `/etc/kubernetes/pki/`.

---

## SYLLABUS ROTATION

Track coverage. **Do not repeat a domain until all five are done.** Then cycle again.

```
[ ] Cluster Architecture, Installation & Configuration   25%
[ ] Workloads & Scheduling                               15%
[ ] Services & Networking                                20%
[ ] Storage                                              10%
[ ] Troubleshooting                                      30%
```

Weight toward **Troubleshooting** (30%) and **Cluster Architecture** (25%) -- they dominate the real exam.

---

## DIFFICULTY CURVE

| Challenge # | Difficulty | Characteristics                                                    |
|-------------|------------|--------------------------------------------------------------------|
| 1-2         | Easy       | Single-file fix, obvious error in logs, single node                |
| 3-4         | Medium     | Multi-step fix, cross-node SSH, requires daemon-reload chain       |
| 5+          | Hard       | Cascading failures, etcd restore + manifest update, SSH env traps  |

Increase difficulty after two consecutive quick correct answers.
Hold difficulty steady if the user struggled (3+ wrong attempts on the previous scenario).

---

## SESSION START PREFERENCE

Silently invent the first scenario. Start from `Troubleshooting` or `Cluster Architecture`.
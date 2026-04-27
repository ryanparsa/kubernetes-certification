# Validating Admission Controllers

| Controller | Repo Path | What It Does |
| --- | --- | --- |
| **AlwaysAdmit** | `plugin/pkg/admission/alwaysadmit/` | Admits every request unconditionally. Used for testing; never enable in production |
| **AlwaysDeny** | `plugin/pkg/admission/alwaysdeny/` | Rejects every request unconditionally. Used for testing only |
| **AlwaysPullImages** | `plugin/pkg/admission/alwayspullimages/` | Forces `imagePullPolicy: Always` on every container so nodes always re-authenticate with the registry before running an image |
| **CertificateApproval** | `plugin/pkg/admission/certificates/approval/` | Restricts who can approve `CertificateSigningRequest` objects based on the signer name |
| **CertificateSigning** | `plugin/pkg/admission/certificates/signing/` | Restricts who can sign CSRs for a given signer name |
| **CertificateSubjectRestriction** | `plugin/pkg/admission/certificates/subjectrestriction/` | Rejects CSRs for the `kubernetes.io/kube-apiserver-client` signer if the requested subject has the `system:masters` group (privilege escalation prevention) |
| **ClusterTrustBundleAttest** | `plugin/pkg/admission/certificates/ctbattest/` | Validates that the signer field in a `ClusterTrustBundle` matches the requesting user’s permissions |
| **DenyServiceExternalIPs** | `plugin/pkg/admission/network/deny/` | Rejects Services that set `.spec.externalIPs` (mitigates a known traffic interception attack vector) |
| **EventRateLimit** | `plugin/pkg/admission/eventratelimit/` | Rate-limits Event creation per user, namespace, or source to prevent event floods from overwhelming the API server |
| **ImagePolicyWebhook** | `plugin/pkg/admission/imagepolicy/` | Calls an external webhook to approve or reject a Pod based on its container images (supply chain security gate) |
| **LimitPodHardAntiAffinityTopology** | `plugin/pkg/admission/antiaffinity/` | Rejects Pods that use `requiredDuringSchedulingIgnoredDuringExecution` anti-affinity with a topology key other than `kubernetes.io/hostname` |
| **NamespaceExists** | `plugin/pkg/admission/namespace/exists/` | Rejects requests to create resources in a Namespace that doesn’t exist |
| **NamespaceLifecycle** | `plugin/pkg/admission/namespace/lifecycle/` | Rejects creation of new objects in a `Terminating` namespace; protects `default`, `kube-system`, `kube-public` from deletion |
| **NodeRestriction** | `plugin/pkg/admission/noderestriction/` | Limits what a kubelet (Node identity) can modify — it can only update its own Node object and Pods bound to itself. Prevents node compromise from spreading |
| **OwnerReferencesPermissionEnforcement** | `plugin/pkg/admission/gc/` | Prevents users from setting `ownerReferences` that point to objects they don’t have delete permission on (prevents privilege escalation via GC) |
| **PersistentVolumeClaimResize** | `plugin/pkg/admission/storage/persistentvolumeclaim/resize/` | Validates that a PVC resize request only increases size (not decrease) and that the StorageClass allows expansion |
| **PodNodeSelector** | `plugin/pkg/admission/podnodeselector/` | Forces Pods in a namespace to use specific node selectors defined in a namespace annotation. Prevents Pods from scheduling outside their allowed node pool |
| **PodSecurity** | `plugin/pkg/admission/security/podsecurity/` | Enforces the Pod Security Standards (`privileged`, `baseline`, `restricted`) defined on the namespace via labels |
| **PodTolerationRestriction** | `plugin/pkg/admission/podtolerationrestriction/` | Merges default tolerations onto Pods and rejects Pods with tolerations not allowed by namespace-level policy |
| **ResourceQuota** | `plugin/pkg/admission/resourcequota/` | Rejects requests that would exceed a `ResourceQuota` in the namespace. Works in tandem with the ResourceQuota controller in kube-controller-manager |
| **ValidatingAdmissionPolicy** | `plugin/pkg/admission/validatingadmissionpolicy/` | Evaluates CEL (Common Expression Language) rules defined in `ValidatingAdmissionPolicy` objects directly in-process — no webhook roundtrip needed |
| **ValidatingAdmissionWebhook** | `plugin/pkg/admission/webhook/validating/` | Calls external webhooks registered via `ValidatingWebhookConfiguration`. The webhook returns allow/deny with an optional reason |

---

### Key Difference: Webhooks vs In-Tree Controllers

```
In-tree admission controller          External admission webhook
(compiled into kube-apiserver)        (your own HTTP server)
        │                                       │
plugin/pkg/admission/xxx/             registered via:
        │                               MutatingWebhookConfiguration
runs in apiserver process               ValidatingWebhookConfiguration
no network hop                                  │
                                       apiserver calls your endpoint
                                       over HTTPS (network hop)
```

---

# LAYER 2 — kube-controller-manager

A **single binary** running control loops that watch the API server and reconcile cluster state. Runs as a static Pod on control plane nodes.

> Source root: `pkg/controller/` in kubernetes/kubernetes
Binary entry: `cmd/kube-controller-manager/main.go`
Bootstrap & registration: `cmd/kube-controller-manager/app/controllermanager.go` — `NewControllerManagerCommand()`, `Run()`
Controller registration by group: `app/apps.go` (Deployment, StatefulSet, DaemonSet, ReplicaSet), `app/batch.go` (Job, CronJob), `app/core.go` (Namespace, GC, Node, Endpoints…)
> 

---


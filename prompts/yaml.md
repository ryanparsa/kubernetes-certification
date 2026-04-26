Practice type: YAML from scratch. Combine with base.md and cka.md or ckad.md.

FORMAT OVERRIDE
- Each challenge requires a complete, valid manifest. No imperative shortcuts.
- Must include: apiVersion, kind, metadata, spec — nothing omitted or placeholder.
- Paste your YAML in a code block. It will be annotated inline with every error.

ERROR ANNOTATION FORMAT
  field: wrong-value    # ❌ should be: correct-value
  field: correct-value  # ✅
  # ❌ missing required field: fieldName
  field: unnecessary    # ⚡ this is a default — omit it

GRADING ADDITIONS
- ✅ only if the manifest would apply cleanly and achieve the task with no runtime failures
- ❌ annotate every wrong or missing field inline, then show the correct full manifest
- Count errors by severity: "2 errors — 1 would prevent apply, 1 would cause runtime failure"
- ⚡ flag unnecessary fields that add noise (status block, explicit defaults)

FOCUS AREAS (rotate — drill the fields people get wrong, not trivial ones):
- volumeMounts vs volumes: name must match exactly, mountPath vs path
- env vs envFrom: valueFrom.secretKeyRef vs valueFrom.configMapKeyRef structure
- container ports vs Service ports vs targetPort (int vs string)
- probe structure: exec.command is an array, httpGet needs path + port
- resource format: CPU in millicores (100m), memory in binary units (128Mi)
- affinity vs nodeSelector: matchExpressions operator, In/NotIn/Exists
- tolerations: key, operator (Equal/Exists), effect, value (omit for Exists)
- RBAC rules: verbs list, resources list, apiGroups (core API group is "")
- NetworkPolicy: podSelector {} means all pods, ports[].protocol must be uppercase
- PVC: accessModes is an array, resources.requests.storage format, storageClassName: ""
- Job: restartPolicy must be Never or OnFailure (not Always)
- StatefulSet: serviceName is required, volumeClaimTemplates structure

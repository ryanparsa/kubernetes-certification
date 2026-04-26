Practice type: imperative speed drills. Combine with base.md and cka.md or ckad.md.

FORMAT OVERRIDE
- Each challenge must be solved with imperative kubectl commands only. No writing YAML from scratch.
- Allowed: kubectl run, create, expose, set, label, annotate, patch, scale, rollout
- If YAML editing is unavoidable: generate with --dry-run=client -o yaml > file.yaml, edit minimally, apply.
- Show the full command sequence, not just the end state.

SPEED RULES
- Never open a text editor if an imperative flag can do it.
- Aliases assumed: k=kubectl, do="--dry-run=client -o yaml"
- Use -n <namespace> not --namespace for speed.

GRADING ADDITIONS
- ⚡ if you wrote YAML manually when an imperative command existed — show the command
- ⚡ if you used more commands than necessary — show the shorter path
- Call out any flag commonly forgotten under pressure (e.g. --restart=Never for one-shot pods, --record is deprecated)
- Note if the solution would fail silently (e.g. wrong port type, missing --tcp for expose)

CHALLENGE MIX (rotate):
- Create a Pod with specific image, labels, env vars, resource limits
- Create a Deployment and immediately scale it or update its image
- Expose a Deployment as ClusterIP or NodePort Service
- Create a ConfigMap or Secret from literals and mount it
- Create a ServiceAccount and bind a Role to it imperatively
- Add or overwrite a label or annotation on a running resource
- Generate a pod spec and patch one field (e.g. add a toleration)
- Run a one-shot pod with --restart=Never and a specific command
- Create a CronJob or Job imperatively
- Switch context and perform an action in a different namespace

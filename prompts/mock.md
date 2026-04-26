Practice type: mock exam. Combine with base.md and cka.md or ckad.md.

FORMAT OVERRIDE
- Present all tasks at once, numbered. Do not drip one at a time.
- Each task specifies: kubectl context, namespace, point value, and the task.
- I submit all answers when done. Tell me my elapsed time when submitting.
- Grade each task separately, then give a total score out of 100.

EXAM RULES
- Time limit: 2 hours (CKA) or 2 hours (CKAD). Honor system.
- Each task has a point value shown in brackets, e.g. [7 pts].
- Multiple cluster contexts in play: k8s-prod, k8s-dev, k8s-cluster1, k8s-cluster2.
- Always begin each task answer with: kubectl config use-context <context>
- Partial credit for partial completion — state what you completed.

TASK DISTRIBUTION (15–17 tasks, ~100 pts total):
- 3–4 easy [5 pts]: create a pod, scale a deployment, expose a service, create a ConfigMap
- 5–6 medium [7 pts]: RBAC, NetworkPolicy, PV/PVC, multi-container pod, rolling update, Helm install
- 4–5 hard [10 pts]: troubleshoot broken component, etcd backup/restore, cert renewal, cluster upgrade step
- 1–2 expert [12 pts]: combine 2–3 concepts, e.g. RBAC + NetworkPolicy + correct probe, or broken node + reschedule workload

GRADING FORMAT
- Per task: score earned / max, one line on what was wrong if not full marks
- For incorrect tasks: show the minimal correct solution only, no explanation beyond one line
- Flag near-misses: right approach, single wrong flag or field — these are the most important to review
- Final summary:
  - Total: X / 100
  - Weakest area: <topic>
  - One targeted drill recommendation based on the mistakes

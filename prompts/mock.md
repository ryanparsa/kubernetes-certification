> **Requires**: [base.md](./base.md) -- paste that first.

Practice type: full mock exam.

## Format

Give me all tasks at once, numbered 1-N (realistic exam count). Each task:
- Is on a specific context/cluster (simulate by naming it, e.g. `kubectl config use-context k8s-cluster-1`)
- Has a point value shown (tasks sum to 100)
- Uses real exam phrasing ("configure", "create", "expose", "ensure")

I work through all tasks, then submit. Grade each one:
- [ok] full credit
- ? partial credit -- show what's missing
- [x] incorrect -- show the correct solution

Then give:
- Total score / 100
- Which domains I was weakest in
- Top 3 things to review before the exam

## Rules

- Mix difficulty: ~30% easy, ~50% medium, ~20% hard/expert
- Cover all domains proportionally to their weights (defined by the exam scope prompt)
- Use realistic cluster/namespace/resource names
- Do NOT give hints or check-ins mid-exam unless I ask

Use the coverage and domain weights defined by the exam scope prompt. Start the mock exam.

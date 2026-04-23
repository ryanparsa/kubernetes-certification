# Conventions Memory

Never rewrite or paraphrase `readme.md` files — copy question, answer steps, and terminal output verbatim from `cka/ref/`.
`fix.sh` must be idempotent: use `kubectl apply`, never `kubectl create`.
`kubeconfig.yaml` and `course/` are git-ignored and must never be committed.
`check.py` class name follows `Test<DescriptiveLabName>` matching the question title.
Use `jsonpath` in `check.py` — avoid parsing plain text output.
Checklist score starts at `0/<N>` and is updated to `<N>/<N>` once all checks pass.
Document all valid solution approaches in `readme.md`; pick the simpler one for `fix.sh`.

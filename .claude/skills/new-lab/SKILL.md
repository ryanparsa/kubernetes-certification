---
name: new-lab
description: Create a complete CKA/CKAD/CKS lab scenario from any input—text description, killer.sh URL, pasted question text, or screenshot. Generates readme.md, all asset scripts, _check.py, and the CI workflow.
disable-model-invocation: true
argument-hint: [cka|ckad|cks] [description, URL, or paste content]
allowed-tools: Bash Read Write WebFetch
---

# new-lab — Generate a Complete Lab Scenario

Convert any input into a fully runnable lab that matches project conventions.

## Input forms this skill handles

- `/new-lab cka create a NetworkPolicy that blocks all ingress to pod X`
- `/new-lab ckad https://killer.sh/...` (fetch the page and extract the question)
- `/new-lab` with a screenshot or pasted question already in the conversation
- Text that begins with a question number and title (killer.sh format)

## Step 1 — Parse the input (`$ARGUMENTS`)

1. **Exam type**: extract `cka`, `ckad`, or `cks` from the first word of `$ARGUMENTS`. If absent, infer from topic (etcd/kubeadm/certificates → CKA; probes/jobs/helm → CKAD; PSP/OPA/falco → CKS). Ask the user if genuinely ambiguous.
2. **URL**: if any argument starts with `http`, fetch it with WebFetch. Extract the question number, title, task description, and any provided answer steps.
3. **Screenshot / pasted text**: if `$ARGUMENTS` is empty or minimal, treat any recent conversation context (screenshot description, pasted text) as the source material.
4. **Question title**: derive a short `<Title>` (3–5 words, title-case, no articles) from the task, e.g. `ETCD Backup Restore`, `RBAC Service Account`.

## Step 2 — Find the next lab number

```bash
ls <exam>/ | grep -E '^[0-9]+$' | sort -n | tail -1
```

Increment by 1 to get `<N>`. Verify `<exam>/<N>/` does not already exist.

## Step 3 — Design the lab content

Before writing any files, reason through:

- **Kind topology**: how many nodes does the task require?
  - Single control-plane only: simple read/inspect tasks (ETCD info, cert check)
  - Control-plane + 1 worker: scheduling, drain, cordon, DaemonSets
  - Control-plane + 2 workers: HA scenarios, PodDisruptionBudgets
- **Pre-seeded state** (`setup.sh`): what resources must exist before the user starts? Create namespaces, broken workloads, RBAC gaps, missing secrets, etc.
- **Solution** (`fix.sh`): what is the minimal correct solution? Use `kubectl apply`, never `kubectl create`. Must be idempotent.
- **Verification** (`_check.py`): one `test_` method per checklist item. Use `jsonpath` for field checks; avoid parsing text output.
- **Checklist**: 2–6 bullet items that map directly to `test_` methods.

## Step 4 — Write all files

Create these files (see [templates.md](templates.md) for the exact boilerplate):

| File | Purpose |
|------|---------|
| `<exam>/<N>/readme.md` | Question + full answer walkthrough + checklist |
| `<exam>/<N>/assets/kind-config.yaml` | Kind cluster topology |
| `<exam>/<N>/assets/setup.sh` | Create cluster + pre-seed state |
| `<exam>/<N>/assets/fix.sh` | Idempotent complete solution |
| `<exam>/<N>/assets/check.sh` | Delegates to _check.py |
| `<exam>/<N>/assets/_check.py` | unittest assertions, one per checklist item |
| `<exam>/<N>/assets/cleanup.sh` | Delete cluster + course/ |
| `.github/workflows/<exam>-lab-<N>.yml` | CI workflow |

Create directories first:
```bash
mkdir -p <exam>/<N>/assets
```

## Step 5 — readme.md format

```markdown
# Question <N> | <Title>

> **Solve this question on:** the "<exam>-lab-<N>" kind cluster

<Task description — written as an exam scenario, imperative mood, mentions Namespace/resource names explicitly.>

## Answer

<Step-by-step walkthrough with bash commands and YAML snippets.>
<Show terminal output where it helps understanding.>
<If multiple valid approaches exist, document all; pick the simpler one for fix.sh.>

## Killer.sh Checklist (Score: 0/<M>)

- [ ] <Requirement 1>
- [ ] <Requirement 2>
```

Rules:
- If the source is killer.sh content, copy the question and answer **verbatim** — do not paraphrase.
- Use fenced code blocks with language tags (`bash`, `yaml`).
- YAML snippets for files in `course/` must show the path as a comment on the first line: `# <exam>/<N>/course/<file>.yaml`.

## Step 6 — _check.py structure

```python
#!/usr/bin/env python3
import os, subprocess, unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    r = subprocess.run(["kubectl", "--kubeconfig", KUBECONFIG, *args],
                       capture_output=True, text=True)
    return r.stdout.strip()

class Test<TitleNospaces>(unittest.TestCase):
    def test_<requirement_1>(self):
        val = kubectl("get", "<resource>", "<name>", "-n", "<ns>",
                      "-o", "jsonpath={.<field>}")
        self.assertEqual(val, "<expected>")

    def test_<requirement_2>(self):
        ...

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

Rules:
- Class name: `Test<TitleNospaces>` matching the question title.
- One method per checklist item — names must be descriptive, not `test_1`.
- Use `jsonpath` for Kubernetes object fields.
- For file-content checks (like etcd-info.txt), read the file directly.
- For node-level checks, use `docker exec <cluster>-control-plane <cmd>`.

## Step 7 — Validate

After writing all files, run:
```bash
bash -n <exam>/<N>/assets/setup.sh
bash -n <exam>/<N>/assets/fix.sh
bash -n <exam>/<N>/assets/cleanup.sh
python3 -m py_compile <exam>/<N>/assets/_check.py
```

Report any syntax errors and fix them before declaring the lab ready.

## Step 8 — Summary

Print a brief summary:
- Lab path and number
- Kind topology (nodes)
- Checklist items generated
- Command to test it: `bash <exam>/<N>/assets/setup.sh && bash <exam>/<N>/assets/fix.sh && bash <exam>/<N>/assets/check.sh`

## Additional resources

- For file templates and boilerplate, see [templates.md](templates.md)
- CONTRIBUTING.md has the authoritative conventions — always prefer it over inference
- Canonical reference lab: `cka/29/`

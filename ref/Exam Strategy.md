# Exam Strategy

> This file covers both exam formats. See the section that matches your target cert.
> - **Lab-based (CKA / CKAD / CKS):** hands-on terminal tasks, scored by automated checkers
> - **MCQ (KCNA / KCSA):** 60 multiple-choice questions, 4 options, 90 minutes

---

# Lab-Based Exams (CKA / CKAD / CKS)

## Terminal Setup (First 2 Minutes)

Do this before touching any question. These two commands save minutes over the course of the exam:

```bash
# Enable kubectl autocompletion
source <(kubectl completion bash)

# Short alias
alias k=kubectl
complete -F __start_kubectl k
```

Keep a scratch file open in a second terminal tab for manifests:

```bash
vim ~/scratch.yaml
```

## Context Switching — Do This for Every Question

Each question runs on a specific cluster. The exam tells you which one. **Always switch context first** — forgetting this is an instant zero for the question.

```bash
kubectl config use-context <context-name>
```

Verify you are on the right cluster before proceeding:

```bash
kubectl config current-context
```

If the question also specifies a namespace, either pass `-n <ns>` on every command or set a default:

```bash
kubectl config set-context --current --namespace=<ns>
```

## The Workflow

**Never solve questions in order.** Q1–Q5 can be the hardest ones and burn your energy and time before you even reach the easy points.

### Step 1 — Explore all questions first
- Skim every question quickly, don't solve anything yet
- For each one, write a one-liner in your notepad with a status and point value

### Step 2 — Build your attack order from the notepad
- Pick your next task by scanning the notepad, not the question list
- Start with easy high-value questions, leave hard/low-value for last

### Step 3 — Execute and update the notepad as you go

## Question Tracker (Notepad)

Open a text editor at the very start. One line per question:

```
Q1   7%  hard – come back
Q2   4%  ignore – too slow
Q3   8%  easy – RBAC
Q4   6%  done
Q5   5%  syntax error – revisit
Q6   7%  in progress
```

Statuses: `easy`, `done`, `in progress`, `hard – come back`, `ignore`, `syntax error – revisit`

## Point-Value Rules

| Weight  | Rule |
|---------|------|
| ≤4%     | Skip immediately if slow — come back only if time allows |
| ≥7%     | Worth fighting for even if slow |
| Storage | Never prioritize if you're behind — only 10% of the exam |

## Partial Credit — Always Do What You Can

Questions are **not all-or-nothing**. The checker runs multiple small checks and awards points for each one independently.

Example: "Create a Pod exposed via a NodePort Service"
- ✅ Pod exists with correct name → +1
- ✅ Pod has correct image → +1
- ❌ NodePort Service missing → 0 for that part

**Rule: even on hard questions, always do the parts you know.** Never leave a question completely blank just because you can't solve all of it. A half-done answer is always better than nothing.

## Verify Before Moving On

Before marking a question done and moving to the next:

```bash
# confirm the resource exists with the right spec
kubectl get <resource> <name> -n <ns> -o yaml | grep <key-field>

# confirm pods are running (for workload questions)
kubectl get pods -n <ns>

# confirm RBAC works (for RBAC questions)
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa> -n <ns>
```

A 30-second sanity check here prevents losing points you already earned.

## Time Boxing

- Mental limit of **~8 minutes per question**
- Not close to done? Update notepad, move on

---

# MCQ Exams (KCNA / KCSA)

## The Core Loop

Repeat this cycle until you're consistently passing mock tests:

```
Checklist → Test → Checklist → Test → ...
```

1. **Week 1 — Checklist pass:** Work through the exam checklist. Tick off what you know confidently. Study what you don't.
2. **After ~1 week — Mock test:** Take a full practice test (see below). Note which domains you failed.
3. **Return to checklist:** Focus study time on the weak domains identified by the test.
4. **Repeat** until you score 85%+ consistently on mocks before booking the real exam.

## How to Simulate MCQ Tests

| Method | How |
|--------|-----|
| LLM-based | Paste `prompts/mcq.md` + `prompts/kcna.md` (or `kcsa.md`) into a new chat session |
| Udemy | Buy a dedicated KCNA/KCSA practice exam course |
| killer.sh | killer.sh offers MCQ-style simulators for associate-level certs |

## Domain-Weighted Study Priority

Don't study all domains equally — weight your time by exam percentage.

**KCNA:** Kubernetes Fundamentals (46%) → Container Orchestration (22%) → Cloud Native Architecture (16%) → Application Delivery (8%)

**KCSA:** Cluster Component Security + Security Fundamentals (44% combined) → Threat Model + Platform Security (32% combined) → Cloud Native Overview (14%) → Compliance (10%)

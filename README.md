# Kubernetes Certification

Open-source practice labs and study materials for Kubernetes certification exams.

## Exams Covered

| Exam | Full Name | Directory |
|------|-----------|-----------|
| [CKA](cka/) | Certified Kubernetes Administrator | `cka/` — 37 hands-on practice labs + exam definition |
| [CKAD](ckad/) | Certified Kubernetes Application Developer | `ckad/` — exam definition |
| [CKS](cks/) | Certified Kubernetes Security Specialist | `cks/` — exam definition |
| [KCNA](kcna/) | Kubernetes and Cloud Native Associate | `kcna/` — study materials, 200 practice questions, checklists |
| [KCSA](kcsa/) | Kubernetes and Cloud Native Security Associate | `kcsa/` — exam definition |

Each exam directory contains a `README.md` with the official exam overview, domain weights, and key topics. The [`prompts/`](prompts/) directory provides AI trainer prompts that reference these definitions.

## Repository Layout

```
.
├── cka/                  # CKA — practice labs + exam definition
│   ├── <N>/              # Each lab:
│   │   ├── README.md     #   Question only
│   │   ├── answer.md     #   Reference solution + killer.sh checklist
│   │   ├── assets/       #   setup / cleanup / fix / check scripts + seed files
│   │   └── lab/          #   Created by setup.sh (git-ignored): kubeconfig + working files
│   ├── ref/              # Verbatim killer.sh simulator source questions
│   └── README.md         # Exam overview, domain weights, topics, lab index
├── ckad/
│   └── README.md         # Exam overview, domain weights, topics
├── cks/
│   └── README.md         # Exam overview, domain weights, topics
├── kcna/                 # KCNA study material + exam definition
│   ├── kcna-assessment-bank.md   # 200 practice Q&A
│   ├── kcna-exam-checklist.md    # Domain-by-domain prep checklist
│   ├── resources.md              # Curated learning resources
│   └── README.md                 # Exam overview, domain weights, topics
├── kcsa/
│   └── README.md         # Exam overview, domain weights, topics
├── prompts/              # AI trainer prompts (reference exam dirs for scope)
│   ├── base.md           # Shared session rules
│   ├── cka.md / ckad.md / cks.md / kcsa.md   # Exam scope (thin wrappers)
│   └── ...               # Practice types: speed, yaml, mock, troubleshoot, docs
├── ref/                  # Kubernetes quick-reference sheets
│   ├── Kubernetes Commands Reference.md
│   ├── RBAC Reference.md
│   ├── Networking Reference.md
│   └── ...               # Storage, TLS, Helm, Scheduling, and more
└── CONTRIBUTING.md       # Lab structure, file templates, CI setup, and conventions
```

## CKA Labs

| Simulator | Labs |
|-----------|------|
| Simulator A | `cka/1` – `cka/17` |
| Simulator B | `cka/18` – `cka/34` |

See [`cka/README.md`](cka/README.md) for the full lab index with status.

### Running a Lab Locally

Most labs run on a local [kind](https://kind.sigs.k8s.io/) cluster. Labs that require real OS-level node operations (kubeadm join, kubeadm upgrade) use [Lima](https://lima-vm.io/) VMs instead. Each lab's `setup.sh` handles the difference — the workflow is the same either way.

**Prerequisites — kind-based labs:** `docker`, `kind`, `kubectl`, `python3`

**Prerequisites — Lima-based labs:** `limactl`, `kubectl`, `python3`

```bash
# 1. Enter the lab directory
cd cka/<N>

# 2. Start the environment
bash assets/setup.sh
export KUBECONFIG=lab/kubeconfig.yaml

# 3. Read the scenario
cat README.md

# 4. Solve (save manifests under lab/)

# 5. Verify your solution
bash assets/check.sh

# 6. Tear down
bash assets/cleanup.sh
```

If you get stuck, `fix.sh` applies the reference solution:

```bash
bash assets/fix.sh
```

## AI Practice Prompts

The [`prompts/`](prompts/) directory contains modular AI trainer prompts. Each exam scope prompt links back to the corresponding exam directory for its topic definitions.

See [`prompts/README.md`](prompts/README.md) for usage instructions.

## Reference Sheets

The [`ref/`](ref/) directory contains concise command and concept references useful during exam preparation:

- **Kubernetes Commands Reference** — essential `kubectl` commands
- **RBAC Reference** — roles, bindings, and service accounts
- **Networking Reference** — services, ingress, and network policies
- **Storage Reference** — PVs, PVCs, and storage classes
- **TLS** — certificate management and kubeadm PKI
- **Helm Reference** — chart lifecycle commands
- **Scheduling Reference** — taints, tolerations, affinity
- **Troubleshooting Reference** — common failure patterns
- And more…

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full lab structure, file templates, CI setup, and conventions.

Contributions are welcome — feel free to open an issue or pull request.

## License

[GNU General Public License v3.0](LICENSE)

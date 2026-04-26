# Kubernetes Certification

Open-source practice labs and study materials for Kubernetes certification exams.

## Exams Covered

| Exam | Full Name | Contents |
|------|-----------|----------|
| [CKA](cka/) | Certified Kubernetes Administrator | 37 hands-on practice labs |
| [KCNA](kcna/) | Kubernetes and Cloud Native Associate | Study materials, 200 practice questions, and checklists |

## Repository Layout

```
.
├── cka/                  # CKA practice labs (numbered sequentially)
│   ├── <N>/              # Each lab: readme.md + assets/ (up/down/fix/check scripts)
│   ├── ref/              # Verbatim killer.sh simulator source questions
│   └── README.md         # Lab index and status table
├── kcna/                 # KCNA study material
│   ├── kcna-assessment-bank.md   # 200 practice Q&A
│   ├── kcna-exam-checklist.md    # Domain-by-domain prep checklist
│   └── resources.md              # Curated learning resources
├── ref/                  # Kubernetes quick-reference sheets
│   ├── Kubernetes Commands Reference.md
│   ├── RBAC Reference.md
│   ├── Networking Reference.md
│   └── ...               # Storage, TLS, Helm, Scheduling, and more
└── CONTRIBUTING.md       # Lab structure, file templates, and conventions
```

## CKA Labs


| Simulator | Labs |
|-----------|------|
| Simulator A | `cka/1` – `cka/17` |
| Simulator B | `cka/18` – `cka/34` |

See [`cka/README.md`](cka/README.md) for the full lab index with status.

### Running a Lab Locally

**Prerequisites:** `docker`, `kind`, `kubectl`, `python3`

```bash
# 1. Start the cluster
bash cka/<N>/assets/up.sh
export KUBECONFIG=cka/<N>/assets/kubeconfig.yaml

# 2. Read the scenario
cat cka/<N>/readme.md

# 3. Solve (save manifests under cka/<N>/course/)

# 4. Verify your solution
bash cka/<N>/assets/check.sh

# 5. Tear down
bash cka/<N>/assets/down.sh
```

If you get stuck, `fix.sh` applies the reference solution:

```bash
bash cka/<N>/assets/fix.sh
```

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

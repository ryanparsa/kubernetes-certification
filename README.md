# Kubernetes Certification

Open-source practice labs and study materials for Kubernetes certification exams.

## Exams Covered

| Exam | Full Name | Directory |
|------|-----------|-----------|
| [KCNA](kcna/) | Kubernetes and Cloud Native Associate | `kcna/` - study materials, 200 practice questions, checklists |
| [KCSA](kcsa/) | Kubernetes and Cloud Native Security Associate | `kcsa/` - exam definition |
| [CKAD](ckad/) | Certified Kubernetes Application Developer | `ckad/` - exam definition |
| [CKA](cka/) | Certified Kubernetes Administrator | `cka/` - 37 hands-on practice labs + exam definition |
| [CKS](cks/) | Certified Kubernetes Security Specialist | `cks/` - exam definition |

Each exam directory contains a `README.md` with the official exam overview, domain weights, and key topics. The [`prompts/`](prompts/) directory provides AI trainer prompts that reference these definitions.

## Repository Layout

```
.
├── kcna/                 # KCNA study material + exam definition
│   ├── kcna-assessment-bank.md   # 200 practice Q&A
│   ├── kcna-exam-checklist.md    # Domain-by-domain prep checklist
│   ├── resources.md              # Curated learning resources
│   └── README.md                 # Exam overview, domain weights, topics
├── kcsa/
│   └── README.md         # Exam overview, domain weights, topics
├── ckad/
│   └── README.md         # Exam overview, domain weights, topics
├── cka/                  # CKA - practice labs + exam definition
│   ├── <N>/              # Each lab:
│   │   ├── README.md     #   Question only
│   │   ├── answer.md     #   Reference solution + killer.sh checklist
│   │   ├── assets/       #   setup / cleanup / fix / check scripts + seed files
│   │   └── lab/          #   Created by setup.sh (git-ignored): kubeconfig + working files
│   ├── ref/              # Verbatim killer.sh simulator source questions
│   └── README.md         # Exam overview, domain weights, topics, lab index
├── cks/
│   └── README.md         # Exam overview, domain weights, topics
├── prompts/              # AI trainer prompts (reference exam dirs for scope)
│   ├── base.md           # Shared session rules
│   ├── kcna.md / kcsa.md / ckad.md / cka.md / cks.md   # Exam scope (thin wrappers)
│   └── ...               # Practice types: speed, yaml, mock, troubleshoot, docs
├── ref/                  # Kubernetes quick-reference sheets
│   ├── Kubernetes Commands Reference.md
│   ├── RBAC Reference.md
│   ├── Networking Reference.md
│   └── ...               # Storage, TLS, Helm, Scheduling, and more
└── CONTRIBUTING.md       # Lab structure, file templates, CI setup, and conventions
```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full lab structure, file templates, CI setup, and conventions.

Contributions are welcome - feel free to open an issue or pull request.

## License

[GNU General Public License v3.0](LICENSE)

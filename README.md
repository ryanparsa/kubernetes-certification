Kubernetes Certification Training

This repository is a comprehensive educational resource for Kubernetes certifications, including **CKA** (Certified Kubernetes Administrator), **KCNA** (Kubernetes and Cloud Native Associate), and **KCSA** (Kubernetes and Cloud Native Security Associate).

## Related Projects

- [kubernetes-project-baseline](https://github.com/ryanparsa/kubernetes-project-baseline) - Production-ready Kubernetes namespace/service baseline
- [klist](https://github.com/ryanparsa/klist) - Interactive Kubernetes operational checklist to verify cluster readiness


## 📂 Project Structure

- **`cka/`**: Hands-on practice scenarios for the CKA exam.
    - **`scenarios/`**: 28 independent tasks (1-28) + a template.
        - `up.sh`: Sets up a local `kind` cluster for the task.
        - `down.sh`: Tears down the cluster.
        - `task.md`: Defines the objective and constraints.
        - `test.sh`: Verifies the solution.
        - `hint.md`: Provides guidance if stuck.
        - `assets/`: Contains `kubeconfig` and manifests used by the scenario.
    - `CKA_200_Scenarios_Detailed.md`: List of scenario descriptions.
- **`kcna/`**: Study materials for the KCNA associate-level exam.
    - `kcna-assessment-bank.md`: 200 multiple-choice questions with explanations.
    - `kcna-exam-checklist.md`: Domain-by-domain preparation guide.
- **`kcsa/`**: Study materials for the KCSA security-focused associate exam.
    - `kcsa_questions.json`: Structured question bank for security topics.
    - `kcsa_quiz.html`: A web-based quiz interface for practice.

## 🛠️ Key Technologies & Tools

- **Kubernetes**: The core subject matter.
- **kind (Kubernetes in Docker)**: Used to spin up lightweight clusters for CKA labs.
- **Docker**: Required as the runtime for `kind`.
- **kubectl**: Primary CLI for interacting with clusters.
- **Helm & Kustomize**: Modern application delivery tools covered in CKA scenarios.
- **Shell Scripting**: Used for lab automation (`up.sh`, `down.sh`, `test.sh`).

## 🚀 Common Workflows

### Running a CKA Practice Task
1. Navigate to the task directory: `cd cka/scenarios/<number>`
2. Provision the environment: `./up.sh`
3. Set the context: `export KUBECONFIG=$PWD/assets/kubeconfig` (or as specified in `task.md`)
4. Solve the task described in `task.md`.
5. Verify your solution: `./test.sh`
6. Cleanup: `./down.sh`

### Reviewing Associate Questions
- **KCNA**: Read through `kcna/kcna-assessment-bank.md`.
- **KCSA**: Review `kcsa/kcsa_questions.json` or open `kcsa/kcsa_quiz.html` in a browser.

## 📝 Development Conventions

- **Surgical Changes**: When updating scenarios, maintain the structure of `up.sh`, `task.md`, and `test.sh`.
- **Context Awareness**: Always specify the `KUBECONFIG` path when performing operations on tasks, as each scenario uses an isolated cluster.
- **Testing**: Every scenario should have a corresponding `test.sh` that provides deterministic pass/fail output.

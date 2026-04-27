# KCSA Resources

## Courses

- [Kubernetes Security (KubeSec) YouTube Playlist](https://www.youtube.com/playlist?list=PLlhKrJNDhoUIc0GNkdSQbnjl4JU7SubE9) — Free video series covering KCSA domains

## Practice Tests

- [Udemy — Kubernetes and Cloud Native Security Associate (KCSA) Practice Exams](https://www.udemy.com/course/kubernetes-and-cloud-native-security-associate-kcsa/) — Domain-mapped MCQ practice

## Hands-On Labs

- [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat) — Intentionally vulnerable Kubernetes cluster for practicing attack and defense scenarios; directly relevant to Threat Model and Platform Security domains

## Official References

- [KCSA Curriculum (CNCF)](https://github.com/cncf/curriculum) — Official exam blueprint and domain breakdown
- [Kubernetes Documentation — Security](https://kubernetes.io/docs/concepts/security/) — Pod Security Standards, RBAC, Secrets, NetworkPolicy, Audit Logging
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes) — The compliance baseline used in Domain 6

## Threat Modeling

- [MITRE ATT&CK for Containers](https://attack.mitre.org/matrices/enterprise/containers/) — Full tactic/technique matrix referenced in Domain 4
- [Microsoft Threat Matrix for Kubernetes](https://microsoft.github.io/Threat-Matrix-for-Kubernetes/) — Kubernetes-specific attack techniques with mitigations

## Key Tool Docs

- [Falco](https://falco.org/docs/) — Runtime security; rules syntax, deployment, Falcosidekick outputs
- [Trivy](https://aquasecurity.github.io/trivy/) — Image and config scanning; CLI flags for CI/CD gates
- [Cosign / Sigstore](https://docs.sigstore.dev/) — Image signing and keyless verification
- [kube-bench](https://github.com/aquasecurity/kube-bench) — CIS Benchmark scanner; understand PASS/FAIL/WARN output
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/) — ConstraintTemplate and Constraint CRDs
- [Kyverno](https://kyverno.io/docs/) — YAML-native policy engine; ClusterPolicy examples
- [cert-manager](https://cert-manager.io/docs/) — Kubernetes-native TLS certificate management

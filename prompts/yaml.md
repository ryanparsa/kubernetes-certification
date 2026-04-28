> **Requires**: [base.md](./base.md) -- paste that first.

Practice type: Kubernetes YAML. Write correct manifests fast and spot bugs.

## Modes (rotate)

- **Write from scratch**: I get a scenario, I write the full manifest.
- **Multiple choice**: show 3-4 YAML options, I pick the correct one(s) and explain why the others are wrong. All options must be the same approximate length. Rotate which letter (A/B/C/D) is correct -- never default to A. Use varied distractor types (wrong field name, wrong indentation level, wrong value type, missing required field -- not the same mistake every time).
- **Debug**: show a manifest with 2-5 intentional mistakes (indentation, apiVersion/kind, selectors, probes, volumes, resources, RBAC subjects, etc.). I list the bugs and submit a fix.

## Grading

- [ok] correct
- [x] wrong or incomplete -- annotate inline which field is wrong and why
- [!] cleaner/safer way exists -- show it
- Show the complete correct manifest. Max 3 lines of explanation.
- Then immediately give the next challenge.

Use the coverage defined by the exam scope prompt. Start with challenge #1.

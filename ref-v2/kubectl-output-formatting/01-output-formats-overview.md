# kubectl Output Formatting Reference

[← Back to index](../README.md)

---

## 1. Output Formats Overview

| Flag | What you get |
|---|---|
| `-o wide` | Extra columns (node, IP, nominated node, etc.) |
| `-o yaml` | Full resource as YAML |
| `-o json` | Full resource as JSON |
| `-o name` | Just `kind/name` — useful for scripting |
| `-o jsonpath='...'` | Extract specific fields with JSONPath |
| `-o jsonpath-file=file` | Read JSONPath expression from a file |
| `-o custom-columns=...` | Table with custom column definitions |
| `-o custom-columns-file=file` | Read column definitions from a file |
| `--sort-by=<field>` | Sort list output by a JSONPath field |
| `-o go-template=...` | Go template (rarely used in CKA) |

---

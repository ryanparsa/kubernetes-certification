---
name: search-reference-material
description: Search the local reference markdown files for Kubernetes exam topics, commands, and concepts. Use this to find inspiration for quiz questions or to check facts.
allowed-tools: Grep Glob Bash
---

Search the local reference documentation at `ref/`. This directory contains curated cheat sheets and exam tips. Note: Ignore the `ref/kubernetes-doc/` subdirectory which contains the full official docs.

The user or prompt needs information about: $ARGUMENTS

1. Use Grep or Bash to search through the markdown files directly in `ref/` (e.g. `ref/etcd Reference.md`).
2. Find the relevant concepts, commands, or YAML snippets to formulate your response or generate questions.
3. Always base your generated questions and explanations on the factual content found in these reference files.

You have permission to use `Grep`, `Glob`, and `Bash` to search the files. You do not need to ask for permission.

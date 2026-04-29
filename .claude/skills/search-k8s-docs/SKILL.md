---
name: search-k8s-docs
description: Search the offline Kubernetes documentation for specific keywords, concepts, or code snippets. Use this whenever you need to look up Kubernetes configurations or documentation.
allowed-tools: Grep Glob Bash
---

Search the offline Kubernetes documentation (https://kubernetes.io/docs/) at `ref/kubernetes-doc/content/en/`.

The user wants to find information about: $ARGUMENTS

1. Use Grep or Bash to search through the markdown files in `ref/kubernetes-doc/content/en/`.
2. Find the relevant documentation pages and provide the summary or exact code snippets requested.
3. If providing code, ensure it aligns with the official documentation formatting.
4. Always mention the source file path (e.g., `ref/kubernetes-doc/content/en/docs/...`) so the user can review it.

You have permission to use `Grep`, `Glob`, and `Bash` to search the files. You do not need to ask for permission.

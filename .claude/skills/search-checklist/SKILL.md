---
name: search-checklist
description: Read and search a specific certification checklist markdown file to find topics, learning objectives, or items to test.
allowed-tools: Grep Glob Bash
---

Search and read the certification checklist at the provided path: $ARGUMENTS

1. Use Grep or Bash to find specific topics or items within the checklist file specified in the arguments.
2. If the path is relative, ensure you are searching within the current repository structure (e.g., `ref/cka-ckad-checklist.md`, `kcsa/checklist.md`).
3. Use the information found to ensure that questions, scenarios, or grading rubrics align perfectly with the exam curriculum defined in the checklist.
4. Always follow the checklist structure to maintain consistent coverage of the syllabus.

You have permission to use `Grep`, `Glob`, and `Bash` to search and read the files. You do not need to ask for permission.

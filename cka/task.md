Your task is to take a given Directory ID from the user (e.g., "19" or "Directory 1") and automatically find, extract, and save the corresponding CKA mock exam question content into that directory.

**Instructions:**

1. **Understand the Target Directory:** The user will provide a Directory ID (e.g., "19").
2. **Reverse Map to Question:** Look at the mapping table located in `/Users/ryan/Projects/kubernetes-certification/cka/readme.md`. Find the row that corresponds to this Directory ID to determine the **Simulator** (e.g., Simulator A or Simulator B) and the **Question Number** (e.g., Question 2).
3. **Locate the Material:** Based on the Simulator identified, look into the corresponding Markdown file in the `/Users/ryan/Projects/kubernetes-certification/cka/` directory:
   - For Simulator A: `CKA Simulator A Kubernetes 1.35.md`
   - For Simulator B: `CKA Simulator B Kubernetes 1.35.md`
4. **Read the Markdown File Directly:** Use the `view_file` tool to navigate—**do not run shell scripts or Python to parse it**.
   - These files are large (~100KB), but manageable.
   - Questions are identified by the header: `Question N | Title`.
   - The question portion follows immediately after the title line.
   - The answer portion starts after the `Answer:` line.
5. **Extract Content:** Identify the full question and answer block. Key patterns to recognize:

   | Content Type | Markdown Pattern |
   |---|---|
   | Question title | `Question N | Title` or `Preview Question N | Title` |
   | SSH target | `Solve this question on: ssh ...` |
   | Step heading | `Step N` |
   | Section heading | `Answer:` |
   | Code/Terminal | Content often preceded by `➜` or appearing in blocks. |

   **Note:** "Simulator A Preview" questions are located at the end of the `CKA Simulator A Kubernetes 1.35.md` file.

6. **Format with GitHub Flavored Markdown:** Format the extracted content accurately.
   
   **Formatting conventions:**
   - Use `# Question N | Title` as the top-level heading.
   - Use `> **Solve this question on:** \`ssh ...\`` for the instance instruction.
   - Use `## Answer` for the answer section.
   - Use `### Step N` for numbered steps.
   - Use ` ```bash ``` ` for terminal commands/sessions (often lines starting with `➜`).
   - Use ` ```yaml ``` ` for YAML blocks.
   - Use plain ` ``` ``` ` (no language) for output/result blocks.
   - Use `> [!NOTE]` or `> [!IMPORTANT]` for informational callouts (info icons in source).

7. **Check Existing File:** Check if `readme.md` already exists in that directory. If it does, verify the content. If the styling is already okay, simply respond to the user that "everything is ok" and do not modify the file.
8. **Save to Directory:** If the file does not exist or needs updates, write the formatted text into `readme.md` at `/Users/ryan/Projects/kubernetes-certification/cka/<ID>/readme.md`.
9. **Update Tracking Status:** Finally, update the `Status` column in `/Users/ryan/Projects/kubernetes-certification/cka/readme.md` for this specific Question to indicate it is "Done".

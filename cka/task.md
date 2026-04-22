Your task is to take a given Directory ID from the user (e.g., "19" or "Directory 1") and automatically find, extract, and save the corresponding CKA mock exam question content into that directory.

**Instructions:**

1. **Understand the Target Directory:** The user will provide a Directory ID (e.g., "19").
2. **Reverse Map to Question:** Look at the mapping table located in `/Users/ryan/Projects/kubernetes-certification/cka/readme.md`. Find the row that corresponds to this Directory ID to determine the **Simulator** (e.g., Simulator A or Simulator B) and the **Question Number** (e.g., Question 2).
3. **Locate the Material:** Based on the Simulator identified, look into the corresponding HTML file in the `/Users/ryan/Projects/kubernetes-certification/cka/` directory. For example:
   - For Simulator A: Search in `CKA Simulator A Kubernetes 1.35.html`
   - For Simulator B: Search in `Killer Shell - B Exam Simulators.html`
4. **Read the HTML File Directly:** Use the `Read` tool with `offset` and `limit` to navigate the file — **do not run shell scripts or Python to parse it**. The files are large (~889KB) so you must read in small chunks (5 lines at a time maximum to stay within token limits).

   **File structure for Simulator A (`CKA Simulator A Kubernetes 1.35.html`):**
   - The actual question content starts around **line 1389**. Each question spans approximately 5–8 lines.
   - Each question is wrapped in: `<details><summary><span>Question N | Title</span></summary>.....</details>`
   - To find a specific question, start reading from line 1389 and read forward 5 lines at a time until you find the `Question N |` marker in a `<summary>` tag.
   - The question ends where the next `</details>` appears before the next `<details><summary>Question N+1 |`.

   **File structure for Simulator B (`Killer Shell - B Exam Simulators.html`):**
   - Use the same approach: read from the beginning in 5-line chunks to find the question markers.

5. **Extract Content:** Read lines until you've captured the full question and answer. Key HTML patterns to recognize:

   | Content Type | HTML Pattern |
   |---|---|
   | Question title | `<summary><span>Question N \| Title</span></summary>` |
   | SSH target | `<code class="copy-on-click">ssh ...</code>` |
   | Paragraph text | `<p><span>TEXT</span></p>` |
   | Inline code | `<code class="copy-on-click">VALUE</code>` |
   | Step heading | `<h6 id="step-N"><span>Step N</span></h6>` |
   | Section heading | `<h5 id="answer"><span>Answer:</span></h5>` |
   | Code block language | `<pre class="md-fences ... " lang="LANG">` (values: `term`, `bash`, `yaml`, or empty for plain output) |
   | Code line content | `<pre class=" CodeMirror-line " role="presentation"><span role="presentation" ...>TEXT</span></pre>` |
   | Terminal command (input) | Same as above but span has `class="input-command"` |
   | Blockquote / note | `<blockquote><p>TEXT</p></blockquote>` |

6. **Format with GitHub Flavored Markdown:** Format the extracted content accurately based on GitHub's official guidelines. Use code blocks, alerts, and formatting correctly. Reference these guides for styling rules:
   - [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
   - [Working with advanced formatting](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting)

   **Formatting conventions:**
   - Use `# Question N | Title` as the top-level heading
   - Use `> **Solve this question on:** \`ssh ...\`` for the instance instruction
   - Use `## Answer` for the answer section, `### Step N` for numbered steps
   - Use ` ```bash ``` ` for `lang="term"` or `lang="bash"` code blocks (terminal sessions)
   - Use ` ```yaml ``` ` for `lang="yaml"` blocks
   - Use plain ` ``` ``` ` (no language) for output/result blocks
   - Use `> [!NOTE]` or `> text` for blockquotes

7. **Check Existing File:** Check if `readme.md` already exists in that directory. If it does, verify the content and try to fix its styling based on the formatting rules above. If the styling is already okay, simply respond to the user that "everything is ok" and do not modify the file.
8. **Save to Directory:** If the file does not exist or needs formatting updates, write the formatted extracted text into the `readme.md` file at `/Users/ryan/Projects/kubernetes-certification/cka/<ID>/readme.md`. Focus on high-quality GitHub Flavored Markdown conversion. Do not alter the intended meaning, commands, or original typos/content from the source text.
9. **Update Tracking Status:** Finally, update the `Status` column in `/Users/ryan/Projects/kubernetes-certification/cka/readme.md` for this specific Question to indicate it is "Done".

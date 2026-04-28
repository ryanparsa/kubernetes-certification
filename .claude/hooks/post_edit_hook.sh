#!/bin/bash
# Read tool input from stdin
input=$(cat)
target_file=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.target_file // .tool_input.TargetFile // empty')

if [ -n "$target_file" ] && [ -f "$target_file" ]; then
    out=$(python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/check_ascii.py" "$target_file")
    if [ $? -ne 0 ]; then
        # Output JSON to warn the user and Claude without blocking
        jq -n --arg msg "$out" --arg file "$target_file" \
          '{systemMessage: ("Warning: Non-ASCII characters detected in " + $file + ".\n" + $msg), additionalContext: ("Warning: Non-ASCII characters detected in " + $file + ":\n\n" + $msg + "\n\nPlease correct them manually. Follow .claude/rules/ascii-only.md")}'
        exit 0
    fi
fi
exit 0

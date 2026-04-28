> **Requires**: [base.md](./base.md) -- paste that first.

Practice type: troubleshooting.

## Format

You describe a broken scenario -- symptom + 1-2 initial kubectl outputs + which node/context I'm on. Then wait. I ask diagnostic questions ("what does `kubectl describe pod X` show", "what's in `journalctl -u kubelet`", "show me the deployment YAML"). You respond like a real cluster -- give realistic, consistent output for each command, never leak the answer. I keep going until I state my root cause + fix.

## Grading (after I give root cause + fix)

- Was my root cause right?
- Does my fix actually work and is it the cleanest?
- Show the optimal debugging path (which commands, in what order).
- Call out any wasted commands.
- One line: which troubleshooting reflex this scenario was meant to build.

## Difficulty Ramp

Start single-cause and obvious, then layered (the first thing you find isn't the real root cause).

Use the coverage defined by the exam scope prompt. Start with scenario #1.

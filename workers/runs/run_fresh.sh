#!/usr/bin/env bash
# C2 test: run the recap skill in a fresh Claude Code session that sees only the brain as handed out, the skill and one transcript.
# usage (from the repo root): workers/runs/run_fresh.sh workers/skills/skill-recap.md inbox/call-1.md /tmp/run1 [--no-brain]
# The brain copy leaves out my A1 and A2 recaps, as in the saved runs. --no-brain is the control. The reply goes to <out>.reply.txt.
set -euo pipefail
SKILL="$1"; TRANSCRIPT="$2"; OUT="$3"; REPO="$(pwd)"
CALL_DATE=$(grep -m1 '^date:' "$TRANSCRIPT" | awk '{print $2}')

rm -rf "$OUT"; mkdir -p "$OUT/workers/skills" "$OUT/inbox"; OUT="$(cd "$OUT" && pwd)"
if [[ "${4:-}" != "--no-brain" ]]; then
  cp -r brain "$OUT/brain"
  rm -f "$OUT"/brain/knowledge/meetings/{2026-09-22-kettle-and-crumb-weekly,2026-09-24-kettle-and-crumb-monthly-business-review}.md
fi
cp "$SKILL" "$OUT/workers/skills/skill-recap.md"
cp "$TRANSCRIPT" "$OUT/inbox/"

cd "$OUT"
echo "Follow the skill in workers/skills/skill-recap.md to recap the call transcript inbox/$(basename "$TRANSCRIPT")." |
  claude -p --setting-sources project --strict-mcp-config --disable-slash-commands --no-session-persistence \
    --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep" | tee "$OUT.reply.txt"
echo
for f in brain/knowledge/meetings/"$CALL_DATE"-*.md; do python "$REPO/extra/check_recap.py" "$f"; done

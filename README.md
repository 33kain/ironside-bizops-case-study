# Ironside Biz Ops case study: Milić Dragović

My answers to the [brief](INSTRUCTIONS.md), worked in the Brightline demo brain. Time spent and the three things AI got wrong are in [log.md](log.md). No questions skipped.

| Question | File |
|---|---|
| A1 Recap of call-1 | [brain/knowledge/meetings/2026-09-22-kettle-and-crumb-weekly.md](brain/knowledge/meetings/2026-09-22-kettle-and-crumb-weekly.md) |
| A2 Recap of call-2, proposed page edits | [brain/knowledge/meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md](brain/knowledge/meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md), [proposed-changes.md](proposed-changes.md) |
| A3 Dana briefing | [answer.md](answer.md) |
| B1, B2 Ranking, one more number, which pod | [numbers.md](numbers.md) (figures from [analysis/pod_numbers.py](analysis/pod_numbers.py) and [analysis/block_b_extra.py](analysis/block_b_extra.py)) |
| B3 One-week plan for South | [plan.md](plan.md) |
| C1 What's wrong with the bad recap | [c1-whats-wrong.md](c1-whats-wrong.md) |
| C2 New skill, before and after | [workers/skills/skill-recap.md](workers/skills/skill-recap.md), [c2-before-after.md](c2-before-after.md), runs in [workers/runs/](workers/runs/) |
| C3 Ticket for the agent's engineer | [fde-ticket.md](fde-ticket.md) |
| Extra | [extra/](extra/) (`check_recap.py`) |

**Rerun things yourself** (Python 3 and Claude Code, nothing to install; use `python3` on macOS):

- `python analysis/pod_numbers.py`: rebuilds the dashboard from `calls.csv` and shows the East mismatch.
- `python extra/check_recap.py brain/knowledge/meetings/`: checks every recap against RESOLVER and SANITIZER.
- `bash workers/runs/run_fresh.sh workers/skills/skill-recap.md inbox/call-1.md /tmp/run1`: runs the skill in a fresh Claude Code session that sees only the brain as handed out, the skill and the transcript (add `--no-brain` for the control).

[CLAUDE.md](CLAUDE.md) holds the working rules my Claude Code setup follows in this folder.

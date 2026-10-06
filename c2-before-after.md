# C2: the recap skill, before and after

The [old skill](workers/runs/skill-recap.v0-original.md) was five steps and never mentioned RESOLVER or SANITIZER. The [new skill](workers/skills/skill-recap.md) turns their rules into steps: read the brain first, cut the transcript where the client leaves, never type results, one owner and a date per action item, check before posting, propose page edits instead of making them. [C1](c1-whats-wrong.md#root-cause) maps each old line to its fix.

## How I tested it

Each run is a fresh Claude Code session (`claude -p`, no project memory, no MCP servers, no plugins) in a folder holding only the brain as handed out, the skill and one transcript ([run_fresh.sh](workers/runs/run_fresh.sh), `--no-brain` for the control). Each output went through [check_recap.py](extra/check_recap.py) in that folder. The copies saved here fail it only on file name and links, because they sit outside `brain/`. One thing still loads in these sessions: my personal Claude Code preferences (language and format rules, nothing about this case).

| Skill | Input | Runs | Checker | What I saw |
|---|---|---|---|---|
| v0, in production | Loop Athletic 15 Sep | [bad-recap.md](workers/output/bad-recap.md) | FAIL | Leaked the DM, typed GMV, no owners or dates, no template |
| v0, no brain in the folder | same | [1](workers/runs/0-old-skill-no-brain.md) | FAIL | Typed GMV in a "Key numbers" table and made up its own template. Left the DM out |
| v0, with the brain | same | [1](workers/runs/1-old-skill-with-brain.md) | FAIL | Followed the brain only by overriding its skill ([its reply](workers/runs/1-old-skill-with-brain.reply.txt): "the skill's steps conflict with `brain/RESOLVER.md` and `brain/SANITIZER.md`"). Its held-back flag still says the cut text came after Theo left |
| v1 (first rewrite) | same, plus call-1 and call-2 | [1](workers/runs/2-new-skill-v1-run1.md) [2](workers/runs/2-new-skill-v1-run2.md) [3](workers/runs/2-new-skill-v1-run3.md), [call-1](workers/runs/2-new-skill-v1-call-1.md), [call-2](workers/runs/2-new-skill-v1-call-2.md) | 5 PASS | Two misses: two of three runs tied the size chart issue to an older size-chart item, which the call never did; the call-1 run kept "tonight", "by Wednesday" and "on Friday" |
| v2 | same | [1](workers/runs/3-new-skill-v2-run1.md) [2](workers/runs/3-new-skill-v2-run2.md) [3](workers/runs/3-new-skill-v2-run3.md), [call-1](workers/runs/3-new-skill-v2-call-1.md), [call-2](workers/runs/3-new-skill-v2-call-2.md) | 5 PASS | Both misses gone (two rules added: dates as dates, link only the same item). Review found three more: weekly figures linked to a sheet that has no column for them; "Dana says she was promoted" reads as doubt on a page Dana reads; gaps that block the plan (no baseline, a cap that may not cover it) not raised |
| v3 (final) | same | [1](workers/runs/4-new-skill-v3-run1.md) [2](workers/runs/4-new-skill-v3-run2.md) [3](workers/runs/4-new-skill-v3-run3.md), [call-1](workers/runs/4-new-skill-v3-call-1.md), [call-2](workers/runs/4-new-skill-v3-call-2.md) | 5 PASS | All three fixed with one line each, plus a rule for "next Tuesday" said early in the week. One run wrote "8 dollars" for "$8": my personal no-dollar-sign rule (meant for AI cost talk) leaking in |

## Before: [bad-recap.md](workers/output/bad-recap.md)

```markdown
# Loop Athletic weekly, 15 Sep

Great call with Theo. All 12 fall videos were delivered and the try-on format is performing much better.
Loop Athletic is at $95K GMV this month. Theo wants 12 more videos for October, all try-on. There's a size
chart issue on the product page. [...one sentence from a private DM, not repeated here...]

## Next steps
- Send the October brief
- Look into the size chart issue
- [...the same DM again, not repeated here...]
```

## After: final skill, [run 1 of 3](workers/runs/4-new-skill-v3-run1.md)

```markdown
# Loop Athletic: weekly

## Summary
- Fall collection creator videos: all 12 delivered, with the last 4 in the try-on format. This completes the
  batch and the format change agreed in the [2026-09-10 recap](2026-09-10-loop-athletic-weekly.md).
- Theo says the try-on videos are performing much better than the earlier format.
- GMV: see [accounts sheet](../reference/accounts-sheet.csv), row `loop-athletic`.
- Decision: October batch of 12 more creator videos, all in the try-on format.
- Theo raised a size chart issue on the product page.

## Action items
| Owner | Action | Due |
|---|---|---|
| Lena Varga | Send the brief for the October batch of 12 try-on videos | 2026-09-18 |

## Open questions
- Who looks into the size chart issue on the product page, by when?

## Flags for a person
- Theo Grant gave a GMV figure that doesn't match the sheet.
- Something from this call was held back under SANITIZER. Ask Lena Varga.
```

The model can follow the brain when it reads it, but v0 told it to do the opposite. The new skill makes the brain's rules its own steps, so a good recap doesn't depend on the model overriding its instructions. What a skill file can't fix is in [fde-ticket.md](fde-ticket.md).

# C1: What's wrong with `bad-recap.md`

The agent's recap of the Loop Athletic weekly on 15 Sep (call c084), checked against its [transcript](workers/output/bad-recap-source.md), [RESOLVER](brain/RESOLVER.md) and [SANITIZER](brain/SANITIZER.md). Most severe first. "l." is a line of [bad-recap.md](workers/output/bad-recap.md), "src" a line of the transcript.

1. **Critical: it posted a private DM about our fees where the client reads it.** The end of l.9 and all of l.14 come from a DM Lena read out, still recording, after Theo left (src 19-20), and the agent posts straight to the client's Slack channel. *SANITIZER 2 and 3.*
2. **High: it typed a GMV figure and missed the conflict.** "$95K GMV this month" (l.9) is Theo's rough number (src 12). The [sheet](brain/knowledge/reference/accounts-sheet.csv) says 62,000 for the last 30 days. *RESOLVER house rule 4.*
3. **High: no next step has an owner or a due date.** The call set one: Lena sends the October brief by Fri 18 Sep (src 14-15). The size chart has no owner (src 16-17), so it belongs in Open questions. *House rule 3.*
4. **Medium: old news written as new.** The try-on switch was decided on 10 Sep, and the recap doesn't link [that recap](brain/knowledge/meetings/2026-09-10-loop-athletic-weekly.md). *House rule 5.*
5. **Medium: a claim written as fact.** "The try-on format is performing much better" (l.9) is Theo's view (src 12). It should read "Theo says ...". *Template: what the client told us.*
6. **Medium: no template.** No `attendees` or `source`, the wrong title, one prose paragraph, "Next steps" instead of an Action items table, and no Open questions or Flags for a person. *RESOLVER template.*
7. **Low: an opinion.** "Great call with Theo." (l.9). *Template: facts, decisions, what the client told us.*

**It still counted as on time:** posted 55 minutes after the call. The number checks a timestamp, not the recap.

## Do now

1. Take the post down and replace it with the clean [rerun](workers/runs/4-new-skill-v3-run1.md).
2. Tell Lena today and copy Priya Nair (Head of Ops). Lena decides how Theo hears about it.
3. Until the cut is in code ([C3](fde-ticket.md)), AMs stop recording when the client leaves. Spot-check the other 58 agent recaps.

## Root cause

The [old skill](workers/runs/skill-recap.v0-original.md) allowed every failure and ordered one: "Include the key numbers". A fresh rerun of it repeated 2, 4 and 6, but not 1 or 3 ([run](workers/runs/0-old-skill-no-brain.md)). Whether a DM gets out depends on the run, so only code can guarantee the cut.

| Old skill said | Led to | [New skill](workers/skills/skill-recap.md) |
|---|---|---|
| Input: "The transcript of one call." | No RESOLVER, SANITIZER, sheet or 10 Sep recap (2, 4, 6) | §1 Read first |
| "Read the whole transcript." | The DM after Theo left was in scope (1) | §2 Cut the transcript |
| "Include everything relevant, so nothing gets lost." | DM kept; prose, a claim as fact, praise (1, 5, 6, 7) | §2 Cut; §3 Summary |
| "Include the key numbers mentioned on the call." | Typed GMV (2) | §3 Numbers |
| "List the next steps." | No owner, no date (3) | §3 Action items, Open questions |
| Output: "A file in `brain/knowledge/meetings/`." | Its own format (6) | §3 File name and template |
| "Post it." | No check (all) | §4 Check, then post |

---
type: skill
step: recap
owner: Brightline ops
updated: 2026-10-07
---

# Skill: recap a client call

You turn one recorded client call into a recap in the brain, then post it to the client's Slack channel. The client can read both. Write every line as if they are reading it.

## 1. Read first, in this order
1. `brain/RESOLVER.md` (rules, recap template), then `brain/SANITIZER.md` (what never goes in).
2. The account page in `brain/knowledge/accounts/` for the brand in the transcript's title, and the people pages it links. The account page's file name is the account slug. No matching page: stop and say so.
3. Every earlier recap for that account in `brain/knowledge/meetings/` (file names contain the slug), and the account's row in `brain/knowledge/reference/accounts-sheet.csv`.
4. The transcript. The call date is its `date:`. Client participants are the attendees not from Brightline.

## 2. Cut the transcript
- Stop where the last client participant leaves (a line like `[<Name> left the call]`). Use nothing after it. If no client leaves, use the whole recording.
- Before that point, also skip pasted DMs or messages, "between us" or "off the record" remarks, and asides not said to the client.
- What you skip never appears in the recap, the post or your reply, not even reworded.

## 3. Write the recap
File: `brain/knowledge/meetings/YYYY-MM-DD-<account-slug>-<meeting-name>.md`, named like the existing recaps. Date = call date. Meeting name = the transcript title without the brand, lowercase, words joined by hyphens.

Copy RESOLVER's recap template exactly: frontmatter `type: meeting`, `date`, `account` (the slug), `attendees` (names only), `source` (the transcript path you were given); title `# <Brand>: <meeting name>`; the GMV line; then Summary, Action items, Open questions, Flags for a person. An empty section says "None."
- **GMV line:** right under the title, from the account's sheet row, never from the call: `**GMV, last 30 days:** $<gmv_last_30d_usd, with commas> ([accounts sheet](../reference/accounts-sheet.csv), row `<slug>`, updated <sheet_updated>)`. If a GMV figure said on the call disagrees with the sheet, write no figure: `**GMV, last 30 days:** under review. <Name> gave a figure that doesn't match the [accounts sheet](../reference/accounts-sheet.csv), row `<slug>`. See Flags for a person.`
- **Summary:** 3 to 6 bullets of facts, decisions ("Decision: ...") and what the client told us. Reword, don't quote. A claim about results we can't check reads as the client's ("<Name> says ..."); what clients tell us about themselves or decide (a new role, a target, a budget) is written as fact. No opinions or praise, about people or the call. Write every date as a date ("23 Sep"), never "tonight", "Wednesday" or "Friday": the page is read long after the call.
- **Already told:** if the client told us this before, or it changes or answers something in an earlier recap (a target, an open question, an action item), say so and link that recap: `[YYYY-MM-DD recap](YYYY-MM-DD-<slug>-<name>.md)`. Link only the same item. Don't say two items are related unless the call says so.
- **Numbers:** targets, budgets, rates and amounts of work the client agrees to are decisions: write them as said. Outside the GMV line, results (GMV of any kind or period, ad spend, active or new affiliates, retention) are never typed: link `[accounts sheet](../reference/accounts-sheet.csv)`, row `<slug>`. If the sheet has no column for a result, say where it is reported instead, or leave it out. If a result said on the call disagrees with the sheet, flag it without the number. Our own fees, margins and rates never go in.
- **Action items:** a table `| Owner | Action | Due |` with a `|---|---|---|` row, one row per commitment made on the call.
  - Owner: exactly one named person, full name, who said they'd do it or agreed when asked.
  - Due: YYYY-MM-DD counted from the call date. "Tonight" = call date. "Tomorrow" = the next day. A weekday ("by Friday", "next Tuesday") = the first one after the call date, except "next <day>" said one or two days before that day, which means the week after. "The day before X" = count back from X's date.
  - Owner is "we", "someone" or two people, or no date was said: don't guess. Put it under Open questions as "Who does ..., by when?"
- **Open questions:** what was asked and not answered, every task without one named owner and a date, and any gap that blocks an action item (a goal with no baseline, a budget that may not cover the plan).
- **Flags for a person:** each sheet conflict, as "<Name> gave a <metric> figure that doesn't match the sheet." If anything you cut could matter: "Something from this call was held back under SANITIZER. Ask <AM from the account page>." Never repeat what you cut.

## 4. Check, then save and post
Run SANITIZER's check on every line. One "no" to either of the first two questions, or a "yes" to the third, and the line comes out.
- Would the person or brand named here be fine reading this line?
- Is every performance number linked to the sheet rather than typed in?
- Did anything come from a DM, a side comment or after the client left?

Then confirm every box. Fix what fails. If you can't fix it, don't post; say why in your reply.
- [ ] Nothing from after the cut. No DM, opinion, personal data or our fees.
- [ ] GMV line under the title: the sheet's figure and date, or "under review" with no figure if the call disagreed.
- [ ] No other result (GMV, ad spend, affiliates, retention) typed anywhere. Agreed targets and budgets are fine.
- [ ] Each action item: exactly one named owner and a YYYY-MM-DD date that comes from the call.
- [ ] Anything told before links its earlier recap.
- [ ] File name, frontmatter, title, GMV line and the four sections match the template.

Speed matters (target: posted within an hour of the call), but never skip a check to post sooner.

## 5. Propose, never edit
Write only the new recap file. Never edit people pages, account pages, earlier recaps or the sheet. End your reply, not the recap, with "Proposed edits" for a pod lead to approve: add this recap to the account page's meeting list; new contacts, roles or answered open threads; each sheet conflict with the call's number and who said it, so a person can check it. Nothing you cut goes here either.

---
type: resolver
owner: Brightline ops
updated: 2026-10-07
---

# RESOLVER: where things go

Read this first, human or agent. Before your first write, read `SANITIZER.md`.

```
brain/
├── RESOLVER.md     this file
├── SANITIZER.md    what never goes in, and the check every write passes
├── NOW.md          this week's priorities. Overwritten weekly
└── knowledge/
    ├── people/     one page per person, facts only
    ├── accounts/   one page per brand we serve
    ├── meetings/   one recap per meeting
    └── reference/  source-of-truth exports. Consult, don't edit
```

## Where does this go?

1. This week's state? `NOW.md`.
2. About one person? `knowledge/people/`.
3. About one brand? `knowledge/accounts/`.
4. About one meeting? `knowledge/meetings/`, named `YYYY-MM-DD-brand-slug.md`.
5. A performance number (GMV, ad spend, active affiliates, retention)? It lives in `knowledge/reference/accounts-sheet.csv`. Pages link to the sheet. They never retype the number, except a recap's GMV line (template below). Targets, budgets and rates the client agrees to are decisions: recaps record them as said.

## House rules

1. **Nothing on the SANITIZER list, ever.**
2. **People and account pages are changed by proposal.** Agents and new team members propose edits. A pod lead approves them.
3. **Every recap has two parts:** a summary, and action items. Every action item has one owner and a due date.
4. **Link, don't retype.** If a call states a number that disagrees with the sheet, flag it. Don't change the sheet and don't copy the call's number onto a page, not even in the GMV line.
5. **When someone has already told us something, say so.** Link the earlier meeting instead of treating it as new.

## Recap template

```
---
type: meeting
date: YYYY-MM-DD
account: brand-slug
attendees: [names]
source: inbox/<file>
---

# <Brand>: <meeting name>

**GMV, last 30 days:** $<gmv_last_30d_usd> ([accounts sheet](../reference/accounts-sheet.csv), row `brand-slug`, updated <sheet_updated>)
The sheet's figure, never the call's. If the call gave a GMV figure that disagrees, no figure:
**GMV, last 30 days:** under review. <Name> gave a figure that doesn't match the [accounts sheet](../reference/accounts-sheet.csv), row `brand-slug`. See Flags for a person.

## Summary
3 to 6 bullets. Facts, decisions, what the client told us.

## Action items
| Owner | Action | Due |

## Open questions

## Flags for a person
Conflicts with the sheet, anything held back under SANITIZER.
```

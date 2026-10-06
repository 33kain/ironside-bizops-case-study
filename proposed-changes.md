# A2: proposed changes to people, account and sheet pages

For Marcus Obi, South pod lead, to approve or reject by ID, for example "all but K5" ([RESOLVER](brain/RESOLVER.md), rule 2). Nothing is applied yet. S1 is on hold; every other row is ready. Each approved page gets `updated:` set to the day of the edit, and each added line links its recap. Sources: recaps of [24 Sep][r24] (call-2), [22 Sep][r22] (call-1) and [17 Sep][r17].

## Sheet: `accounts-sheet.csv`, row `kettle-and-crumb`

| ID | Column | Now | Proposed | Status |
|---|---|---|---|---|
| S1 | `gmv_last_30d_usd` | `140000` (sheet of 21 Sep) | `210000`: Dana Reyes on 24 Sep, her finance team's 30-day figure | **Hold** |

- **Why hold:** Marcus asked if it is TikTok Shop only; Dana didn't say. Kettle & Crumb also sells DTC ([account page](brain/knowledge/accounts/kettle-and-crumb.md)), and the sheet doesn't state its scope. Get both in writing. If they differ, `210000` doesn't go in this column.
- **Route:** the sheet is an export ("Consult, don't edit"), so whoever owns it fixes the figure at the source. No hand edit.

## `people/dana-reyes.md`

| ID | Field | Proposed | From |
|---|---|---|---|
| D1 | Role | VP Growth, Kettle & Crumb (client). Was Head of Growth. | 24 Sep |
| D2 | Meetings (new line) | Attends the monthly business reviews | 24 Sep |
| D3 | What she has told us | Add 2026-09-17: fall flavor launch moves to 6 Oct; about 70 creators to sample for it in October. | 17 Sep |
| D4 | What she has told us | Add 2026-09-22: restated the 60-affiliate target; sample shipping up to $8 a box for now; keep the Wednesday summary and add top sellers. | 22 Sep |
| D5 | What she has told us | Add 2026-09-24: her promotion; a 30-day GMV figure from her finance team (scope open); double the fall flavor posting rate after the 6 Oct launch. | 24 Sep |
| D6 | Open threads | Close "sample shipping budget" (Jess answered it). Add: GMV scope; baseline for "double"; who approves creators now. | 24 Sep |

## New page: `people/jess-park.md` (J1)

```markdown
---
type: person
updated: <day of the edit>
---

# Jess Park

- **Role:** ops and fulfillment, Kettle & Crumb (client). Title not given.
- **Owns on their side:** samples, sample shipping, inventory (from 2026-09-24)
- **Works with:** Marcus Obi (AM, South pod)
- **Meetings:** joins the Kettle & Crumb weeklies
- **What she has told us:**
  - 2026-09-24: sample shipping budget is $8 a box, capped at $600 a month; she needs the fall flavor sample list by 1 Oct to ship on time. [recap](../meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md)
- **Open threads:** does the cap cover both fall flavor and affiliate samples?
```

## `accounts/kettle-and-crumb.md`

| ID | Field | Proposed | From |
|---|---|---|---|
| K1 | Client contact | Dana Reyes, VP Growth. Attends the monthly business reviews. | 24 Sep |
| K2 | Ops contact (new line) | Jess Park (link her page, J1): samples, shipping and inventory; joins the weeklies | 24 Sep |
| K3 | Sample shipping budget (new line) | $8 a box, capped at $600 a month (Jess Park, 2026-09-24) | 24 Sep |
| K4 | Current focus | Add: fall flavor launches 6 Oct; goal: double its posting rate after launch (baseline to agree) | 24 Sep |
| K5 | Numbers | Add: "GMV under review: see the 24 Sep recap." Remove once S1 is settled. | 24 Sep |
| K6 | Reporting (new line) | Wednesday affiliates summary, asked for on 3 Sep; from 23 Sep it also lists top sellers | 22 Sep |
| K7 | Meetings | Add the 2026-09-22 weekly and the 2026-09-24 monthly business review | 22, 24 Sep |

## `people/marcus-obi.md`

| ID | Field | Proposed | From |
|---|---|---|---|
| M1 | Working on | Add: Kettle & Crumb fall flavor launch on 6 Oct (creator plan, sample list) | 24 Sep |

[r24]: brain/knowledge/meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md
[r22]: brain/knowledge/meetings/2026-09-22-kettle-and-crumb-weekly.md
[r17]: brain/knowledge/meetings/2026-09-17-kettle-and-crumb-weekly.md

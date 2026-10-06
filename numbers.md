# B1 and B2: the recap number

**The number:** share of client calls with a recap posted within an hour. **Target:** 80% in every pod by 31 Oct. **Data:** 140 calls in [`calls.csv`](calls.csv), 1 to 24 Sep; figures from [`analysis/pod_numbers.py`](analysis/pod_numbers.py) and [`analysis/block_b_extra.py`](analysis/block_b_extra.py).

## B1. Ranking

| Rank | Pod (lead) | On time / calls held | Share | Dashboard | Short of 80% |
|---|---|---|---|---|---|
| 1 | North (Sam Whitaker) | 36 / 40 | 90% | 90% | on target |
| 2 | East (Aisha Rahman) | 21 / 30 | **70%** | 75% | 3 calls |
| 3 | South (Marcus Obi) | 14 / 40 | 35% | 35% | 18 calls |
| 4 | West (Lena Varga) | 3 / 30 | 10% | 10% | 21 calls |

**The dashboard overstates East.** Its 75% divides by the 28 *recorded* calls; the other pods divide by calls *held*. On 30 held, East is at 70%: 10 points short, not 5. Fix it before the October report.

**It counts bad recaps too:** the one a pod lead complained about ([c084](workers/output/bad-recap.md)) was on time (55 minutes).

### One more number: the agent posts on time for 49% of its recaps

| Posted by | Recaps | Within the hour | Median time |
|---|---|---|---|
| Recap agent | 59 | 29 (49%) | 65 min |
| Account manager | 45 | 45 (100%) | 18 min |

- **On the agent alone, a pod lands near 50%,** even with every call recorded: it is never faster than 45 minutes.
- **So today the number measures the AM routine, the October lever.** North's AMs posted 33 of its 36 on-time recaps; East went from 7 of 15 on time (1–13 Sep) to 14 of 15 (14–24 Sep) once its AMs posted. A faster agent is the lasting fix ([plan.md](plan.md)).

## B2. South first

**The cause: South leaves every recap to the agent, the agent is slowest on South calls, and the pod works around it.**

- **Not capture, content or coverage.** 36 of 40 calls were recorded, "the content is fine when it shows up" (Marcus), and 34 got an agent recap. Only 14 came within the hour.
- **Speed.** The agent's South median is 74 minutes, the slowest of any pod (56 to 59 elsewhere). The 20 late recaps took 69 to 91 minutes: not near misses.
- **Workaround.** Marcus and Tomas email clients their own summary first and skip the bot ([#pod-south, 18 Sep](slack-thread.txt)), so their summary never reaches the channel or the brain. Kettle & Crumb, South's focus account ([NOW.md](brain/NOW.md)), got 0 of 4 recaps on time.

**Why South:**

- **One routine moves the pod.** Marcus is the AM on all five accounts ([his page](brain/knowledge/people/marcus-obi.md)), and his summaries already reach clients. They only have to become the recap.
- **Biggest upside in reach.** Had its 34 recaps landed within the hour, South would be at 85%, not 35%.
- **It has been done.** East copied North's routine: 3 of 7 calls on time, then 8 of 8 the next week.

**Not West yet, though its gap is bigger.** 26 of its 30 calls were on WhatsApp, unseen by the agent, and capture alone won't reach 80%. West needs the AM routine too, but nothing shows its AMs send clients summaries. South proves it this week; West is next, with Lena's capture work ([NOW.md](brain/NOW.md)) in parallel.

**Not East:** 14 of 15 on time since 14 Sep, so on track.

**Priya Nair's fix (Head of Ops, 18 Sep), counting emailed summaries:** she's right that the work should count, but it moves the dashboard, not the outcome. Emails never reach the brain, so their action items go untracked, and timing them means auditing sent mail; the September baseline would break. Instead, the AM's summary *becomes* the recap: same notes, in the template, in the client channel and the brain within the hour. Same work, and it counts.

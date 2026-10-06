"""Rebuild the recap dashboard from calls.csv and check it against adoption.csv.

Run from the repo root:  python analysis/pod_numbers.py
"""
import csv
from collections import defaultdict
from datetime import datetime
from statistics import median

FMT = "%Y-%m-%d %H:%M"
WINDOW_MIN = 60


def minutes_to_post(row):
    if not row["recap_posted_at"]:
        return None
    end = datetime.strptime(row["call_end"], FMT)
    posted = datetime.strptime(row["recap_posted_at"], FMT)
    return (posted - end).total_seconds() / 60


def on_time(row):
    m = minutes_to_post(row)
    return m is not None and m <= WINDOW_MIN


calls = list(csv.DictReader(open("calls.csv", encoding="utf-8")))
dashboard = {r["pod"]: r for r in csv.DictReader(open("adoption.csv", encoding="utf-8"))}

by_pod = defaultdict(list)
for c in calls:
    by_pod[c["pod"]].append(c)

print("B1. The number: share of client calls with a recap posted within an hour")
print(f"{'pod':<6}{'held':>5}{'recorded':>9}{'on time':>8}{'share':>7}   dashboard says")
ranked = sorted(by_pod, key=lambda p: -sum(map(on_time, by_pod[p])) / len(by_pod[p]))
for pod in ranked:
    rows = by_pod[pod]
    held, rec, ok = len(rows), sum(r["recorded"] == "yes" for r in rows), sum(map(on_time, rows))
    dash = dashboard[pod]["share_of_calls_with_recap_within_1hr"]
    note = "" if f"{ok / held:.0%}" == dash else f"  <-- mismatch: {ok}/{rec} recorded = {ok / rec:.0%}"
    print(f"{pod:<6}{held:>5}{rec:>9}{ok:>8}{ok / held:>7.0%}   {dash}{note}")

print("\nWho posts the recap, and how fast (minutes from call end)")
for who in ("agent", "AM"):
    rows = [c for c in calls if c["posted_by"] == who]
    mins = [minutes_to_post(c) for c in rows]
    ok = sum(m <= WINDOW_MIN for m in mins)
    print(f"{who:<6} {len(rows):>3} recaps, {ok} on time ({ok / len(rows):.0%}), "
          f"median {median(mins):.0f} min, range {min(mins):.0f}-{max(mins):.0f}")
for pod in ranked:
    mins = [minutes_to_post(c) for c in by_pod[pod] if c["posted_by"] == "agent"]
    if mins:
        print(f"  agent in {pod:<6} median {median(mins):.0f} min over {len(mins)} recaps")

print("\nWeek by week (ISO week: on time / calls held, recaps posted by AM)")
for pod in ranked:
    weeks = defaultdict(lambda: [0, 0, 0])
    for c in by_pod[pod]:
        w = weeks[datetime.strptime(c["date"], "%Y-%m-%d").isocalendar()[1]]
        w[0] += on_time(c)
        w[1] += 1
        w[2] += c["posted_by"] == "AM"
    print(f"{pod:<6}" + "  ".join(f"w{k}: {a}/{b} (AM {m})" for k, (a, b, m) in sorted(weeks.items())))

print("\nCalls with no recap")
for c in calls:
    if not c["recap_posted_at"]:
        why = "not recorded" if c["recorded"] != "yes" else "recorded, no recap"
        if c["recorded"] == "yes":
            print(f"  {c['call_id']} {c['date']} {c['pod']} {c['account']} {c['platform']}: {why}")
unrec = defaultdict(int)
for c in calls:
    if c["recorded"] != "yes":
        unrec[(c["pod"], c["platform"])] += 1
print("  not recorded: " + ", ".join(f"{p} {pl} {n}" for (p, pl), n in sorted(unrec.items())))

"""Extra numbers behind numbers.md (B1, B2) and plan.md (B3). Reads calls.csv only.

Run from the repo root:  python analysis/block_b_extra.py
Same definitions as pod_numbers.py: on time = recap posted <= 60 min after call end,
share = on time / calls held.
"""
import csv
from collections import Counter
from datetime import date, datetime
from statistics import median

FMT = "%Y-%m-%d %H:%M"
calls = list(csv.DictReader(open("calls.csv", encoding="utf-8")))
FIRST, LAST = min(c["date"] for c in calls), max(c["date"] for c in calls)


def minutes_to_post(c):
    if not c["recap_posted_at"]:
        return None
    end = datetime.strptime(c["call_end"], FMT)
    return (datetime.strptime(c["recap_posted_at"], FMT) - end).total_seconds() / 60


def on_time(c):
    m = minutes_to_post(c)
    return m is not None and m <= 60


def week(c):
    return datetime.strptime(c["date"], "%Y-%m-%d").isocalendar()[1]


def span(weeks):
    """Calendar dates these ISO weeks cover, clipped to the first and last call in calls.csv."""
    year = int(FIRST[:4])
    lo = max(date.fromisocalendar(year, weeks[0], 1).isoformat(), FIRST)
    hi = min(date.fromisocalendar(year, weeks[-1], 7).isoformat(), LAST)
    return f"{lo} to {hi}"


pods = ["North", "East", "South", "West"]
by_pod = {p: [c for c in calls if c["pod"] == p] for p in pods}

print("1. Gap to the 80% target, and who posted the on-time recaps")
for p in pods:
    rows = by_pod[p]
    ok = sum(map(on_time, rows))
    need = round(0.8 * len(rows))
    who = Counter(c["posted_by"] for c in rows if on_time(c))
    print(f"  {p:<6}{ok}/{len(rows)} on time, 80% = {need} calls, short by {max(0, need - ok)}; "
          f"on-time recaps posted by: {dict(who)}")

print("\n2. East before and after its AMs started posting (first AM post: "
      + next(c["date"] for c in by_pod["East"] if c["posted_by"] == "AM") + ")")
for weeks in ((36, 37), (38, 39), (37,), (38,)):
    rows = [c for c in by_pod["East"] if week(c) in weeks]
    label = f"{span(weeks)} (ISO week{'s' if len(weeks) > 1 else ''} {'-'.join(map(str, weeks))})"
    print(f"  {label}: {sum(map(on_time, rows))}/{len(rows)} on time, AM-posted {sum(c['posted_by'] == 'AM' for c in rows)}")

south = by_pod["South"]
print("\n3. South")
print("  accounts:", dict(Counter(c["account"] for c in south)))
print("  calls per week:", {w: n for w, n in sorted(Counter(map(week, south)).items())})
print("  posted by:", dict(Counter(c["posted_by"] or "no recap" for c in south)))
agent = [minutes_to_post(c) for c in south if c["posted_by"] == "agent"]
late = sorted(m for m in agent if m > 60)
print(f"  agent recaps: {len(agent)}, on time {len(agent) - len(late)}, late {len(late)} "
      f"(late ones {late[0]:.0f}-{late[-1]:.0f} min), median {median(agent):.0f} min")
print("  not recorded:", [(c["call_id"], c["platform"], c["account"]) for c in south if c["recorded"] != "yes"])
print("  recorded, no recap:", [(c["call_id"], c["date"], c["account"]) for c in south
                                if c["recorded"] == "yes" and not c["recap_posted_at"]])
print(f"  if all {len(agent)} agent recaps had landed within the hour: {len(agent)}/{len(south)} = {len(agent) / len(south):.0%}")
print(f"  last week of data, {span((39,))} (ISO week 39): {sum(on_time(c) for c in south if week(c) == 39)}/"
      f"{sum(week(c) == 39 for c in south)} on time")

print("\n4. Kettle & Crumb (South's focus account in NOW.md)")
for c in calls:
    if c["account"] == "kettle-and-crumb":
        m = minutes_to_post(c)
        print(f"  {c['call_id']} {c['date']} posted by {c['posted_by'] or '-'}: "
              + (f"{m:.0f} min" if m is not None else "no recap"))

west = by_pod["West"]
print("\n5. West")
print("  platform x recorded:", dict(Counter((c["platform"], c["recorded"]) for c in west)))
rw = [c for c in west if c["recorded"] == "yes"]
print(f"  recorded calls: {len(rw)}, on time {sum(map(on_time, rw))}, "
      f"minutes {[round(minutes_to_post(c)) for c in rw]}")

bad = next(c for c in calls if c["call_id"] == "c084")
print("\n6. The recap a pod lead complained about (workers/output/bad-recap.md)")
print(f"  {bad['call_id']} {bad['date']} {bad['pod']} {bad['account']}: posted {minutes_to_post(bad):.0f} min "
      f"after the call by {bad['posted_by']}, " + ("on time" if on_time(bad) else "late"))

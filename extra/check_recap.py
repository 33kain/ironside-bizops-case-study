#!/usr/bin/env python3
"""Check meeting recaps against the brain's rules (brain/RESOLVER.md, brain/SANITIZER.md) before posting.

Usage: python extra/check_recap.py PATH [PATH ...] [--source TRANSCRIPT]
PATH is a recap .md file or a folder of them. Prints PASS / WARN / FAIL per file with line
numbers and reasons. Exit code 1 if any file FAILs. Python 3 standard library only.
"""
import argparse
import csv
import re
import sys
import textwrap
from datetime import date
from pathlib import Path

SECTIONS = ["Summary", "Action items", "Open questions", "Flags for a person"]
FRONTMATTER = ["type", "date", "account", "attendees", "source"]
INTERNAL = "Brightline"  # our side in transcript attendee lists; everyone else is the client
MONTHS = "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
VAGUE_OWNERS = {"", "tbd", "tba", "?", "-", "n/a", "team", "we", "us", "all", "everyone", "someone", "brightline"}

# (level, pattern, reason), run on every line below the frontmatter, case-insensitive.
RULES = [(level, re.compile(rx, re.I), why) for level, rx, why in [
    ("FAIL", r"\bbetween (us|you and me)\b|\boff the record\b|\bdon'?t (mention|tell|share)\b|\bprivately\b"
             r"|\bin private\b|\bside (comment|chat|conversation)s?\b|(?-i:\bDM(s|ed|'d)?\b)|\bdirect message",
     "private remark or DM (SANITIZER 2)"),
    ("FAIL", r"\b(left|dropped off|dropped from|hung up on) the call\b|\bafter (the client|\w+) (left|dropped|hung up)\b",
     "side talk after the client left (SANITIZER 2)"),
    ("WARN", r"\bafter the call\b", "is this side talk after the client left? (SANITIZER 2)"),
    ("FAIL", r"\b(flaky|difficult|checked out|unreliable|lazy|rude|clueless|incompetent|useless|annoying)\b",
     "opinion about a person (SANITIZER 1): write what happened, with a date"),
    ("WARN", r"\b(great call|frustrat\w*|angry|upset|annoyed|unhappy|disappointed)\b",
     "opinion or mood, not a fact (SANITIZER 1)"),
    ("FAIL", r"\bagency fees?\b|\bour (fees?|margins?|rates?|pricing)\b|\bretainers?\b", "our commercial terms (SANITIZER 3)"),
    ("WARN", r"(?<!agency )(?<!our )\b(fees?|margins?)\b", "fee or margin: if it is ours, it can't go in (SANITIZER 3)"),
    ("FAIL", r"[\w.+-]+@[\w-]+\.\w+|\+?\(?\d{2,4}\)?[ .-]\d{3,4}[ .-]\d{3,4}\b", "personal data: email or phone (SANITIZER 4)"),
    ("WARN", r"\b(sick|illness|hospital|surgery|pregnan\w*|maternity|medical|divorce\w*|wife|husband|funeral)\b",
     "personal data? health or family (SANITIZER 4)"),
    ("FAIL", r"^\s*[-*>]?\s*\d{1,2}:\d{2}\s+(?-i:[A-Z])[\w.' -]*:", "raw transcript line (SANITIZER 5)"),
]]
METRIC = re.compile(r"\b(GMV|ad spend|(active|new) affiliates|retention|revenue|ROAS)\b", re.I)
TARGET = re.compile(rf"\b(target|goal|aim)|\bby (the )?end of\b|\bby (\d{{1,2}} )?({MONTHS})|\bby \d{{4}}-", re.I)
NOT_AMOUNT = re.compile(rf"\]\([^)]*\)|\b\d{{4}}-\d\d-\d\d\b|\b\d{{1,2}} ({MONTHS})|\b({MONTHS})[a-z]* \d{{1,2}}\b"
                        r"|\b20\d\d\b|\b\d+[- ](day|week|month|hour|min)", re.I)  # dates and periods are not amounts
AMOUNT = re.compile(r"\$\s?\d|\b\d|\b(hundred|thousand|million|billion)\b", re.I)
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
GMV_LINE = re.compile(r"\*\*GMV, last 30 days:\*\*\s*(.*)")
GMV_CONFLICT = re.compile(r"\bGMV\b.*\b(doesn't|does not) match\b", re.I)


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace").replace("\u2019", "'").splitlines()


def iso(s):
    """The date for a YYYY-MM-DD string, else None."""
    try:
        return date.fromisoformat(s) if re.fullmatch(r"\d{4}-\d\d-\d\d", s) else None
    except ValueError:
        return None


def grams(text, n=4):
    """Lowercase word n-grams, in order."""
    w = re.findall(r"[a-z0-9']+", text.lower())
    return [" ".join(w[k:k + n]) for k in range(len(w) - n + 1)]


def find_up(path, rel):
    """<ancestor>/<rel> for the nearest ancestor of path that has that file, else None."""
    return next((d / rel for d in path.resolve().parents if (d / rel).is_file()), None)


def side_talk(transcript):
    """[(line, 4-grams)] for lines spoken after the last client left the call. Only 4-grams with a
    word nobody said while the client was there count, so repeats of on-call content don't."""
    lines = read(transcript)
    head = next((l for l in lines if l.startswith("attendees:")), "")
    clients = {n.strip() for n, org in re.findall(r"([^,\[\]]+?)\s*\(([^)]*)\)", head) if org.strip() != INTERNAL}
    public, private, gone = set(), [], False
    for i, line in enumerate(lines, 1):
        if m := re.search(r"\[(.+?) left the call\]", line):
            clients.discard(m[1])
            gone = gone or not clients  # no client list in the header: the first to leave counts
        elif m := re.match(r"\d+:\d+\s+[^:\[]+:\s*(.*)", line):
            if gone:
                private.append((i, m[1]))
            else:
                public.update(grams(m[1], 1))
    return [(i, {g for g in grams(text) if set(g.split()) - public}) for i, text in private]


def check(path, transcript=None):
    """Return (issues, transcript used or None). An issue is (line, or 0 for the whole file, level, reason)."""
    issues, lines = [], read(path)
    add = lambda line, level, why: issues.append((line, level, why))

    # Frontmatter and file name
    fm, at, end = {}, {}, 0
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0)
    for k in range(1, end):
        key, _, val = lines[k].partition(":")
        fm[key.strip()], at[key.strip()] = val.strip(), k + 1
    if missing := [k for k in FRONTMATTER if not fm.get(k, "").strip("[] ")]:
        add(1, "FAIL", "frontmatter missing: " + ", ".join(missing) + " (RESOLVER template)")
    day, acct, src = fm.get("date", ""), fm.get("account", ""), fm.get("source", "")
    meeting = iso(day)
    attendees = {a.strip(" '\"").lower() for a in fm.get("attendees", "").strip("[]").split(",") if a.strip(" '\"")}
    if fm.get("type", "meeting") != "meeting":
        add(at["type"], "FAIL", f"type should be meeting, not {fm['type']}")
    if day and not meeting:
        add(at["date"], "FAIL", f"date should be YYYY-MM-DD, not {day}")
    brain = find_up(path, "brain/RESOLVER.md")
    if acct and brain and not (brain.parent / "knowledge" / "accounts" / f"{acct}.md").is_file():
        add(at["account"], "WARN", f"no account page knowledge/accounts/{acct}.md: check the slug")
    name = re.fullmatch(r"(\d{4}-\d\d-\d\d)-([a-z0-9-]+)\.md", path.name)
    if not (name and name[1] == day and (name[2] + "-").startswith(acct + "-")):
        add(0, "FAIL", f"file name should be {day if meeting else 'YYYY-MM-DD'}-{acct or '<account>'}-<meeting>.md (RESOLVER 4)")

    # Sections, in template order; 3 to 6 summary bullets
    body, sec, head, cur = list(enumerate(lines, 1))[end + 1 if end else 0:], {}, {}, None
    for i, l in body:
        if l.startswith("## "):
            title = l[3:].strip()
            cur = next((s for s in SECTIONS if s.lower() == title.lower()), None)
            if cur:
                sec[cur], head[cur] = [], i
            else:
                add(i, "WARN", f'"{title}" is not a template section ({", ".join(SECTIONS)})')
        elif cur:
            sec[cur].append((i, l))
    if missing := [s for s in SECTIONS if s not in sec]:
        add(0, "FAIL", "missing sections: " + ", ".join(missing) + " (RESOLVER template)")
    if list(sec) != [s for s in SECTIONS if s in sec]:
        add(0, "FAIL", "sections out of order, should be: " + " > ".join(SECTIONS))
    if "Summary" in sec and not 3 <= (n := sum(bool(re.match(r"[-*+] \S", l)) for _, l in sec["Summary"])) <= 6:
        add(head["Summary"], "FAIL", f"Summary has {n} bullets, needs 3 to 6")

    # GMV line under the title: the sheet's figure and date, or "under review" with no figure if the call disagreed
    gmv_at = 0
    top = next(((i, l.strip()) for i, l in body if l.strip() and not l.startswith("# ")), (0, ""))
    conflict = any(GMV_CONFLICT.search(l) for _, l in sec.get("Flags for a person", []))
    if not (m := GMV_LINE.match(top[1])):
        add(top[0], "WARN", "no GMV line under the title (RESOLVER template since 2026-10-07)")
    else:
        gmv_at, rest = top[0], m[1]
        sheet = brain.parent / "knowledge" / "reference" / "accounts-sheet.csv" if brain else None
        sheet_rows = csv.DictReader(read(sheet)) if sheet and sheet.is_file() else []
        row = next((r for r in sheet_rows if r["account"] == acct), None)
        if "accounts-sheet.csv" not in rest or f"`{acct}`" not in rest:
            add(gmv_at, "FAIL", f"GMV line must link the accounts sheet, row `{acct}`")
        if rest.lower().startswith("under review"):
            if AMOUNT.search(NOT_AMOUNT.sub(" ", rest)):
                add(gmv_at, "FAIL", "GMV under review: no figure, not the sheet's or the call's")
            if not conflict:
                add(gmv_at, "WARN", "GMV under review, but Flags for a person has no GMV conflict")
        elif conflict:
            add(gmv_at, "FAIL", "Flags has a GMV conflict: the GMV line should say 'under review', with no figure")
        elif not row:
            add(gmv_at, "WARN", f"can't check the GMV figure: no accounts sheet row for {acct or 'this account'}")
        else:
            fig = re.match(r"\$([\d,]+) ", rest)
            upd = re.search(r"updated (\d{4}-\d\d-\d\d)", rest)
            if not fig or fig[1].replace(",", "") != row["gmv_last_30d_usd"]:
                add(gmv_at, "FAIL", f"GMV figure must be the sheet's: ${int(row['gmv_last_30d_usd']):,}")
            if not upd or upd[1] != row["sheet_updated"]:
                add(gmv_at, "FAIL", f"GMV line must say the sheet's date: updated {row['sheet_updated']}")

    # Action items: a table, one named owner and a YYYY-MM-DD due date per row
    rows = [(i, [LINK.sub(r"\1", c).strip("*_` ") for c in l.strip().strip("|").split("|")])  # [Name](link) -> Name
            for i, l in sec.get("Action items", []) if l.strip().startswith("|")]
    rows = [(i, r) for i, r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]  # drop the |---| row
    col = {c.lower(): k for k, c in enumerate(rows[0][1])} if rows else {}
    table = {"owner", "due"} <= col.keys()
    if "Action items" in sec and not table:
        add(head["Action items"], "FAIL", "action items need a table: | Owner | Action | Due |")
    elif "Action items" in sec and len(rows) < 2:
        add(head["Action items"], "FAIL", "no action items: a recap needs at least one, with owner and due date")
    for i, r in rows[1:] if table else []:
        owner, due = (r[col[k]] if col[k] < len(r) else "" for k in ("owner", "due"))
        if owner.lower() in VAGUE_OWNERS:
            add(i, "FAIL", f"no named owner ('{owner}'): if the call didn't name one, move it to Open questions")
        elif re.search(r",|&|/|\+|\band\b", owner):
            add(i, "FAIL", f"one owner per action item, not '{owner}'")
        elif attendees and owner.lower() not in attendees:
            add(i, "WARN", f"owner '{owner}' is not in attendees")
        if not iso(due):
            add(i, "FAIL", f"due '{due}' is not a YYYY-MM-DD date: if the call didn't set one, move it to Open questions")
        elif meeting and iso(due) < meeting:
            add(i, "WARN", f"due {due} is before the meeting ({day})")

    # Every line: SANITIZER wording, typed performance numbers, broken links, side talk copied from the transcript
    if not transcript and re.search(r"[/\\]|\.md$", src):
        transcript = find_up(path, src)
    side = side_talk(transcript) if transcript else []
    for i, l in body:
        for level, rx, why in RULES:
            hits = dict.fromkeys(m[0] for m in rx.finditer(l))
            if hits:  # no exemption for "held back" notes: saying when or where it was said is a hint too
                add(i, level, f"{why}: " + ", ".join(f'"{h}"' for h in hits))
        for s in re.split(r"(?<=[.!?;])\s+", l) if i != gmv_at else []:  # the GMV line is checked above
            if METRIC.search(s) and not TARGET.search(s) and AMOUNT.search(NOT_AMOUNT.sub(" ", s)):
                quote = textwrap.shorten(s.strip(" -*|"), 70, placeholder="...")
                add(i, "FAIL", f'performance number typed in, link the accounts sheet (RESOLVER 5): "{quote}"')
        for _, t in LINK.findall(l):
            if not re.match(r"[a-z]+:|#", t) and not (path.parent / t.split("#")[0]).exists():
                add(i, "FAIL", f"broken link: {t}")
        for j, private in side:
            if hit := next((g for g in grams(l) if g in private), None):
                add(i, "FAIL", f'repeats side talk from after the client left ({transcript.name} line {j}): "{hit}"')
                break
    return issues, transcript


def main():
    ap = argparse.ArgumentParser(description="Check meeting recaps against the brain's rules before posting.")
    ap.add_argument("paths", nargs="+", type=Path, help="recap .md files, or folders of them")
    ap.add_argument("--source", type=Path, help="transcript to check one recap against for leaked side talk "
                                                "(default: the file in the recap's source: field, if it exists)")
    args = ap.parse_args()
    files = [f for p in args.paths for f in (sorted(p.glob("*.md")) if p.is_dir() else [p])]
    if not files:
        ap.error("no recap files found")
    if args.source and (len(files) != 1 or not args.source.is_file()):
        ap.error("--source takes one existing transcript and exactly one recap")
    sys.stdout.reconfigure(errors="replace")
    count = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for f in files:
        issues, transcript = check(f, args.source) if f.is_file() else ([(0, "FAIL", "file not found")], None)
        verdict = "FAIL" if any(level == "FAIL" for _, level, _ in issues) else "WARN" if issues else "PASS"
        count[verdict] += 1
        print(f"{verdict}  {f.as_posix()}" + (f"  (side talk checked against {transcript.name})" if transcript else ""))
        for line, level, why in sorted(issues, key=lambda x: (x[0], x[1] != "FAIL")):
            print(f"  {f'line {line}' if line else 'file':<8} {level}  {why}")
    print(f"\n{len(files)} file(s): " + ", ".join(f"{n} {k}" for k, n in count.items()))
    return 1 if count["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())

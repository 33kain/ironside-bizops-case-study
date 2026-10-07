# Ironside Biz Ops case study: working rules

This repo is the Brightline demo brain (fictional) plus my answers. Answers sit at the root; `README.md` maps each question to its file.

- Before any write into `brain/`, read `brain/RESOLVER.md` and `brain/SANITIZER.md`. Brain pages are read by the people and brands they name.
- Recaps: follow `workers/skills/skill-recap.md`, then run `python extra/check_recap.py <file>` and fix every FAIL before calling it done.
- Never edit people pages, account pages or `brain/knowledge/reference/`. Add proposed edits to `proposed-changes.md` for a pod lead to approve.
- Never type a performance number (GMV, ad spend, active or new affiliates, retention) on a brain page, except a recap's GMV line, copied from the sheet (RESOLVER template). Link the sheet; flag conflicts.
- Pod numbers come from `python analysis/pod_numbers.py` and `python analysis/block_b_extra.py` (both read `calls.csv`). Don't count rows by eye.
- Resolve relative dates ("by Friday") from the call date to YYYY-MM-DD. Never invent an owner or a due date.
- Keep answers short and plain. English for everything in this repo.

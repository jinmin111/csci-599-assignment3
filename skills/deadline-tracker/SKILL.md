---
name: deadline-tracker
description: Track assignment and project deadlines in a small JSON file - add, list, see what is due soon, mark done.
version: 1.0.0
author: CSCI 599 A3 student
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [productivity, deadlines, planning, reminders]
---

# Deadline Tracker

Keep a short list of deadlines and answer "what is due soon?". Use it when the user mentions a
due date, asks what is coming up, or when you compose a daily briefing or an end-of-day recap.

## How to run it

If a tool named `deadlines` is available, call that tool (it offers the same actions).
Otherwise run the bundled script with the terminal tool:

```bash
python ${HERMES_SKILL_DIR}/scripts/deadlines.py add "A3 report" 2026-11-14 --note "submit on Brightspace"
python ${HERMES_SKILL_DIR}/scripts/deadlines.py list
python ${HERMES_SKILL_DIR}/scripts/deadlines.py due --days 7
python ${HERMES_SKILL_DIR}/scripts/deadlines.py done 1
python ${HERMES_SKILL_DIR}/scripts/deadlines.py remove 1
```

The script `scripts/deadlines.py` uses only the Python standard library. It stores its data in
`$DEADLINES_FILE`, or in `$HERMES_HOME/deadlines.json` when that variable is not set.
Every command prints JSON. Each item has `id`, `title`, `due`, `days_left` and `status`.

## Procedure

1. Dates must be `YYYY-MM-DD`. Turn relative dates ("next Friday") into a real date first.
2. After `add`, confirm the title, the date and how many days are left.
3. For "what is due?", run `due --days 7` and list the items by date, overdue ones first.
4. In a briefing, mention only items with `days_left` of 3 or less, one line each.
5. Never invent a deadline. If the list is empty, say so.

## Pitfalls

- `done` and `remove` need the numeric `id` shown by `list`, not the title.
- An item due today has `days_left` 0 and status `due today`; a negative value means overdue.

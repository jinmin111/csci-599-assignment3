#!/usr/bin/env python3
"""deadline-tracker: a small deadline list kept in one JSON file (standard library only).

Commands:
  deadlines.py add "<title>" <YYYY-MM-DD> [--note "..."]
  deadlines.py list [--all]
  deadlines.py due [--days N]
  deadlines.py done <id>
  deadlines.py remove <id>

The file is $DEADLINES_FILE, else $HERMES_HOME/deadlines.json, else ~/.hermes/deadlines.json.
Every command prints JSON so an agent can read the result reliably.
"""
import argparse
import json
import os
import sys
import tempfile
from datetime import date, datetime


def store_path():
    chosen = os.environ.get("DEADLINES_FILE")
    if chosen:
        return chosen
    home = os.environ.get("HERMES_HOME") or os.path.join(os.path.expanduser("~"), ".hermes")
    return os.path.join(home, "deadlines.json")


def load():
    try:
        with open(store_path(), encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"next_id": 1, "items": []}


def save(data):
    """Write to a temporary file, then rename: a crash never leaves a half-written file."""
    path = store_path()
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=folder, prefix=".deadlines-")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(temp, path)


def describe(item, today=None):
    """Add days_left and a readable status to a stored item."""
    today = today or date.today()
    left = (datetime.strptime(item["due"], "%Y-%m-%d").date() - today).days
    if item.get("done"):
        status = "done"
    elif left < 0:
        status = "overdue"
    elif left == 0:
        status = "due today"
    else:
        status = f"in {left} day" + ("" if left == 1 else "s")
    return dict(item, days_left=left, status=status)


def add(title, due, note=""):
    datetime.strptime(due, "%Y-%m-%d")          # raises ValueError for a bad date
    if not title.strip():
        raise ValueError("title is empty")
    data = load()
    for existing in data["items"]:
        # The same open deadline again (an agent repeating a command): report it, do not duplicate it.
        if (not existing.get("done") and existing["due"] == due
                and existing["title"].strip().lower() == title.strip().lower()):
            return dict(describe(existing), already_exists=True)
    item = {"id": data["next_id"], "title": title.strip(), "due": due, "note": note, "done": False}
    data["items"].append(item)
    data["next_id"] += 1
    save(data)
    return describe(item)


def list_items(include_done=False):
    items = [describe(item) for item in load()["items"] if include_done or not item.get("done")]
    return sorted(items, key=lambda item: item["due"])


def due_within(days=3):
    """Open items due within `days` days, overdue ones included."""
    return [item for item in list_items() if item["days_left"] <= int(days)]


def mark_done(item_id):
    data = load()
    for item in data["items"]:
        if item["id"] == int(item_id):
            item["done"] = True
            save(data)
            return describe(item)
    raise KeyError(f"no deadline with id {item_id}")


def remove(item_id):
    data = load()
    remaining = [item for item in data["items"] if item["id"] != int(item_id)]
    if len(remaining) == len(data["items"]):
        raise KeyError(f"no deadline with id {item_id}")
    data["items"] = remaining
    save(data)
    return {"removed": int(item_id)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="deadlines.py", description="Track deadlines in a JSON file.")
    commands = parser.add_subparsers(dest="command", required=True)
    add_cmd = commands.add_parser("add")
    add_cmd.add_argument("title")
    add_cmd.add_argument("due")
    add_cmd.add_argument("--note", default="")
    commands.add_parser("list").add_argument("--all", action="store_true")
    commands.add_parser("due").add_argument("--days", type=int, default=3)
    commands.add_parser("done").add_argument("id", type=int)
    commands.add_parser("remove").add_argument("id", type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            result = add(args.title, args.due, args.note)
        elif args.command == "list":
            result = list_items(args.all)
        elif args.command == "due":
            result = due_within(args.days)
        elif args.command == "done":
            result = mark_done(args.id)
        else:
            result = remove(args.id)
    except (KeyError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

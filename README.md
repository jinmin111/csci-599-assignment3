# CSCI 599 Assignment 3 — personal assistant

A course project: an always-on personal assistant that runs on Google Cloud Run and answers
over Telegram. It routes each request to a cloud language model or to a local model on the
owner's laptop, and it can read a calendar, read mail, prepare mail drafts and keep track of
deadlines.

The assistant is used by one person with one dedicated test Google account that holds only
made-up data. It is not offered to the public.

- [Privacy policy](PRIVACY.md)

## Hermes skill tap: `deadline-tracker`

This repository is a Hermes skill tap. It publishes one skill written for the project:

- [`skills/deadline-tracker`](skills/deadline-tracker/SKILL.md) — keep a short list of assignment and
  project deadlines in one JSON file: add, list, see what is due soon, mark done. The helper script
  uses only the Python standard library and needs no credentials.

Install it with the Hermes skill hub (tested with Hermes Agent v0.22.7):

```bash
hermes skills tap add jinmin111/csci-599-assignment3
hermes skills install jinmin111/csci-599-assignment3/deadline-tracker
```

The published version is tagged `v1.0.1`. It passes Hermes's install-time security scan with the verdict
`safe`, so no `--force` is needed. (`v1.0.0` read one environment variable in a way the scanner flags
and was blocked on a fresh install; `v1.0.1` changes that line only.)

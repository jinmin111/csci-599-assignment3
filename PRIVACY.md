# Privacy policy

Last updated: 2026-11-10

This policy covers the personal assistant built for CSCI 599 Assignment 3 ("the app").
The app is a course project. It is used by its owner only, with one dedicated test Google
account that holds made-up data. Nobody else can sign in to it.

## What the app accesses

With the account owner's consent the app uses two Gmail permissions:

- `gmail.readonly` — list and read messages in the test mailbox.
- `gmail.compose` — create drafts. Sending a draft happens only after the owner approves
  that one message in the chat; the app never sends mail on its own.

The app does not access contacts, files, or any other Google data.

## How the data is used

Mail is read only to answer the owner's requests: summaries of unread mail, a morning
briefing, an end-of-day recap, and drafts of replies.

To write those answers, the text of the messages involved is processed by a language model:
a model on the owner's own laptop, or a cloud model provided by OpenAI. Requests the owner
marks as private are handled by the laptop model only. Apart from this processing, mail data
is not shared with anyone, is not sold, and is not used for advertising or for training models
by the app.

## What is stored

- The Gmail sign-in token is kept in Google Secret Manager in the owner's Google Cloud project.
- The assistant's conversation history, which can contain parts of messages it has read, is
  kept in a private storage bucket in the same project.
- Operational logs record which model answered and how long it took. They do not contain
  message text.

## Removing access and data

The account owner can remove the app's access at any time at
<https://myaccount.google.com/permissions>. The stored history and the sign-in token are
deleted when the course project ends.

## Contact

Questions: open an issue in this repository.

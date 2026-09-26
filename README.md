# claude2tech-lead

A Claude Code plugin that turns the main session into a tech lead. You discuss the product
with it; it decides the architecture, builds the base, and hands the code to persistent
worker subagents — one per part of the project — while it tests, reviews and steers.

Why: when one AI discusses design and also writes every line, its context fills with code
and logs and quality drops after the first batch. Here the lead keeps the whole project in
its head and spends that context on decisions; workers carry the code.

## How it works

- **lead** — the main session (`--agent`). Talks to you in your language, asks what matters,
  picks the simplest architecture, writes briefs, runs the fix loop. Its system prompt fully
  replaces Claude Code's default one.
- **fork** — a copy of the lead's context. Builds the base, runs and tests parts (Playwright
  for UI), reviews with fixed verdicts (OK / MINOR / REWORK / REJECT), makes small fixes.
- **worker** — writes and fixes code in its own folders only, runs type checks and
  compilation, commits its own files. Named per part (`sync-1c-01`); every later task for
  that part goes to the same worker via SendMessage. Up to 3 in parallel. Retired around
  250k tokens.
- Agents talk to each other in English; long notes go to `/tmp/tech-lead/<project>/`.
- No spec documents: the code is the documentation, plus a short block-structured
  `CLAUDE.md` in each project.

## Install

Requires Claude Code and Node.js (for the Playwright MCP server).

```sh
git clone https://github.com/eduard256/claude2tech-lead ~/Projects/claude2tech-lead
ln -s ~/Projects/claude2tech-lead/launcher/aa ~/.local/bin/aa
```

Then run `aa` in any project directory. Arguments pass through to `claude`
(`aa --model fable`, `aa --resume`).

The launcher loads the plugin only for that session, so your normal `claude` sessions don't
change.

## What `aa` sets

- permission mode `auto`;
- auto-compaction off (`DISABLE_AUTO_COMPACT`) — you watch the lead's context yourself;
- fork subagents on;
- `git push` and `git reset --hard` denied; reading or editing `.env` files asks first;
- Playwright MCP server from the plugin.

See `settings/aa-settings.json`.

## Status

Experimental.

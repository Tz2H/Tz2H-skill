# Tz2H-skill

> "Attendance is optional. Also, missing attendance will zero out your
> participation grade."

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/env-uv-2E7BFF)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/lint%20%2B%20format-Ruff-46A758)](https://docs.astral.sh/ruff/)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

Tz2H-skill is a pedant-first fork of
[titanwings/colleague-skill](https://github.com/titanwings/colleague-skill).
The upstream project distilled colleagues into reusable work/persona skills.
This fork keeps that useful engine, trims the repo down for local development,
and adds `pedant`: a new family for undergraduate teaching-power cases.

`pedant` is for situations where classroom language and institutional power do
not match: optional-but-punished attendance, "growth opportunities" that look
like unpaid labor, vague grading threats, moralized compliance, authorship
erasure, and responsibility pushed onto students who cannot safely refuse.

It turns course notes, chat excerpts, assignment requirements, emails, and
subjective descriptions into a reusable Agent Skill that can analyze behavior,
decode rhetoric, assess evidence, and draft risk-aware responses.

The original `colleague`, `relationship`, and `celebrity` flows remain available
as secondary families.

[Supported Sources](#supported-material-sources) ·
[Install](#install) ·
[Usage](#usage) ·
[Demo](#demo) ·
[Features](#features) ·
[Privacy](#imap-email-privacy-rules) ·
[Project Structure](#project-structure)

---

## Supported Material Sources

`pedant` works best when source material preserves the gap between what a
teaching authority says and what the student is structurally pressured to do.
Good inputs include course announcements, grading rules, assignment text, chat
logs, emails, meeting notes, and the student's own timeline.

| Source | Messages | Docs / Wiki | Spreadsheets | Notes |
| --- | :---: | :---: | :---: | --- |
| Feishu auto collection | Yes | Yes | Yes | App credentials required |
| Feishu browser collection | Partial | Yes | Yes | Reuses local browser login state |
| Feishu MCP collection | No | Yes | Partial | Requires `feishu-mcp` |
| DingTalk auto collection | Partial | Yes | Yes | Message history depends on browser flow |
| Slack auto collection | Yes | No | No | Bot token and workspace permissions required |
| IMAP email collection | Yes | No | No | Privacy-gated, see rules below |
| Email `.eml` / `.mbox` parsing | Yes | No | No | Local files only |
| PDF / images / screenshots | Partial | Yes | No | Manual upload or paste |
| Markdown / direct paste | Yes | Yes | No | Lowest setup cost |

---

## Install

### Requirements

- Python 3.13+
- `uv`
- Optional: Node.js 16+, only for Feishu MCP
- Optional: Playwright Chromium, only for browser-based collection

Install the base environment:

```bash
uv sync
```

Install the full development environment and optional collectors:

```bash
uv sync --all-extras --dev
uv run playwright install chromium
npm install -g feishu-mcp
```

### Supported hosts

The whole repository is the Agent Skill directory. The entrypoint is `SKILL.md`.

Supported hosts:

| Host | Install |
| --- | --- |
| Claude Code | `git clone <this-repo-url> .claude/skills/Tz2H-skill` |
| OpenClaw | `uv run python tools/install_openclaw_skill.py --force` |
| Hermes | `uv run python tools/install_hermes_skill.py --force` |
| Codex | `uv run python tools/install_codex_skill.py --force` |

Manual host paths:

```bash
mkdir -p .claude/skills
git clone <this-repo-url> .claude/skills/Tz2H-skill

git clone <this-repo-url> ~/.claude/skills/Tz2H-skill
git clone <this-repo-url> ~/.openclaw/workspace/skills/Tz2H-skill
git clone <this-repo-url> ~/.codex/skills/Tz2H-skill
```

In slash-command hosts, launch the root skill with:

```text
/Tz2H-skill
```

Codex discovers `Tz2H-skill` as a local skill name instead of relying on a
fixed slash command.

---

## Usage

Start the root skill:

```text
/Tz2H-skill
```

For the main fork-specific workflow, choose `pedant`.

### Pedant Workflow

`pedant` is not a teacher impersonation mode. It is an analyst for teaching
power, rhetoric, evidence, and safe response planning.

The intake asks for:

1. A case slug or codename.
2. The teaching relationship and power structure.
3. Specific behavior, wording, timeline, evidence, and impact.
4. The user's goal and risk boundary.

Typical outputs:

- Power-structure analysis: grades, graduation, recommendation, authorship,
  lab access, or other leverage.
- Behavior classification: moralized exploitation, vague threats, boundary
  crossing, responsibility shifting, promise ambiguity, or credit erasure.
- Rhetoric decoding: what phrases like "for your growth", "attitude matters",
  or "everyone does this" accomplish in context.
- Evidence map: facts, reasonable inferences, emotional judgments, and missing
  proof.
- Response drafts: low-conflict messages, firm boundary requests, complaint
  outlines, or private self-protection plans.

`pedant` should criticize behavior, structure, and rhetoric. It should not
doxx, harass, threaten, or make unsupported personal accusations.

### Other Families

The upstream-style families are still available:

| Family | Use case | Storage root |
| --- | --- | --- |
| `pedant` | Teaching-power behavior, moralized exploitation, rhetoric analysis | `./skills/pedant` |
| `colleague` | Coworkers, mentors, collaborators, work-context figures | `./skills/colleague` |
| `relationship` | Friends, partners, family members, personal relationships | `./skills/relationship` |
| `celebrity` | Public figures, writers, creators, fictional characters | `./skills/celebrity` |

Non-pedant flows usually ask for:

1. A slug or alias.
2. Basic profile information.
3. Subjective personality, behavior, or rhetoric notes.
4. Source material.

Most fields can be skipped. A manual description alone can generate a rough
Skill; better source material gives better behavioral fidelity.

Generated files are written to:

```text
./skills/{character}/{slug}/
```

Install a generated Skill into a host:

```bash
uv run python tools/install_claude_generated_skill.py --skill-dir skills/{character}/{slug} --force
uv run python tools/install_openclaw_generated_skill.py --skill-dir skills/{character}/{slug} --force
uv run python tools/install_codex_generated_skill.py --skill-dir skills/{character}/{slug} --force
```

Generated slash command:

```text
/{character}-{slug}
```

Codex skill name:

```text
{character}-{slug}
```

---

## Commands

| Command | Description |
| --- | --- |
| `/Tz2H-skill` | Root creator skill |
| `/{character}-{slug}` | Invoke generated combined Skill |
| `/{character}-{slug}-work` | Invoke work module only, where available |
| `/{character}-{slug}-persona` | Invoke persona module only |
| `uv run python tools/skill_writer.py --action list --base-dir ./skills/colleague` | List colleague Skills |
| `uv run python tools/skill_writer.py --action list --base-dir ./skills/relationship` | List relationship Skills |
| `uv run python tools/skill_writer.py --action list --base-dir ./skills/celebrity` | List celebrity Skills |
| `uv run python tools/skill_writer.py --action list --base-dir ./skills/pedant` | List pedant Skills |
| `uv run python tools/version_manager.py --action rollback --skill-dir ./skills/{character}/{slug}` | Roll back a generated Skill |

Useful help commands:

```bash
uv run python tools/feishu_parser.py --help
uv run python tools/email_parser.py --help
uv run python tools/collect_email_imap.py --help
uv run python tools/slack_auto_collector.py --help
uv run python tools/research/quality_check.py --help
```

---

## Demo

### Pedant

Input:

```text
Undergraduate teaching-power case notes, chat excerpts, assignments, and rhetoric samples
```

Expected flavor:

```text
User    > Why does this feedback feel so hard to argue with?
pedant  > Because it frames obedience as maturity, then treats disagreement as proof
          that the student has not yet earned interpretive authority.
```

### Pedant: Response Planning

Input:

```text
The teacher says the project is voluntary, but later says students who did not join
"lack initiative" and may not receive recommendation support.
```

Expected flavor:

```text
pedant  > The problem is not the word "voluntary"; it is the hidden penalty.
          Ask for written clarification: whether non-participation affects grades,
          recommendations, lab access, or future opportunities.
```

### Colleague

Input:

```text
ByteDance 2-1 backend engineer, INTJ, direct reviewer, CR is strict but terse
```

Expected flavor:

```text
User       > Can you review this API design?
colleague  > Context first. What's the impact and rollback plan?
             Also, this has an N+1 query. Fix that before discussing naming.
```

### Celebrity

Input:

```text
Interviews, essays, talks, public decisions, and third-party criticism
```

Expected flavor:

```text
User       > What would they say about AI agents?
celebrity  > The question is not whether the demo is impressive.
             The question is whether the evaluation loop survives contact with reality.
```

---

## Features

### Generated Skill structure

| Family | Core output | Extra modules |
| --- | --- | --- |
| `pedant` | Pedant Analyst Persona | Behavior analysis, rhetoric analysis, response shaping |
| `colleague` | Persona + Work Skill | Work standards, code review habits, workflows |
| `relationship` | Relationship Persona | Emotional rhythm, conflict, repair, silence patterns |
| `celebrity` | Public Persona | Research notes, timeline, source-grounding checks |

Execution model:

```text
source material -> analyzer prompts -> builder prompts -> generated Skill -> host install
```

### Pedant Safety Boundary

`pedant` is designed to be sharp without becoming reckless:

- It separates facts, inferences, emotional judgments, and missing evidence.
- It analyzes power asymmetry rather than pretending every classroom conflict is
  a symmetric disagreement.
- It can name exploitation, coercion, responsibility shifting, or rhetorical
  laundering when the material supports that judgment.
- It refuses doxxing, harassment, threats, revenge instructions, and unsupported
  claims about a named person's character or legality.
- It treats public sharing, complaint drafts, and saved emails as privacy- and
  retaliation-risk surfaces.

### Evolution

- Append new files, then merge only the delta.
- Correct behavior in conversation, then write durable correction rules.
- Archive versions automatically and roll back when needed.
- Run celebrity research checks before trusting public-figure synthesis.

### Celebrity research tools

```bash
uv run bash tools/research/download_subtitles.sh "<video-url>" "./tmp/subtitles"
uv run python tools/research/srt_to_transcript.py "./tmp/subtitles/example.srt"
uv run python tools/research/merge_research.py "./skills/celebrity/{slug}"
uv run python tools/research/quality_check.py "./skills/celebrity/{slug}/SKILL.md"
```

---

## IMAP Email Privacy Rules

If an AI agent wants to use `tools/collect_email_imap.py`, the user must provide
or explicitly confirm the following information.

| Information | Purpose | Privacy level |
| --- | --- | --- |
| IMAP server, for example `imap.gmail.com` | Connect to the mailbox provider | Not sensitive |
| Mailbox name, for example `INBOX` | Select the mailbox to fetch from | Potentially sensitive |
| Fetch limit, `--limit` | Bound the collection scope | Not sensitive |
| Output directory, `--output` | Store collected `.eml` files | Potentially sensitive |
| Email account, `--email` | Log in to IMAP | Privacy-sensitive |
| App password or password environment variable | Log in to IMAP | Highly sensitive |
| Sender filter, `--from` | Collect mail from a specific sender | Privacy-sensitive |
| Permission to save `.eml` files | Confirm raw email can be written locally | Highly sensitive |

Prefer `--password-env` over `--password`. Do not put passwords in commands,
scripts, or committed files.

Local model example:

```bash
uv run python tools/collect_email_imap.py \
  --server imap.gmail.com \
  --email your_email@gmail.com \
  --password-env GMAIL_APP_PASSWORD \
  --model-context local \
  --limit 50 \
  --output collected_emails
```

Online model example after platform privacy approval:

```bash
uv run python tools/collect_email_imap.py \
  --server imap.gmail.com \
  --email your_email@gmail.com \
  --password-env GMAIL_APP_PASSWORD \
  --from someone@example.com \
  --privacy-approved \
  --limit 50 \
  --output collected_emails
```

---

## Project Structure

This project follows the AgentSkills-style layout: the repository itself is the
root skill.

```text
Tz2H-skill/
|-- SKILL.md                 # Root Skill entrypoint
|-- README.md                # Project usage guide
|-- prompts/                 # Family prompt templates
|   |-- colleague/           # Colleague intake, analyzers, builders
|   |-- relationship/        # Relationship persona prompts
|   |-- celebrity/           # Public-figure research and persona prompts
|   `-- pedant/              # Teaching-power behavior and rhetoric prompts
|-- references/              # Celebrity deep-research references
|-- skills/                  # Example and generated Skills
|-- tools/                   # Installers, collectors, parsers, version tools
|-- tests/                   # Unit tests
|-- docs/agents/             # Local agent operating notes
|-- pyproject.toml           # uv environment and Ruff configuration
|-- uv.lock                  # uv lockfile
`-- LICENSE
```

---

## Notes

- Source material quality is Skill quality.
- Long-form writing by the target beats summaries about the target.
- Keep raw private materials local unless the user explicitly approves sharing.
- `uv sync --all-extras --dev` is the canonical development setup.
- This repo intentionally does not carry upstream community, roadmap, or
  multilingual README material.

---

## Local Verification

```bash
uv run ruff check .
uv run ruff format --check .
uv run python -m compileall tools
uv run python -m unittest discover -s tests -p 'test_*.py' -v
```

MIT License. Upstream lineage: [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill).

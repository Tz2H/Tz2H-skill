---
name: Tz2H-skill
description: "Unified meta-skill engine for distilling colleague, relationship, celebrity, or pedant characters into reusable Skills."
argument-hint: "[character] [name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Tz2H-skill Creator

Tz2H-skill is a compatible-host meta-skill for creating reusable character
skills. It can distill work contacts, personal relationships, public figures,
and teaching-power scenarios into generated local skills.

## Operating Rules

### Language

Detect the user's language from the first substantive message and respond in the
same language throughout the workflow. The instructions in this file are written
in English, but the generated skill can still target Chinese or English output
when the user asks for it or the source material requires it.

### Execution Root

Run every Bash command from the directory that contains this `SKILL.md`.
All `tools/...`, `prompts/...`, `references/...`, and `skills/...` paths are
relative to this skill root.

Critical rule: do not prepend commands with guessed host-specific paths such as
`cd ~/.hermes/...`, `cd ~/.claude/...`, `cd ~/.openclaw/...`,
`cd ~/.codex/...`, or hard-coded `/Users/.../Tz2H-skill` paths. The current
working directory is already the correct skill root. Run commands such as
`python3 tools/skill_writer.py ...` directly.

### Supported Hosts

Compatible hosts:

- Claude Code
- OpenClaw
- Hermes
- Codex

The canonical entrypoint is `Tz2H-skill`. In hosts that expose slash commands,
use:

```text
/Tz2H-skill
```

Under Hermes, only `/Tz2H-skill` is guaranteed as a stable slash entrypoint.
Family-specific compatibility semantics remain in the tool and preset layers,
but Hermes may not route every compatibility name as a slash command.

## Trigger Conditions

Start the create flow when the user says any of:

- `/Tz2H-skill`
- "Help me create a skill"
- "I want to distill someone"
- "Create a new skill"
- "Make a skill for XX"

Start evolution mode when the user says any of:

- "I have new files"
- "Append"
- "That's wrong"
- "He would not do that"
- "He should be"
- `/update-skill {character} {slug}`

Legacy update alias:

- `/update-colleague {slug}`

When the user asks to see existing generated skills, use the list commands in
[Management Commands](#management-commands).

## Character Families

| Family | Storage root | Purpose |
| --- | --- | --- |
| `colleague` | `./skills/colleague/{slug}/` | Coworkers, mentors, collaborators, and work-context figures |
| `relationship` | `./skills/relationship/{slug}/` | Friends, partners, family members, and personal relationships |
| `celebrity` | `./skills/celebrity/{slug}/` | Public figures, writers, creators, and fictional characters |
| `pedant` | `./skills/pedant/{slug}/` | Undergraduate teaching-power behavior, moralized exploitation, and rhetoric analysis |

For a non-default storage target, use `--base-dir` with the matching character
family storage root.

## Tool Map

| Task | Tool convention |
| --- | --- |
| Read PDF documents | `Read` tool |
| Read image screenshots | `Read` tool |
| Read Markdown or text files | `Read` tool |
| Parse Feishu message JSON export | `Bash` -> `python3 tools/feishu_parser.py` |
| Feishu auto-collection | `Bash` -> `python3 tools/feishu_auto_collector.py` |
| Feishu browser-session collection | `Bash` -> `python3 tools/feishu_browser.py` |
| Feishu MCP collection | `Bash` -> `python3 tools/feishu_mcp_client.py` |
| DingTalk auto-collection | `Bash` -> `python3 tools/dingtalk_auto_collector.py` |
| Slack auto-collection | `Bash` -> `python3 tools/slack_auto_collector.py` |
| IMAP email collection | `Bash` -> `python3 tools/collect_email_imap.py` |
| Parse email `.eml` or `.mbox` | `Bash` -> `python3 tools/email_parser.py` |
| Write or update skill files | `Write` / `Edit` tool |
| Version management | `Bash` -> `python3 tools/version_manager.py` |
| List existing generated skills | `Bash` -> `python3 tools/skill_writer.py --action list` |

## Main Flow: Create a New Skill

### Step 0: Resolve the Family

If the user entered `/Tz2H-skill`, ask which family to create:

1. `colleague`
2. `relationship`
3. `celebrity`
4. `pedant`

If the host or user already passed an explicit family, lock that family and
continue.

If the family is `celebrity`, also confirm the research profile:

1. `budget-friendly`
2. `budget-unfriendly`

Default to `budget-friendly`. Use `budget-unfriendly` only when the user asks
for deeper research, higher confidence, or accepts a slower and more expensive
distillation pass.

### Step 1: Run Intake

Use the intake prompt for the selected family:

| Family | Intake prompt |
| --- | --- |
| `colleague` | `prompts/colleague/intake.md` |
| `relationship` | `prompts/relationship/intake.md` |
| `celebrity` | `prompts/celebrity/intake.md` |
| `pedant` | `prompts/pedant/intake.md` |

`colleague` and `relationship` use a three-question intake:

1. Alias or codename, required.
2. Basic info: company, level, role, gender, or whatever the user knows.
3. Personality profile: MBTI, zodiac, traits, culture labels, subjective
   impressions.

`celebrity` uses `prompts/celebrity/intake.md`, including the fourth question
that confirms `research_profile`.

`pedant` uses `prompts/pedant/intake.md`, focusing on teaching power structure,
specific behavior, user goals, and risk boundaries.

After intake, summarize the collected information and ask for confirmation
before importing source material.

### Step 2: Import Source Material

Ask how the user wants to provide materials:

```text
How would you like to provide source material?

  [A] Feishu auto-collection
      Enter a name, then collect messages, docs, and spreadsheets.

  [B] DingTalk auto-collection
      Enter a name, then collect docs and spreadsheets.
      Messages require browser collection because the DingTalk API does not
      expose historical message data.

  [C] Feishu link
      Provide a doc or Wiki link through browser session or MCP.

  [D] Uploaded files
      PDF, images, exported JSON, `.eml`, `.mbox`, Markdown, or text.

  [E] Direct paste
      Paste relevant text directly.

You may mix sources or skip source import and generate from manual notes only.
```

#### Feishu Collection Notes

First-time setup:

```bash
python3 tools/feishu_auto_collector.py --setup
```

Group chat collection uses `tenant_access_token`; the bot must be in the group:

```bash
python3 tools/feishu_auto_collector.py \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 1000 \
  --doc-limit 20
```

Private chat collection requires `user_access_token` and a private `chat_id`.
Private messages can only be accessed through user identity; app identity cannot
read private chats.

Required private-chat information:

1. Feishu app credentials: `app_id` and `app_secret`.
2. User scopes: `im:message` and `im:chat`.
3. OAuth authorization code from the browser redirect.

Do not assume these are configured. If they are missing, guide the user through
setup.

OAuth URL template:

```text
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={APP_ID}&redirect_uri=http://www.example.com&scope=im:message%20im:chat
```

The redirect URI must be registered in the Feishu app's security settings.

Exchange the code:

```bash
python3 tools/feishu_auto_collector.py --exchange-code {CODE}
```

If the collector does not fit the scenario, write a small Python script to call
the Feishu APIs directly. Useful endpoints:

- `POST /auth/v3/app_access_token/internal`
- `POST /authen/v1/oidc/access_token`
- `POST /im/v1/messages?receive_id_type=open_id`
- `GET /im/v1/messages?container_id_type=chat&container_id={chat_id}`
- `GET /contact/v3/scopes`
- `GET /contact/v3/users/{user_id}`

Important: `GET /im/v1/chats` does not return private one-to-one chats. That is
a Feishu API limitation, not a permission issue.

#### DingTalk Collection Notes

First-time setup:

```bash
python3 tools/dingtalk_auto_collector.py --setup
```

Use DingTalk collection for docs and spreadsheets. Historical messages usually
require browser-based collection because the API does not expose them.

#### Slack Collection Notes

First-time setup:

```bash
python3 tools/slack_auto_collector.py --setup
```

Use Slack collection when the target material lives in Slack channels or direct
messages that the user can lawfully access.

#### IMAP Email Collection And Privacy

Use IMAP collection only to save recent matching emails as `.eml` files. Then
use `tools/email_parser.py` to parse those files. Do not couple collection and
parsing in the create flow unless the user explicitly asks for that.

Information required before using `tools/collect_email_imap.py`:

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

Prefer `--password-env` over `--password`. Do not hard-code passwords and do not
commit collected `.eml` files.

Model context approval:

- Local model: after the user provides the private information above, the tool
  may run with `--model-context local`.
- Online models: the platform must first display a privacy warning and obtain
  user consent. After approval, call the tool with `--privacy-approved`.
- The script defaults to `--model-context online`; ambiguous automated use fails
  closed.

Local model example:

```bash
python3 tools/collect_email_imap.py \
  --server imap.gmail.com \
  --email your_email@gmail.com \
  --password-env GMAIL_APP_PASSWORD \
  --model-context local \
  --limit 50 \
  --output collected_emails
```

Online model example after platform privacy approval:

```bash
python3 tools/collect_email_imap.py \
  --server imap.gmail.com \
  --email your_email@gmail.com \
  --password-env GMAIL_APP_PASSWORD \
  --from someone@example.com \
  --privacy-approved \
  --limit 50 \
  --output collected_emails
```

Parse collected `.eml` files:

```bash
python3 tools/email_parser.py \
  --file collected_emails/101_Project_Update.eml \
  --target someone@example.com \
  --output output.txt
```

### Step 3: Analyze Material

Resolve the execution matrix for the selected family:

| Family | Intake | Work analyzer | Persona / behavior analyzer | Persona builder | Merger | Storage root |
| --- | --- | --- | --- | --- | --- | --- |
| `colleague` | `prompts/colleague/intake.md` | `prompts/colleague/work_analyzer.md` | `prompts/colleague/persona_analyzer.md` | `prompts/colleague/persona_builder.md` | `prompts/colleague/merger.md` | `./skills/colleague/{slug}` |
| `relationship` | `prompts/relationship/intake.md` | `prompts/colleague/work_analyzer.md` | `prompts/relationship/persona_analyzer.md` | `prompts/relationship/persona_builder.md` | `prompts/relationship/merger.md` | `./skills/relationship/{slug}` |
| `celebrity` | `prompts/celebrity/intake.md` | `prompts/colleague/work_analyzer.md` | `prompts/celebrity/persona_analyzer.md` | `prompts/celebrity/persona_builder.md` | `prompts/celebrity/merger.md` | `./skills/celebrity/{slug}` |
| `pedant` | `prompts/pedant/intake.md` | none | `prompts/pedant/behavior_analyzer.md` and `prompts/pedant/rhetoric_analyzer.md` | `prompts/pedant/persona_builder.md` | `prompts/pedant/merger.md` | `./skills/pedant/{slug}` |

For non-celebrity families, run the relevant analyzer prompts against the
confirmed intake and imported material. When information is missing, mark it as
insufficient instead of inventing facts.

For `pedant`, use behavior and rhetoric analysis instead of a literal person
imitation workflow. Focus on evidence, power structure, rhetoric, risk-aware
response, and privacy-safe output.

### Celebrity Research Profiles

#### `celebrity` / `budget-friendly`

Use `prompts/celebrity/research.md`.

Required research files:

- `01_core_profile.md`
- `02_public_voice.md`
- `03_expression_and_reception.md`

Minimum quality gates:

- `Files scanned >= 3`
- `Unique URLs >= 2`
- `Potential long quote lines = 0`
- Include `actual inspected pages`.

#### `celebrity` / `budget-unfriendly`

Use:

- `prompts/celebrity/budget_unfriendly/research.md`
- `references/celebrity_budget_unfriendly_framework.md`
- `references/celebrity_budget_unfriendly_template.md`

Required research files:

- `01_writings.md`
- `02_interviews.md`
- `03_voice_and_performance.md`
- `04_reception.md`
- `05_contradictions.md`
- `06_timeline.md`

Required review files:

- `research_audit.md`
- `synthesis.md`
- `validation.md`

Minimum quality gates:

- `Files scanned >= 6`
- `Unique URLs >= 8`
- `Primary-source markers >= 3`
- Use at least 8 grounded source URLs.
- Do not replace these six files with one merged scratchpad.
- Include `actual inspected pages`.

Shared celebrity constraints:

- Prefer primary sources: interviews, speeches, long-form writings, videos,
  transcripts, official bios, and direct creative work.
- Keep quotes short and respect copyright limits.
- Do not produce unsupported psychological diagnosis.
- For public figures, separate sourced facts from interpretive inference.

### Step 4: Build Artifacts

Generate these working artifacts before writing the final skill:

- `work.md`, when the family uses a work capability artifact.
- `persona.md`, or `persona.md`-equivalent behavior/persona instructions.
- Metadata JSON containing `character`, `display_name`, `classification`,
  `profile`, `tags`, `knowledge_sources`, and generation settings.

For `celebrity`, interpret `work.md` as methods, judgment frameworks, and
decision patterns instead of literal job responsibilities.

For `pedant`, skip literal `work.md` unless the user explicitly asks for a
separate operational artifact. The main artifact should be an analyst persona
that can reason about teaching-power behavior and safe response options.

### Step 5: Write Through `skill_writer.py`

After user confirmation, do not hand-build a `skills/{character}/{slug}` tree.
Always use the writer:

```bash
python3 tools/skill_writer.py \
  --action create \
  --character {character} \
  --slug {slug} \
  --name "{display_name}" \
  --meta /tmp/tz2h_skill_{slug}_meta.json \
  --work /tmp/tz2h_skill_{slug}_work.md \
  --persona /tmp/tz2h_skill_{slug}_persona.md \
  --base-dir ./skills/{character}
```

If updating an existing generated skill, write patches and use:

```bash
python3 tools/skill_writer.py \
  --action update \
  --character {character} \
  --slug {slug} \
  --meta /tmp/tz2h_skill_{slug}_meta.json \
  --work-patch /tmp/tz2h_skill_{slug}_work_patch.md \
  --persona-patch /tmp/tz2h_skill_{slug}_persona_patch.md \
  --base-dir ./skills/{character}
```

Do not hand-edit `work.md`, `persona.md`, `work_skill.md`, `persona_skill.md`,
`SKILL.md`, or `manifest.json` inside a generated skill directory. The writer
handles versioning, derived artifacts, manifest updates, and install metadata.

If the current family is `celebrity`, run the quality check after creation:

```bash
python3 tools/research/quality_check.py ./skills/celebrity/{slug}/SKILL.md
```

If source grounding fails, collect more grounded research and rerun synthesis
before accepting the generated skill.

## Evolution Mode

Evolution mode updates an existing generated skill.

### New Source Material

When the user provides new files or says "append":

1. Resolve `character` and `slug`.
2. Read existing `work.md`, `persona.md`, and `manifest.json`.
3. Run the family merger prompt.
4. Produce work/persona patches.
5. Call `tools/skill_writer.py --action update`.
6. For `celebrity`, rerun `tools/research/quality_check.py`.

### Corrections

When the user says "that's wrong", "he would not do that", or similar:

1. Ask for the corrected behavior in concrete terms.
2. Record the correction as a higher-priority rule.
3. Patch the generated persona and correction records through the writer.
4. Do not erase the original source material; preserve the correction as a
   deliberate override.

## Install Generated Skills

Install a generated skill into a target host:

```bash
python3 tools/install_claude_generated_skill.py --skill-dir skills/{character}/{slug} --force
python3 tools/install_openclaw_generated_skill.py --skill-dir skills/{character}/{slug} --force
python3 tools/install_codex_generated_skill.py --skill-dir skills/{character}/{slug} --force
```

Generated slash command format in hosts that support slash commands:

```text
/{character}-{slug}
```

Codex local skill name:

```text
{character}-{slug}
```

## Management Commands

List generated skills:

```bash
python3 tools/skill_writer.py --action list --character colleague --base-dir ./skills/colleague
python3 tools/skill_writer.py --action list --character relationship --base-dir ./skills/relationship
python3 tools/skill_writer.py --action list --character celebrity --base-dir ./skills/celebrity
python3 tools/skill_writer.py --action list --character pedant --base-dir ./skills/pedant
```

Roll back a generated skill:

```bash
python3 tools/version_manager.py --action rollback --character colleague --slug {slug} --version {version} --base-dir ./skills/colleague
python3 tools/version_manager.py --action rollback --character relationship --slug {slug} --version {version} --base-dir ./skills/relationship
python3 tools/version_manager.py --action rollback --character celebrity --slug {slug} --version {version} --base-dir ./skills/celebrity
python3 tools/version_manager.py --action rollback --character pedant --slug {slug} --version {version} --base-dir ./skills/pedant
```

Delete a generated skill only after confirming the character family and slug:

```bash
rm -rf skills/{character}/{slug}
```

## Local Verification

Run these checks before committing repository changes:

```bash
python3 -m unittest discover -s tests
python3 -m compileall tools
```

If the development environment is installed, also run:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Host Path Examples

Use these examples only when explaining installation targets. Do not prepend
them to ordinary tool commands:

- `~/.openclaw/...`
- `~/.codex/...`
- `~/.claude/...`

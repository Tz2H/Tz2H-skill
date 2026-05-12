# Tz2H-skill

这是一个用于二次开发的本地 Skill 项目。当前仓库已清理上游项目的宣传、路线图、多语言文档和社区资料，只保留运行、安装、开发所需的最小使用说明。

## 环境要求

- Python 3.9+
- 可选：Node.js 16+，仅在使用飞书 MCP 方案时需要
- 可选：Playwright Chromium，仅在使用飞书浏览器采集方案时需要

安装基础依赖：

```bash
pip3 install -r requirements.txt
```

按需安装可选依赖：

```bash
pip3 install pypinyin
pip3 install playwright
playwright install chromium
npm install -g feishu-mcp
```

## 安装到宿主

整个仓库就是一个 Agent Skill 目录，入口文件是 `SKILL.md`。兼容宿主包括 Claude Code、OpenClaw、Hermes 和 Codex。

### Claude Code

安装到当前项目：

```bash
mkdir -p .claude/skills
git clone <this-repo-url> .claude/skills/Tz2H-skill
```

安装到全局：

```bash
git clone <this-repo-url> ~/.claude/skills/Tz2H-skill
```

安装后在 Claude Code 中使用：

```text
/Tz2H-skill
```

### OpenClaw

使用安装器：

```bash
python3 tools/install_openclaw_skill.py --force
```

或者直接 clone：

```bash
git clone <this-repo-url> ~/.openclaw/workspace/skills/Tz2H-skill
```

### Hermes

```bash
python3 tools/install_hermes_skill.py --force
hermes skills list | rg Tz2H-skill
```

如需预览安装目标：

```bash
python3 tools/install_hermes_skill.py --dry-run
```

### Codex

```bash
python3 tools/install_codex_skill.py --force
```

或者直接 clone：

```bash
git clone <this-repo-url> ~/.codex/skills/Tz2H-skill
```

Codex 中没有固定 slash 入口，安装后它会把 `Tz2H-skill` 作为本地 skill 发现。

## 使用方法

在支持 slash command 的宿主中启动：

```text
/Tz2H-skill
```

启动后按提示选择要生成的角色类型：

- `colleague`：同事、导师、合作方等工作场景角色
- `relationship`：朋友、伴侣、家人等关系场景角色
- `celebrity`：公众人物、作者、创作者、虚构角色等

随后输入角色代号、基础信息、性格画像，并选择原材料来源。除代号外，大部分字段都可以跳过；也可以只凭手动描述生成 Skill。

生成后的文件默认写入：

```text
./skills/{character}/{slug}/
```

其中 `character` 通常是 `colleague`、`relationship` 或 `celebrity`。

## 原材料来源

常用方式：

- 飞书自动采集：`python3 tools/feishu_auto_collector.py`
- 飞书浏览器采集：`python3 tools/feishu_browser.py`
- 飞书 MCP 采集：`python3 tools/feishu_mcp_client.py`
- 钉钉自动采集：`python3 tools/dingtalk_auto_collector.py`
- Slack 自动采集：`python3 tools/slack_auto_collector.py`
- 邮件解析：`python3 tools/email_parser.py`
- 手动上传 PDF、图片、JSON、Markdown 或直接粘贴文本

首次配置示例：

```bash
python3 tools/feishu_auto_collector.py --setup
python3 tools/dingtalk_auto_collector.py --setup
python3 tools/feishu_mcp_client.py --setup
python3 tools/slack_auto_collector.py --setup
```

## 生成后安装角色 Skill

如果已经生成某个角色 Skill，并希望安装到具体宿主：

```bash
python3 tools/install_claude_generated_skill.py --skill-dir skills/{character}/{slug} --force
python3 tools/install_openclaw_generated_skill.py --skill-dir skills/{character}/{slug} --force
python3 tools/install_codex_generated_skill.py --skill-dir skills/{character}/{slug} --force
```

在 Claude Code、OpenClaw、Hermes 等支持 slash command 的宿主中，触发格式通常是：

```text
/{character}-{slug}
```

在 Codex 中，对应本地 skill 名称通常是：

```text
{character}-{slug}
```

## 管理命令

列出已有 Skill：

```bash
python3 tools/skill_writer.py --action list --base-dir ./skills/colleague
python3 tools/skill_writer.py --action list --base-dir ./skills/relationship
python3 tools/skill_writer.py --action list --base-dir ./skills/celebrity
```

回滚版本：

```bash
python3 tools/version_manager.py --action rollback --skill-dir ./skills/{character}/{slug}
```

查看工具帮助：

```bash
python3 tools/feishu_parser.py --help
python3 tools/email_parser.py --help
python3 tools/slack_auto_collector.py --help
python3 tools/research/quality_check.py --help
```

## Celebrity Research 工具链

`celebrity` 类型可使用研究工具链整理字幕、访谈和研究材料：

```bash
bash tools/research/download_subtitles.sh "<video-url>" "./tmp/subtitles"
python3 tools/research/srt_to_transcript.py "./tmp/subtitles/example.srt"
python3 tools/research/merge_research.py "./skills/celebrity/{slug}"
python3 tools/research/quality_check.py "./skills/celebrity/{slug}/SKILL.md"
```

## 目录结构

```text
.
├── SKILL.md                 # Skill 入口
├── README.md                # 当前项目使用说明
├── prompts/                 # 生成和分析用 Prompt 模板
├── references/              # celebrity 深度研究模板
├── skills/                  # 示例和生成后的角色 Skill
├── tools/                   # 安装器、采集器、解析器、版本管理工具
├── tests/                   # 单元测试
├── requirements.txt         # Python 依赖
└── LICENSE
```

## 本地验证

```bash
python3 -m compileall tools
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillEntrypointDocsTest(unittest.TestCase):
    def test_root_skill_uses_tz2h_skill_entrypoint(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: Tz2H-skill", content)
        self.assertIn("`/Tz2H-skill`", content)
        self.assertIn("兼容宿主", content)
        self.assertIn("compatible hosts", content.lower())
        self.assertIn("管理操作", content)
        self.assertIn("tools/skill_writer.py", content)
        self.assertIn("prompts/celebrity/research.md", content)
        self.assertIn("budget-unfriendly", content)
        self.assertIn("references/celebrity_budget_unfriendly_framework.md", content)
        self.assertIn("01_core_profile.md", content)
        self.assertIn("03_expression_and_reception.md", content)
        self.assertIn("Files scanned >= 3", content)
        self.assertIn("Unique URLs >= 2", content)
        self.assertIn("Potential long quote lines = 0", content)
        self.assertIn("实际打开过的具体页面", content)
        self.assertIn("actual inspected pages", content)
        self.assertIn("01_writings.md", content)
        self.assertIn("06_timeline.md", content)
        self.assertIn("Files scanned >= 6", content)
        self.assertIn("Unique URLs >= 8", content)
        self.assertIn("Primary-source markers >= 3", content)
        self.assertIn("research_audit.md", content)
        self.assertIn("--work-patch /tmp/tz2h_skill_{slug}_work_patch.md", content)
        self.assertIn("Do not hand-edit `work.md`", content)
        self.assertIn("~/.openclaw/...", content)
        self.assertIn("~/.codex/...", content)
        self.assertNotIn("${CLAUDE_SKILL_DIR}", content)
        self.assertNotIn("`/list-skills`", content)
        self.assertNotIn("Compatibility aliases:", content)

    def test_readme_contains_usage_only_tz2h_skill_paths(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn(".claude/skills/Tz2H-skill", readme)
        self.assertIn("~/.openclaw/workspace/skills/Tz2H-skill", readme)
        self.assertIn("~/.codex/skills/Tz2H-skill", readme)
        self.assertIn("/Tz2H-skill", readme)
        self.assertIn("./skills/colleague", readme)
        self.assertIn("./skills/pedant", readme)

        self.assertIn("install_claude_generated_skill.py", readme)
        self.assertIn("install_openclaw_generated_skill.py", readme)
        self.assertIn("install_codex_generated_skill.py", readme)
        self.assertIn("install_openclaw_skill.py", readme)
        self.assertIn("install_codex_skill.py", readme)
        self.assertIn("/{character}-{slug}", readme)
        self.assertIn("./skills/colleague", skill)
        self.assertIn("./skills/pedant", skill)
        self.assertIn("兼容宿主", readme)
        self.assertFalse((ROOT / "INSTALL.md").exists())
        self.assertFalse((ROOT / "ROADMAP.md").exists())
        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())

    def test_repo_examples_live_under_skills_colleague(self) -> None:
        self.assertTrue((ROOT / "skills" / "colleague" / "example_zhangsan").exists())
        self.assertTrue((ROOT / "skills" / "colleague" / "example_tianyi").exists())
        self.assertTrue((ROOT / "skills" / "colleague" / "example_jiaxiu").exists())
        self.assertFalse((ROOT / "colleagues").exists())

    def test_upstream_docs_have_been_removed(self) -> None:
        docs_dir = ROOT / "docs"
        if docs_dir.exists():
            allowed_docs = {docs_dir / "agents"}
            self.assertTrue(set(docs_dir.iterdir()).issubset(allowed_docs))
        self.assertFalse((ROOT / "colleague_skill.pdf").exists())
        self.assertFalse((ROOT / "openarena-claim.txt").exists())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import os
import unittest
from unittest import mock

from tools.collect_email_imap import (
    build_search_criteria,
    decode_mime_str,
    resolve_password,
    safe_filename,
    validate_privacy_approval,
)


class CollectEmailImapTest(unittest.TestCase):
    def test_decode_mime_str_decodes_encoded_subject(self) -> None:
        self.assertEqual(decode_mime_str("=?utf-8?b?5rWL6K+V?="), "测试")

    def test_safe_filename_removes_unsafe_characters(self) -> None:
        self.assertEqual(safe_filename(' Re: a/b:c* "x" '), "Re__a_b_c___x")
        self.assertEqual(safe_filename(""), "no_subject")

    def test_build_search_criteria_can_filter_sender(self) -> None:
        self.assertEqual(build_search_criteria(), ("ALL",))
        self.assertEqual(
            build_search_criteria('someone@example.com'),
            ("FROM", '"someone@example.com"'),
        )

    def test_resolve_password_prefers_cli_value(self) -> None:
        with mock.patch.dict(os.environ, {"IMAP_PASSWORD": "env-secret"}):
            self.assertEqual(resolve_password("cli-secret", "IMAP_PASSWORD"), "cli-secret")

    def test_resolve_password_reads_environment_variable(self) -> None:
        with mock.patch.dict(os.environ, {"IMAP_PASSWORD": "env-secret"}):
            self.assertEqual(resolve_password(None, "IMAP_PASSWORD"), "env-secret")

    def test_resolve_password_requires_a_source(self) -> None:
        with self.assertRaises(RuntimeError):
            resolve_password(None, None)

    def test_validate_privacy_approval_allows_local_model(self) -> None:
        validate_privacy_approval("local", False)

    def test_validate_privacy_approval_requires_consent_for_online_model(self) -> None:
        with self.assertRaises(RuntimeError):
            validate_privacy_approval("online", False)
        validate_privacy_approval("online", True)


if __name__ == "__main__":
    unittest.main()

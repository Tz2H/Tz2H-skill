#!/usr/bin/env python3
"""
Collect recent emails from an IMAP mailbox and save them as .eml files.

This script intentionally stops at collection. Feed the saved .eml files into
tools/email_parser.py for target-person extraction and formatting.

Examples:
    python3 tools/collect_email_imap.py \
        --server imap.gmail.com \
        --email your_email@gmail.com \
        --password-env GMAIL_APP_PASSWORD \
        --limit 50 \
        --output collected_emails

    python3 tools/email_parser.py \
        --file collected_emails/101_Project_Update.eml \
        --target someone@example.com \
        --output output.txt
"""

from __future__ import annotations

import argparse
import email
import imaplib
import os
import re
import sys
from email.header import decode_header
from pathlib import Path


def decode_mime_str(value: str | None) -> str:
    """Decode MIME-encoded email header fields."""
    if not value:
        return ""

    decoded_parts: list[str] = []
    for part, charset in decode_header(value):
        if isinstance(part, bytes):
            charset = charset or "utf-8"
            try:
                decoded_parts.append(part.decode(charset, errors="replace"))
            except Exception:
                decoded_parts.append(part.decode("utf-8", errors="replace"))
        else:
            decoded_parts.append(str(part))

    return "".join(decoded_parts)


def safe_filename(text: str, max_len: int = 80) -> str:
    """Convert an email subject into a filesystem-safe filename segment."""
    cleaned = text.strip()
    cleaned = re.sub(r"[\\/:*?\"<>|]", "_", cleaned)
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = cleaned.strip("._ ")
    return cleaned[:max_len] or "no_subject"


def quote_imap_value(value: str) -> str:
    """Quote a value for simple IMAP SEARCH criteria."""
    escaped = value.replace("\\", "\\\\").replace('"', r"\"")
    return f'"{escaped}"'


def build_search_criteria(from_address: str | None = None) -> tuple[str, ...]:
    """Build the IMAP SEARCH criteria for this MVP collector."""
    if from_address:
        return ("FROM", quote_imap_value(from_address))
    return ("ALL",)


def extract_raw_message(fetch_data: list | tuple) -> bytes | None:
    """Return the RFC822 bytes from imaplib.fetch response data."""
    for item in fetch_data:
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
            return item[1]
    return None


def resolve_password(password: str | None, password_env: str | None) -> str:
    """Resolve the IMAP password from CLI args or an environment variable."""
    if password:
        return password
    if password_env:
        env_password = os.environ.get(password_env)
        if env_password:
            return env_password
        raise RuntimeError(f"环境变量 {password_env} 未设置或为空")
    raise RuntimeError("请通过 --password 或 --password-env 提供邮箱密码/应用专用密码")


def collect_emails(
    server: str,
    email_account: str,
    password: str,
    mailbox: str,
    limit: int,
    output_dir: str,
    from_address: str | None = None,
    port: int = 993,
) -> int:
    """Collect recent matching emails and save them as .eml files."""
    if limit <= 0:
        raise ValueError("--limit 必须大于 0")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(email_account, password)

    try:
        status, _ = mail.select(mailbox, readonly=True)
        if status != "OK":
            raise RuntimeError(f"无法打开邮箱目录：{mailbox}")

        search_criteria = build_search_criteria(from_address)
        status, data = mail.search(None, *search_criteria)
        if status != "OK":
            raise RuntimeError("搜索邮件失败")

        email_ids = data[0].split() if data and data[0] else []
        if not email_ids:
            print("没有找到匹配邮件")
            return 0

        recent_ids = email_ids[-limit:]
        saved_count = 0

        for email_id_bytes in recent_ids:
            email_id = email_id_bytes.decode("ascii", errors="replace")
            status, msg_data = mail.fetch(email_id_bytes, "(BODY.PEEK[])")
            if status != "OK":
                print(f"跳过邮件 ID {email_id}：获取失败", file=sys.stderr)
                continue

            raw_email = extract_raw_message(msg_data)
            if raw_email is None:
                print(f"跳过邮件 ID {email_id}：响应中没有邮件正文", file=sys.stderr)
                continue

            msg = email.message_from_bytes(raw_email)
            subject = decode_mime_str(msg.get("Subject", ""))
            from_field = decode_mime_str(msg.get("From", ""))
            date = msg.get("Date", "")

            filename = f"{email_id}_{safe_filename(subject)}.eml"
            file_path = output_path / filename

            if file_path.exists():
                print(f"已存在，跳过：{filename}")
                continue

            with open(file_path, "wb") as f:
                f.write(raw_email)

            saved_count += 1
            print(f"已保存：{filename}")
            print(f"  From: {from_field}")
            print(f"  Date: {date}")
            print()

        print(f"完成：新增保存 {saved_count} 封邮件")
        return saved_count

    finally:
        mail.logout()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="通过 IMAP 收集邮件并保存为 .eml 文件，后续交给 email_parser.py 处理"
    )
    parser.add_argument("--server", required=True, help="IMAP 服务器，例如 imap.gmail.com")
    parser.add_argument("--port", type=int, default=993, help="IMAP SSL 端口，默认 993")
    parser.add_argument("--email", required=True, help="邮箱账号")
    parser.add_argument("--password", default=None, help="邮箱密码或应用专用密码")
    parser.add_argument(
        "--password-env",
        default=None,
        help="从指定环境变量读取密码，例如 GMAIL_APP_PASSWORD",
    )
    parser.add_argument("--mailbox", default="INBOX", help="邮箱目录，默认 INBOX")
    parser.add_argument("--from", dest="from_address", default=None, help="只收集指定发件人的邮件")
    parser.add_argument("--limit", type=int, default=50, help="拉取最近多少封匹配邮件")
    parser.add_argument("--output", default="collected_emails", help="输出目录")

    args = parser.parse_args()

    try:
        password = resolve_password(args.password, args.password_env)
        collect_emails(
            server=args.server,
            port=args.port,
            email_account=args.email,
            password=password,
            mailbox=args.mailbox,
            limit=args.limit,
            output_dir=args.output,
            from_address=args.from_address,
        )
    except Exception as exc:
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

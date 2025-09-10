#!/usr/bin/env python3
import os, re, sys, pathlib

REDACT_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?([A-Za-z0-9-_]{16,})"), r"\1: ***REDACTED***"),
    (re.compile(r"https?://[\w.-]*internal[\w./-]*"), "https://internal.example.invalid"),
]

def redact_text(text: str) -> str:
    for pattern, repl in REDACT_PATTERNS:
        text = pattern.sub(repl, text)
    return text

def process_file(src: pathlib.Path, dst: pathlib.Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    content = src.read_text(encoding="utf-8")
    redacted = redact_text(content)
    dst.write_text(redacted, encoding="utf-8")

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: redact.py <src_path> <dst_path>")
        return 2
    src_root = pathlib.Path(sys.argv[1])
    dst_root = pathlib.Path(sys.argv[2])
    for src in src_root.rglob("*"):
        if src.is_file():
            rel = src.relative_to(src_root)
            process_file(src, dst_root / rel)
    print(f"Redacted from {src_root} -> {dst_root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

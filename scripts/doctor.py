"""Local environment checks for araboja-shorts."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


MIN_PYTHON = (3, 10)
REQUIRED_IMPORTS = {
    "requests": "requests",
    "PIL": "Pillow",
    "openai": "openai",
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def check_python_version(version_info: Sequence[int] = sys.version_info) -> CheckResult:
    current = tuple(version_info[:3])
    ok = tuple(version_info[:2]) >= MIN_PYTHON
    return CheckResult(
        "python",
        ok,
        f"found {current[0]}.{current[1]}.{current[2]}, require {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+",
    )


def check_import(module_name: str, package_name: str) -> CheckResult:
    ok = importlib.util.find_spec(module_name) is not None
    detail = "installed" if ok else f"missing; install {package_name}"
    return CheckResult(f"package:{package_name}", ok, detail)


def check_executable(name: str, override: str | None = None) -> CheckResult:
    if override:
        path = Path(override)
        ok = path.exists()
        return CheckResult(name, ok, str(path) if ok else f"not found: {path}")

    found = shutil.which(name)
    return CheckResult(name, bool(found), found or f"{name} not found on PATH")


def check_env_var(name: str) -> CheckResult:
    ok = bool(os.getenv(name, "").strip())
    return CheckResult(f"env:{name}", ok, "set" if ok else "not set")


def build_checks(ffmpeg_path: str | None = None) -> list[CheckResult]:
    checks = [check_python_version()]
    checks.extend(check_import(module, package) for module, package in REQUIRED_IMPORTS.items())
    checks.append(check_executable("ffmpeg", ffmpeg_path))
    checks.append(check_executable("ffprobe"))
    checks.append(check_env_var("OPENAI_API_KEY"))
    return checks


def render_text(checks: Iterable[CheckResult]) -> str:
    lines = []
    for check in checks:
        status = "ok" if check.ok else "fail"
        lines.append(f"[{status}] {check.name}: {check.detail}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check local araboja-shorts runtime prerequisites.")
    parser.add_argument("--ffmpeg-path", default=None, help="Explicit ffmpeg executable path.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    checks = build_checks(args.ffmpeg_path)
    if args.json:
        print(json.dumps([asdict(check) for check in checks], indent=2))
    else:
        print(render_text(checks))
    return 0 if all(check.ok for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

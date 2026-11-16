#!/usr/bin/env python3
"""Governance invariant checker for the generic two-repo template."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Iterable


CHECKS: dict[str, Callable[["Context"], list["Failure"]]] = {}


@dataclass(frozen=True)
class Failure:
    check: str
    path: Path
    message: str


@dataclass(frozen=True)
class Context:
    product: Path
    dev: Path
    budgets: dict
    today: date


SCHEMAS = {
    "prompt": {"id", "title", "status", "depends_on", "touches"},
    "build_report": {"id", "prompt", "date", "status", "validated"},
    "issue": {
        "id",
        "type",
        "status",
        "severity",
        "scope",
        "found_in",
        "summary",
        "created",
        "updated",
    },
    "adr": {"id", "status", "date", "updated", "supersedes"},
    "spec": {"id", "status", "date", "updated", "unit_or_scope"},
    "contract": {"id", "status", "date", "updated", "owners", "sync_required"},
    "unit": {"id", "status", "date", "updated", "unit_type"},
    "work_package": {"id", "title", "purpose", "status", "depends_on"},
}

ISSUE_RULES = {
    "gap": ("GAP", "gaps"),
    "deferred": ("DEF", "deferred"),
    "bug": ("BUG", "bugs"),
    "upstream": ("REQ", "upstream"),
}

GENERATED_BANNER = "<!-- DO NOT EDIT - generated from {source} -->"


def check(name: str) -> Callable:
    def decorate(func: Callable[[Context], list[Failure]]) -> Callable:
        CHECKS[name] = func
        return func

    return decorate


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def all_files(root: Path, suffix: str | None = None) -> Iterable[Path]:
    if not root.exists():
        return []
    files = (p for p in root.rglob("*") if p.is_file())
    if suffix:
        return (p for p in files if p.suffix.lower() == suffix)
    return files


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value in ("[]", "{}"):
        return []
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        return [item.strip().strip("'\"") for item in body.split(",")]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value.strip("'\"")


def parse_simple_yaml(text: str) -> dict:
    data: dict = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        data[key] = parse_scalar(value)
        current_key = key if value.strip() == "" else None
        if current_key:
            data[current_key] = []
    return data


def front_matter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return parse_simple_yaml(text[4:end])


def missing_fields(data: dict | None, schema: str) -> set[str]:
    if data is None:
        return set(SCHEMAS[schema])
    return {field for field in SCHEMAS[schema] if field not in data}


def generated_index(path: Path, source: str, title: str, source_dir: Path) -> str:
    lines = [GENERATED_BANNER.format(source=source), "", f"# {title}", ""]
    files = sorted(p for p in source_dir.iterdir() if p.is_file() and p.name != "INDEX.md")
    if files:
        lines.extend(f"- [{p.name}]({p.name})" for p in files)
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def generated_pattern_index(root: Path, source: str, title: str, source_label: str | None = None) -> str:
    lines = [GENERATED_BANNER.format(source=source_label or source), "", f"# {title}", ""]
    files = sorted(p for p in root.glob(source) if p.is_file() and p.name != "INDEX.md")
    if files:
        lines.extend(f"- [{rel(p, root)}]({rel(p, root)})" for p in files)
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def generated_yaml_view(path: Path, source: str, title: str, source_file: Path) -> str:
    lines = [GENERATED_BANNER.format(source=source), "", f"# {title}", ""]
    data = parse_simple_yaml(source_file.read_text(encoding="utf-8"))
    if data:
        lines.extend(f"- **{key}**: {value}" for key, value in sorted(data.items()))
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def generated_queue(dev: Path) -> str:
    prompts = sorted((dev / "work").glob("*/prompts/*.md"))
    rows = []
    for prompt in prompts:
        data = front_matter(prompt) or {}
        rows.append(
            "| {id} | [{title}]({path}) | `{status}` |".format(
                id=data.get("id", "?"),
                title=data.get("title", prompt.stem),
                status=data.get("status", "?"),
                path=rel(prompt, dev),
            )
        )
    lines = [
        GENERATED_BANNER.format(source="work/*/prompts/*.md"),
        "",
        "# Queue",
        "",
        "| ID | Prompt | Status |",
        "|---|---|---|",
    ]
    lines.extend(rows or ["| - | - | - |"])
    return "\n".join(lines) + "\n"


def generated_status(product: Path, dev: Path) -> str:
    prompt_count = len(list((dev / "work").glob("*/prompts/*.md")))
    report_count = len(list((dev / "build-reports").glob("*.md"))) - int((dev / "build-reports" / "INDEX.md").exists())
    lines = [
        GENERATED_BANNER.format(source="../generic-dev/work and ../generic-dev/build-reports"),
        "",
        "# Status",
        "",
        f"- Prompts: {prompt_count}",
        f"- Build reports: {max(report_count, 0)}",
        "- Details: ../generic-dev/QUEUE.md",
    ]
    return "\n".join(lines) + "\n"


@check("line-byte-budgets")
def check_line_byte_budgets(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    roots = [ctx.product, ctx.dev]
    hot = ctx.budgets["hot"]
    warm = ctx.budgets["warm"]
    for root in roots:
        for path_name in hot["paths"]:
            path = root / path_name
            if path.exists():
                if line_count(path) > hot["max_lines"] or path.stat().st_size > hot["max_bytes"]:
                    failures.append(Failure("line-byte-budgets", path, "hot-tier budget exceeded"))
        for pattern in warm["patterns"]:
            for path in root.glob(pattern):
                if line_count(path) > warm["max_lines"] or path.stat().st_size > warm["max_bytes"]:
                    failures.append(Failure("line-byte-budgets", path, "warm-tier budget exceeded"))
    return failures


@check("relative-links")
def check_relative_links(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for root in [ctx.product, ctx.dev]:
        for path in all_files(root, ".md"):
            text = path.read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                target = match.group(1).strip()
                if re.match(r"^[a-z]+://", target) or target.startswith("#") or target.startswith("mailto:"):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                if not (path.parent / clean).resolve().exists():
                    failures.append(Failure("relative-links", path, f"missing relative link target: {target}"))
    return failures


@check("section-length")
def check_section_length(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    limit = ctx.budgets["section_max_lines_without_subheading"]
    h2 = re.compile(r"^##(?!#)\s+")
    h3 = re.compile(r"^###\s+")
    for root in [ctx.product, ctx.dev]:
        for path in all_files(root, ".md"):
            lines = path.read_text(encoding="utf-8").splitlines()
            starts = [i for i, line in enumerate(lines) if h2.match(line)]
            for index, start in enumerate(starts):
                end = starts[index + 1] if index + 1 < len(starts) else len(lines)
                block = lines[start:end]
                if len(block) > limit and not any(h3.match(line) for line in block[1:]):
                    failures.append(Failure("section-length", path, f"## section exceeds {limit} lines without ###"))
    return failures


@check("schemas")
def check_schemas(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    markdown_sets = [
        (ctx.dev.glob("work/*/prompts/*.md"), "prompt"),
        (ctx.dev.glob("build-reports/*.md"), "build_report"),
        (ctx.product.glob("governance/adr/ADR-*.md"), "adr"),
        (ctx.product.glob("governance/specs/SPEC-*.md"), "spec"),
        (ctx.product.glob("governance/contracts/*.md"), "contract"),
        (ctx.product.glob("governance/units/UNIT-*.md"), "unit"),
    ]
    for paths, schema in markdown_sets:
        for path in paths:
            if path.name == "INDEX.md":
                continue
            missing = missing_fields(front_matter(path), schema)
            if missing:
                failures.append(Failure("schemas", path, f"missing {schema} fields: {', '.join(sorted(missing))}"))
    for path in ctx.dev.glob("work/*/package.yml"):
        missing = missing_fields(parse_simple_yaml(path.read_text(encoding="utf-8")), "work_package")
        if missing:
            failures.append(Failure("schemas", path, f"missing work_package fields: {', '.join(sorted(missing))}"))
    for path in ctx.dev.glob("issues/*/*.yml"):
        missing = missing_fields(parse_simple_yaml(path.read_text(encoding="utf-8")), "issue")
        if missing:
            failures.append(Failure("schemas", path, f"missing issue fields: {', '.join(sorted(missing))}"))
    return failures


@check("generated-files")
def check_generated_files(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    expected: dict[Path, str] = {
        ctx.product / "STATUS.md": generated_status(ctx.product, ctx.dev),
        ctx.product / "governance" / "INDEX.md": generated_index(ctx.product / "governance" / "INDEX.md", "governance/*", "Governance Index", ctx.product / "governance"),
        ctx.product / "governance" / "adr" / "INDEX.md": generated_index(ctx.product / "governance" / "adr" / "INDEX.md", "governance/adr/*.md", "ADR Index", ctx.product / "governance" / "adr"),
        ctx.product / "governance" / "specs" / "INDEX.md": generated_index(ctx.product / "governance" / "specs" / "INDEX.md", "governance/specs/*.md", "Spec Index", ctx.product / "governance" / "specs"),
        ctx.product / "governance" / "contracts" / "INDEX.md": generated_index(ctx.product / "governance" / "contracts" / "INDEX.md", "governance/contracts/*.md", "Contract Index", ctx.product / "governance" / "contracts"),
        ctx.product / "governance" / "units" / "INDEX.md": generated_index(ctx.product / "governance" / "units" / "INDEX.md", "governance/units/*.md", "Unit Index", ctx.product / "governance" / "units"),
        ctx.product / "governance" / "capabilities.md": generated_yaml_view(ctx.product / "governance" / "capabilities.md", "governance/capabilities.yml", "Capabilities", ctx.product / "governance" / "capabilities.yml"),
        ctx.product / "governance" / "ai-reference" / "routing.md": generated_yaml_view(ctx.product / "governance" / "ai-reference" / "routing.md", "governance/ai-reference/routing.yml", "AI Routing", ctx.product / "governance" / "ai-reference" / "routing.yml"),
        ctx.dev / "QUEUE.md": generated_queue(ctx.dev),
        ctx.dev / "build-reports" / "INDEX.md": generated_index(ctx.dev / "build-reports" / "INDEX.md", "build-reports/*.md", "Build Report Index", ctx.dev / "build-reports"),
        ctx.dev / "issues" / "INDEX.md": generated_pattern_index(ctx.dev / "issues", "*/*.yml", "Issue Index", "issues/*/*.yml"),
        ctx.dev / "design" / "INDEX.md": generated_index(ctx.dev / "design" / "INDEX.md", "design/*", "Design Index", ctx.dev / "design"),
        ctx.dev / "state" / "INDEX.md": generated_index(ctx.dev / "state" / "INDEX.md", "state/*.md", "State Index", ctx.dev / "state"),
    }
    for path, content in expected.items():
        if not path.exists():
            failures.append(Failure("generated-files", path, "required generated file is missing"))
        elif path.read_text(encoding="utf-8") != content:
            failures.append(Failure("generated-files", path, "generated file is stale or hand-edited"))
    return failures


@check("sync-pins")
def check_sync_pins(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    sync_path = ctx.product / "governance" / "contracts" / "SYNC.yml"
    sync = parse_simple_yaml(sync_path.read_text(encoding="utf-8")) if sync_path.exists() else {}
    entries = set(sync.get("paths", []))
    for contract in ctx.product.glob("governance/contracts/*.md"):
        if contract.name == "INDEX.md":
            continue
        contract_rel = rel(contract, ctx.product)
        if contract_rel not in entries:
            failures.append(Failure("sync-pins", contract, "contract missing SYNC.yml path entry"))
    last_checked = sync.get("last_checked")
    if last_checked:
        try:
            age = (ctx.today - date.fromisoformat(str(last_checked))).days
            if age > ctx.budgets["sync_max_age_days"]:
                failures.append(Failure("sync-pins", sync_path, f"sync pin is {age} days old"))
        except ValueError:
            failures.append(Failure("sync-pins", sync_path, "last_checked is not ISO date"))
    return failures


@check("dev-not-ignored")
def check_dev_not_ignored(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    forbidden = [ctx.dev.name, f"{ctx.dev.name}/", "**/.notes/", ".notes/", "*-dev/"]
    for root in [ctx.product.parent, ctx.dev.parent]:
        for ignore_name in [".gitignore", ".claudeignore"]:
            path = root / ignore_name
            if not path.exists():
                continue
            for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if any(fnmatch.fnmatch(ctx.dev.name + "/", pattern) or pattern == line for pattern in forbidden):
                    failures.append(Failure("dev-not-ignored", path, f"coordination corpus ignored on line {line_no}: {line}"))
    return failures


@check("closed-prompts-have-reports")
def check_closed_prompts_have_reports(ctx: Context) -> list[Failure]:
    reports = []
    for path in ctx.dev.glob("build-reports/*.md"):
        data = front_matter(path) or {}
        reports.append(str(data.get("prompt", "")))
    failures: list[Failure] = []
    for prompt in ctx.dev.glob("work/*/prompts/*.md"):
        data = front_matter(prompt) or {}
        if data.get("status") == "closed":
            prompt_keys = {str(data.get("id", "")), prompt.stem}
            if not any(key and key in reports for key in prompt_keys):
                failures.append(Failure("closed-prompts-have-reports", prompt, "closed prompt has no matching build report"))
    return failures


@check("mutable-state-in-constitution")
def check_mutable_state_in_constitution(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    state_patterns = [
        r"^##\s+current\s+(phase|status|work|queue)",
        r"\b(in progress|queued|blocked|current phase)\b",
        r"\|\s*status\s*\|",
    ]
    for root in [ctx.product, ctx.dev]:
        for name in ["CLAUDE.md", "AGENTS.md"]:
            path = root / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8").lower()
            for pattern in state_patterns:
                if re.search(pattern, text, re.MULTILINE):
                    failures.append(Failure("mutable-state-in-constitution", path, "constitution contains mutable status/work state"))
                    break
    return failures


@check("no-amendment-drift")
def check_no_amendment_drift(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    amendment = re.compile(r"^#{2,3}\s+.*\b(amendment|revision|update-only|addendum)\b", re.IGNORECASE | re.MULTILINE)
    for path in list((ctx.product / "governance").rglob("*.md")) + list((ctx.dev / "work").rglob("*.md")):
        if path.name == "INDEX.md":
            continue
        data = front_matter(path) or {}
        if data.get("status") in {"superseded", "historical", "archived"}:
            continue
        if amendment.search(path.read_text(encoding="utf-8")):
            failures.append(Failure("no-amendment-drift", path, "active file contains amendment-only section"))
    return failures


@check("issue-type-prefix-folder")
def check_issue_type_prefix_folder(ctx: Context) -> list[Failure]:
    failures: list[Failure] = []
    for path in ctx.dev.glob("issues/*/*.yml"):
        data = parse_simple_yaml(path.read_text(encoding="utf-8"))
        issue_type = str(data.get("type", "")).lower()
        issue_id = str(data.get("id", ""))
        expected = ISSUE_RULES.get(issue_type)
        if not expected:
            failures.append(Failure("issue-type-prefix-folder", path, f"unknown issue type: {issue_type}"))
            continue
        prefix, folder = expected
        if not issue_id.startswith(prefix + "-") or path.parent.name != folder:
            failures.append(Failure("issue-type-prefix-folder", path, f"type/id/folder mismatch for {issue_id}/{issue_type}"))
    return failures


def run(ctx: Context, selected: list[str]) -> list[Failure]:
    failures: list[Failure] = []
    for name in selected:
        failures.extend(CHECKS[name](ctx))
    return failures


def main(argv: list[str] | None = None) -> int:
    script_dir = Path(__file__).resolve().parent
    default_product = script_dir.parent
    parser = argparse.ArgumentParser(description="Validate generic governance invariants.")
    parser.add_argument("--product-root", type=Path, default=default_product)
    parser.add_argument("--dev-root", type=Path, default=default_product.parent / f"{default_product.name}-dev")
    parser.add_argument("--budgets", type=Path, default=script_dir / "governance-budgets.json")
    parser.add_argument("--check", action="append", choices=sorted(CHECKS), help="Run one check; may be repeated.")
    parser.add_argument("--list-checks", action="store_true")
    parser.add_argument("--today", default=date.today().isoformat())
    args = parser.parse_args(argv)

    if args.list_checks:
        for name in sorted(CHECKS):
            print(name)
        return 0

    ctx = Context(
        product=args.product_root.resolve(),
        dev=args.dev_root.resolve(),
        budgets=json.loads(args.budgets.read_text(encoding="utf-8")),
        today=date.fromisoformat(args.today),
    )
    selected = args.check or sorted(CHECKS)
    failures = run(ctx, selected)
    for failure in failures:
        print(f"{failure.check}: {failure.path}: {failure.message}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

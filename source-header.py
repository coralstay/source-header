#!/usr/bin/env python3
# ---
# title: source-header
# description: 소스 파일 머리 주석의 YAML 헤더를 검사·유지하는 도구
# authors: [coralstay]
# license: AGPL-3.0-only
# status: draft
# task: TASK-1
# created_date: '2026-10-31'
# updated_date: '2026-10-31'
# ---
# [설계 메모]
# 프로젝트 상태와 간단한 소스 관리의 SSOT는 소스 파일 자체와 그 머리 주석이다.
# 이 도구는 그 머리 주석 안의 YAML 헤더(위 블록이 그 형식이다)를 읽고, 검사하고,
# git에서 유도할 수 있는 값(created_date, authors, license, updated_date)을 채운다.
#
# - 표준 라이브러리만 쓴다: 워크스페이스에 PyYAML이 없고, pre-commit·CI·다른 에이전트
#   어디서든 python3와 git만 있으면 같은 결과가 나와야 하기 때문이다.
# - 파서는 agile-hooks scripts/work_order.py의 parse_frontmatter 사본이다. 주석 접두사를
#   벗기면 Backlog.md 카드와 같은 텍스트가 되므로, 새 YAML 파서를 만들지 않고 훅과 같은
#   동작을 공유한다. 사본이 원본과 같은지는 테스트가 확인한다.
# - --staged는 작업 트리가 아니라 인덱스(git show :path)를 읽는다. 커밋되는 것은 인덱스
#   내용이므로, 작업 트리를 보면 고친 척만 하고 틀린 내용이 커밋될 수 있다.
# - fix는 일부만 staged된 파일을 고치지 않는다. 작업 트리 파일을 고쳐 다시 git add하면
#   아직 stage하지 않은 변경까지 커밋에 섞여 들어가기 때문이다.
# - 규칙은 (fields, ctx) -> [Finding] 함수 목록(RULES)이라 단계마다 덧붙이기 쉽다.
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from itertools import pairwise
from pathlib import Path, PurePath

# --- 헤더 스키마 ---

# 확장자 → 주석 접두사. .md는 접두사 없이 1번 줄의 일반 프론트 매터를 쓴다.
COMMENT_PREFIX = {
    **dict.fromkeys((".py", ".sh", ".bash", ".yaml", ".yml", ".toml", ".rb"), "#"),
    **dict.fromkeys(
        (".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".hpp",
         ".kt", ".swift"),
        "//",
    ),
    **dict.fromkeys((".sql", ".lua"), "--"),
    ".md": "",
}

# REUSE 관례의 라이선스 줄. 헤더 필드로 써도, 머리 주석에 따로 써도 된다.
SPDX_KEY = "SPDX-License-Identifier"
REQUIRED = ("title", "description", "authors", "license", "status", "created_date",
            "updated_date")
OPTIONAL = ("task", "reviewers", "reviewed_date", "published_date", "deprecated_date",
            "superseded_by", "labels", "version", "upstream", SPDX_KEY)
# render가 쓰는 고정 순서. 사람이 쓰는 필드 → 상태 → git 유도 날짜 → 수명 주기 날짜.
FIELD_ORDER = ("title", "description", "authors", "reviewers", "license", "status", "task",
               "labels", "version", "upstream", "superseded_by", "created_date",
               "updated_date", "reviewed_date", "published_date", "deprecated_date")
LIST_FIELDS = ("authors", "reviewers", "labels")
DATE_FIELDS = ("created_date", "updated_date", "reviewed_date", "published_date",
               "deprecated_date")
STATUSES = ("draft", "review", "published", "deprecated", "archived")
# 날짜 형식: Backlog.md 카드처럼 날짜만, 또는 날짜 + 시:분
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?$")

# shebang 다음에 올 수 있는 PEP 263 encoding 줄
ENCODING_RE = re.compile(r"^[ \t\f]*#.*?coding[:=]")


# --- agile-hooks와 공유하는 파서 (scripts/work_order.py 사본, 수정 금지) ---

KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def parse_frontmatter(text):
    """The top-level keys of a `---` frontmatter block. Values are strings,
    or lists for block (`- x`) and inline (`[x, y]`) lists. Only what
    backlog.md writes is understood - this is not a YAML parser."""

    def unquote(value):
        if len(value) >= 2 and value[0] == value[-1] == "'":
            return value[1:-1].replace("''", "'")
        if len(value) >= 2 and value[0] == value[-1] == '"':
            return value[1:-1]
        return value

    lines = text.split("\n")
    if lines[0].strip() != "---":
        return {}
    fields = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = KEY_RE.match(line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                fields[key] = [unquote(v.strip()) for v in inner.split(",")] if inner else []
            elif value in (">-", ">", "|", "|-"):
                fields[key] = ""
            else:
                fields[key] = unquote(value)
            continue
        item = line.strip()
        if key is None or not item:
            continue
        if item == "-" or item.startswith("- "):
            if not isinstance(fields[key], list):
                fields[key] = []
            fields[key].append(unquote(item[2:].strip()))
        elif isinstance(fields[key], str):
            fields[key] = (fields[key] + " " + item).strip()
    return fields


# --- 추출 · 렌더 ---


@dataclass
class Header:
    """파일 안 헤더 하나. start/end는 여는·닫는 `---` 줄 번호(1부터), lines는 필드별 줄 번호."""

    fields: dict
    start: int
    end: int
    prefix: str
    lines: dict = field(default_factory=dict)


def prefix_for(path) -> str | None:
    """확장자의 주석 접두사. 모르는 형식(JSON 등 주석을 못 다는 파일)은 None."""
    return COMMENT_PREFIX.get(PurePath(str(path)).suffix.lower())


def strip_yaml_comment(line: str) -> str:
    """따옴표 밖의 YAML 주석(` #...`, 줄 머리 `#`)을 떼어 낸다.

    템플릿은 필드마다 설명 주석을 단다. parse_frontmatter는 주석을 모르므로 넘기기 전에
    여기서 지운다. 주석이 없는 줄은 그대로라 원본 파서와의 동일성이 깨지지 않는다."""
    if line.lstrip().startswith("#"):
        return ""
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == quote == "'" and line[i + 1:i + 2] == "'":
                i += 1  # 작은따옴표 안의 '' 는 이스케이프된 '
            elif ch == quote:
                quote = None
        elif ch in "'\"" and (i == 0 or line[i - 1] in " \t[,:-"):
            quote = ch
        elif ch == "#" and i > 0 and line[i - 1] in " \t":
            return line[:i].rstrip()
        i += 1
    return line


def header_start(lines: list[str], prefix: str) -> int:
    """헤더가 시작할 수 있는 줄 위치(0부터). shebang과 encoding 줄을 건너뛴다."""
    i = 0
    if prefix and i < len(lines) and lines[i].startswith("#!"):
        i += 1
    while prefix == "#" and i < len(lines) and i < 2 and ENCODING_RE.match(lines[i]):
        i += 1
    return i


def _unprefix(line: str, prefix: str) -> str | None:
    """`<prefix> text`에서 text를 꺼낸다. 접두사가 아니면 None(헤더 밖)."""
    if not prefix:
        return line
    stripped = line.rstrip("\r")
    if stripped == prefix:
        return ""
    if stripped.startswith(prefix + " "):
        return stripped[len(prefix) + 1:]
    return None


def extract_header(text: str, path) -> Header | None:
    """파일 텍스트에서 헤더를 찾아 필드와 줄 위치를 돌려준다. 없거나 닫히지 않으면 None.

    접두사를 벗기고 YAML 주석을 지운 `---` 블록을 parse_frontmatter에 넘기므로,
    필드 해석은 Backlog.md 카드를 읽는 agile-hooks와 똑같다."""
    prefix = prefix_for(path)
    if prefix is None:
        return None
    lines = text.split("\n")
    i = header_start(lines, prefix)
    if i >= len(lines) or (_unprefix(lines[i], prefix) or "").strip() != "---":
        return None
    body: list[tuple[int, str]] = []
    for j in range(i + 1, len(lines)):
        inner = _unprefix(lines[j], prefix)
        if inner is None:
            return None
        if inner.strip() == "---":
            block = "\n".join(["---", *(t for _, t in body), "---"])
            key_lines = {}
            for lineno, t in body:
                m = KEY_RE.match(t)
                if m and m.group(1) not in key_lines:
                    key_lines[m.group(1)] = lineno
            return Header(parse_frontmatter(block), i + 1, j + 1, prefix, key_lines)
        body.append((j + 1, strip_yaml_comment(inner)))
    return None


def _needs_quote(value: str) -> bool:
    if value == "" or value != value.strip():
        return True
    if value in (">-", ">", "|", "|-") or value[0] in "'\"[{&*!%@`|>":
        return True
    if value.startswith(("- ", "#")) or value == "-" or " #" in value:
        return True
    return bool(DATE_RE.match(value))


def render_value(value) -> str:
    """값 하나를 YAML 스칼라/인라인 리스트로. 날짜는 Backlog.md처럼 작은따옴표로 감싼다."""
    if isinstance(value, list):
        return "[" + ", ".join(render_scalar(v) for v in value) + "]"
    return render_scalar(value)


def render_scalar(value: str) -> str:
    if _needs_quote(value):
        return "'" + value.replace("'", "''") + "'"
    return value


def render_header(fields: dict, prefix: str) -> str:
    """필드를 헤더 블록 텍스트로 만든다. FIELD_ORDER 순서 고정, 모르는 필드는 그 뒤에 원래 순서로.

    순서를 고정해야 사람·도구가 고친 헤더의 diff가 작고 예측 가능하다."""
    keys = [k for k in FIELD_ORDER if k in fields] + [k for k in fields if k not in FIELD_ORDER]
    lines = ["---"]
    for key in keys:
        value = fields[key]
        if isinstance(value, list) and any("," in v for v in value):
            # 인라인 리스트는 쉼표로 나뉘므로 쉼표가 든 항목은 블록 리스트로 쓴다.
            lines.append(f"{key}:")
            lines.extend(f"  - {render_scalar(v)}" for v in value)
        else:
            lines.append(f"{key}: {render_value(value)}")
    lines.append("---")
    if not prefix:
        return "\n".join(lines) + "\n"
    return "".join(f"{prefix} {line}\n" for line in lines)


# --- lint 규칙 ---


@dataclass
class Finding:
    """규칙 위반 하나. code는 문서·억제에 쓰는 안정된 식별자다(README 규칙 표 참고)."""

    path: str
    line: int
    level: str  # "error" | "warning"
    code: str
    message: str

    def format(self) -> str:
        # 편집기·CI가 바로 점프할 수 있는 컴파일러식 형식
        return f"{self.path}:{self.line}: {self.level}: {self.message} ({self.code})"


@dataclass
class LintContext:
    """규칙이 필드 밖에서 알아야 하는 것: 파일 위치, 저장소 루트, 옵션, 저장소 기본값."""

    path: str
    root: Path
    strict: bool = False
    default_license: str | None = None
    header: Header | None = None
    text: str = ""
    staged: bool = False  # True면 head_text와 비교하는 B8 검사를 한다
    head_text: str | None = None  # HEAD의 같은 파일(없으면 새 파일)


def parse_date(value) -> date | None:
    """헤더 날짜의 날짜 부분. 형식이 틀리거나 실존하지 않는 날짜·시각이면 None.

    순서 비교(B4)는 날짜 단위라 시각은 검증만 하고 버린다. 시간대가 없는 값이므로
    datetime 대신 date로 다룬다."""
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    day, _, clock = value.partition(" ")
    if clock and not (int(clock[:2]) < 24 and int(clock[3:]) < 60):
        return None
    try:
        return date.fromisoformat(day)
    except ValueError:
        return None


def _line(ctx: LintContext, key: str | None = None) -> int:
    """필드가 적힌 줄. 필드가 없으면(누락 등) 헤더 시작 줄."""
    header = ctx.header
    if header is None:
        return 1
    return header.lines.get(key, header.start) if key else header.start


def _finding(ctx, key, level, code, message) -> Finding:
    return Finding(ctx.path, _line(ctx, key), level, code, message)


def rule_required(fields, ctx):
    """F001 필수 필드 누락, F005 빈 필수 값(description만 경고: init이 일부러 비워 둔다)."""
    out = []
    for key in REQUIRED:
        if key not in fields:
            out.append(_finding(ctx, None, "error", "F001", f"required field '{key}' is missing"))
        elif fields[key] in ("", []):
            level = "warning" if key == "description" else "error"
            out.append(_finding(ctx, key, level, "F005", f"field '{key}' is empty"))
    return out


def rule_unknown(fields, ctx):
    """F002 모르는 필드. 오타를 잡으려는 것이라 기본은 경고, --strict면 오류."""
    level = "error" if ctx.strict else "warning"
    return [
        _finding(ctx, key, level, "F002", f"unknown field '{key}'")
        for key in fields
        if key not in REQUIRED and key not in OPTIONAL
    ]


def rule_types(fields, ctx):
    """F003 리스트여야 하는 필드가 스칼라, F004 스칼라여야 하는 필드가 리스트."""
    out = []
    for key, value in fields.items():
        if key in LIST_FIELDS and not isinstance(value, list) and value != "":
            out.append(_finding(ctx, key, "error", "F003", f"field '{key}' must be a list"))
        elif key not in LIST_FIELDS and (key in REQUIRED or key in OPTIONAL) and isinstance(value, list):
            out.append(_finding(ctx, key, "error", "F004", f"field '{key}' must be a scalar"))
    return out


def rule_status(fields, ctx):
    """S001 status 값이 정해진 다섯 가지가 아님."""
    status = fields.get("status")
    if status in (None, "") or status in STATUSES:
        return []
    return [_finding(ctx, "status", "error", "S001",
                     f"status '{status}' is not one of {', '.join(STATUSES)}")]


def rule_dates(fields, ctx):
    """D001 날짜 형식(YYYY-MM-DD 또는 YYYY-MM-DD HH:MM)·실존 날짜."""
    out = []
    for key in DATE_FIELDS:
        value = fields.get(key)
        if value in (None, "") or isinstance(value, list):
            continue
        if parse_date(value) is None:
            out.append(_finding(ctx, key, "error", "D001",
                                f"'{key}' must be a real date as YYYY-MM-DD or YYYY-MM-DD HH:MM"))
    return out


def _blank(fields, key) -> bool:
    return fields.get(key) in (None, "", [])


def rule_lifecycle(fields, ctx):
    """B1~B3 상태마다 있어야 하는 필드. 상태를 올렸으면 그 근거(검토자·날짜·후속)를 남기게 한다."""
    status = fields.get("status")
    out = []
    if status in ("review", "published", "deprecated", "archived") and _blank(fields, "reviewers"):
        out.append(_finding(ctx, "status", "error", "B1",
                            f"status '{status}' requires reviewers"))
    if status == "published":
        for key in ("reviewed_date", "published_date"):
            if _blank(fields, key):
                out.append(_finding(ctx, "status", "error", "B2",
                                    f"status 'published' requires {key}"))
    if status in ("deprecated", "archived"):
        for key in ("deprecated_date", "superseded_by"):
            if _blank(fields, key):
                out.append(_finding(ctx, "status", "error", "B3",
                                    f"status '{status}' requires {key}"))
    return out


def rule_date_order(fields, ctx):
    """B4 수명 주기 날짜 순서. 날짜 단위로 비교하고(같은 날 시각 차이는 허용), 빠진·틀린 날짜는 건너뛴다."""
    days = {}
    for key in DATE_FIELDS:
        parsed = parse_date(fields.get(key))
        if parsed is not None:
            days[key] = parsed
    chain = [k for k in ("created_date", "reviewed_date", "published_date", "deprecated_date")
             if k in days]
    pairs = list(pairwise(chain))
    if "created_date" in days and "updated_date" in days:
        pairs.append(("created_date", "updated_date"))
    return [
        _finding(ctx, later, "error", "B4", f"{later} ({days[later]}) is before {earlier} ({days[earlier]})")
        for earlier, later in pairs
        if days[later] < days[earlier]
    ]


# --- 라이선스 ---

# 오프라인에서 쓰는 SPDX 목록의 일부(흔히 쓰는 것). 여기 없는 것은 LicenseRef-로 쓴다.
SPDX_IDS = {i.lower(): i for i in (
    "0BSD", "AFL-3.0", "AGPL-1.0-only", "AGPL-1.0-or-later", "AGPL-3.0-only",
    "AGPL-3.0-or-later", "Apache-1.1", "Apache-2.0", "Artistic-2.0", "BlueOak-1.0.0",
    "BSD-1-Clause", "BSD-2-Clause", "BSD-2-Clause-Patent", "BSD-3-Clause",
    "BSD-3-Clause-Clear", "BSD-4-Clause", "BSL-1.0", "CC-BY-4.0", "CC-BY-SA-4.0",
    "CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "CC-BY-ND-4.0", "CC0-1.0", "CDDL-1.0", "CDDL-1.1",
    "CECILL-2.1", "EPL-1.0", "EPL-2.0", "EUPL-1.2", "GFDL-1.3-only", "GFDL-1.3-or-later",
    "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later", "ISC",
    "LGPL-2.0-only", "LGPL-2.0-or-later", "LGPL-2.1-only", "LGPL-2.1-or-later",
    "LGPL-3.0-only", "LGPL-3.0-or-later", "LPPL-1.3c", "MIT", "MIT-0", "MPL-1.1", "MPL-2.0",
    "MPL-2.0-no-copyleft-exception", "MS-PL", "MS-RL", "MulanPSL-2.0", "NCSA", "ODbL-1.0",
    "OFL-1.1", "OpenSSL", "OSL-3.0", "PostgreSQL", "PSF-2.0", "Python-2.0", "Ruby",
    "SSPL-1.0", "Unicode-3.0", "Unicode-DFS-2016", "Unlicense", "UPL-1.0", "Vim", "W3C",
    "WTFPL", "X11", "Zlib", "ZPL-2.1", "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0",
    "AGPL-3.0",
)}
SPDX_EXCEPTIONS = {e.lower() for e in (
    "Autoconf-exception-3.0", "Bison-exception-2.2", "Classpath-exception-2.0",
    "GCC-exception-2.0", "GCC-exception-3.1", "LLVM-exception",
    "OpenJDK-assembly-exception-1.0", "Qt-GPL-exception-1.0", "Qt-LGPL-exception-1.1",
    "Font-exception-2.0", "Linux-syscall-note", "openvpn-openssl-exception",
)}
SPDX_TOKEN_RE = re.compile(r"\(|\)|[A-Za-z0-9.+:-]+")
LICENSE_REF_RE = re.compile(r"^(DocumentRef-[A-Za-z0-9.-]+:)?LicenseRef-[A-Za-z0-9.-]+$")


def valid_spdx(expr: str) -> bool:
    """SPDX 라이선스 식인지. 문법: expr := and (OR and)*, and := atom (AND atom)*,
    atom := '(' expr ')' | id['+'] [WITH exception]. 연산자는 대소문자를 가리지 않는다."""
    if not isinstance(expr, str) or SPDX_TOKEN_RE.sub("", expr).strip():
        return False
    tokens = SPDX_TOKEN_RE.findall(expr)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        pos += 1
        return tokens[pos - 1]

    def atom() -> bool:
        tok = peek()
        if tok is None:
            return False
        if tok == "(":
            take()
            if not or_expr() or peek() != ")":
                return False
            take()
            return True
        if tok.upper() in ("AND", "OR", "WITH") or tok == ")":
            return False
        take()
        ident = tok.removesuffix("+")
        if ident.lower() not in SPDX_IDS and not LICENSE_REF_RE.match(ident):
            return False
        if (peek() or "").upper() == "WITH":
            take()
            exc = peek()
            if exc is None or exc.lower() not in SPDX_EXCEPTIONS:
                return False
            take()
        return True

    def and_expr() -> bool:
        if not atom():
            return False
        while (peek() or "").upper() == "AND":
            take()
            if not atom():
                return False
        return True

    def or_expr() -> bool:
        if not and_expr():
            return False
        while (peek() or "").upper() == "OR":
            take()
            if not and_expr():
                return False
        return True

    return or_expr() and pos == len(tokens)


def spdx_ids(expr: str) -> set[str]:
    """식에 든 라이선스 계열 이름(-only/-or-later/+를 뗀 소문자). 같은 계열인지 비교하는 데 쓴다."""
    out = set()
    for tok in SPDX_TOKEN_RE.findall(expr or ""):
        if tok in "()" or tok.upper() in ("AND", "OR", "WITH"):
            continue
        out.add(re.sub(r"(-only|-or-later|\+)$", "", tok.lower()))
    return out


# (감지할 SPDX, 첫머리에 모두 있어야 하는 문구). 위에서부터 먼저 맞는 것을 쓴다.
LICENSE_SIGNATURES = (
    ("AGPL-3.0-only", ("gnu affero general public license", "version 3")),
    ("LGPL-3.0-only", ("gnu lesser general public license", "version 3")),
    ("LGPL-2.1-only", ("gnu lesser general public license", "version 2.1")),
    ("GPL-3.0-only", ("gnu general public license", "version 3")),
    ("GPL-2.0-only", ("gnu general public license", "version 2")),
    ("Apache-2.0", ("apache license", "version 2.0")),
    ("MPL-2.0", ("mozilla public license", "2.0")),
    ("BSD-3-Clause", ("redistribution and use in source and binary forms", "neither the name")),
    ("BSD-2-Clause", ("redistribution and use in source and binary forms",)),
    ("MIT", ("permission is hereby granted, free of charge",)),
    ("ISC", ("permission to use, copy, modify, and/or distribute this software",)),
    ("Unlicense", ("this is free and unencumbered software",)),
)


def repo_license(root: Path) -> str | None:
    """저장소 LICENSE 파일 첫머리에서 기본 라이선스(SPDX)를 감지한다. 파일이 없거나 모르면 None.

    -only/-or-later는 본문으로 구분할 수 없어 -only로 본다(L2는 계열만 비교하므로 무관)."""
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        path = Path(root) / name
        if not path.is_file():
            continue
        head = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:40])
        m = re.search(SPDX_KEY + r":\s*(\S+)", head)
        if m:
            return m.group(1)
        lowered = " ".join(head.lower().split())
        for spdx, needles in LICENSE_SIGNATURES:
            if all(n in lowered for n in needles):
                return spdx
        return None
    return None


SPDX_LINE_RE = re.compile(SPDX_KEY + r":\s*['\"]?(.+?)['\"]?\s*(\*/|-->)?\s*$")


def leading_comment(text: str, header: Header):
    """(줄 번호, 줄) - 파일 머리부터 헤더 뒤에 이어지는 주석 블록 끝까지.

    SPDX 줄은 이 범위에서만 찾는다. 본문이나 문서 예시 속 문자열을 잘못 잡지 않기 위해서다."""
    lines = text.split("\n")
    end = header.end
    lead = header.prefix or "<!--"
    while end < len(lines) and lines[end].startswith(lead):
        end += 1
    return list(enumerate(lines[:end], start=1))


def rule_license(fields, ctx):
    """B5 SPDX 식, L1 SPDX-License-Identifier 줄과 license 불일치, L2 저장소 LICENSE와 다른 계열."""
    lic = fields.get("license")
    if not isinstance(lic, str) or lic == "":
        return []
    out = []
    if not valid_spdx(lic):
        out.append(_finding(ctx, "license", "error", "B5",
                            f"license '{lic}' is not an SPDX identifier or expression"))
    for lineno, line in leading_comment(ctx.text, ctx.header):
        m = SPDX_LINE_RE.search(line)
        if m and m.group(1) != lic:
            out.append(Finding(ctx.path, lineno, "error", "L1",
                               f"{SPDX_KEY} '{m.group(1)}' differs from license '{lic}'"))
    if ctx.default_license and not (spdx_ids(ctx.default_license) & spdx_ids(lic)):
        out.append(_finding(ctx, "license", "warning", "L2",
                            f"license '{lic}' differs from repository LICENSE ({ctx.default_license})"))
    return out


def rule_upstream(fields, ctx):
    """B6 외부에서 가져온 파일(upstream)은 THIRD_PARTY_NOTICES.md에 출처가 적혀 있어야 한다."""
    upstream = fields.get("upstream")
    if not isinstance(upstream, str) or not upstream:
        return []
    notices = Path(ctx.root) / "THIRD_PARTY_NOTICES.md"
    text = notices.read_text(encoding="utf-8", errors="replace") if notices.is_file() else ""
    if upstream in text:
        return []
    return [_finding(ctx, "upstream", "error", "B6",
                     f"upstream '{upstream}' is not listed in THIRD_PARTY_NOTICES.md")]


def rule_fresh(fields, ctx):
    """B8 (--staged만) 본문이 HEAD와 다른데 updated_date가 오늘이 아님. fix --staged를 건너뛴 커밋을 막는다."""
    if not ctx.staged:
        return []
    if ctx.head_text is not None and body_of(ctx.head_text, ctx.path) == body_of(ctx.text, ctx.path):
        return []
    updated = fields.get("updated_date")
    if not isinstance(updated, str) or parse_date(updated) is None or updated[:10] == today():
        return []  # 누락·형식 오류는 F001/D001이 보고한다
    return [_finding(ctx, "updated_date", "error", "B8",
                     f"content changed but updated_date is {updated}; run 'source-header fix --staged'")]


RULES = [rule_required, rule_unknown, rule_types, rule_status, rule_dates, rule_lifecycle,
         rule_date_order, rule_license, rule_upstream, rule_fresh]


def lint_text(text: str, path: str, ctx: LintContext) -> list[Finding]:
    """파일 텍스트 하나에 RULES를 모두 적용한다. 헤더가 없으면 H001/H002 하나만 보고한다."""
    header = extract_header(text, path)
    if header is None:
        prefix = prefix_for(path) or ""
        lines = text.split("\n")
        i = header_start(lines, prefix)
        opened = i < len(lines) and (_unprefix(lines[i], prefix) or "").strip() == "---"
        if opened:
            return [Finding(path, i + 1, "error", "H002", "header block is not closed")]
        return [Finding(path, 1, "error", "H001", "source header is missing")]
    ctx.header = header
    ctx.text = text
    out = []
    for rule in RULES:
        out.extend(rule(header.fields, ctx))
    return out


# --- CLI ---


def repo_root(cwd: Path) -> Path:
    """cwd가 속한 git 저장소의 최상위. git 저장소가 아니면 cwd 자체."""
    out = git(["rev-parse", "--show-toplevel"], cwd)
    return Path(out.strip()) if out else cwd


def git(args: list[str], cwd: Path) -> str | None:
    """git 명령 출력. 실패(저장소 아님, 파일 없음 등)하면 None."""
    try:
        res = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None
    return res.stdout if res.returncode == 0 else None


# --- 대상 선택 ---

CONFIG_NAME = ".source-header.json"
DEFAULT_INCLUDE = ["**"]
DEFAULT_EXCLUDE = ["**/node_modules/**", "**/.venv/**", "**/venv/**", "**/__pycache__/**",
                   "**/opensource/**", "**/.opensource/**", "**/backlog/**"]


def glob_re(pattern: str) -> re.Pattern:
    """저장소 상대 경로 글롭 → 정규식. `**`는 /를 넘고(`**/`는 0단계도), `*`·`?`는 넘지 않는다."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


@dataclass
class Workspace:
    """한 번 실행하는 동안의 위치 정보와 설정. 경로는 모두 resolve해서 비교한다(macOS /private 등)."""

    cwd: Path
    root: Path
    include: list
    exclude: list

    @classmethod
    def load(cls) -> Workspace:
        cwd = Path.cwd().resolve()
        root = repo_root(cwd).resolve()
        config = {}
        path = root / CONFIG_NAME
        if path.is_file():
            config = json.loads(path.read_text(encoding="utf-8"))
        # 설정 파일의 키는 기본값을 대체한다. .git은 언제나 제외한다.
        include = [glob_re(g) for g in config.get("include", DEFAULT_INCLUDE)]
        exclude = [glob_re(g) for g in [*config.get("exclude", DEFAULT_EXCLUDE), ".git/**",
                                        "**/.git/**"]]
        return cls(cwd, root, include, exclude)

    def rel(self, path: Path) -> str | None:
        """저장소 루트 기준 posix 경로. 저장소 밖이면 None."""
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return None

    def display(self, rel: str) -> str:
        """사람에게 보일 경로(cwd 기준)."""
        return os.path.relpath(self.root / rel, self.cwd)

    def selected(self, rel: str | None) -> bool:
        """헤더를 달 수 있는 형식이고 include에 걸리며 exclude에 안 걸리는가."""
        if rel is None:
            return False
        if prefix_for(rel) is None:
            return False
        if not any(p.match(rel) for p in self.include):
            return False
        return not any(p.match(rel) for p in self.exclude)

    def pruned(self, rel_dir: str) -> bool:
        """디렉터리 전체가 `<dir>/**` 꼴 exclude에 걸리면 내려가지 않는다(node_modules 등)."""
        return any(p.match(rel_dir + "/x") and p.pattern.endswith(".*\\Z") for p in self.exclude)


@dataclass
class Target:
    """검사할 파일 하나. text는 작업 트리 또는 인덱스에서 읽은 내용이다."""

    rel: str
    display: str
    text: str


def walk_targets(paths: list[str], ws: Workspace, missing: list | None = None) -> list[Target]:
    """경로 인자를 펼친다. 디렉터리는 재귀로, 대상 여부는 설정으로 거른다.

    없는 경로는 missing에 모은다. 오타 난 경로를 조용히 통과시키지 않기 위해서다."""
    seen: dict[str, Target] = {}
    for raw in paths:
        start = Path(raw)
        if start.is_file():
            files = [start]
        elif start.is_dir():
            files = []
            for dirpath, dirnames, filenames in os.walk(start):
                base = Path(dirpath)
                dirnames[:] = sorted(
                    d for d in dirnames
                    if d != ".git" and not ws.pruned(ws.rel(base / d) or "")
                )
                files.extend(base / f for f in sorted(filenames))
        else:
            print(f"source-header: {raw}: no such file or directory", file=sys.stderr)
            if missing is not None:
                missing.append(raw)
            continue
        for path in files:
            rel = ws.rel(path)
            if rel in seen or not ws.selected(rel):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            seen[rel] = Target(rel, ws.display(rel), text)
    return list(seen.values())


def staged_paths(ws: Workspace) -> list[str]:
    """추가·수정되어 stage된 파일(삭제 제외), 저장소 루트 기준."""
    out = git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], ws.root) or ""
    return [p for p in out.split("\0") if p]


def staged_targets(ws: Workspace) -> list[Target]:
    """인덱스의 내용(git show :path)을 읽는다. 커밋되는 것은 작업 트리가 아니라 인덱스다."""
    targets = []
    for rel in staged_paths(ws):
        if not ws.selected(rel):
            continue
        text = git(["show", f":{rel}"], ws.root)
        if text is not None:
            targets.append(Target(rel, ws.display(rel), text))
    return targets


def since_targets(ws: Workspace, ref: str) -> list[Target] | None:
    """ref 이후 바뀐(추가·수정) 파일의 작업 트리 내용. ref가 없으면 None."""
    if git(["rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"], ws.root) is None:
        return None
    out = git(["diff", "--name-only", "--diff-filter=ACMR", "-z", ref], ws.root) or ""
    targets = []
    for rel in sorted(p for p in out.split("\0") if p):
        path = ws.root / rel
        if ws.selected(rel) and path.is_file():
            targets.append(Target(rel, ws.display(rel),
                                  path.read_text(encoding="utf-8", errors="replace")))
    return targets


def cmd_lint(args) -> int:
    ws = Workspace.load()
    if args.staged:
        targets = staged_targets(ws)
    elif args.since:
        targets = since_targets(ws, args.since)
        if targets is None:
            print(f"source-header: unknown ref '{args.since}'", file=sys.stderr)
            return 2
    else:
        missing: list[str] = []
        targets = walk_targets(args.paths or ["."], ws, missing)
        if missing:
            return 2
    default_license = repo_license(ws.root)
    findings: list[Finding] = []
    for t in targets:
        ctx = LintContext(path=t.display, root=ws.root, strict=args.strict,
                          default_license=default_license, staged=args.staged)
        if args.staged:
            ctx.head_text = git(["show", f"HEAD:{t.rel}"], ws.root)
        findings.extend(lint_text(t.text, t.display, ctx))
    for f in findings:
        print(f.format())
    return 1 if any(f.level == "error" for f in findings) else 0


# --- git에서 유도하는 값 ---


def today() -> str:
    """로컬 시간대의 오늘. 사람이 커밋하는 날짜와 같아야 하므로 UTC가 아니라 로컬이다."""
    return datetime.now().astimezone().date().isoformat()


def git_created_date(root: Path, rel: str) -> str | None:
    """파일이 처음 추가된 커밋 날짜(YYYY-MM-DD). --follow로 이름 바뀐 파일도 원래 추가일을 찾는다.

    git log는 최신순이라 마지막 줄이 가장 오래된 추가다. 추적되지 않은 파일은 None."""
    out = git(["log", "--diff-filter=A", "--follow", "--format=%as", "--", rel], root)
    lines = [line for line in (out or "").splitlines() if line.strip()]
    return lines[-1] if lines else None


def git_last_date(root: Path, rel: str) -> str | None:
    """파일을 마지막으로 바꾼 커밋 날짜. 추적되지 않은 파일은 None."""
    out = (git(["log", "-1", "--follow", "--format=%as", "--", rel], root) or "").strip()
    return out or None


def git_user(root: Path) -> str | None:
    """git 사용자 이름. 이메일이 있으면 mailmap을 거친 정규 이름을 돌려준다(TASK-3#4).

    git_authors와 같은 이유로 git check-mailmap에 맡긴다. 옛 이름으로 설정된 기계에서
    새 파일을 만들어도 커밋된 파일과 같은 이름이 나와야 하기 때문이다."""
    name = (git(["config", "user.name"], root) or "").strip()
    email = (git(["config", "user.email"], root) or "").strip()
    if name and email:
        # 출력은 "이름 <이메일>"이다. 매핑이 없으면 입력이 그대로 돌아온다.
        out = (git(["check-mailmap", f"{name} <{email}>"], root) or "").strip()
        mapped = out.rsplit(" <", 1)[0].strip() if " <" in out else ""
        name = mapped or name
    return name or None


def git_authors(root: Path, rel: str) -> list[str]:
    """파일을 고친 git 작성자 이름, 처음 등장한 순서(오래된 것부터)로 중복 없이.

    TASK-3#4 이름은 %aN(대문자 N)으로 읽어 git mailmap을 거친다. 계정 이름이 바뀌면
    옛 커밋에 옛 이름이 남는데, .mailmap에 묶어 두면
    한 사람으로 나온다. .mailmap을 직접 파싱하지 않는 이유: git이 저장소 .mailmap뿐
    아니라 mailmap.file·mailmap.blob 설정까지 같은 규칙으로 해석해 주기 때문이다."""
    # --follow와 --reverse를 같이 쓰면 git이 이름 바뀌기 전 기록을 놓치므로 뒤집기는 여기서 한다.
    out = git(["log", "--follow", "--use-mailmap", "--format=%aN", "--", rel], root) or ""
    names: list[str] = []
    for name in reversed(out.splitlines()):
        if name.strip() and name not in names:
            names.append(name)
    return names


def derive_fields(ws: Workspace, rel: str, license_: str | None) -> dict:
    """init·new가 쓰는 새 헤더. 사람이 쓸 필드는 비워 두고, git이 아는 것만 채운다(B7).

    추적되지 않은 새 파일은 오늘 날짜와 git 사용자 이름을 쓴다. 라이선스는
    --license > 저장소 LICENSE > NOASSERTION(lint가 B5로 잡아 사람이 채우게 한다)."""
    created = git_created_date(ws.root, rel) or today()
    updated = git_last_date(ws.root, rel) or today()
    authors = git_authors(ws.root, rel) or [git_user(ws.root) or os.environ.get("USER", "unknown")]
    return {
        "title": PurePath(rel).stem,
        "description": "",
        "authors": authors,
        "license": license_ or repo_license(ws.root) or "NOASSERTION",
        "status": "draft",
        "created_date": created,
        "updated_date": max(created, updated),
    }


def insert_header(text: str, path, fields: dict) -> str:
    """헤더를 shebang·encoding 줄 바로 뒤(.md는 맨 앞)에 끼워 넣는다."""
    prefix = prefix_for(path) or ""
    lines = text.split("\n")
    i = header_start(lines, prefix)
    block = render_header(fields, prefix).rstrip("\n").split("\n")
    return "\n".join(lines[:i] + block + lines[i:])


def cmd_init(args) -> int:
    """헤더가 없는 파일에만 넣는다. 이미 있으면 건드리지 않으므로 몇 번을 돌려도 같다."""
    ws = Workspace.load()
    for t in walk_targets(args.paths or ["."], ws):
        if extract_header(t.text, t.rel) is not None:
            continue
        fields = derive_fields(ws, t.rel, args.license)
        (ws.root / t.rel).write_text(insert_header(t.text, t.rel, fields), encoding="utf-8")
        print(f"{t.display}: header added")
    return 0


# --- fix ---


def body_of(text: str, path) -> str:
    """헤더 줄을 뺀 나머지. updated_date 갱신 여부는 헤더가 아니라 이 본문이 바뀌었는지로 정한다."""
    header = extract_header(text, path)
    if header is None:
        return text
    lines = text.split("\n")
    return "\n".join(lines[:header.start - 1] + lines[header.end:])


def set_field(text: str, path, key: str, value) -> str:
    """헤더의 필드 한 줄만 바꾼다. 다시 render하지 않으므로 다른 줄과 줄 끝 설명 주석이 그대로 남는다."""
    header = extract_header(text, path)
    if header is None:
        return text
    lines = text.split("\n")
    rendered = f"{key}: {render_value(value)}"
    if key in header.lines:
        i = header.lines[key] - 1
        inner = _unprefix(lines[i], header.prefix) or ""
        comment = inner[len(strip_yaml_comment(inner)):]
        lines[i] = (f"{header.prefix} " if header.prefix else "") + rendered + comment
    else:
        lines.insert(header.end - 1, (f"{header.prefix} " if header.prefix else "") + rendered)
    return "\n".join(lines)


def stamp_like(old) -> str:
    """오늘 날짜를 기존 값과 같은 형식으로(HH:MM이 있었으면 지금 시각까지)."""
    if isinstance(old, str) and parse_date(old) and " " in old:
        return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    return today()


def cmd_fix(args) -> int:
    """staged 파일의 updated_date를 맞추고 다시 stage한다(B8). 일부만 staged면 손대지 않는다(B9).

    부분 staged 파일을 고쳐 git add하면 stage하지 않은 변경까지 커밋에 섞이므로, 오류로 멈추고
    사람이 정리하게 한다."""
    if not args.staged:
        print("source-header: fix needs --staged", file=sys.stderr)
        return 2
    ws = Workspace.load()
    status = 0
    for rel in staged_paths(ws):
        if not ws.selected(rel):
            continue
        staged = git(["show", f":{rel}"], ws.root)
        header = extract_header(staged or "", rel)
        if header is None:
            continue  # 헤더가 없는 파일은 lint가 H001로 잡는다
        if git(["diff", "--name-only", "--", rel], ws.root):
            print(Finding(ws.display(rel), 1, "error", "B9",
                          "partially staged; stage or stash the rest, then run fix again").format())
            status = 1
            continue
        head = git(["show", f"HEAD:{rel}"], ws.root)
        if head is not None and body_of(head, rel) == body_of(staged, rel):
            continue
        old = header.fields.get("updated_date")
        if isinstance(old, str) and old[:10] == today():
            continue
        new = stamp_like(old)
        (ws.root / rel).write_text(set_field(staged, rel, "updated_date", new), encoding="utf-8")
        git(["add", "--", rel], ws.root)
        print(f"{ws.display(rel)}: updated_date {old} -> {new}")
    return status


# --- status · new ---


def cmd_status(args) -> int:
    """헤더를 모아 상태 표를 낸다. 파일이 SSOT이므로 이 표가 곧 프로젝트 상태 조회다."""
    ws = Workspace.load()
    rows = []
    for t in sorted(walk_targets(args.paths or ["."], ws), key=lambda t: t.display):
        header = extract_header(t.text, t.rel)
        if header is None:
            continue
        f = header.fields
        status, task = str(f.get("status") or "-"), str(f.get("task") or "-")
        if args.status and status != args.status:
            continue
        if args.task and task.upper() != args.task.upper():
            continue
        rows.append((status, t.display, task, str(f.get("updated_date") or "-")))
    table = [("STATUS", "FILE", "TASK", "UPDATED"), *rows]
    widths = [max(len(row[i]) for row in table) for i in range(3)]
    for row in table:
        print("  ".join(cell.ljust(w) for cell, w in zip(row, widths)) + "  " + row[3])
    return 0


SHEBANGS = {".sh": "#!/usr/bin/env bash", ".bash": "#!/usr/bin/env bash"}


def cmd_new(args) -> int:
    """헤더가 들어간 새 파일을 만든다. 처음부터 헤더를 쓰게 하는 가장 쉬운 길이다."""
    ws = Workspace.load()
    path = Path(args.path)
    if prefix_for(path) is None:
        print(f"source-header: {args.path}: no comment syntax for this file type", file=sys.stderr)
        return 2
    if path.exists():
        print(f"source-header: {args.path}: already exists", file=sys.stderr)
        return 1
    rel = ws.rel(path.parent.resolve() / path.name) or path.name
    fields = derive_fields(ws, rel, args.license)
    fields.update(title=args.title, description=args.description or "")
    if args.task:
        fields["task"] = args.task
    shebang = SHEBANGS.get(path.suffix.lower())
    text = (shebang + "\n" if shebang else "") + render_header(fields, prefix_for(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"{args.path}: created")
    return 0


# --- git 훅 진입점 ---

HOOKS = ["pre-commit"]


def cmd_hook(args) -> int:
    """git 훅이 부르는 진입점. 지금은 pre-commit = fix --staged → lint --staged.

    훅 연결(.githooks 디스패처, core.hooksPath)은 coding-agent-git-commit-tool이 맡고, 여기서는
    부를 명령만 준다. 로직은 cmd_fix·cmd_lint를 그대로 재사용한다.
    - B2: 저장소 루트에 .source-header.json이 없으면 아무것도 하지 않는다(opt-in). 디스패처가
      모든 저장소에 같은 훅을 걸어도, 헤더를 도입하지 않은 저장소의 커밋은 막지 않기 위해서다.
    - B1: fix가 실패하면 lint를 돌리지 않고 그 코드로 끝낸다. fix가 손대지 못한(부분 staged)
      상태에서 lint까지 돌면 같은 파일을 두 번 보고해 원인이 흐려진다."""
    root = repo_root(Path.cwd().resolve())
    if not (root / CONFIG_NAME).is_file():
        return 0
    staged = argparse.Namespace(staged=True, since=None, paths=[], strict=False)
    code = cmd_fix(staged)
    if code != 0:
        return code
    return cmd_lint(staged)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="source-header", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("lint", help="헤더 규칙 검사")
    p.add_argument("paths", nargs="*", help="파일·디렉터리(재귀). 기본은 현재 디렉터리")
    p.add_argument("--staged", action="store_true", help="인덱스에 stage된 내용을 검사")
    p.add_argument("--since", metavar="REF", help="REF 이후 바뀐 파일만 검사(CI용)")
    p.add_argument("--strict", action="store_true", help="모르는 필드도 오류로")
    p.set_defaults(func=cmd_lint)
    p = sub.add_parser("init", help="헤더 없는 파일에 git에서 유도한 헤더를 넣는다")
    p.add_argument("paths", nargs="*", help="파일·디렉터리(재귀). 기본은 현재 디렉터리")
    p.add_argument("--license", help="저장소 LICENSE 대신 쓸 SPDX 식")
    p.set_defaults(func=cmd_init)
    p = sub.add_parser("fix", help="staged 파일의 updated_date를 고치고 다시 stage")
    p.add_argument("--staged", action="store_true", help="stage된 파일을 대상으로(필수)")
    p.set_defaults(func=cmd_fix)
    p = sub.add_parser("status", help="헤더를 모아 STATUS·FILE·TASK·UPDATED 표 출력")
    p.add_argument("paths", nargs="*", help="파일·디렉터리(재귀). 기본은 현재 디렉터리")
    p.add_argument("--status", choices=STATUSES, help="이 status만")
    p.add_argument("--task", help="이 task ID만(대소문자 무시)")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("new", help="헤더가 들어간 새 파일 만들기")
    p.add_argument("path")
    p.add_argument("--title", required=True)
    p.add_argument("--task")
    p.add_argument("--description")
    p.add_argument("--license", help="저장소 LICENSE 대신 쓸 SPDX 식")
    p.set_defaults(func=cmd_new)
    p = sub.add_parser("hook", help="git 훅 진입점(.source-header.json이 있는 저장소에서만 동작)")
    # 훅 이름을 선택지로 두어 나중에 commit-msg 등을 같은 자리에 더할 수 있게 한다.
    p.add_argument("name", choices=HOOKS, help="pre-commit: fix --staged 후 lint --staged")
    p.set_defaults(func=cmd_hook)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

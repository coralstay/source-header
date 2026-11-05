---
title: source-header
description: 소스 파일 머리 주석 YAML 헤더의 규칙과 사용법
authors: [coralstay]
license: AGPL-3.0-only
status: draft
task: TASK-1
created_date: '2026-10-31'
updated_date: '2026-10-31'
---

# source-header

프로젝트 상태 관리와 간단한 소스 코드 관리의 SSOT는 **소스 파일 자체와 그 머리 주석**이다.
`source-header`는 파일 맨 위 주석 안의 YAML 헤더(Backlog.md 필드 관례)를 검사하고, git에서
알 수 있는 값을 채우고, 커밋 때 `updated_date`를 맞춘다.

- 단일 파일 `source-header.py`, 표준 라이브러리만 쓴다(Python 3.12 + git).
- 헤더 파서는 agile-hooks `scripts/work_order.py`의 `parse_frontmatter` 사본이다. 원본과 같은
  결과를 내는지 테스트가 확인한다.
- 이 저장소에는 아직 `LICENSE` 파일이 없다. 헤더는 다른 저장소들과 같은 `AGPL-3.0-only`를 쓴다.

## 헤더 형식

shebang·encoding 줄 다음에, 언어의 주석 접두사를 붙인 `---` YAML 블록을 둔다. 닫는 `---` 뒤의
주석은 자유 서술(설계 메모)이다.

```python
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
# [설계 메모] 이후 자유 서술
```

| 접두사 | 확장자 |
|---|---|
| `#` | py sh bash yaml yml toml rb |
| `//` | js ts tsx jsx go rs java c h cpp hpp kt swift |
| `--` | sql lua |
| (없음) | md — 1번 줄의 일반 `---` 블록 |

그 밖의 형식(JSON, lock 파일 등 주석을 못 다는 파일)은 대상이 아니다.

- 값은 Backlog.md가 쓰는 YAML 부분집합이다: 스칼라, 따옴표 문자열, `[a, b]`, `- item` 블록 리스트.
- 날짜는 `YYYY-MM-DD` 또는 `YYYY-MM-DD HH:MM`(따옴표는 있어도 없어도 된다). 실존하는 날짜여야 한다.
- 헤더 안의 YAML 주석(` # ...`, `# ...` 줄)은 무시한다. 그래서 템플릿처럼 필드마다 설명을 달 수 있다.
  값에 ` #`이 들어가야 하면 따옴표로 감싼다.
- `SPDX-License-Identifier:` 줄(REUSE 관례)은 헤더 필드로 써도, 헤더 바로 뒤 주석에 써도 된다.
  없어도 되고, 있으면 `license`와 같아야 한다.

### 필드

| 필드 | 필수 | 형식 | 누가 채우나 |
|---|---|---|---|
| title | 필수 | str | 사람 (init은 파일 이름) |
| description | 필수 | str | 사람 (init은 비워 두고 F005 경고) |
| authors | 필수 | list | git 작성자 (init) |
| license | 필수 | SPDX 식 | 저장소 LICENSE (init), 없으면 `--license` 또는 NOASSERTION |
| status | 필수 | draft · review · published · deprecated · archived | 사람 |
| created_date | 필수 | date | 처음 추가된 커밋 날짜 (init) |
| updated_date | 필수 | date | 본문이 바뀐 커밋 날짜 (fix --staged) |
| task | 선택 | str | 사람 — Backlog.md 카드 ID |
| reviewers | 선택 | list | 사람 |
| reviewed_date · published_date · deprecated_date | 선택 | date | 사람 |
| superseded_by | 선택 | str | 사람 — 대신 쓸 파일 |
| labels | 선택 | list | 사람 |
| version | 선택 | str | 사람 |
| upstream | 선택 | str | 사람 — 외부에서 가져온 파일의 출처 |

`render`는 필드를 위 순서(`FIELD_ORDER`)로 쓰고, 모르는 필드는 그 뒤에 원래 순서대로 보존한다.

## 규칙

출력은 `path:line: level: message (code)`이고, 오류가 하나라도 있으면 exit 1이다.

| 코드 | 수준 | 내용 |
|---|---|---|
| H001 | error | 헤더가 없다 |
| H002 | error | 헤더 블록이 닫히지 않았다 |
| F001 | error | 필수 필드 누락 |
| F002 | warning (`--strict`면 error) | 모르는 필드 |
| F003 | error | authors · reviewers · labels가 리스트가 아니다 |
| F004 | error | 스칼라여야 하는 필드가 리스트다 |
| F005 | error (description만 warning) | 필수 필드 값이 비었다 |
| S001 | error | status가 정해진 다섯 값이 아니다 |
| D001 | error | 날짜 형식이 틀렸거나 없는 날짜다 |
| B1 | error | review · published · deprecated · archived면 reviewers가 있어야 한다 |
| B2 | error | published면 reviewed_date와 published_date가 있어야 한다 |
| B3 | error | deprecated · archived면 deprecated_date와 superseded_by가 있어야 한다 |
| B4 | error | created ≤ reviewed ≤ published ≤ deprecated, created ≤ updated (날짜 단위 비교) |
| B5 | error | license가 SPDX 식별자 또는 AND/OR/WITH 식이 아니다 |
| B6 | error | upstream이 THIRD_PARTY_NOTICES.md에 적혀 있지 않다 |
| B8 | error | (`lint --staged`) 본문이 HEAD와 다른데 updated_date가 오늘이 아니다 |
| B9 | error | (`fix --staged`) 일부만 staged된 파일이라 고치지 않았다 |
| L1 | error | SPDX-License-Identifier 줄이 license와 다르다 |
| L2 | warning | license가 저장소 LICENSE와 다른 계열이다 (-only/-or-later 차이는 같은 계열) |

B1~B9는 TASK-1 카드의 비즈니스 규칙 번호와 같다. B7은 `init`이 값을 유도하는 규칙(created_date =
처음 추가된 커밋, authors = git 작성자, license = 저장소 LICENSE)이라 lint 코드가 없다.

SPDX 식별자는 흔히 쓰는 것만 도구 안 목록(`SPDX_IDS`)에 있다. 목록에 없는 라이선스는
`LicenseRef-<이름>`으로 쓴다. 저장소 LICENSE 감지는 AGPL-3.0, LGPL, GPL-3.0/2.0, Apache-2.0,
MPL-2.0, BSD-3/2-Clause, MIT, ISC, Unlicense 본문 첫머리와 `SPDX-License-Identifier:` 줄을 본다.

## status 전이

| status | 뜻 | 들어가려면 |
|---|---|---|
| draft | 작성 중. 새 파일과 init의 기본값 | — |
| review | 검토 중 | reviewers (B1) |
| published | 검토를 마치고 쓰는 중 | reviewers, reviewed_date, published_date (B1, B2) |
| deprecated | 아직 있지만 쓰지 말 것 | reviewers, deprecated_date, superseded_by (B1, B3) |
| archived | 더 이상 유지하지 않음 | reviewers, deprecated_date, superseded_by (B1, B3) |

보통 흐름은 `draft → review → published → deprecated → archived`이고, 검토에서 되돌아가면
`review → draft`다. 도구는 전이 순서 자체를 막지 않고, 각 status에 필요한 필드와 날짜 순서(B4)만
검사한다.

## 사용법

```sh
source-header lint [paths...]          # 파일·디렉터리(재귀) 검사. 기본은 현재 디렉터리
source-header lint --strict .          # 모르는 필드도 오류
source-header lint --staged            # 인덱스(git show :path)의 커밋될 내용 검사 + B8
source-header lint --since origin/main # CI: 그 ref 이후 바뀐 파일만
source-header init [paths...] [--license SPDX]   # 헤더 없는 파일에 git 유도 헤더 삽입(멱등)
source-header fix --staged             # staged 파일의 updated_date를 오늘로 맞추고 다시 git add
source-header status [--status published] [--task TASK-1]   # STATUS·FILE·TASK·UPDATED 표
source-header new path/to/file.py --title 이름 [--task TASK-1] [--description 설명] [--license SPDX]
source-header hook pre-commit          # git pre-commit 진입점: fix --staged → lint --staged
```

실행 파일은 `~/githubs/bin/source-header` → `../dev-tools/source-header/source-header.py`
심볼릭 링크다. `~/githubs/bin`을 PATH에 두면 어디서든 `source-header`로 부를 수 있다.

### git pre-commit 훅 `source-header hook pre-commit`

- 저장소 루트에 `.source-header.json`이 없으면 아무것도 하지 않고 exit 0이다(opt-in, B2).
  헤더를 도입한 저장소만 빈 `{}`라도 이 파일을 두면 된다.
- 있으면 `fix --staged`를 먼저 돌린다. fix가 실패하면(예: 일부만 staged된 파일, B9) lint를
  돌리지 않고 그 exit 코드로 끝낸다(B1).
- fix가 성공하면 `lint --staged`를 돌리고 그 exit 코드를 돌려준다. 오류가 있으면 1이라 커밋이
  막힌다.

저장소에 훅을 거는 일은 이 도구가 하지 않는다. coding-agent-git-commit-tool의 `.githooks`
디스패처(`core.hooksPath`)가 `pre-commit.d/20-source-header`에서 이 명령을 부른다.

### 대상 선택 `.source-header.json`

저장소 루트에 두면 대상 파일을 거른다. 글롭은 저장소 기준 경로 전체에 맞춘다. `**`는 `/`를
넘고(`**/`는 0단계도 포함), `*`·`?`는 넘지 않는다.

```json
{ "include": ["src/**", "*.py"], "exclude": ["src/generated/**"] }
```

- 키가 있으면 그 키의 기본값을 대체한다. `.git`은 언제나 제외한다.
- 기본값: include `**`, exclude `**/node_modules/**`, `**/.venv/**`, `**/venv/**`,
  `**/__pycache__/**`, `**/opensource/**`, `**/.opensource/**`, `**/backlog/**`.
- 어느 경우든 주석 접두사를 아는 확장자만 대상이다.

### fix가 하는 일과 하지 않는 일

- 본문(헤더를 뺀 나머지)이 HEAD와 다르거나 HEAD에 없는 새 파일이면 `updated_date`를 오늘로
  바꾼다(B8). 헤더만 바뀐 경우는 그대로 둔다. 기존 값에 `HH:MM`이 있었으면 지금 시각까지 쓴다.
- `updated_date` 줄 하나만 바꾸므로 다른 줄과 줄 끝 설명 주석은 그대로다.
- 일부만 staged된 파일(작업 트리에 stage하지 않은 변경이 더 있는 파일)은 고치지 않고 B9 오류로
  exit 1이다. 고친 뒤 `git add`하면 stage하지 않은 변경까지 커밋에 섞이기 때문이다.

### authors와 `.mailmap`

`init`·`new`의 authors는 git mailmap을 거친 이름이다(`git log --use-mailmap --format=%aN`,
추적 안 된 파일의 git 사용자는 `git check-mailmap`). 도구가 `.mailmap`을 직접 읽지 않고 git에
맡기므로 저장소의 `.mailmap`뿐 아니라 `mailmap.file`·`mailmap.blob` 설정도 그대로 따른다.
같은 사람이 여러 이름으로 나오면 처음 등장한 순서로 한 번만 쓴다.

계정 이름이 바뀌어 옛 커밋에 옛 이름·이메일이 남아 있으면
저장소 루트 `.mailmap`에 정규 이름으로 묶는다.

```text
# 정규 이름 <정규 이메일>  옛 이름 <옛 이메일>
new-name <new-name@example.com> old-me <old-me@example.com>
new-name <new-name@example.com> <12345+old-name@users.noreply.github.com>
```

저장소마다 두기 싫으면 `git config --global mailmap.file ~/.mailmap`으로 한 파일을 함께 쓴다.

## 템플릿

`templates/`에 언어별 시작 파일이 있다(python.py, shell.sh, typescript.ts, go.go, sql.sql,
markdown.md). 필드마다 `# 필수 · date · ...` 꼴의 설명 주석이 붙어 있고, 선택 필드는 주석 처리돼
있다. 복사해서 값만 바꿔 쓰면 된다.

## 개발

```sh
uvx --with pytest pytest -q -p no:cacheprovider   # 또는 python3 -m unittest -q
ruff check .
python3 source-header.py lint .
```

## 라이선스

AGPL-3.0-only. 전문은 [LICENSE](LICENSE)에 있다(형제 저장소 claude-code-agile-hooks의
LICENSE와 같은 GNU Affero General Public License v3.0 원문).

이 저장소의 소스 파일 헤더는 `license: AGPL-3.0-only`를 쓴다. `source-header lint`는 저장소
LICENSE에서 AGPL-3.0을 감지해 헤더의 license와 계열이 다르면 L2 경고를 낸다.

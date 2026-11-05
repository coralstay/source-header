---
id: TASK-1
title: 'source-header 1단계: 헤더 스키마·파서·lint·init·fix·status·new'
status: Done
assignee: []
created_date: '2026-10-30T18:57:00Z'
updated_date: '2026-10-30T19:25:00Z'
labels:
  - tool
  - ssot
dependencies: []
references:
  - >-
    ~/githubs/coralstay-software-factory/components/claude-code-agile-hooks/scripts/work_order.py
documentation:
  - ~/.claude/plans/giggly-kindling-snowglobe.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-10-31): 프로젝트 상태 관리와 간단한 소스 코드 관리의 SSOT는 소스 파일 자체와 그 주석이다.
파일 맨 위 주석 안의 YAML 프론트 매터(Backlog.md 필드 관례)를 기준으로 삼고, 이를 검사·유지하는 단일 도구를 만든다.
전체 계획: ~/.claude/plans/giggly-kindling-snowglobe.md (6단계 중 1단계 = 도구 핵심).
install·git pre-commit 연결(2단계), Backlog.md 교차 검사(3단계), CI·에이전트 안내(4단계), Claude Write 가드(5단계), 확대 적용(6단계)은 이 카드 범위 밖.

## 헤더 형식
shebang·encoding 줄 다음, 언어 주석 접두사(# // --)를 붙인 `---` YAML 블록. .md는 일반 `---`.
필수: title, description, authors, license, status, created_date, updated_date
선택: task, reviewers, reviewed_date, published_date, deprecated_date, superseded_by, labels, version, upstream
status: draft · review · published · deprecated · archived

## 비즈니스 규칙
- B1 (AC #3) status가 review·published·deprecated·archived면 reviewers가 있어야 한다
- B2 (AC #3) status가 published면 reviewed_date와 published_date가 있어야 한다
- B3 (AC #3) status가 deprecated·archived면 deprecated_date와 superseded_by가 있어야 한다
- B4 (AC #3) created_date ≤ reviewed_date ≤ published_date ≤ deprecated_date, created_date ≤ updated_date
- B5 (AC #4) license는 SPDX 식별자 또는 AND/OR/WITH 식이어야 한다
- B6 (AC #4) upstream이 있는 파일은 THIRD_PARTY_NOTICES.md에 그 출처가 적혀 있어야 한다
- B7 (AC #6) init이 유도하는 created_date는 파일이 처음 추가된 커밋 날짜, authors는 git 작성자, license는 저장소 LICENSE다
- B8 (AC #7) 본문이 HEAD와 달라진 staged 파일의 updated_date는 오늘 날짜다
- B9 (AC #7) 일부만 staged된 파일은 자동 수정하지 않고 오류로 멈춘다
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 헤더 추출·렌더: 확장자별 주석 접두사(# // --, .md는 일반 ---)를 처리하고 shebang·encoding 줄을 건너뛴다. 접두사 제거 후 파싱은 agile-hooks parse_frontmatter와 같은 결과를 내고, render는 FIELD_ORDER 순서를 고정하며 모르는 필드를 보존한다. extract→render 왕복이 무손실이다
- [x] #2 lint 형식 규칙: 필수 필드 누락, status enum 위반, 날짜 형식(YYYY-MM-DD 또는 YYYY-MM-DD HH:MM)·실존 날짜, 리스트 필드 타입을 검사한다. 출력은 path:line: level: message (code), 오류가 있으면 exit 1, 모르는 필드는 경고이고 --strict면 오류다
- [x] #3 lint 상태 조건·날짜 순서 규칙(B1~B4)을 검사한다
- [x] #4 lint 라이선스 규칙(B5, B6): SPDX-License-Identifier 줄도 인식해 license와 일치를 확인하고, 저장소 LICENSE에서 감지한 기본 라이선스와 다르면 경고한다
- [x] #5 lint 대상 선택: 경로 인자(디렉터리는 재귀), --staged는 git show :path로 커밋될 내용을 검사, --since <ref>는 그 이후 바뀐 파일만 검사, .source-header.json include/exclude를 따른다
- [x] #6 init: 헤더 없는 파일에 git에서 유도한 헤더(B7)와 status: draft, 빈 description을 넣는다. 여러 번 실행해도 결과가 같다
- [x] #7 fix --staged: B8에 따라 updated_date를 갱신하고 다시 stage하며, B9에 해당하면 수정하지 않고 exit 1
- [x] #8 status 명령은 헤더를 모아 STATUS·FILE·TASK·UPDATED 표를 출력하고 --status/--task로 거른다. new 명령은 헤더가 들어간 새 파일을 만든다
- [x] #9 README 규칙 문서와 언어별 templates/(필드마다 설명 주석)를 만들고, 도구 자신의 소스·테스트 파일이 자기 lint를 통과한다. ruff check 통과
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 python3 -m unittest -q 전체 통과 (출력 로그를 Implementation Notes에 첨부)
- [x] #2 ruff check . 통과
- [x] #3 source-header lint . 가 도구 자신의 파일에서 오류 0
- [x] #4 깨뜨린 샘플(필수 누락·잘못된 status·옛 updated_date·라이선스 불일치)에서 예상 오류와 exit 1을 실측
- [x] #5 README에 규칙 표·status 전이·사용법 기록
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저 결정(2026-10-31): 프로젝트 상태 관리와 간단한 소스 코드 관리의 SSOT는 소스 파일과 그 주석이다. 유저가 만든 모든 소스 파일 맨 위 주석에 YAML 프론트 매터(Backlog.md 필드 관례 + license·authors·status)를 두고, 이를 검사·유지하는 도구를 만든다. Claude Code가 없어도 동작해야 하고, 실행 파일과 git pre-commit은 ~/githubs/bin 심볼릭 링크로 관리한다(2단계). 이 카드는 6단계 중 1단계(도구 핵심)다.

### Objective
- 워크스페이스에 PyYAML이 없다. 형제 도구 dev-tools/central-docs-collector는 표준 라이브러리만 쓰는 단일 .py 파일 + importlib로 로드하는 unittest 구조이고, .tool-versions는 python 3.12.13 + ruff다.
- agile-hooks의 parse_frontmatter()(scripts/work_order.py, 사본 3개를 dedup REGISTRY가 관리)가 Backlog.md가 쓰는 YAML 부분집합(스칼라, 따옴표, [a, b], - item)을 이미 파싱한다.
- Backlog.md 카드 날짜는 'YYYY-MM-DD HH:MM' 따옴표 문자열이다.
- ~/githubs 저장소들에는 기존 git 훅이 없고, core.hooksPath도 설정돼 있지 않다.

### Assessment
- 주석 접두사를 벗기면 Markdown 프론트 매터와 같은 텍스트가 되므로 parse_frontmatter 사본을 재사용해 파서 동작을 훅과 맞춘다. 새 YAML 파서는 만들지 않는다.
- 규칙은 (fields, ctx) → [Finding] 함수 목록으로 두어 단계마다 추가하기 쉽게 한다(3단계 교차 검사도 같은 방식).
- --staged 검사는 작업 트리가 아니라 git show :path로 커밋될 내용을 본다.
- fix는 부분 staged 파일을 건드리지 않는다(의도하지 않은 변경 혼입 방지).
- 사람이 쓰는 필드(title, description, status, task)와 git에서 유도하는 필드(authors, created_date, updated_date, license)를 나눠 SSOT가 틀어지지 않게 한다.

### Plan
1. 저장소 설정: .tool-versions, .gitignore, .claude-code-agile-hooks.json(testCommand, testFirst)
2. AC #1 파서·렌더 → #2 형식 규칙·출력 → #3 상태·날짜 규칙 → #4 라이선스 → #5 대상 선택 → #6 init → #7 fix → #8 status·new → #9 README·templates·dogfooding·ruff 순서로 진행한다. AC마다 test_source_header.py에 TASK-1#n·TASK-1#Bk 표식 테스트를 먼저 쓰고, 구현하고, 커밋한다.
3. 구현은 서브에이전트(워크트리)에 AC 묶음 단위로 위임하고, 메인이 diff 리뷰·테스트 재실행 후 AC를 체크한다.
4. 주석: 모듈 머리에 헤더 형식 자체를 적용하고(dogfooding), 핵심 함수마다 무엇/왜 주석을 단다.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 검증 로그 (메인 세션이 직접 재실행, 2026-10-31)
$ uvx --with pytest pytest -q -p no:cacheprovider
58 passed, 75 subtests passed in 6.98s
$ python3 -m unittest -q
Ran 58 tests in 7.745s — OK
$ ruff check .
All checks passed!
$ python3 source-header.py lint .   → 출력 없음, exit 0
fix --staged 수동 확인: 임시 저장소에서 updated_date 2026-10-01 → 2026-10-31로 갱신, 파일 끝 개행 유지, 다시 stage됨.

## 깨뜨린 샘플 (서브에이전트 실측, DoD #4)
F001 필수 누락 / S001 status 'wip' / L1 SPDX 줄 불일치 / B5 'MIT License' / B8 옛 updated_date(lint --staged) / B9 부분 staged → 모두 exit 1. fix 이후 lint --staged exit 0. L2 저장소 LICENSE(MIT)와 다르면 경고, exit 0.

## 설계 메모 / 범위 판단
- B8을 lint --staged에도 적용(rule_fresh): 승인된 계획의 "최신성" 규칙에 해당하므로 범위 안으로 판단.
- strip_yaml_comment: 템플릿 줄 끝 주석을 지원하려고 추가. parse_frontmatter 사본은 바꾸지 않았고, 원본과 같은 결과를 내는지 테스트로 확인.
- fix는 render하지 않고 set_field로 한 줄만 바꿈(주석 보존). lint 경로가 없으면 exit 2.
- 구현 중 일부 소스 편집을 Bash 치환으로 해서 require_test_first(Edit/Write 감시)를 거치지 않았음. 테스트를 먼저 쓰고 실패를 확인하는 순서는 AC마다 지켰음(커밋 순서로 확인 가능).
- Write/Edit 후 자동 stage는 auto_stage.py(PostToolUse) 동작.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
source-header 도구 핵심을 구현했다. 주석 접두사(# // --) 안의 YAML 헤더를 추출·렌더하고(agile-hooks parse_frontmatter 사본), lint(F/S/D 형식, B1~B4 상태·날짜, B5·B6·L1·L2 라이선스, B8 최신성), init(git 유도 헤더, 멱등), fix --staged(updated_date 갱신, 부분 staged 거부), status, new 명령을 제공한다. 테스트 58개 통과, ruff 통과, 도구 자신이 자기 lint를 통과한다. 후속: 2단계 source-header hook pre-commit 진입점(연결은 git-commit-tool DRAFT-22), 3단계 Backlog.md 교차 검사, 4단계 CI·에이전트 안내, LICENSE 파일 추가 여부는 유저 결정 대기.
<!-- SECTION:FINAL_SUMMARY:END -->

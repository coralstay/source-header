---
id: DRAFT-10
title: 'README: 헤더 주석이 ruff ERA001에 오탐되는 문제와 해결 안내'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
updated_date: '2026-11-11T11:34:00Z'
labels:
  - source-header
  - followup
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
doctree에서 프론트매터 헤더(`# title: ...`)와 하단 노트(`# 1 제목`)가 ruff ERA001(주석 처리된 코드)에 306개 오류로 잡혔다(main은 0). 해결: pyproject에 `[tool.ruff.lint.per-file-ignores]`로 src·tests의 ERA001을 무시(doctree 커밋 3304c28). 다른 저장소는 영향이 없었다(ERA 미선택).

## 범위
source-header README에 '린터와의 충돌' 절을 추가한다: ERA001 오탐 원인, 무시 설정 예, 헤더가 코드로 오탐되는 다른 규칙이 있는지 확인한 범위(ruff 기본 + ERA).

## 완료 기준 (승격 후 --ac로 등록)
1. README에 절이 있고 예시 설정이 실제로 오류 0을 만든다(doctree에서 확인).
2. 도구 테스트(README 검사)가 통과한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 README에 '린터와의 충돌' 절이 있다: ruff ERA001이 프론트매터·하단 노트를 주석 처리된 코드로 오탐하는 원인과 해결 설정 예(pyproject의 per-file-ignores)를 담는다
- [ ] #2 README의 예시 설정 블록이 유효한 TOML이며 ERA001을 per-file-ignores에 담는다(파싱으로 검증)
- [ ] #3 README에 '표식은 소스 파일에만 달고 테스트 파일은 헤더만 둔다'는 방침이 한 줄로 적혀 있다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 source-header 전체 테스트와 ruff가 통과한다(출력을 Implementation Notes에 첨부)
- [ ] #2 doctree에서 같은 설정으로 ruff check src tests가 오류 0임을 확인했다(커밋 3304c28)
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
2026-11-11 유저 승인: doctree에서 프론트매터·노트가 ERA001에 306개 오류로 잡혀 per-file-ignores로 풀었다. 같은 문제를 다른 저장소가 겪지 않도록 README에 안내를 남긴다. 테스트 파일은 헤더만 둔다는 방침도 한 줄 적는다.

### Objective
- README에 '본문 노트 표식' 절은 있으나 린터 충돌 안내는 없다.
- doctree pyproject에 적용한 설정(커밋 3304c28): [tool.ruff.lint.per-file-ignores] "src/**/*.py"·"tests/**/*.py" = ["ERA001"]. 이 설정으로 ruff check src tests 통과, 테스트 282개 통과.
- 다른 6개 Python 저장소는 ERA를 선택하지 않아 영향이 없었다.

### Assessment
도구 코드는 건드리지 않고 README와 README 검사 테스트만 바꾼다. README 편집은 testFirst(sourceGlobs=source-header.py) 대상이 아니지만 Done 게이트는 AC마다 TASK-N#n 테스트 표식을 요구하므로 README 내용을 실제로 검사하는 테스트(예: TestNoteMarkerSpec 방식)를 먼저 쓴다.

### Plan
1. AC1 테스트(절 존재·원인·예시 포함)를 먼저 쓰고 README 절을 추가해 통과시킨다.
2. AC2 테스트(예시 TOML 파싱, per-file-ignores에 ERA001)를 쓰고 통과시킨다.
3. AC3 테스트(방침 한 줄)를 쓰고 README에 방침을 적는다.
4. 전체 테스트와 ruff를 돌려 증거를 남긴다.
<!-- SECTION:PLAN:END -->

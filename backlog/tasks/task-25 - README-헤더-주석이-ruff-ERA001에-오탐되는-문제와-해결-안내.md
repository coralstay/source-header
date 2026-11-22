---
id: TASK-25
title: 'README: 헤더 주석이 ruff ERA001에 오탐되는 문제와 해결 안내'
status: Done
assignee: []
created_date: '2026-11-11T11:29:00Z'
updated_date: '2026-11-22T11:57:00Z'
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
- [x] #1 README에 '린터와의 충돌' 절이 있다: ruff ERA001이 프론트매터·하단 노트를 주석 처리된 코드로 오탐하는 원인과 해결 설정 예(pyproject의 per-file-ignores)를 담는다
- [x] #2 README의 예시 설정 블록이 유효한 TOML이며 ERA001을 per-file-ignores에 담는다(파싱으로 검증)
- [x] #3 README에 '표식은 소스 파일에만 달고 테스트 파일은 헤더만 둔다'는 방침이 한 줄로 적혀 있다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 source-header 전체 테스트와 ruff가 통과한다(출력을 Implementation Notes에 첨부)
- [x] #2 doctree에서 같은 설정으로 ruff check src tests가 오류 0임을 확인했다(커밋 3304c28)
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-12 구현·검증 기록 (브랜치 task/TASK-25, 커밋 d0d1cbe d1dbc38 97bb788 1143bd8 b8f7049)
- AC #1: README에 '린터와의 충돌' 절. ERA001 원인과 doctree 사례(306개: 헤더 268 + 노트 38), per-file-ignores 설정 예, 대가(그 경로의 ERA001 포기)를 담았다. 테스트 TestLinterConflictDoc.test_readme_explains_era001_conflict(TASK-25#1)가 절 추가 전에 실패했다가 통과했다(서브에이전트 보고).
- AC #2: 예시 TOML을 tomllib로 파싱해 per-file-ignores가 {src/**/*.py, tests/**/*.py}=[ERA001]임을 검사하는 테스트(TASK-25#2). 서브에이전트는 이 테스트가 실패하는 것을 못 봤다고 보고해 직접 확인했다: README의 ERA001을 ERA002로 일부러 바꾸자 테스트가 실패했고 원복했다.
- AC #3: 방침 문장. 처음에는 '테스트 파일은 표식·하단 노트 없음'이라고 썼으나 이 저장소 자신의 test_source_header.py가 표식 3개를 갖고 TASK-6#4 테스트가 그것을 요구하므로 모순이었다. 직접 확인해 '기본은 소스에만, 테스트는 헤더만, 이 도구 자신의 테스트처럼 표식을 일부러 다는 예외는 허용하되 번호 연속·노트 1:1은 지킨다'로 고쳤다(b8f7049). 테스트(TASK-25#3)는 그대로 통과.
- DoD #1(직접 실행): uvx pytest 84 passed·91 subtests passed, ruff All checks passed, source-header lint --strict . exit 0.
- DoD #2(직접 실행, doctree task/TASK-15 커밋 3304c28): .venv/bin/ruff check src tests → All checks passed!, pytest 282 passed.
- Done 이동은 하지 않았다: source-header의 testFirst 게이트가 DoD 항목에도 TASK-25#D1·#D2 테스트 표식을 요구하고, DoD #2는 다른 저장소(doctree)의 상태라 이 저장소 테스트로 검증할 수 없다(DRAFT-13의 같은 문제).

## 2026-11-22 TASK-42 에서 마감
- 브랜치 task/TASK-25(25커밋, 원격에 없었음)를 정리 브랜치 task/TASK-42 에 merge 로 합침(f096337, 충돌 없음)
- 작업 트리(task/TASK-42)에서 pytest 84 passed, 91 subtests passed(2026-11-22). AC·DoD 는 2026-11-12 에 이미 증거와 함께 체크됨
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
README 에 ruff ERA001 이 source-header 헤더·하단 노트를 주석 처리된 코드로 오탐하는 원인과 per-file-ignores 해결 예(TOML 파싱 검증)를 추가하고, 표식은 소스에만·테스트는 헤더만 둔다는 방침을 적었다. 2026-11-12 에 끝났지만 브랜치가 병합되지 않아 2026-11-22 TASK-42 정리 브랜치로 들였다.
<!-- SECTION:FINAL_SUMMARY:END -->

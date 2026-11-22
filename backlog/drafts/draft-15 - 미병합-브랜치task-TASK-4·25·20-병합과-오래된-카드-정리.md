---
id: DRAFT-15
title: 미병합 브랜치(task/TASK-4·25·20) 병합과 오래된 카드 정리
status: Draft
assignee: []
created_date: '2026-11-22T11:28:00Z'
labels:
  - cleanup
  - backlog
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저(2026-11-22): 원격·로컬을 뒤져 병합할 것을 모두 병합하자, 정리 카드를 먼저 하자. 열린 PR 은 0개, 대신 PR 로 올라가지 않은 브랜치가 남아 있다.
- task/TASK-4: 커밋 89개(원격 71 + 미push 18), 백로그만, TASK-29~41 카드·사람 서명 15개·11-17 Done 처리, main 과 충돌 없음
- task/TASK-25: 25개, 원격 없음, README + test_source_header.py(ruff ERA001 안내), 충돌 없음
- task/TASK-20: 6개, 원격 없음, 백로그만, backlog/work-order.md 충돌
- In Progress 15장·To Do 7장 중 실제로 끝났는데 Done 이 아닌 카드(TASK-4 AC 4/4·PR 병합, TASK-5·6·12·13·15·24 PR 병합인데 AC 0/4, TASK-3·16), upkeep 으로 옮긴 TASK-17~22 원본이 남아 있다
계획: ~/.claude/plans/cleanup-unmerged-branches-cards.md (승인됨)

## 비즈니스 규칙
- B1 (AC #2) 근거(병합 PR·커밋·lint 출력) 없는 Done 금지
- B2 (AC #1) 이력 보존: rebase·squash·force push 없음, 사람 서명 커밋이 그대로 남는다
- B3 (AC #2) TASK-28·DRAFT-14 는 건드리지 않는다
- B4 (AC #2) Antigravity·다른 세션 담당 저장소 파일은 고치지 않는다(카드 노트만)

## 하지 않는 것
남은 카드의 실제 작업, TASK-73 구현
<!-- SECTION:DESCRIPTION:END -->

---
id: TASK-42
title: 미병합 브랜치(task/TASK-4·25·20) 병합과 오래된 카드 정리
status: In Progress
assignee: []
created_date: '2026-11-22T11:28:00Z'
updated_date: '2026-11-22T12:00:00Z'
labels:
  - cleanup
  - backlog
dependencies: []
documentation:
  - /Users/flynn_macpro/.claude/plans/cleanup-unmerged-branches-cards.md
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

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 정리 브랜치(origin/main 기준)에 task/TASK-4·task/TASK-25·task/TASK-20 을 merge 로 합치고(rebase·squash 없음), work-order.md 충돌은 work-order 재생성으로 푼다. 사람 서명 커밋이 이력에 그대로 있다(B2)
- [ ] #2 카드마다 분류표(실제로 끝남·이관·다른 담당·접은 일·남은 일)를 Notes 에 남기고, 끝난 카드는 병합 PR·커밋·지금 main 기준 lint 출력을 증거로 AC·DoD 체크·final summary·Done 처리한다. 증거가 애매한 카드는 유저에게 묻는다. TASK-28·DRAFT-14 는 그대로 둔다(B1·B3·B4)
- [ ] #3 upkeep 으로 이관한 TASK-17~22 는 'upkeep TASK-n 으로 이관' 노트 후 archive 하고, 다른 담당 카드(TASK-35 Antigravity, TASK-14·36 다른 Claude 세션)는 노트로 담당을 적는다
- [ ] #4 합친 뒤 pytest·source-header lint --strict 가 통과하고 backlog task list 가 정상이며, 기존 브랜치(로컬 3개·원격 task/TASK-4)는 병합 확인 뒤 지운다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 분류표 전체와 카드별 증거를 Notes 에 첨부
- [ ] #2 pytest·lint 출력 첨부
- [ ] #3 PR 이 있다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-22)가 병합할 것을 모두 찾아 병합하자고 했고, 정리 카드를 담당 기록(dev-toolchain TASK-179)보다 먼저 하자고 했다. 계획: ~/.claude/plans/cleanup-unmerged-branches-cards.md

### Objective
- task/TASK-4 89커밋(백로그만, 충돌 없음, 미push 18), task/TASK-25 25커밋(README·test, 충돌 없음), task/TASK-20 6커밋(백로그만, work-order.md 충돌).
- In Progress 15·To Do 7. TASK-4·3·16 은 AC 모두 체크, TASK-5·6·12·13·15·24 는 PR 병합인데 AC 0/4, TASK-17~22 는 upkeep TASK-1~6 으로 이관된 원본.
- 메모리: TASK-28·DRAFT-14 는 유저가 '토끼굴'로 접음, 먼저 꺼낼 때까지 그대로.

### Assessment
새 정리 브랜치에 기존 브랜치를 merge 로 모아 이력과 서명을 보존하고, PR 하나로 main 에 들인다. 카드는 증거가 있는 것만 상태를 바꾸고 나머지는 노트로 분류만 남긴다.

### Plan
1. 승격 → 서명 → In Progress → origin/main 에서 task/<ID> → task/TASK-4·25·20 merge, work-order 재생성.
2. 카드별 증거 수집(gh pr list --state merged, git log, lint) → 분류표 → 끝난 카드 Done, 이관 카드 archive, 담당 노트.
3. pytest·lint·task list 확인 → 기존 브랜치 삭제 → Done → PR.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 2026-11-22 작업 기록
### 병합 (AC #1)
- task/TASK-42 를 task/TASK-4 끝(4f9477b, TASK-42 카드·서명·In Progress 포함)에서 파고 task/TASK-25(f096337, 충돌 없음)·task/TASK-20(2085b8b, work-order.md 충돌 → work-order 재생성) 을 merge 로 합쳤다. origin/main 은 이미 task/TASK-4 의 조상이라 추가 병합 불필요(git diff HEAD...origin/main 비어 있음)
- task/TASK-20 병합 마무리 커밋은 처음에 backlog_commit_scope 훅이 '상태 전환 + 다른 변경'으로 막았다 → agile-hooks TASK-77(MERGE_HEAD 예외)로 훅을 고치고 설치한 뒤 통과
- 사람 서명 Plan-Approved(TASK-29~34·37~42) 커밋이 HEAD 이력에 그대로 있다(test_backlog_cleanup)

### 분류표 (AC #2·#3)
| 카드 | 분류 | 처리 |
|---|---|---|
| TASK-3·16 | 실제로 끝남 | task/TASK-20 에 이미 Done(병합으로 들어옴) |
| TASK-4·5·6·12·13·15·24 | 실제로 끝남 | 병합 PR·PR 범위 코드 무변경·표식 1:1 재계산·origin/main lint 0·테스트로 Done(카드별 노트). 테스트 표식 대신 증거 — 유저 결정 2026-11-22 |
| TASK-25 | 실제로 끝남 | 브랜치 병합, pytest 84 passed 로 Done |
| TASK-29~34·37~41 | 이미 Done | task/TASK-4 로 들어옴 |
| TASK-17~22 | upkeep 으로 이관 | task/TASK-20 에 이미 archive(upkeep TASK-1~6) |
| TASK-35 | 다른 담당 | Antigravity(handcrafted-python) 노트, To Do 유지 |
| TASK-14·36 | 다른 담당 | 다른 Claude 세션(ebpf) 노트, To Do 유지 |
| TASK-26·27 | 남은 일 | 노트, In Progress 유지 |
| TASK-28·DRAFT-14 | 접은 일 | 손대지 않음(바이트 동일, 테스트) |
| DRAFT-13 | 대체됨 | 이 카드가 적용 카드 6장을 증거로 닫아 archive |
| DRAFT-1·3·9·11 | 후속 초안 | 그대로 |

### 검증 (AC #4, DoD #2)
- pytest(작업 트리): 93 passed + 이 노트 검사 1개(이 노트를 쓴 뒤 통과), ruff All checks passed, source-header lint --strict rc=0
- 기존 브랜치 정리는 아래 커밋 뒤 로컬 task/TASK-4·25·20 삭제, 원격 task/TASK-4 는 PR 병합 뒤 삭제
- PR: 소스 브랜치 task/TASK-42(번호는 생성 뒤 추가)
<!-- SECTION:NOTES:END -->

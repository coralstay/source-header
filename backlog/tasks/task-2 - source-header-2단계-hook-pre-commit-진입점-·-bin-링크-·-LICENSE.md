---
id: TASK-2
title: 'source-header 2단계: hook pre-commit 진입점 · bin 링크 · LICENSE'
status: Done
assignee: []
created_date: '2026-10-30T19:31:00Z'
updated_date: '2026-10-30T19:39:00Z'
labels:
  - tool
  - hooks
dependencies: []
documentation:
  - ~/.claude/plans/giggly-kindling-snowglobe.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
계획 2단계(2026-10-31 변경본). git 훅 연결은 coding-agent-git-commit-tool DRAFT-22가 `.githooks` + `core.hooksPath`로 맡는다. source-header는 그 디스패처가 부를 진입점만 제공한다.
유저 결정: ~/githubs 아래 코드는 AGPL-3.0-only. 이 저장소에 LICENSE 파일을 추가한다.

## 범위
- `source-header hook pre-commit`: `fix --staged` 후 `lint --staged`를 실행. `.source-header.json`이 없는 저장소에서는 아무것도 하지 않고 exit 0
- `~/githubs/bin/source-header` → `../dev-tools/source-header/source-header.py` 심볼릭 링크 (bin의 다른 항목과 같은 방식)
- LICENSE(AGPL-3.0 전문, 형제 저장소 claude-code-agile-hooks의 LICENSE와 동일), README에 라이선스 절

## 비즈니스 규칙
- B1 (AC #1) fix가 실패(exit≠0)하면 lint를 돌리지 않고 같은 코드로 끝낸다
- B2 (AC #1) .source-header.json이 없는 저장소에서는 검사하지 않는다(opt-in)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 source-header hook pre-commit이 B1·B2에 따라 fix --staged → lint --staged를 실행하고 그 exit 코드를 돌려준다. 임시 저장소에서 통과·차단·opt-out 세 경우를 테스트한다
- [x] #2 ~/githubs/bin/source-header 심볼릭 링크가 있고 PATH에서 source-header --help가 동작한다
- [x] #3 LICENSE(AGPL-3.0 전문)와 README 라이선스 절이 있고, source-header lint .에서 L2 경고가 없다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 테스트 전체 통과(로그를 Implementation Notes에 첨부)
- [x] #2 ruff check . 통과
- [x] #3 source-header lint . 오류·경고 0
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저가 2단계 진행, LICENSE 추가를 승인했다(2026-10-31). git 훅 연결은 git-commit-tool DRAFT-22가 맡는다.

### Objective
TASK-1로 lint·fix·--staged가 이미 있다. ~/githubs/bin의 다른 항목은 모두 상대 경로 심볼릭 링크다. claude-code-agile-hooks에 AGPL-3.0 LICENSE 전문이 있다.

### Assessment
진입점은 기존 cmd_fix·cmd_lint를 차례로 부르는 얇은 서브커맨드로 둔다. 로직을 새로 만들지 않는다.

### Plan
1. 테스트(TASK-<ID>#1, #B1, #B2) → hook 서브커맨드 → 커밋
2. bin 링크 생성 → 확인 → 커밋은 없음(bin은 git 밖) — 결과는 Implementation Notes에 기록
3. LICENSE 복사 + README 절 → 자기 lint L2 경고 0 → 커밋
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 검증 로그 (메인 세션 재실행, 2026-10-31)
$ uvx --with pytest pytest -q -p no:cacheprovider → 67 passed, 75 subtests passed
$ ruff check . → All checks passed!
$ python3 source-header.py lint . → 출력 없음, exit 0 (오류·경고 0)
$ ls -l ~/githubs/bin/source-header → ../dev-tools/source-header/source-header.py (bin은 git 밖이라 커밋 없음)
$ (cd /tmp; PATH=~/githubs/bin:$PATH source-header --help) → usage: source-header [-h] {lint,init,fix,status,new,hook} ...
$ cmp LICENSE <claude-code-agile-hooks>/LICENSE → 같음
cmd_hook 코드 리뷰: cmd_fix → (0이 아니면 즉시 반환) → cmd_lint. 설정 없으면 exit 0.

## 메모
- test_bin_link_exists는 링크가 없는 머신에서 skip한다(다른 머신·CI에서 bin이 없을 수 있으므로 의도적).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
source-header hook pre-commit 진입점(fix --staged → lint --staged, .source-header.json 없으면 통과, fix 실패 시 lint 생략), ~/githubs/bin/source-header 심볼릭 링크, AGPL-3.0 LICENSE와 README 라이선스·훅 절을 추가했다. 테스트 67개 통과. 저장소 연결은 git-commit-tool GF-148의 .githooks/pre-commit.d/20-source-header가 맡는다.
<!-- SECTION:FINAL_SUMMARY:END -->

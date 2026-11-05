---
id: DRAFT-1
title: 'ebpf tracer_agent: --ui tui가 --html-out을 무시하는 버그'
status: Draft
assignee: []
created_date: '2026-11-01T13:19:00Z'
updated_date: '2026-11-01T13:19:00Z'
labels:
  - ebpf
  - bug
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
TASK-18 HEAD 정리 중(2026-11-01) 서브에이전트가 범위 밖으로 고친 한 줄을 유저 결정에 따라 되돌리고 이 카드로 남긴다. ebpf 저장소에는 backlog가 없어 source-header backlog에 둔다.

## 문제
dev-tools/ebpf-wire-to-code-tracer/tracer_agent.py main()의 `if args.ui == "tui": run_interactive_tui(diag)`가 `--html-out` 값을 넘기지 않는다. 그래서 `--ui tui --html-out <경로>`를 줘도 항상 현재 디렉터리의 trace_dashboard.html을 쓴다.
영향: test_verification_suite.py를 돌리면 TUI 테스트가 저장소에 추적되는 trace_dashboard.html을 절대 경로가 든 내용으로 다시 쓴다(2026-11-01 실측: 24/24 PASSED 뒤 파일이 바뀜 → 백업에서 복원).

## 고칠 방향
`run_interactive_tui(diag, args.html_out)` — run_interactive_tui가 이미 출력 경로 인자를 받는지 확인하고, 테스트로 --html-out이 지켜지는지 검증한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 --ui tui --html-out <경로>로 실행하면 그 경로에만 대시보드를 쓰고 저장소의 trace_dashboard.html은 바뀌지 않는다
- [ ] #2 test_verification_suite.py를 돌려도 추적 파일이 바뀌지 않음을 테스트로 확인한다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 test_verification_suite.py 24/24 통과
<!-- DOD:END -->

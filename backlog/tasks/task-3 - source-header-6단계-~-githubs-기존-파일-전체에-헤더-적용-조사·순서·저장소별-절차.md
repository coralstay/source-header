---
id: TASK-3
title: 'source-header 6단계: ~/githubs 기존 파일 전체에 헤더 적용 (조사·순서·저장소별 절차)'
status: In Progress
assignee: []
created_date: '2026-10-30T19:31:00Z'
updated_date: '2026-11-02T02:25:00Z'
labels:
  - rollout
dependencies: []
documentation:
  - ~/.claude/plans/giggly-kindling-snowglobe.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-10-31): ~/githubs에서 관리하는 기존 파일 전체에 소스 헤더를 적용한다.
- freeride: 내가 짠 코드만. 책 예제 코드는 저장소별 규칙(디렉터리 패턴)을 먼저 조사해 .source-header.json exclude로 뺀다
- description: 서브에이전트가 파일을 읽고 한 줄 초안을 쓴다. 저장소마다 커밋을 나눠 diff로 검토한다
- .md: README·CHANGELOG 같은 표지 문서는 제외하고 design/·docs/ 설계 문서는 포함. backlog/는 원래 제외
- MIT 저장소(dev-toolchain, omnivim, devOps-LifeCycle)는 AGPL-3.0-only로 전환

## 조사 결과 (2026-10-31)
- 대상: factory·dev-tools·toy-project 9개 저장소(소스 약 860 / md 약 280), freeride 7개(소스 약 8,200 / md 약 3,300, 책 예제 분리 전)
- 제외: opensource/, ebpf-wire-to-code-tracer/references/*(외부 클론 3개), backlog/
- 지금 작업 중이라 나중에 할 저장소: agent-orchestrator(task/AO-32, 변경 있음), claude-code-agile-hooks(task/TASK-71), ebpf-wire-to-code-tracer(변경 24), freeride/doctree(변경 9), freeride(변경 1)
- 작성자: 같은 계정의 옛 이름들 → .mailmap으로 coralstay로 묶어 authors에 반영
- ⚠️ dev-toolchain 커밋에 옛 이메일 작성자가 있다 → 다른 사람이면 그 코드는 MIT 유지 또는 동의 필요. AGPL 전환 전에 유저 확인

## 저장소별 절차 (저장소 하나 = 커밋 묶음 하나)
1. backlog 프로젝트면 그 저장소에 카드(draft → 승인 → promote)를 만들고 그 저장소의 task 브랜치에서 진행
2. .source-header.json(include/exclude) 작성 → source-header init → 서브에이전트가 description 초안 → lint 오류 0
3. 유저가 diff 검토 → 병합
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 [수동 검증] freeride 각 저장소의 '내가 짠 코드 vs 책 예제' 구분 규칙을 조사해 표로 정리하고 유저 승인을 받는다
- [x] #2 [수동 검증] dev-toolchain의 외부 작성자 커밋을 확인해 AGPL 전환 가능 여부를 유저에게 보고한다
- [x] #3 [수동 검증] 적용 순서표(바로 가능한 저장소 → 작업 끝난 뒤 할 저장소)를 work-order에 반영하고, 저장소마다 후속 카드를 만든다
- [x] #4 .mailmap 기반 authors 정규화를 source-header init에 반영한다(테스트 포함)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 [수동 검증] 조사 결과 표(freeride 구분 규칙, dev-toolchain 작성자)를 Implementation Notes에 기록하고 유저 승인을 받음
- [x] #2 .mailmap 테스트 포함 전체 테스트 통과, ruff 통과
- [x] #3 [수동 검증] 저장소별 후속 draft가 만들어지고 work-order에 반영됨
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저 결정(2026-10-31): ~/githubs 기존 파일 전체 적용. freeride는 내가 짠 코드만, description은 에이전트 초안, README 제외·설계 문서 포함, MIT 저장소는 AGPL로 전환.

### Objective
조사 결과는 Description 참고. 저장소 16개(외부 클론 제외), 그중 5개는 작업 중이다. dev-toolchain에 외부 이메일 작성자가 있다.

### Assessment
규모가 커서 이 카드는 조사·순서·공통 기능(.mailmap)까지만 한다. 실제 적용은 저장소별 후속 카드로 나눠 하나씩 검토 가능하게 한다.

### Plan
1. freeride 책 예제 구분 규칙 조사(서브에이전트) → 표로 유저 승인
2. dev-toolchain 외부 작성자 커밋 확인 → 보고
3. .mailmap 정규화를 init에 추가(테스트 먼저)
4. 순서표 + 저장소별 후속 draft 생성
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## AC #1 freeride 구분 규칙 (Explore 서브에이전트 조사 + 메인 표본 확인, 유저 승인 2026-10-31)
| 저장소 | 포함 | 제외·비고 | 유저 결정 |
|---|---|---|---|
| freeride(루트) | layout.yaml | */** (하위 저장소) | - |
| handcrafted-cpp | scripts/**, CMakeLists.txt (41) | practice/** 전체: 책 원문 3,055(Professional C++, Extreme C+googletest, 종만북) + 책을 옮겨 적는 스켈레톤 3,699 + BPF·ARM·Knuth 110 | scripts만(가장 보수적) |
| coding-style | scripts/** (48), practice/** (1,049, 생성물) | tracks/**(심링크), docs/** | practice는 생성기에서 헤더 생성 |
| databases | scripts/** (85), practice/** (171, 생성물) | 기출 16~18번, SQL-docs/** | 생성기에서 헤더 생성, 기출 제외 |
| devOps-LifeCycle | 약 360 (tf·tla·rego 포함) | .terraform, lock | MIT→AGPL |
| doctree | 46 | cassettes yaml, docs | - |
| handcrafted-java | 87 | gradlew·gradle/ (Apache-2.0) | - |
- test.cpp TODO 스텁 698개 재포함 기능: 추가하지 않음(유저 결정)
- 메인 확인: googletest 사본 326개 파일, @book 머리 주석 6,767개, 심링크 2개(mode 120000), devOps LICENSE 저작권자 표기가 옛 계정 이름
- ⚠️ handcrafted-cpp README는 실습 코드가 .gitignore로 격리된다고 하지만 책 원문이 커밋돼 있음(GitHub Private). 헤더 범위 밖 — 유저에게 보고함

## AC #2 dev-toolchain 외부 작성자
옛 이메일 커밋(2026-03-21, 초기 셋업 zsh)은 옛 계정 이름으로 작성됨. 유저 확인: 본인, 지금은 쓰지 않음 → AGPL 전환 가능.
계정 정리: 전역 ~/.mailmap + git config --global mailmap.file 설정 → 워크스페이스 전체 git log --use-mailmap 작성자가 coralstay 1명(2,550 커밋)으로 수렴.

## AC #3 적용 순서와 저장소별 draft
기존 저장소 .githooks는 source-header 플러그인만(유저 결정) → 선행: git-commit-tool DRAFT-22(install --plugins 옵션)
| 순서 | 저장소 | draft 위치 / ID |
|---|---|---|
| 1-now | central-docs-collector | source-header DRAFT-1 |
| 1-now | omnivim (MIT→AGPL) | source-header DRAFT-2 |
| 1-now | dev-toolchain (MIT→AGPL) | dev-toolchain DRAFT-15 |
| 1-now | coralstay-software-factory | factory DRAFT-1 |
| 1-now | coding-agent-git-commit-tool (+자기 migrate) | git-commit-tool DRAFT-23 |
| 1-now | toy-project/react-next-… | toy-project DRAFT-24 |
| 1-now | source-header 자신 | source-header DRAFT-3 |
| 2-freeride | freeride 루트 / handcrafted-cpp / coding-style / databases / handcrafted-java | source-header DRAFT-4 / 5 / 6 / 7 / 8 |
| 2-freeride | devOps-LifeCycle (MIT→AGPL, tf·tla·rego 확장자 지원 판단) | devOps DRAFT-1 |
| 3-later | agent-orchestrator(AO-32 진행 중) / claude-code-agile-hooks(TASK-71) / ebpf(미커밋 24) / doctree(미커밋 9) | source-header DRAFT-9 / 10 / 11 / 12 |
work-order는 task만 계산하므로 draft 순서는 이 표가 기준. 승격 시 각 저장소 work-order에 반영.

## AC #4 .mailmap
554df0f: git_authors는 %aN(--use-mailmap), git_user는 git check-mailmap. 메인 재실행: 71 passed, ruff OK, lint 0.

재오픈(2026-10-31): 전역 mailmap.file(~/.mailmap) 설정 후 test_without_mailmap_old_names_remain이 실패 → GitCase에서 GIT_CONFIG_GLOBAL을 빈 파일로, GIT_CONFIG_NOSYSTEM=1로 격리(a056327). 재실행: 71 passed, ruff OK, lint 0. Done 재전환은 require_test_first가 비코드 AC(#1~#3, DoD) 표식을 요구해 보류 — 유저 결정 대기.

2026-11-01: test_staged_reads_index_not_worktree가 날짜가 바뀌자 B8로 실패(고정 날짜 픽스처) → 오늘 날짜로 수정. .gitignore에 .claude-code-agile-hooks/ 추가(감사 S-4). 71 passed.

## 수동 검증 증거
- 증거: TASK-3#1 — freeride 구분 규칙 표(Notes 'AC #1' 절), 유저 승인(2026-10-31: cpp는 scripts만, 생성 카타는 생성기에서, 재포함 기능 없음)
- 증거: TASK-3#2 — dev-toolchain 외부 작성자 확인 표, 유저 확인(본인)
- 증거: TASK-3#3 — 저장소별 draft 17장 생성·승격(Notes 'AC #3' 표), work-order 반영
- 증거: TASK-3#D1 TASK-3#D3 — 위 각 절
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
~/githubs 기존 파일 적용을 위한 조사·결정·공통 기능을 마쳤다. freeride는 내가 짠 코드만(handcrafted-cpp는 scripts만, 생성 카타는 생성기에서 헤더), 옛 계정 이름·이메일은 본인 확인 후 전역 .mailmap으로 coralstay에 묶었고, init·new의 authors는 git mailmap을 따른다. 저장소별 적용 draft 17장을 순서 그룹(1-now 7, 2-freeride 6, 3-later 4)으로 만들었고, 기존 저장소 .githooks는 source-header 플러그인만 설치하기 위해 git-commit-tool DRAFT-22(--plugins)가 선행한다.
<!-- SECTION:FINAL_SUMMARY:END -->

---
id: TASK-27
title: >-
  기존 주석을 본문 노트 포맷으로 변환 — dev-toolchain 1차 (scripts/lib.sh,
  scripts/install/00_select.sh)
status: In Progress
assignee: []
created_date: '2026-11-11T11:29:00Z'
updated_date: '2026-11-12T01:56:00Z'
labels:
  - source-header
  - followup
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
2026-11-06 적용 라운드에서 서브에이전트들은 기존 주석을 지우지 않고 표식·노트만 추가했다. 기존 설명 주석을 새 포맷(줄 끝 `---- N` + 하단 노트)으로 옮기는 변환(source-header README '기존 주석 변환', B4)은 유저 결정으로 후속으로 뺐다. 이 카드는 그 1차로 dev-toolchain의 가장 큰 두 파일만 한다. 다른 저장소(agent-orchestrator의 Javadoc, omnivim 등)는 이 카드의 결과를 보고 필요하면 별도 카드로 한다.

## 규모 (실측, dev-toolchain main 기준)
파일 42개·9,174줄 중 주석 전용 3,529줄. scripts/lib.sh 1,566줄(전체 2,320줄), scripts/install/00_select.sh 507줄(전체 919줄)에 몰려 있다. 이 두 파일이 주석 줄의 약 59%다.

## 범위
- 대상: 표식(---- N)이 달린 지점을 설명하는 주석만. 자명한 주석, 구분선, 지시 주석(shellcheck disable 등)은 대상이 아니다.
- 설명 주석은 해당 노트의 설명으로 옮기고 원래 주석 줄은 지운다. 정보는 노트에 남는다.
- 코드 줄은 바뀌지 않는다.

## 선행
dev-toolchain PR #1(task/TASK-175)을 기준으로 한다(병합 전이면 그 브랜치 위에 쌓는다).

## 하지 않는 것
다른 저장소, 나머지 40개 파일, 확장자 없는 파일.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 scripts/lib.sh에서 표식 지점을 설명하는 주석을 해당 노트의 설명으로 옮기고 원 주석 줄을 지운다(구분선·지시 주석·자명한 주석은 그대로)
- [ ] #2 scripts/install/00_select.sh에 같은 변환을 한다
- [ ] #3 두 파일의 코드가 바뀌지 않았다: bash -n 통과, shfmt -mn으로 주석을 걷어낸 구조가 변환 전과 같다
- [ ] #4 옮긴 주석의 내용이 노트에 있다: 지운 주석 줄마다 노트 텍스트에서 단어 일치율을 검사해 낮은 줄 목록을 검토하고 정리한다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 shellspec 전체 통과(출력을 Implementation Notes에 첨부)
- [ ] #2 source-header lint --strict 통과, 표식 번호 연속·노트 1:1 유지
- [ ] #3 변환 전후 주석 전용 줄 수와 지운 줄 수를 Implementation Notes에 기록
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
2026-11-12 유저 승인: 기존 주석 변환(B4)을 후속으로 하되 범위를 줄여 dev-toolchain의 큰 파일 두 개를 1차로 한다.

### Objective
- dev-toolchain main: 파일 42개·9,174줄 중 주석 전용 3,529줄이고 lib.sh 1,566줄, 00_select.sh 507줄에 몰려 있다(직접 측정).
- 두 파일에는 TASK-175에서 표식과 노트가 이미 있다(lib.sh 18개, 00_select.sh 11개). 기존 설명 주석은 그대로 남아 있다.
- 코드 무변경 증명 도구: bash -n, shfmt -mn(주석 제거 구조 비교), shellspec 228 examples.

### Assessment
읽기·판단이 필요한 작업이라 토큰이 많이 든다. lib.sh(2,320줄)를 구간으로 나눠 서브에이전트를 나누되 같은 파일을 동시에 고치지 않는다(한 파일은 한 에이전트). 두 파일은 서로 독립이라 에이전트 둘을 동시에 돌릴 수 있다. 주석을 지우는 작업이므로 정보 손실 방지가 핵심이고, 지운 줄의 단어 일치율 검사로 확인한다.

### Plan
1. 변환 대상 선별 기준을 서브에이전트에 준다(표식이 달린 지점 바로 위·옆의 설명 주석만).
2. lib.sh와 00_select.sh를 각각 서브에이전트가 변환한다(Edit 도구만).
3. 검증: bash -n, shfmt -mn 구조 동일, shellspec, lint --strict, 단어 일치율 검사, 주석 줄 수 전후 비교.
4. 결과를 PR로 올린다(dev-toolchain PR #1 위).
<!-- SECTION:PLAN:END -->

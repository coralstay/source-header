---
id: DRAFT-13
title: '적용 카드 마감: testFirst 게이트 해소 후 Done (TASK-4·5·12·13·15·24)'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
labels:
  - source-header
  - followup
  - bookkeeping
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
source-header 백로그에 있는 적용 카드 6장(TASK-4, 5, 12, 13, 15, 24)과 toy-project의 TASK-68은 작업이 끝났거나(4·5·12·13·15·24) 보류인데, source-header의 testFirst 게이트가 모든 AC·DoD에 'TASK-N#n' 테스트 표식을 요구해 Done으로 옮길 수 없다. 이 작업은 다른 저장소의 파일을 고치는 일이라 source-header의 테스트로 검증할 수 없다.

## 정석 해결
agile-hooks의 TASK-69·73(수동 검증 AC는 표식 대신 Notes 증거+사람 서명으로 Done)이 구현·설치된 뒤 이 카드들을 Done으로 옮긴다. 그 앞에 TASK-75(게이트 대상 저장소 판정)가 있다. 현재 모든 카드는 AC·DoD 체크와 증거(Implementation Notes)가 TASK-4 외에는 아직 기록되지 않았다.

## 해야 할 일
- 카드마다 AC·DoD 체크 + 증거 기록 + final summary (증거는 각 PR 본문과 이 세션의 직접 검증 결과).
- DoD '유저가 description diff 검토'는 유저가 286개 중 무작위 20개 샘플을 검토하고 모두 유지하기로 결정했다(2026-11-11).
- TASK-69·73 구현 뒤 Done.

## 완료 기준 (승격 후 --ac로 등록)
1. 6장이 Done이고 각 final summary가 있다.
2. toy-project TASK-68은 VM을 켠 뒤 재개하거나 별도 결정으로 닫는다.
<!-- SECTION:DESCRIPTION:END -->

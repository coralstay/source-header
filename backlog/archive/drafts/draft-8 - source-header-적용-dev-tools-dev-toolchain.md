---
id: DRAFT-8
title: 'source-header 적용: dev-tools/dev-toolchain'
status: Draft
assignee: []
created_date: '2026-11-06T11:25:00Z'
labels:
  - source-header
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-06): GitHub에 올라간 저장소 전체에 헤더+본문 노트 표식을 단다. 규격은 TASK-23. 절차는 기존 적용 카드와 같다: .source-header.json → source-header init → description 초안(서브에이전트) → lint --strict.

## 대상 저장소
`~/githubs/dev-tools/dev-toolchain` (sh 40, yml 1).

## 메모
선행: TASK-23. 표식·노트는 헤더 적용 뒤 별도 커밋(양식: DRAFT-6). 셸 스크립트라 접두사는 '#', 노트 구역도 '#'로 쓴다.
<!-- SECTION:DESCRIPTION:END -->

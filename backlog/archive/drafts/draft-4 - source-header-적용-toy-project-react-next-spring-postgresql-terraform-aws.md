---
id: DRAFT-4
title: 'source-header 적용: toy-project/react-next-spring-postgresql-terraform-aws'
status: Draft
assignee: []
created_date: '2026-11-06T11:18:00Z'
labels:
  - source-header
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-06): toy-project는 전체 포함. 규격은 TASK-23(README '본문 노트 표식')을 따른다. 기존 헤더 적용 카드(TASK-4~15)와 같은 절차: .source-header.json → source-header init → description 초안(서브에이전트) → lint --strict.

## 대상 저장소
`~/githubs/toy-project/react-next-spring-postgresql-terraform-aws` (Java 323, TSX 87, TS 39, HCL 70 등 약 970 파일). 디렉터리 단위로 쪼갠다(backend / frontend / terraform).

## 메모
선행: TASK-23. 표식·노트는 헤더 적용을 끝낸 뒤 별도 커밋으로 단다. 토큰 예산상 서브에이전트당 한 디렉터리.
<!-- SECTION:DESCRIPTION:END -->

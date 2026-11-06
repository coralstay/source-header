---
id: DRAFT-7
title: >-
  source-header 적용:
  coralstay-software-factory/components/coding-agent-git-commit-tool
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
유저 결정(2026-11-06): GitHub에 올라간 저장소 전체에 헤더+본문 노트 표식을 단다. 규격은 TASK-23. 기존 헤더 적용 카드(TASK-4~15)와 같은 절차: .source-header.json → source-header init → description 초안(서브에이전트) → lint --strict.

## 대상 저장소
`~/githubs/coralstay-software-factory/components/coding-agent-git-commit-tool` (py 24, yml 1, sh 1).

## 메모
선행: TASK-23. 표식·노트는 헤더 적용 뒤 별도 커밋(양식: DRAFT-6). 이 저장소가 .githooks 디스패처의 호스트라 source-header 플러그인 설치 방식에 주의한다(source-header-ssot 결정).
<!-- SECTION:DESCRIPTION:END -->

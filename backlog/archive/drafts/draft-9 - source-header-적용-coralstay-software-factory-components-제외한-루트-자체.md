---
id: DRAFT-9
title: 'source-header 적용: coralstay-software-factory (components 제외한 루트 자체)'
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
`~/githubs/coralstay-software-factory` 루트. components/* (agent-orchestrator, claude-code-agile-hooks, coding-agent-git-commit-tool)는 각자 별도 저장소이자 별도 카드이므로 .source-header.json에서 제외한다. 루트 자체의 소스는 design/, backlog/ 밖의 스크립트 등으로 적을 것으로 보이며 실제 개수는 카드 시작 때 확인한다.

## 메모
선행: TASK-23. 표식·노트는 헤더 적용 뒤 별도 커밋(양식: DRAFT-6). 참고: build-diagrams.py + diagrams/*.dot이 여기에 있다는 CLAUDE.md 기록이 있다.
<!-- SECTION:DESCRIPTION:END -->

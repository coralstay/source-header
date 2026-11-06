---
id: DRAFT-7
title: '저장소별 .githooks 설치: source-header 플러그인과 헤더 없는 커밋 차단 실측 (GF-149 이후)'
status: Draft
assignee: []
created_date: '2026-11-06T12:11:00Z'
labels:
  - source-header
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-06): 각 저장소 적용 카드의 AC '.githooks로 source-header 플러그인을 설치하고 헤더 없는 파일 커밋이 막히는 것을 실측한다'를 별도 카드로 뗀다. 이유: git-commit-tool에 --plugins 옵션이 아직 없다(coding-agent-git-commit-tool GF-149 To Do). 이 옵션 없이는 모든 저장소 카드가 이 AC에서 막힌다.

## 선행
- coding-agent-git-commit-tool GF-149 (install --plugins source-header) 완료
- 대상 저장소의 헤더 적용(해당 카드 Done)

## 대상 저장소
central-docs-collector, omnivim, source-header, agent-orchestrator, claude-code-agile-hooks, doctree, toy-project, coding-agent-git-commit-tool, dev-toolchain, coralstay-software-factory, upkeep, troubleshooting (카드 Done 순서대로).

## 완료 기준 (승격 후 --ac로 등록)
1. 저장소마다 git-commit-tool --plugins source-header로 .githooks를 설치하고 core.hooksPath=.githooks를 설정한다.
2. 헤더 없는 파일을 커밋하면 막히고, 헤더 있는 파일은 통과하는 것을 저장소마다 실측한다.
3. 기존 .githooks가 있는 저장소(git-commit-tool 자신 등)는 기존 훅을 깨지 않고 플러그인만 추가한다.
<!-- SECTION:DESCRIPTION:END -->

---
id: DRAFT-7
title: '저장소별 .githooks 설치: source-header 플러그인으로 헤더 없는 커밋 차단 (파일럿 후 확대)'
status: Draft
assignee: []
created_date: '2026-11-06T12:11:00Z'
updated_date: '2026-11-12T02:57:00Z'
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

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 파일럿 저장소(troubleshooting)에 git-commit-tool --plugins source-header로 .githooks를 설치하고, 헤더 없는 파일 커밋은 차단되고 헤더가 있는 파일은 통과하는 것을 실측한다
- [ ] #2 source-header가 PATH에 없는 환경(다른 클론·CI)에서 플러그인이 어떻게 동작하는지 확인하고 결과(통과/실패, 안내 메시지)를 문서화한다
- [ ] #3 나머지 10개 저장소에 같은 방식으로 .githooks를 저장소별 PR로 추가한다(커밋 형식 플러그인은 설치하지 않는다)
- [ ] #4 클론마다 core.hooksPath=.githooks를 로컬에 설정해야 한다는 안내와 설정 절차를 문서에 적는다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 각 저장소에서 헤더 없는 파일 커밋 차단과 헤더 있는 파일 통과를 실측한 출력을 Implementation Notes에 기록했다
- [ ] #2 설치 전에 이미 있던 훅이나 hooksPath를 덮어쓰지 않았다(설치 전 상태를 기록했다)
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
2026-11-12 유저 요청: 새 파일을 만들 때마다 이 포맷이 강제되게 한다. 지금까지는 이미 있는 파일에 헤더·표식을 달았을 뿐이고 앞으로 헤더 없는 파일이 커밋돼도 막는 장치가 없다.

### Objective
- 11개 저장소 모두 git 훅이 없다: core.hooksPath 설정 없음, .githooks 없음, .git/hooks 비어 있음(2026-11-12 직접 확인). 커밋 때 돌던 것은 Claude Code 훅이었다.
- 선행 구현 GF-149(--plugins 옵션)는 Done이고 PR coralstay/coding-agent-git-commit-tool#2에 있다. --plugins source-header를 쓰면 .githooks/pre-commit, prepare-commit-msg, pre-commit.d/20-source-header 세 개만 설치되고 커밋 형식 플러그인은 설치되지 않는다(임시 저장소 실측).
- 플러그인은 source-header hook pre-commit을 부른다. 이 명령은 저장소 루트에 .source-header.json이 있어야만 동작한다(없으면 아무것도 안 한다). 그 파일은 각 저장소의 적용 PR에 들어 있고 아직 병합되지 않았다.
- ~/githubs/bin/git-commit-tool은 coding-agent-git-commit-tool 클론의 install.sh 심볼릭 링크다. 어느 브랜치가 체크아웃돼 있는지에 따라 동작이 달라진다(--plugins는 GF-149 브랜치에만 있음).

### Assessment
설치는 저장소의 커밋되는 파일(.githooks/)과 로컬 설정(core.hooksPath)으로 나뉜다. 커밋되는 파일은 PR로 올리고, hooksPath는 클론마다 로컬에서 설정해야 해서 문서화가 필요하다. 11개를 한꺼번에 하지 않고 가장 작은 troubleshooting에서 파일럿을 해 차단·통과·PATH 없음 동작을 확인한 뒤 확대한다. 이미 훅을 쓰는 저장소가 있으면 덮어쓰지 않아야 하므로 설치 전 상태를 기록한다(지금은 모두 없음).

### Plan
1. 선행 확인: GF-149 PR 병합(또는 클론이 --plugins가 있는 브랜치), 각 저장소 적용 PR 병합(.source-header.json이 main에 있어야 플러그인이 동작).
2. 파일럿: troubleshooting에서 설치 → 헤더 없는 파일 커밋 차단/통과 실측 → source-header가 PATH에 없을 때 동작 확인.
3. 파일럿 결과로 안내 문서를 쓰고, 나머지 10개 저장소에 저장소별로 .githooks 추가 PR을 만든다.
4. 저장소마다 실측 출력을 카드에 기록한다.
<!-- SECTION:PLAN:END -->

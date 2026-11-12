---
id: DRAFT-22
title: 'source-header 적용 2차: ebpf-wire-to-code-tracer (마지막)'
status: Draft
assignee: []
created_date: '2026-11-12T07:33:00Z'
updated_date: '2026-11-12T07:34:00Z'
labels:
  - source-header
  - rollout
  - round2
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 지시(2026-11-12): 비공개로 남아 있던 9개 저장소에도 공개한 11개와 같은 헤더(프론트매터 + AGPL-3.0-only)와 본문 노트 표식을 단다. 계획: ~/.claude/plans/shimmering-spinning-cherny.md (승인됨). 규격: source-header README '본문 노트 표식'·'기존 주석 변환'.

## 적용 규칙 (공통)
- 포함: source-header가 주석 문법을 아는 모든 파일(소스 + 마크다운).
- 제외: LLM이 만든 README.md, 학습자가 타이핑하는 practice/**/main.*, .skeleton/ 사본, backlog/**, 도구가 모르는 형식(JSON·lock·.tf·Makefile 등).
- 본문 표식은 손으로 쓴 핵심 소스에만. 생성 파일·테스트·마크다운은 헤더만.
- 작업은 origin/main에서 판 git worktree에서 한다(로컬 작업 폴더의 미커밋 변경을 건드리지 않는다).
- 코드는 한 줄도 바뀌지 않는다(py ast, sh shfmt -mn, c/cpp 오브젝트, md 본문 바이트 동일).

## 대상
~/githubs/dev-tools/ebpf-wire-to-code-tracer — 유저 지시로 이 라운드의 **맨 마지막**에 한다. 로컬 저장소(커밋 8개). 추적되는 소스 31개(.py 12·.c 10·.h 7·.cpp 2; 루트 15, progs 7, kray 5, daemon 4). references/와 빌드 산출물은 추적되지 않는다.
**미커밋 변경 41개는 유저 작업이라 건드리지 않는다**(worktree 격리).
**라이선스가 둘**: LICENSE(AGPL-3.0)와 LICENSE.GPL-2.0. 커널 쪽 C는 이미 'SPDX-License-Identifier: GPL-2.0' 주석이 11개 파일에 있다 → 그 파일 헤더 license는 GPL-2.0-only이고 기존 SPDX 줄도 같은 값으로 맞춘다(L1 오류 방지). 사용자 공간 .py/.cpp는 AGPL-3.0-only. 파일별 판단이 모호하면 멈추고 묻는다.
origin은 coralstay/ebpf-wire-to-code-tracer인데 GitHub에서는 coralstay-archive로 이전된 상태(활성 원격 없음). 푸시·공개는 이 카드 범위 밖이고 그때 묻는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [ ] #2 파일별 라이선스를 정한다: 커널 쪽 C(progs/ 등 GPL-2.0 SPDX 주석이 이미 있는 파일)는 GPL-2.0-only, 사용자 공간 py·cpp는 AGPL-3.0-only. 헤더 license와 기존 SPDX-License-Identifier 줄이 일치해 lint L1 오류가 없다
- [ ] #3 .source-header.json(제외: README.md, practice/**/main.*, .skeleton/**, backlog/** 등)을 확정하고 source-header init으로 헤더를 넣고, 파일마다 한 줄 description을 쓴다. source-header lint --strict 오류 0
- [ ] #4 코드가 바뀌지 않았다: 변경 파일마다 py는 ast.dump 동일, sh는 bash -n·shfmt -mn 구조 동일, c·cpp는 오브젝트 동일, md는 헤더를 뺀 본문이 바이트 동일이다
- [ ] #5 규격(source-header README '본문 노트 표식')에 따라 손으로 쓴 핵심 소스의 중요한 지점 줄 끝에 '---- N' 표식을 달고 하단에 노트를 쓴다(번호 연속·표식:노트 1:1). 생성 파일·테스트·마크다운은 헤더만 둔다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 source-header lint --strict . 오류 0 (출력을 Implementation Notes에 첨부)
- [ ] #2 저장소의 기존 테스트·빌드가 통과한다(이 환경에서 못 돌리는 것은 건너뛴 이유와 함께 기록)
- [ ] #3 description을 무작위 20개 이상 표본 검토했다(생성 문장은 규칙을 검토)
- [ ] #4 표식 번호 연속·1:1 확인 출력과 코드 무변경 증명 결과를 Implementation Notes에 첨부했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-12)가 비공개로 남은 저장소에도 공개한 11개와 같은 헤더·표식을 달라고 했다. 이 카드는 ebpf-wire-to-code-tracer (마지막)을 맡는다. 계획: ~/.claude/plans/shimmering-spinning-cherny.md.

### Objective
추적되는 소스 31개(py 12·c 10·h 7·cpp 2; 루트 15·progs 7·kray 5·daemon 4), 전체 추적 파일 53개. LICENSE(AGPL-3.0)와 LICENSE.GPL-2.0 두 개. 'SPDX-License-Identifier: GPL-2.0' 주석이 '/* */' 형식으로 11곳, '#' 형식으로 1곳 있다(파일 종류는 시작 때 확인). 로컬 저장소(커밋 8개), 미커밋 변경 41개, origin은 coralstay-archive로 이전된 옛 주소.

### Assessment
마지막에 하는 작은 저장소지만 라이선스가 파일마다 다르다. 커널 쪽 C는 header license가 GPL-2.0-only여야 하고 기존 SPDX 줄도 같은 값이어야 한다(L1). 사용자 공간 py·cpp는 AGPL-3.0-only. 어느 파일이 어느 쪽인지 모호하면 멈추고 묻는다. 미커밋 변경 41개는 유저의 작업이라 worktree로 격리한다. 모든 작업은 origin/main에서 판 git worktree에서 하고 로컬 작업 폴더는 건드리지 않는다. 읽기가 필요한 부분(description·표식)은 서브에이전트(새 컨텍스트)에 맡기고, 에이전트 보고는 믿지 않고 같은 검증을 다시 돌린다. 에이전트는 편집만 하고 커밋은 내가 한다.

### Plan
1. 다른 저장소(freeride~toy-project)가 끝난 뒤 시작. 파일별 라이선스 표를 먼저 만들어 유저에게 보여 준다(GPL-2.0-only / AGPL-3.0-only).
2. worktree 생성(HEAD). 인프라 커밋: .mailmap, .source-header.json, 라이선스 일치 확인 (AC #1 #2).
3. 헤더 삽입(init은 저장소 LICENSE를 기본으로 하므로 GPL 파일은 --license로 지정) + description + 기존 SPDX 줄 정리 (AC #3).
4. 핵심 소스에 표식, 코드 무변경 증명(py ast, c·cpp 오브젝트), 기존 테스트 (AC #4 #5).
5. 푸시는 새 원격 결정 후(이 카드 범위 밖).
<!-- SECTION:PLAN:END -->

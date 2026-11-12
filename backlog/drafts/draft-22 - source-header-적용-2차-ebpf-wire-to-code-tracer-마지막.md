---
id: DRAFT-22
title: 'source-header 적용 2차: ebpf-wire-to-code-tracer (마지막)'
status: Draft
assignee: []
created_date: '2026-11-12T07:33:00Z'
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

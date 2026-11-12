---
id: DRAFT-20
title: 'source-header 적용 2차: coding-style-refactoring-principles'
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
~/githubs/freeride/coding-style-refactoring-principles (private). 소스 1,071개(practice 1,049: 테스트 373·기타 318·main.* 358 제외, scripts 22), 다른 md 525개(PITFALLS.md 509 등), README.md 2개 제외. LICENSE 있음.
생성기 scripts/apply_file_frontmatter.py가 @file 배너를 만든다(현재 배너 1,035개). 생성기를 source-header 헤더를 내보내게 고쳐 일괄 변환한다(배너 중복 방지). 테스트: scripts/test.sh.
<!-- SECTION:DESCRIPTION:END -->

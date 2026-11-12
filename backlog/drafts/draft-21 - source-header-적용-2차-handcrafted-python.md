---
id: DRAFT-21
title: 'source-header 적용 2차: handcrafted-python'
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
~/githubs/freeride/handcrafted-python (private). 소스 1,816개(practice 1,320: 테스트 880·main.* 440 제외, scripts 495, pyproject), 다른 md 469개(PITFALLS.md 440·report_*.md 27 등), README.md 1개 제외.
**선행**: LICENSE 추가 PR coralstay/handcrafted-python#1 병합(이 저장소만 LICENSE가 없었다). **로컬 작업 폴더에 미커밋 변경 14,157개** — 절대 건드리지 않고 worktree로만 작업한다.
생성기 scripts/handcrafted/frontmatter.py의 apply_all/banner가 @file/@path/@book 배너를 만들고 자기 배너만 지우고 맨 위에 다시 붙인다(헤더를 먼저 넣으면 재생성 때 중복) → 생성기를 고쳐 source-header 헤더를 내보내게 하고 hc frontmatter로 일괄 변환. 현재 배너 387개. scripts/<도서>/(495)는 책마다 반복되는 생성 스크립트라 헤더만.
<!-- SECTION:DESCRIPTION:END -->

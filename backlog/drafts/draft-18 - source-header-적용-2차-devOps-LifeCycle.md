---
id: DRAFT-18
title: 'source-header 적용 2차: devOps-LifeCycle'
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
~/githubs/freeride/devOps-LifeCycle (private). 소스 21개(scripts 6, .github 2, scenarios 3, 루트 설정 yaml·toml 등), 다른 md 72개(Lesson-and-learn.md 66 등), README.md 72개는 제외. 내용 대부분이 Terraform(.tf)이라 도구 미지원 → 헤더 불가. 자체 backlog가 있고 backlog/**(475개 카드)는 제외. LICENSE 있음.
테스트: scripts/test.sh.
<!-- SECTION:DESCRIPTION:END -->

---
id: TASK-34
title: 'source-header 적용 2차: coding-style-refactoring-principles'
status: To Do
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
~/githubs/freeride/coding-style-refactoring-principles (private). 소스 1,071개(practice 1,049: 테스트 373·기타 318·main.* 358 제외, scripts 22), 다른 md 525개(PITFALLS.md 509 등), README.md 2개 제외. LICENSE 있음.
생성기 scripts/apply_file_frontmatter.py가 @file 배너를 만든다(현재 배너 1,035개). 생성기를 source-header 헤더를 내보내게 고쳐 일괄 변환한다(배너 중복 방지). 테스트: scripts/test.sh.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [ ] #2 라이선스를 확인한다: LICENSE가 AGPL-3.0 표준 본문이고 헤더 license는 AGPL-3.0-only다
- [ ] #3 .source-header.json(제외: README.md, practice/**/main.*, .skeleton/**, backlog/** 등)을 확정하고 source-header init으로 헤더를 넣고, 파일마다 한 줄 description을 쓴다. source-header lint --strict 오류 0
- [ ] #4 생성기를 source-header 헤더를 내보내게 고친다: 옛 @file 배너를 헤더로 변환(@path→title, @book→description)하고 두 번 돌려도 결과가 같다(멱등). 생성기 테스트를 먼저 쓴다
- [ ] #5 코드가 바뀌지 않았다: 변경 파일마다 py는 ast.dump 동일, sh는 bash -n·shfmt -mn 구조 동일, c·cpp는 오브젝트 동일, md는 헤더를 뺀 본문이 바이트 동일이다
- [ ] #6 규격(source-header README '본문 노트 표식')에 따라 손으로 쓴 핵심 소스의 중요한 지점 줄 끝에 '---- N' 표식을 달고 하단에 노트를 쓴다(번호 연속·표식:노트 1:1). 생성 파일·테스트·마크다운은 헤더만 둔다
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
유저(2026-11-12)가 비공개로 남은 저장소에도 공개한 11개와 같은 헤더·표식을 달라고 했다. 이 카드는 coding-style-refactoring-principles을 맡는다. 계획: ~/.claude/plans/shimmering-spinning-cherny.md.

### Objective
소스 1,071개(practice 1,049: 테스트 373·기타 318·main.* 358 제외, scripts 22), 다른 md 525개(PITFALLS.md 509 등), README.md 2개 제외. 생성기 scripts/apply_file_frontmatter.py가 @file 배너를 만든다(현재 배너 1,035개). 테스트는 scripts/test.sh.

### Assessment
대부분이 생성물이라 파일마다 읽지 않고 생성기를 고쳐 일괄 변환한다. 생성기를 먼저 테스트로 고정하고, 변환 결과가 두 번 돌려도 같은지(멱등)를 확인한다. scripts 22개는 손으로 쓴 도구라 핵심은 표식까지. 다섯 언어(cpp·ts·java·py·sh)가 섞여 있어 언어별 코드 무변경 증명이 필요하다. 모든 작업은 origin/main에서 판 git worktree에서 하고 로컬 작업 폴더는 건드리지 않는다. 읽기가 필요한 부분(description·표식)은 서브에이전트(새 컨텍스트)에 맡기고, 에이전트 보고는 믿지 않고 같은 검증을 다시 돌린다. 에이전트는 편집만 하고 커밋은 내가 한다.

### Plan
1. worktree 생성(origin/main). 인프라 커밋: .mailmap, .source-header.json (AC #1 #2).
2. 생성기 테스트를 먼저 쓰고 생성기를 고친다(배너→헤더, 옛 배너 제거, 멱등) (AC #4). 생성기 변경은 별도 커밋.
3. 생성기 일괄 실행으로 practice의 테스트·기타·PITFALLS 헤더를 넣는다(파일별 AI 읽기 없음). 언어별 코드 무변경 증명을 돌린다.
4. scripts 22개: init + 서브에이전트 description + 핵심 표식 (AC #3 #5).
5. 검증, 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

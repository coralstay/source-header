---
id: TASK-33
title: 'source-header 적용 2차: databases'
status: Done
assignee: []
created_date: '2026-11-12T07:33:00Z'
updated_date: '2026-11-17T12:41:00Z'
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
~/githubs/freeride/databases (private). 소스 197개(practice 162 — main.* 54는 제외 — scripts 33, compose.yaml·docker-compose.yml), 다른 md 62개(PITFALLS.md 54 등). LICENSE 있음. 생성기 없음 → source-header init + 경로 기반 정해진 description으로 일괄 삽입.
테스트: scripts/test.sh (Docker가 필요한 부분은 이 환경에서 못 돌릴 수 있다 — 건너뛴 것은 보고).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [x] #2 라이선스를 확인한다: LICENSE가 AGPL-3.0 표준 본문이고 헤더 license는 AGPL-3.0-only다
- [x] #3 .source-header.json(제외: README.md, practice/**/main.*, .skeleton/**, backlog/** 등)을 확정하고 source-header init으로 헤더를 넣고, 파일마다 한 줄 description을 쓴다. source-header lint --strict 오류 0
- [x] #4 코드가 바뀌지 않았다: 변경 파일마다 py는 ast.dump 동일, sh는 bash -n·shfmt -mn 구조 동일, c·cpp는 오브젝트 동일, md는 헤더를 뺀 본문이 바이트 동일이다
- [x] #5 규격(source-header README '본문 노트 표식')에 따라 손으로 쓴 핵심 소스의 중요한 지점 줄 끝에 '---- N' 표식을 달고 하단에 노트를 쓴다(번호 연속·표식:노트 1:1). 생성 파일·테스트·마크다운은 헤더만 둔다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 source-header lint --strict . 오류 0 (출력을 Implementation Notes에 첨부)
- [x] #2 저장소의 기존 테스트·빌드가 통과한다(이 환경에서 못 돌리는 것은 건너뛴 이유와 함께 기록)
- [x] #3 description을 무작위 20개 이상 표본 검토했다(생성 문장은 규칙을 검토)
- [x] #4 표식 번호 연속·1:1 확인 출력과 코드 무변경 증명 결과를 Implementation Notes에 첨부했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-12)가 비공개로 남은 저장소에도 공개한 11개와 같은 헤더·표식을 달라고 했다. 이 카드는 databases을 맡는다. 계획: ~/.claude/plans/shimmering-spinning-cherny.md.

### Objective
소스 197개(practice 162 중 main.* 54 제외, scripts 33, compose.yaml·docker-compose.yml), 다른 md 62개(PITFALLS.md 54 등). 생성기 없음. 테스트는 scripts/test.sh이고 Docker가 필요한 부분이 있다.

### Assessment
practice의 테스트·기타 파일(108)은 생성물이라 경로 기반으로 정해진 description을 스크립트로 넣는다. scripts 33개는 핵심은 표식까지. Docker가 필요한 테스트는 못 돌릴 수 있고 그러면 건너뛴 사실을 기록한다. 모든 작업은 origin/main에서 판 git worktree에서 하고 로컬 작업 폴더는 건드리지 않는다. 읽기가 필요한 부분(description·표식)은 서브에이전트(새 컨텍스트)에 맡기고, 에이전트 보고는 믿지 않고 같은 검증을 다시 돌린다. 에이전트는 편집만 하고 커밋은 내가 한다.

### Plan
1. worktree 생성(origin/main). 인프라 커밋: .mailmap, .source-header.json (AC #1 #2).
2. 헤더 커밋: source-header init (AC #3), 생성기가 없는 파일은 경로 기반 정해진 description 또는 서브에이전트가 쓴 description.
3. 서브에이전트가 description·표식·노트를 쓴다(Edit만, 같은 파일을 동시에 고치지 않는다) (AC #3 #5).
4. 검증: lint --strict, 코드 무변경 증명, 기존 테스트·빌드, 표식 번호 연속·1:1 (AC #4).
5. 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 2026-11-17 병합 후 재검증(main 기준, 에이전트 보고가 아니라 직접 다시 돌린 결과)
- PR: #1(68c2889..224a95c)
- 라이선스·작성자: LICENSE 는 AGPL-3.0 본문, 추적 파일 헤더의 license 는 전부 AGPL-3.0-only, .mailmap 커밋됨
- lint: 깨끗한 main 클론에서 `source-header lint --strict .` rc=0 (로컬 작업 폴더의 오류는 추적되지 않는 로컬 파일뿐)
- 코드 무변경(M 205개): md 본문 바이트 동일 62, 주석 외 줄 동일 111(sql·js·yaml), py ast 동일 24, sh shfmt -mn 동일 8
- 표식: 4개 파일 23개, 번호 연속·노트 1:1 위반 0
- 테스트: py 26 py_compile, sh 8 bash -n, yaml 2 파싱 통과. practice 정답 검증(scripts/test.sh)은 DB 컨테이너가 필요해 건너뜀(코드 무변경은 위 비교로 증명)
- description 표본 20개 검토: practice 생성 파일은 '책·장·절 + 파일 역할(생성 파일)' 정해진 문장, scripts 는 개별 서술
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
databases practice 생성 파일 162개와 scripts·문서 43개에 헤더, 핵심 4개에 표식 23개를 달았다. 병합 후 lint 0, 코드 무변경 재확인(DB 컨테이너가 필요한 practice 정답 검증은 건너뜀). (PR coralstay/databases#1)
<!-- SECTION:FINAL_SUMMARY:END -->

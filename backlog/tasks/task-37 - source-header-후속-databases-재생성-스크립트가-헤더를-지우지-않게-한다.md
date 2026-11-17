---
id: TASK-37
title: 'source-header 후속: databases 재생성 스크립트가 헤더를 지우지 않게 한다'
status: Done
assignee: []
created_date: '2026-11-12T11:37:00Z'
updated_date: '2026-11-17T12:41:00Z'
labels:
  - source-header
  - followup
  - round2
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
2차 라운드(TASK-29~34)로 databases 에 source-header 헤더를 달았다. 그런데 일부 생성 스크립트는 파일을 통째로 다시 써서 다시 돌리면 헤더가 조용히 사라진다. 병합된 PR 과 에이전트 보고(2026-11-12)에서 확인했다.

## 범위
파일을 다시 쓸 때 기존 파일 맨 위의 source-header 헤더를 보존한다(내용 생성 로직은 건드리지 않는다). 저장소마다 작은 도우미 `keep_header(path, new_text)` 를 둔다: 기존 파일에 헤더가 있으면 새 내용 앞에 그대로 붙이고, 없으면 만들지 않는다. 이미 헤더가 있으면 두 번 돌려도 결과가 같다(멱등).

## 고칠 쓰기 지점
- scripts/scaffold_engine.py: schema 파일(166행)·test 파일(173행) 쓰기
- scripts/snippets.py: export md(308행)·posts(366행) 쓰기

## 하지 않는 것
README.md 와 학습자가 타이핑하는 main.* (제외 대상). 생성 내용 자체의 변경. 실제 저장소 파일을 덮어쓰는 재생성 실행(임시 복사본에서만 확인).

## 참고
scaffold_engine.py 는 practice 의 schema/test 파일을 재생성 때마다 덮어쓴다(54개 PITFALLS.md·102개 sql·6개 js 는 이번에 헤더를 달았다).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 도우미 keep_header(path, new_text) 를 추가한다(테스트 먼저): 기존 파일에 source-header 헤더가 있으면 새 내용 앞에 그대로 붙이고, 없으면 만들지 않는다. 헤더 보존은 두 번 돌려도 결과가 같다(멱등)
- [x] #2 카드 본문 '고칠 쓰기 지점'의 모든 파일 쓰기에 도우미를 적용한다. 헤더를 뺀 생성 내용은 변경 전과 바이트 동일하다
- [x] #3 헤더가 있는 파일을 가진 임시 복사본에서 각 스크립트를 실제로 돌려 헤더가 유지됨을 보인다(실제 저장소 파일은 덮어쓰지 않는다). 돌릴 수 없는 스크립트는 이유와 함께 단위 테스트로 대체한다
- [x] #4 source-header lint --strict . 오류 0 이고 기존 테스트·검증 스크립트가 변경 전과 같은 결과다(이 환경에서 못 돌리는 것은 이유 기록)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 테스트 먼저 작성: 변경 전 실패, 변경 후 통과 출력을 Implementation Notes 에 첨부했다
- [x] #2 source-header lint --strict . 종료 코드 0 출력을 Implementation Notes 에 첨부했다
- [x] #3 임시 복사본 재생성 증거(헤더 유지, 두 번째 실행 변경 0)를 첨부했다
- [x] #4 에이전트 보고를 믿지 않고 같은 검증을 직접 다시 돌렸다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
2차 라운드로 databases 에 단 헤더가 생성 스크립트를 다시 돌리면 사라진다(2026-11-12 병합 PR 후속). 유저가 후속 작업을 승인했다.

### Objective
카드 본문 '고칠 쓰기 지점' 참고. 각 쓰기 지점은 write_text/open('w') 로 파일을 통째로 쓴다. 헤더를 만들지 않는 생성기들이다.

### Assessment
생성 로직은 건드리지 않고 쓰기 직전에 기존 헤더를 보존하는 최소 변경이 안전하다. 저장소별로 독립된 작은 함수(공용 모듈을 두지 않음)가 유지보수상 단순하다. 실제 재생성은 파일을 덮어쓰므로 임시 복사본에서만 확인한다. 구현·검증은 서브에이전트(새 컨텍스트)에 맡기고 나는 같은 검증을 다시 돌린다. 에이전트는 편집만 하고 커밋은 내가 한다.

### Plan
1. origin/main 에서 worktree(~/githubs-work/databases, 브랜치 task/SH-<n>)를 판다. 인프라 변경 없음.
2. keep_header 테스트를 먼저 쓰고 실패를 확인한 뒤 도우미를 만든다(멱등 포함).
3. 쓰기 지점마다 도우미를 적용한다. 생성 내용이 바이트 동일한지 비교한다.
4. 임시 복사본 재생성, lint, 기존 검증을 돌린다.
5. 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 2026-11-17 병합 후 재검증(main 기준, 에이전트 보고가 아니라 직접 다시 돌린 결과)
- PR: #2(224a95c..ffdb3b2). 쓰기 지점: scaffold_engine.py schema(167행)·test(174행), snippets.py export(309행)·posts(367행) 모두 keep_header 적용
- 테스트 먼저: 새 test_header_keep.py 를 변경 전 코드에 돌리면 1 error(header_keep 없음), 변경 후 24 passed / 5 subtests passed
- 라이선스·작성자: LICENSE 는 AGPL-3.0 본문, 추적 파일 헤더의 license 는 전부 AGPL-3.0-only, .mailmap 커밋됨
- lint: 깨끗한 main 클론에서 `source-header lint --strict .` rc=0 (로컬 작업 폴더의 오류는 추적되지 않는 로컬 파일뿐)
- 임시 복사본 재생성: 깨끗한 클론 + 로컬 미추적 데이터로 generate_all.py·snippets.py --export·--export-blog 실행 — practice 339개를 다시 써도 헤더가 있던 182개 모두 유지, 내용도 HEAD 와 동일(tips/snippets.md 만 로컬 레지스트리 반영으로 본문이 바뀌고 헤더는 유지)
- 2회차: 바뀐 것은 snippets.md 의 '자동 갱신 일시' 한 줄뿐(원래 동작), 헤더·나머지 0 변경
- 기존 테스트: scripts py 26 py_compile 통과
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
databases 재생성 스크립트(scaffold_engine, snippets)가 keep_header 로 기존 헤더를 보존한다. 테스트 먼저(변경 전 error → 24 passed), 임시 복사본 재생성에서 헤더 182개 유지 확인. (PR coralstay/databases#2)
<!-- SECTION:FINAL_SUMMARY:END -->

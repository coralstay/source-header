---
id: DRAFT-12
title: 'agile-hooks 잔여 표식: 소스 3개와 테스트 파일 정책'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
updated_date: '2026-11-11T11:34:00Z'
labels:
  - source-header
  - followup
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
agile-hooks PR #3 이후 남은 것.
- 표식이 없는 소스: `design/build-diagrams.py`, `hooks/conftest.py`, `install.sh`
- 테스트 46개는 헤더만 있고 표식은 없다(소스에만 표식을 단다는 결정). 이 방침을 source-header README에 한 줄 적을지 결정.

## 완료 기준 (승격 후 --ac로 등록)
1. 소스 3개에 표식·노트(1:1, 연속)를 달고 py ast 동일, install.sh bash -n 통과.
2. 테스트 파일 정책을 README에 한 줄 명시(또는 필요 없다고 결정).
3. 전체 테스트·커버리지 100% 유지.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 agile-hooks의 표식이 없던 소스 3개(design/build-diagrams.py, hooks/conftest.py, install.sh)에 줄 끝 '---- N' 표식과 하단 노트를 단다(번호 연속, 표식:노트 1:1)
- [ ] #2 py 2개는 ast.dump가 변경 전과 같고 install.sh는 bash -n이 통과한다(코드 줄 무변경)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 전체 테스트가 통과하고 커버리지가 100%이다(출력을 Implementation Notes에 첨부)
- [ ] #2 source-header lint --strict .가 오류 0이다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
2026-11-11 유저 승인: agile-hooks PR #3 이후 남은 소스 3개에 표식을 마친다. 테스트 46개는 헤더만 두는 방침이다(README 한 줄은 DRAFT-10).

### Objective
- 표식이 없는 비테스트 소스는 design/build-diagrams.py, hooks/conftest.py, install.sh 세 개뿐이다(PR #3 시점 직접 확인).
- agile-hooks 브랜치 task/SH-13(PR #3)에 쌓는다. 이 저장소에는 testFirst 설정이 없고 전체 테스트 2509개·커버리지 100%.

### Assessment
작은 작업이라 서브에이전트 1명으로 충분하다. hooks/conftest.py는 pytest 설정 파일이라 표식 위치에 주의한다. 실행 코드는 바뀌지 않아야 하므로 py는 AST 동일로 증명한다.

### Plan
1. 3개 파일을 읽고 중요한 지점에만 표식과 하단 노트를 단다(줄 끝 \, 여러 줄 문자열, 이미 주석이 있는 줄은 피한다).
2. py 2개 ast 동일, install.sh bash -n, 마커 번호 연속·1:1을 확인한다.
3. 전체 테스트·커버리지와 lint --strict를 돌려 증거를 남기고 커밋한다.
<!-- SECTION:PLAN:END -->

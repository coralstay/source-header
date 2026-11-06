---
id: TASK-23
title: source-header 규격에 본문 노트 표식(---- N) 절 추가
status: In Progress
assignee: []
created_date: '2026-11-06T11:12:00Z'
updated_date: '2026-11-06T11:41:00Z'
labels:
  - source-header
  - spec
dependencies: []
documentation:
  - /Users/flynn_macpro/.claude/plans/shimmering-spinning-cherny.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-06, 플랜 ~/.claude/plans/shimmering-spinning-cherny.md): 헤더 적용(TASK-4~15) 뒤에 중요한 코드 줄 끝에 `---- N` 표식(번호만)을 달고, 설명은 파일 맨 아래 노트 구역에 모은다. 이미 주석이 있는 파일도 같은 포맷으로 일괄 변환한다(카드마다 `task/<ID>` 브랜치 → 커밋 → 다음 카드). 규격 본문은 이 저장소 README.md 한 곳에 둔다(별도 decision·CLAUDE.md·메모리 복제 없음). 이 카드가 표식 작업의 선행 카드다.

## 비즈니스 규칙
- B1 (AC #1) 코드 쪽 표식은 줄 끝 `<접두사> ---- N`(번호만)이고 번호는 파일 안에서 1부터 연속이다.
- B2 (AC #1) 설명은 파일 맨 아래 `======== 노트 ========` 구역에 `N 제목` 다음 `설명 / 관련: / 개념:` 순서로 쓰고 없는 항목은 생략한다. 표식과 노트는 일대일이다.
- B3 (AC #2) 접두사는 기존 확장자 표를 재사용한다(#, //, --). md는 대상 아님.
- B4 (AC #4) 이미 있는 주석(`@file/@path/@book` 배너, 자유 서술 주석)은 새 포맷으로 변환한다: 배너 정보는 프론트매터로, 코드 설명 주석은 표식+노트로 옮기고 정보를 버리지 않는다.

## 완료 기준 (승격 후 --ac로 등록)
1. README.md에 '본문 노트 표식' 절이 있다: 형식, 하단 노트 구역, 번호 규칙, 예시.
2. templates/*(python.py, shell.sh, typescript.ts, go.go, sql.sql)에 ---- N 예시가 있고 source-header lint가 통과한다.
3. 기존 테스트가 통과한다(줄 끝 표식이 헤더 파서에 영향을 주지 않음).
4. README.md에 기존 주석 변환 규칙(B4)이 적혀 있다.

## 범위 밖
표식 달기 자체(저장소별 후속 카드), 번호 연속성·관련 경로 lint 규칙(별도 카드), freeride 생성기 조사.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README.md에 '본문 노트 표식' 절이 있다: 형식, 하단 노트 구역, 번호 규칙, 예시
- [x] #2 templates/*(python.py, shell.sh, typescript.ts, go.go, sql.sql)에 ---- N 예시가 있고 source-header lint가 통과한다
- [x] #3 기존 테스트가 통과한다(줄 끝 표식이 헤더 파서에 영향을 주지 않음)
- [x] #4 README.md에 기존 주석 변환 규칙(B4)이 적혀 있다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 pytest 전체 통과 로그를 확인했다
- [x] #2 templates 5개가 source-header lint --strict를 통과했다
- [x] #3 README의 새 절이 AC #1·#4 항목을 모두 담고 있다
- [x] #4 도구 코드(source-header.py) 변경이 없거나, 있으면 유저 확인을 받았다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-06)가 모든 소스에 프론트매터·라이선스·본문 노트 표식을 달기로 했다. 표식은 코드 줄 끝 '# ---- N'(번호만), 설명은 파일 맨 아래 노트 구역에 모은다. 규격 본문은 이 README 한 곳에 둔다.

### Objective
- README.md에 헤더 필드·status·lint 규칙·접두사 표(# // -- 및 md 예외)가 이미 있다.
- templates/에 python.py, shell.sh, typescript.ts, go.go, sql.sql, markdown.md가 있다.
- 헤더 파서는 파일 맨 위 헤더만 읽는다. 본문의 줄 끝 '# ---- N'이 헤더 닫는 줄 '# ---'와 충돌하는지는 아직 테스트로 확인하지 않았다.
- 테스트는 test_source_header.py.

### Assessment
규격은 문서와 템플릿만 바꾸고 도구 코드는 건드리지 않는다. 번호 연속성·관련 경로 lint는 범위 밖(별도 카드). 위험은 본문의 '---- N'이 헤더 파서나 lint에 영향을 주는지이므로 테스트를 먼저 추가해 확인한다.

### Plan
1. AC #3: test_source_header.py에 '본문 줄 끝 # ---- N과 하단 노트 구역이 있어도 lint/init/fix 결과가 같다' 테스트(표식 <ID>#3)를 먼저 쓰고 통과를 확인한다(실패하면 파서 수정 범위를 유저에게 확인).
2. AC #1: README.md에 '본문 노트 표식' 절 추가(형식, 하단 노트 구역, 번호 규칙, 예시).
3. AC #2: templates 5개에 ---- N 예시와 노트 구역을 넣고 source-header lint가 통과하는지 확인.
4. AC #4: README에 기존 주석 변환 규칙(B4) 추가.
5. 테스트 전체 실행 후 AC·DoD 체크, final summary, Done.
<!-- SECTION:PLAN:END -->

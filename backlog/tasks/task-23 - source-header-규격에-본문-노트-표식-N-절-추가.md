---
id: TASK-23
title: source-header 규격에 본문 노트 표식(---- N) 절 추가
status: To Do
assignee: []
created_date: '2026-11-06T11:12:00Z'
updated_date: '2026-11-06T11:17:00Z'
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
- [ ] #1 README.md에 '본문 노트 표식' 절이 있다: 형식, 하단 노트 구역, 번호 규칙, 예시
- [ ] #2 templates/*(python.py, shell.sh, typescript.ts, go.go, sql.sql)에 ---- N 예시가 있고 source-header lint가 통과한다
- [ ] #3 기존 테스트가 통과한다(줄 끝 표식이 헤더 파서에 영향을 주지 않음)
- [ ] #4 README.md에 기존 주석 변환 규칙(B4)이 적혀 있다
<!-- AC:END -->

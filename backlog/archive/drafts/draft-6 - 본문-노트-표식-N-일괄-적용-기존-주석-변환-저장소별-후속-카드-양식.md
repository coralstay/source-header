---
id: DRAFT-6
title: 본문 노트 표식(---- N) 일괄 적용 + 기존 주석 변환 (저장소별 후속 카드 양식)
status: Draft
assignee: []
created_date: '2026-11-06T11:19:00Z'
labels:
  - source-header
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
헤더 적용(TASK-4~15 및 신규 draft)이 끝난 저장소마다 표식 작업을 한다. 규격: TASK-23. 이미 있는 주석(@file/@path/@book 배너, 자유 서술 주석)은 B4에 따라 새 포맷으로 변환한다.

## 절차 (저장소 1개 = 카드 1개)
1. task/<ID> 브랜치 → 서브에이전트가 디렉터리 단위로 파일을 읽고 중요한 지점에만 줄 끝 '---- N' + 하단 노트 작성.
2. 헤더 삽입 커밋과 표식 커밋을 분리한다.
3. 검증: lint --strict, 번호 1부터 연속, 코드 줄 변경 없음(git diff), 기존 테스트 통과.
4. 커밋하고 다음 저장소 카드로 넘어간다.

## 메모
저장소 순서: 소형 도구 → coralstay-software-factory → freeride 소스 → toy-project. 이 draft는 양식이고, 승격 시 저장소별로 복제한다. 선행: TASK-23, 각 저장소 헤더 적용 카드.
<!-- SECTION:DESCRIPTION:END -->

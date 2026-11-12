---
id: DRAFT-11
title: upkeep runbook 소스(.py·.c) 헤더·표식 적용
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
labels:
  - source-header
  - followup
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
TASK-24는 upkeep `main`에 있는 셸 6개만 처리했다. `runbooks/secretive-short-read/`의 `secretive_short_read_repro.py`·`framing_demo.c`는 푸시되지 않은 로컬 `task/TASK-1` 브랜치에만 있어 포함하지 못했다.

## 선행
upkeep의 `task/TASK-1`(53커밋)이 푸시·병합되거나 정리된 뒤.

## 범위
두 소스에 헤더(AGPL-3.0-only)와 표식. 같은 내용의 troubleshooting 저장소 파일과 중복 여부를 확인한다(사본이면 한쪽만).

## 완료 기준 (승격 후 --ac로 등록)
1. 두 파일에 lint --strict 통과 헤더와 표식·노트(1:1, 연속).
2. py ast 동일, C 오브젝트 파일 동일.
3. 노트에 비밀값·개인 정보가 없다.
<!-- SECTION:DESCRIPTION:END -->

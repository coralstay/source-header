---
id: DRAFT-12
title: 'agile-hooks 잔여 표식: 소스 3개와 테스트 파일 정책'
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
agile-hooks PR #3 이후 남은 것.
- 표식이 없는 소스: `design/build-diagrams.py`, `hooks/conftest.py`, `install.sh`
- 테스트 46개는 헤더만 있고 표식은 없다(소스에만 표식을 단다는 결정). 이 방침을 source-header README에 한 줄 적을지 결정.

## 완료 기준 (승격 후 --ac로 등록)
1. 소스 3개에 표식·노트(1:1, 연속)를 달고 py ast 동일, install.sh bash -n 통과.
2. 테스트 파일 정책을 README에 한 줄 명시(또는 필요 없다고 결정).
3. 전체 테스트·커버리지 100% 유지.
<!-- SECTION:DESCRIPTION:END -->

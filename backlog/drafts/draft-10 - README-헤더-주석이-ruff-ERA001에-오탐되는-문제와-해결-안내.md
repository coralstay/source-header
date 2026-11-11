---
id: DRAFT-10
title: 'README: 헤더 주석이 ruff ERA001에 오탐되는 문제와 해결 안내'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
labels:
  - source-header
  - followup
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
doctree에서 프론트매터 헤더(`# title: ...`)와 하단 노트(`# 1 제목`)가 ruff ERA001(주석 처리된 코드)에 306개 오류로 잡혔다(main은 0). 해결: pyproject에 `[tool.ruff.lint.per-file-ignores]`로 src·tests의 ERA001을 무시(doctree 커밋 3304c28). 다른 저장소는 영향이 없었다(ERA 미선택).

## 범위
source-header README에 '린터와의 충돌' 절을 추가한다: ERA001 오탐 원인, 무시 설정 예, 헤더가 코드로 오탐되는 다른 규칙이 있는지 확인한 범위(ruff 기본 + ERA).

## 완료 기준 (승격 후 --ac로 등록)
1. README에 절이 있고 예시 설정이 실제로 오류 0을 만든다(doctree에서 확인).
2. 도구 테스트(README 검사)가 통과한다.
<!-- SECTION:DESCRIPTION:END -->

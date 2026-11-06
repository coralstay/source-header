---
id: DRAFT-5
title: >-
  source-header 적용: freeride 하위 프로젝트(handcrafted-python·ts, math, real-estate,
  architecture)
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
기존 freeride 카드(TASK-7~11, 15)에 빠진 하위 프로젝트. 하위 디렉터리는 각자 별도 저장소(TASK-7 메모)이므로 저장소별로 쪼갠다.

## 범위
- 제외: freeride 안의 .md 전부, 학습자가 타이핑하는 main.<ext>, .skeleton/ 사본(트랜스크라이브), contents/·content_data/.
- 포함: scripts/, 생성기, test.* 등 그 외 소스.
- practice/*의 기존 @file/@path/@book 배너는 프로젝트별 scripts/apply_file_frontmatter.py가 만든다(handcrafted-python·cpp·coding-style-refactoring-principles에 각자 있음). 생성기가 source-header 헤더를 내보내게 고치거나 생성물을 .source-header.json에서 제외한다. 저장소별 조사 뒤에 결정한다.

## 메모
선행: TASK-23. 제외 두 파일의 정체(main.<ext>, .skeleton/ 사본)는 유저 확인 대기.
<!-- SECTION:DESCRIPTION:END -->

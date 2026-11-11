---
id: DRAFT-9
title: 'source-header 도구: 확장자 없는 파일·vim script·Terraform 지원'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
labels:
  - source-header
  - followup
  - tool
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
이번 적용에서 도구가 주석 접두사를 몰라 헤더·표식을 못 단 파일들이 있다.
- coding-agent-git-commit-tool `hooks/prepare-commit-msg` (786줄 핵심 Python 훅, 확장자 없음)
- omnivim: `bin/*`, `.vimrc`, `*.vim`, `.ideavimrc` (vim script는 `"` 접두사)
- toy-project: `*.tf` (HCL, `#`·`//`)
README의 접두사 표는 확장자 기반이라 위 파일은 대상이 아니다.

## 범위
- 확장자 없는 파일: shebang(`#!/usr/bin/env python3` 등)으로 언어를 판별하거나 설정 파일에서 경로별 접두사를 매핑한다 — 둘 중 어느 쪽이 맞는지 결정 필요.
- vim script `"` 접두사, HCL 접두사를 표에 추가할지 결정.
- 구현 시 README 접두사 표·테스트·`templates/`에 반영한다.

## 완료 기준 (승격 후 --ac로 등록)
1. 결정(shebang 판별 vs 경로 매핑)을 README에 적는다.
2. 도구가 prepare-commit-msg 같은 파일에 lint·init을 적용한다(테스트 포함).
3. 기존 대상 파일의 동작이 바뀌지 않는다(전체 테스트 통과).
<!-- SECTION:DESCRIPTION:END -->

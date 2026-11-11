---
id: DRAFT-9
title: 'source-header 도구: vim script·Terraform 주석 접두사 지원 (확장자 없는 파일은 대상 아님)'
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
updated_date: '2026-11-11T11:42:00Z'
labels:
  - source-header
  - followup
  - tool
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 결정 (유저, 2026-11-11)
**확장자 없는 파일의 언어는 읽지 않는다.** shebang(#!) 판별도, 경로별 접두사 설정도 하지 않는다. coding-agent-git-commit-tool의 `hooks/prepare-commit-msg`(786줄), omnivim의 `bin/*` 같은 확장자 없는 파일은 **의도적으로 대상이 아니다** — 헤더·표식이 없는 것이 정상이다. 이 규칙을 에이전트에게 강제하는 Claude Code 훅은 agile-hooks 백로그의 draft로 따로 만든다(이 카드의 범위가 아니다).

## 이 카드에 남은 범위
확장자가 있는데 도구가 접두사를 모르는 파일들만 다룬다.
- vim script: `.vim`, `.vimrc`, `.ideavimrc` (접두사 `"`) — omnivim
- Terraform/HCL: `.tf`, `.tftest.hcl` (접두사 `#` 또는 `//`) — toy-project (재개 시점에 필요)
- 위 둘을 지원할지, 하지 않기로 할지 먼저 결정한다.

## 하지 않는 것
확장자 없는 파일 지원, shebang 판별. README에 '확장자 없는 파일은 대상이 아니다'를 명시하는 것은 이 카드에 포함한다.

## 완료 기준 (승격 후 --ac로 등록)
1. vim script·Terraform 지원 여부를 결정하고 README 접두사 표에 반영한다(지원 안 하면 이유와 함께 '대상 아님'으로 명시).
2. README에 '확장자 없는 파일은 언어를 판별하지 않으며 대상이 아니다'가 적혀 있다.
3. 도구가 확장자 없는 파일을 모든 명령(lint, init, fix, status, new, 훅 진입점)에서 같은 방식으로 건너뛴다는 것을 테스트가 고정한다.
4. 기존 대상 파일의 동작이 바뀌지 않는다(전체 테스트 통과).
<!-- SECTION:DESCRIPTION:END -->

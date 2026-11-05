---
id: DRAFT-3
title: '테스트 git 격리: 전역 서명 설정(commit.gpgsign·Secretive) 때문에 생기는 간헐 실패와 Touch ID 폭주 막기'
status: Draft
assignee: []
created_date: '2026-11-05T15:12:00Z'
updated_date: '2026-11-05T15:12:00Z'
labels:
  - tests
  - git
  - signing
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
TASK-19(사람 키 Secure Enclave·Touch ID, AI 키 Secretive, 전역 commit.gpgsign=true) 뒤 2026-11-06 실측:
claude-code-agile-hooks 전체 테스트를 병렬(-n auto)로 돌리면 매번 1개씩 무작위로 실패(`git commit` exit 128). 단독·파일 단위 실행은 통과.
원인: 테스트가 임시 저장소에서 git commit을 하면서 사용자 전역 git 설정을 그대로 물려받아, 테스트 커밋마다 Secretive 서명을 요청한다. 병렬 실행 시 서명 요청이 몰려 간헐 실패.
사람 터미널에서는 기본 서명 키가 사람 키라 테스트 커밋마다 Touch ID 창이 뜬다.
source-header는 TASK-3에서 이미 격리함(GitCase: GIT_CONFIG_GLOBAL=빈 파일, GIT_CONFIG_NOSYSTEM=1).

## 대상(확인된 곳)
- coralstay-software-factory/components/claude-code-agile-hooks (hooks/test_*.py — 예: test_block_stop_if_dirty, test_pre_push_coverage_check)
- coralstay-software-factory/components/coding-agent-git-commit-tool (tests/ 144개, 임시 커밋 다수)
- 그 밖에 테스트에서 git commit을 하는 저장소는 TASK-20 재초기화 뒤 grep으로 확인

## 고칠 방향
테스트 공통 설정(conftest/fixture/헬퍼)에서 git 하위 프로세스가 사용자 전역·시스템 설정을 읽지 않게 한다: GIT_CONFIG_GLOBAL을 빈 임시 파일로, GIT_CONFIG_NOSYSTEM=1. 서명을 검증하는 테스트만 테스트용 키를 명시적으로 쓴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 agile-hooks와 git-commit-tool의 테스트가 사용자 전역·시스템 git 설정 없이 동작하고, 전체 병렬 실행을 5회 연속 돌려도 실패가 없다
- [ ] #2 사람 터미널에서 테스트를 돌려도 Touch ID 요청이 뜨지 않는다
- [ ] #3 TASK-20 재초기화 뒤 나머지 저장소에서 테스트 중 git commit을 하는 곳을 찾아 같은 방식으로 격리한다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 각 저장소 테스트 전체 통과 로그
<!-- DOD:END -->

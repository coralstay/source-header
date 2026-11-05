---
id: DRAFT-2
title: 'agile-hooks: [수동 검증] 수용 기준은 테스트 표식 대신 Notes의 증거로 Done 허용'
status: Draft
assignee: []
created_date: '2026-11-02T02:26:00Z'
updated_date: '2026-11-02T02:26:00Z'
labels:
  - agile-hooks
  - workflow
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-02): 테스트로 쓸 수 없는 운영·수동 작업 수용 기준은 "[수동 검증]"으로 표시하고, 터미널 작업 기록을 증거로 남긴다.
지금 require_test_first는 testFirst가 켜진 프로젝트에서 Done 전환 시 모든 AC·B·DoD에 테스트 표식(<ID>#n)을 요구해, 운영 카드(source-header TASK-3·16·19, 앞으로 TASK-20·22)가 Done으로 갈 수 없다. 표식만 맞추는 가짜 테스트를 만들 유인이 생긴다.
또 cwd가 backlog 프로젝트일 때만 검사해, 같은 카드라도 명령을 어디서 실행했는지에 따라 결과가 달라졌다(TASK-3 첫 Done은 cwd가 달라 통과).
claude-code-agile-hooks는 TASK-20에서 재초기화되므로, 이 카드는 재초기화 뒤 agile-hooks 저장소 backlog로 옮겨 진행한다.

## 제안 규칙
- AC·비즈니스 규칙·DoD 줄 본문이 "[수동 검증]"으로 시작하면, 테스트 표식 대신 Implementation Notes에 "증거: <ID>#<n>"(규칙은 <ID>#B<k>, DoD는 <ID>#D<n>) 줄이 있어야 Done을 허용한다
- 증거 줄에는 실행한 명령이나 확인 방법과 결과가 있어야 한다(빈 줄·표식만 있는 줄은 불인정)
- "[수동 검증]"이 아닌 항목은 지금처럼 테스트 표식을 요구한다
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 [수동 검증]으로 시작하는 AC·B·DoD는 Notes에 '증거: <ID>#…' 줄이 있으면 표식 없이 Done을 허용하고, 없으면 빠진 증거를 나열하며 거부한다
- [ ] #2 증거 줄이 표식만 있고 내용이 없으면 증거로 치지 않는다
- [ ] #3 [수동 검증]이 아닌 항목의 테스트 표식 요구는 그대로다
- [ ] #4 cwd와 무관하게 카드가 속한 프로젝트 기준으로 검사하는지 검토하고 결정을 decision으로 남긴다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 hooks/ 테스트 전체 통과
- [ ] #2 source-header TASK-3·16·19로 실제 Done 전환을 확인
<!-- DOD:END -->

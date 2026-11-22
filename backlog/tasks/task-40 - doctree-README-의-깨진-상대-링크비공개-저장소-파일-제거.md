---
id: TASK-40
title: 'doctree: README 의 깨진 상대 링크(비공개 저장소 파일) 제거'
status: Done
assignee: []
created_date: '2026-11-12T12:11:00Z'
updated_date: '2026-11-17T12:41:00Z'
labels:
  - source-header
  - followup
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
공개 저장소 doctree 의 README.md 427행이 `../coding-style-refactoring-principles/contents-overview-tocs.md#L27-L255` 를 링크한다. 이 경로는 다른(비공개) 저장소를 가리키고, 그 파일은 coding-style 저장소에도 존재하지 않는다. 공개된 README 에서는 항상 깨진다. 공개 11개 저장소의 상대 링크를 전수 검사(2026-11-12)해 찾았다.

## 범위
README.md 427행에서 링크만 제거하고 문장은 유지한다: '본 저장소([contents-overview-tocs.md](…))의 《Code Complete 2판》(Steve McConnell)이 정의한' → '《Code Complete 2판》(Steve McConnell)이 정의한'. 그 외 본문은 한 글자도 바꾸지 않는다.

## 하지 않는 것
다른 저장소에 contents-overview-tocs.md 를 만들지 않는다. CLI 도움말의 상대 경로 예시(`../databases` 등)는 링크가 아니라 사용 예시라 그대로 둔다. 책 내용 관련 변경 없음.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README.md 427행에서 상대 링크만 제거하고 문장은 유지한다. 변경은 그 한 줄뿐이다(git diff 로 확인)
- [x] #2 doctree 의 모든 .md 에 대해 상대 링크 전수 검사 결과 깨진 링크가 0이다(검사 스크립트 출력 첨부)
- [x] #3 source-header lint --strict . 오류 0 이다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 변경 전 깨진 링크 1건, 변경 후 0건 출력을 Implementation Notes 에 첨부했다
- [x] #2 diff 가 427행 한 줄임을 확인하는 출력을 첨부했다
- [x] #3 PR 에 병합 전 확인 사항(다른 저장소 파일을 만들지 않음)을 적었다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
공개 doctree README 에 비공개 저장소를 가리키는 깨진 링크가 있다. 유저가 정리하라고 했다(2026-11-12).

### Objective
README.md 427행 한 곳. 링크 대상 contents-overview-tocs.md 는 어느 저장소에도 없다.

### Assessment
링크만 제거하면 문장 의미(코드 작명 원칙이 Code Complete 2판을 따른다)는 그대로다. 한 줄 변경이라 서브에이전트 없이 인라인으로 처리하고, 검증은 상대 링크 전수 검사와 diff 로 한다.

### Plan
1. origin/main 에서 worktree(~/githubs-work/doctree, 브랜치 task/SH-<n>)를 판다.
2. 427행의 링크 표기만 제거한다.
3. 링크 전수 검사와 lint, diff 로 검증한다.
4. 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## 2026-11-17 병합 후 재검증(main 기준, 에이전트 보고가 아니라 직접 다시 돌린 결과)
- PR: #2(c547650..02c3738) 병합
- diff: README.md 한 줄(1 insertion, 1 deletion). 링크와 그 링크를 가리키던 '본 저장소(...)의' 부분만 빠지고 문장은 유지
- 상대 링크 전수 검사: 변경 전 61개 중 깨짐 1(README.md → ../coding-style-refactoring-principles/contents-overview-tocs.md), 변경 후 60개 중 0
- lint --strict rc=0
- PR 본문에 다른 저장소 파일을 만들지 않고 링크만 뺐다는 확인 사항 기재됨
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
doctree README 의 비공개 저장소 링크 1건을 한 줄 변경으로 제거했다. 깨진 상대 링크 1 → 0, lint 0. (PR coralstay/doctree#2)
<!-- SECTION:FINAL_SUMMARY:END -->

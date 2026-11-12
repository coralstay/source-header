---
id: DRAFT-16
title: 'omnivim: PRACTICAL_VIM_MAP.md 깨진 링크 6곳 정리(파일은 저작권으로 비공개)'
status: Draft
assignee: []
created_date: '2026-11-12T12:11:00Z'
updated_date: '2026-11-12T12:12:00Z'
labels:
  - source-header
  - followup
  - docs
  - copyright
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
omnivim 문서 5개가 PRACTICAL_VIM_MAP.md 를 링크하지만 이 파일은 저장소에 없다. 《Practical Vim》의 팁 목록·페이지 데이터를 담고 있어 TASK-16(2026-10-31)에서 저작권을 이유로 공개 대상에서 일부러 뺐다(.gitignore 36행, README 210행에 명시). 따라서 파일을 새로 만들어서는 안 되고 링크를 정리해야 한다. 공개 11개 저장소 링크 전수 검사(2026-11-12)로 확인했다.

## 범위 (링크 6곳, 문서 5개)
- README.md 5행: 144 Tips 배지의 링크 대상 제거(배지 표시는 유지)
- README.md 13행, PRACTICE_GUIDE.md 17행, PROJECT_STRUCTURE.md 17행: '144 팁 전체 색인…' 링크를 일반 텍스트로(또는 해당 줄 정리)
- AI_AGENT_INTERFACE.md 12행, JETBRAINS_VIM_KEYMAP_PRACTICE.md 12행: Quick Links 줄의 해당 항목 제거
- PROJECT_STRUCTURE.md 57행: 디렉터리 트리에서 PRACTICAL_VIM_MAP.md 항목을 '(저작권으로 비공개)'로 표시하거나 제거
본문의 나머지는 바이트 동일하게 유지한다.

## 하지 않는 것
PRACTICAL_VIM_MAP.md 를 만들거나 공개하지 않는다. scripts/audit_all.py 의 문서 검사 목록(388행)은 코드라 이번 범위 밖이다 — 파일이 없을 때의 동작만 Notes 에 기록한다. .gitignore·.source-header.json 은 그대로.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 카드 본문 '범위'의 링크 6곳과 PROJECT_STRUCTURE.md 의 트리 항목을 정리한다. PRACTICAL_VIM_MAP.md 를 만들거나 추적 대상에 넣지 않는다
- [ ] #2 각 문서의 변경은 해당 줄뿐이다. 변경 줄을 뺀 나머지 본문은 변경 전과 바이트 동일하다
- [ ] #3 omnivim 의 모든 .md 에 대해 상대 링크 전수 검사 결과 깨진 링크가 0이다(%20 등 URL 인코딩은 디코딩해서 검사)
- [ ] #4 source-header lint --strict . 오류 0 이다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 변경 전 깨진 링크 6건, 변경 후 0건 출력을 Implementation Notes 에 첨부했다
- [ ] #2 PRACTICAL_VIM_MAP.md 가 git ls-files 에 없음을 확인한 출력을 첨부했다
- [ ] #3 scripts/audit_all.py 가 파일이 없을 때 어떻게 동작하는지(코드 읽기 또는 실행 결과)를 Notes 에 기록했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
omnivim 문서 5개가 저작권으로 비공개한 PRACTICAL_VIM_MAP.md 를 링크한다. 유저가 정리하라고 했고 링크 상태를 확인하라고 했다(2026-11-12). 확인 결과 파일은 일부러 뺀 것이다.

### Objective
링크 6곳(README 2, PRACTICE_GUIDE, PROJECT_STRUCTURE, AI_AGENT_INTERFACE, JETBRAINS_VIM_KEYMAP_PRACTICE) + PROJECT_STRUCTURE 트리 1곳. .gitignore 36행·README 210행이 비공개 사유를 적고 있다.

### Assessment
파일을 만들면 책 팁 목록·페이지 데이터를 공개하게 되어 TASK-16 의 저작권 정리를 되돌린다. 링크만 정리하는 것이 안전하다. 문서 5개의 줄 단위 변경이라 인라인으로 처리하고 서브에이전트 검증은 필요 없다고 본다. 검증은 변경 줄 외 본문 바이트 동일과 링크 전수 검사로 한다.

### Plan
1. origin/main 에서 worktree(~/githubs-work/omnivim, 브랜치 task/SH-<n>)를 판다.
2. 6곳 링크와 트리 항목을 정리한다.
3. 줄 단위 diff, 링크 전수 검사, lint 로 검증하고 audit_all.py 동작을 확인한다.
4. 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

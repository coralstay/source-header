---
id: TASK-41
title: 'omnivim: PRACTICAL_VIM_MAP.md 를 공개하고 깨진 링크 6곳을 살린다'
status: To Do
assignee: []
created_date: '2026-11-12T12:11:00Z'
updated_date: '2026-11-12T12:16:00Z'
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
omnivim 문서 5개가 PRACTICAL_VIM_MAP.md 를 링크하지만 이 파일은 TASK-16(2026-10-31)에서 저작권을 이유로 공개 대상에서 뺐다(.gitignore 36행, README 210행). 유저가 2026-11-12 파일 내용을 확인한 뒤 공개하기로 결정했다(선택지 A).

## 파일 내용(로컬 21,842바이트, 확인함)
- 1장: 크로스 에디터 단축키 명세 — 직접 쓴 내용
- 2장: Tip 1~144 색인 — 책의 팁 제목(영어)과 직접 쓴 한국어 한 줄 요약. 책 본문·문장은 없고 페이지 번호 0건
- 책 페이지 번호와 concept 데이터는 scripts/data/all_tips.py 에 있고 이번에도 비공개 유지

## 범위
1. PRACTICAL_VIM_MAP.md 를 저장소에 추가(source-header 헤더만 붙이고 본문은 바이트 동일)
2. .gitignore 36행 `/PRACTICAL_VIM_MAP.md` 와 .source-header.json exclude 의 같은 항목만 제거
3. README 210행의 '포함하지 않습니다' 목록에서 PRACTICAL_VIM_MAP.md 만 뺀다. all_tips.py·official_sources 등 나머지 비공개 항목 문구는 그대로

## 주의
omnivim 은 공개 저장소다. 브랜치를 푸시하는 순간 병합 전에도 파일이 공개된다. 그래서 푸시 전에 최종 diff 를 유저에게 보여 주고 확인을 받는다.

## 하지 않는 것
all_tips.py, official_sources/, 공식 예제와 같은 실습 파일 공개. 책 페이지 번호 공개. 파일 본문 수정. audit_all.py 코드 변경.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 공개 전 점검: 파일에 책 페이지 번호가 없고(p.NN·쪽·page 검색 0건) 영어 문장은 팁 제목뿐임을 grep 출력으로 보인다. 본문 줄 수·크기를 기록한다
- [ ] #2 PRACTICAL_VIM_MAP.md 에 source-header 헤더(license AGPL-3.0-only, 한 줄 description)를 붙여 추적한다. 헤더를 뺀 본문은 로컬 파일과 바이트 동일하다
- [ ] #3 .gitignore 와 .source-header.json 에서 이 파일 항목만 제거한다. git check-ignore 로 all_tips.py·official_sources/ 등은 여전히 무시됨을 보인다
- [ ] #4 README 210행 문구에서 이 파일만 뺀다(나머지 비공개 항목 문구 불변). 변경은 그 줄뿐이다
- [ ] #5 omnivim 의 모든 .md 상대 링크 전수 검사(URL 디코딩 포함)에서 깨진 링크가 0이다(변경 전 6건). source-header lint --strict . 오류 0, scripts/audit_all.py 의 문서 검사 항목이 통과한다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 공개 전 점검 grep 출력과 바이트 동일 검증 출력을 Implementation Notes 에 첨부했다
- [ ] #2 링크 검사 변경 전 6건 / 변경 후 0건 출력을 첨부했다
- [ ] #3 푸시 전에 최종 diff 를 유저에게 보여 주고 확인받았다(공개 저장소라 푸시 즉시 공개됨)
- [ ] #4 audit_all.py 문서 검사 결과(통과 여부)를 Notes 에 기록했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저가 PRACTICAL_VIM_MAP.md 를 공개하기로 결정했다(2026-11-12, 선택지 A). TASK-16 의 비공개 방침은 이 파일에 한해 필요 이상으로 보수적이었을 수 있다(페이지 데이터는 all_tips.py 에만 있음).

### Objective
로컬 파일 21,842바이트, 페이지 번호 0건, 2장은 팁 제목+직접 쓴 한국어 요약, 1장은 직접 쓴 단축키 명세. 현재 .gitignore 36행·.source-header.json·README 210행이 비공개로 적고 있다. 공개본 문서 5곳(링크 6)이 이 파일을 가리켜 깨져 있다.

### Assessment
링크를 고치는 대신 파일을 공개하면 문서 구조가 원래 의도대로 복원되고 DRAFT-16 이전 제안보다 변경이 적다(문서 5개를 안 건드림). 위험: 팁 제목 전체 나열이 책 목차와 비슷하다는 점(낮지만 0은 아님, 유저가 수용). 공개 저장소라 푸시=공개이므로 푸시 전 유저 확인을 계획에 넣는다. 파일 추가와 줄 단위 수정뿐이라 서브에이전트 없이 인라인으로 하고 검증은 바이트 동일·링크 전수·lint 로 한다.

### Plan
1. origin/main 에서 worktree(~/githubs-work/omnivim, 브랜치 task/SH-<n>)를 판다.
2. 공개 전 점검(grep)을 돌려 출력을 남긴다.
3. 로컬 PRACTICAL_VIM_MAP.md 를 worktree 로 복사하고 source-header init 으로 헤더를 붙이고 description 을 쓴다. 본문 바이트 동일을 확인한다.
4. .gitignore·.source-header.json·README 210행을 줄 단위로 수정한다.
5. 링크 전수 검사, lint, audit_all.py 문서 항목을 확인한다.
6. 최종 diff 를 유저에게 보여 주고 확인받은 뒤에만 푸시·PR. 병합은 유저.
<!-- SECTION:PLAN:END -->

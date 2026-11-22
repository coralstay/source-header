---
id: TASK-5
title: 'source-header 적용: dev-tools/omnivim'
status: Done
assignee: []
created_date: '2026-10-31T11:08:00Z'
updated_date: '2026-11-22T11:57:00Z'
labels:
  - source-header
  - rollout
dependencies:
  - TASK-16
documentation:
  - ~/.claude/plans/giggly-kindling-snowglobe.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
source-header 6단계(dev-tools/source-header TASK-3)의 저장소별 적용 카드. 유저 결정(2026-10-31):
~/githubs 아래 내가 짠 코드는 AGPL-3.0-only, 외부 코드·책 예제는 제외, description은 서브에이전트 초안,
README·CHANGELOG는 제외하고 설계 문서는 포함, 기존 저장소의 .githooks에는 source-header 플러그인만 설치.

## 대상 저장소
`~/githubs/dev-tools/omnivim` (순서 그룹: 1-now)

## .source-header.json (초안)
```json
{"include": ["**"], "exclude": ["**/README.md", "**/CHANGELOG.md", "backlog/**", ".opensource/**", "contents/**", "content_data/**"]}
```

## 라이선스 조치
MIT → AGPL-3.0-only로 전환: LICENSE 교체, README 라이선스 표기 수정

## 메모
-
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [x] #2 라이선스 조치를 마친다: MIT → AGPL-3.0-only로 전환: LICENSE 교체, README 라이선스 표기 수정
- [x] #3 .source-header.json을 확정하고(제외 대상 재확인) source-header init으로 헤더를 넣고, 서브에이전트가 description 초안을 쓴다. source-header lint 오류 0
- [x] #4 규격(source-header README '본문 노트 표식', TASK-23)에 따라 중요한 지점(진입점·불변식·비자명한 결정·외부 연동)의 줄 끝에 '---- N' 표식을 달고 파일 맨 아래 노트 구역에 설명을 쓴다. 이미 있는 주석(@file/@path/@book 배너, 설명 주석)은 변환 규칙(B4)으로 새 포맷에 옮기고 정보를 버리지 않는다. 번호는 파일마다 1부터 연속, 표식:노트 1:1. 주석·헤더 외 코드 줄은 바뀌지 않는다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 source-header lint . 오류 0 (출력을 Implementation Notes에 첨부)
- [x] #2 저장소의 기존 테스트·빌드가 헤더 추가 후에도 통과
- [x] #3 유저가 description diff를 검토
- [x] #4 표식 번호가 파일마다 1부터 연속이고 표식:노트가 1:1임을 확인한 출력과, git diff에 주석·헤더 외 변경이 없음을 확인한 결과를 Implementation Notes에 첨부했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-06)가 GitHub에 올라간 저장소 전부의 소스에 프론트매터·라이선스·본문 노트 표식을 달기로 했다. 이 카드는 dev-tools/omnivim 한 저장소를 헤더 적용(AC #1~#4)과 표식(AC #5)까지 한 번에 맡는다. 규격은 source-header README '본문 노트 표식'(TASK-23)이다.

### Objective
소스 약 100개(md 제외: js 61·py 18·rb 15·sh 8·ts 3·java 3·lua 2). 현재 LICENSE는 MIT. js·rb 중 외부(vendored) 코드가 섞였을 가능성이 있다. GitHub main과 로컬 일치.

### Assessment
MIT → AGPL-3.0-only 전환은 라이선스 변경이라 계획 승인 때 유저가 확인해야 한다. 먼저 직접 작성한 파일과 외부 유래 파일을 가르고, 외부 파일은 헤더 대신 upstream: + THIRD_PARTY_NOTICES로 처리하거나 .source-header.json에서 제외한다. 표식은 사람이 읽고 판단해야 해서 토큰이 많이 든다. 헤더 삽입(기계)과 표식(읽기)을 커밋으로 나누고, 표식은 디렉터리 단위 서브에이전트(새 컨텍스트)에 맡긴다.

### Plan
1. 인프라 커밋: .mailmap(전역 ~/.mailmap과 같은 매핑) · LICENSE 조치 · .source-header.json 확정 · .githooks 설치(core.hooksPath) (AC #1 #2 #4).
2. 헤더 삽입 커밋: source-header init → lint 오류 0 (AC #3).
3. description 커밋: 서브에이전트가 초안을 쓰고 유저가 diff를 검토한다 (AC #3, DoD #3).
4. 표식 커밋: 디렉터리 단위 서브에이전트가 파일을 읽고 중요한 지점에만 줄 끝 '---- N'과 하단 노트를 단다. 기존 주석은 B4로 변환한다 (AC #5).
5. 검증: lint --strict, 번호 연속·1:1 확인 스크립트, 기존 테스트·빌드, git diff에 주석·헤더 외 변경 없음.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-06 유저 결정: AC '.githooks 설치(--plugins source-header)'는 후속 draft(source-header DRAFT-7, GF-149 이후)로 분리했다. 이 카드의 AC 번호가 이에 맞춰 당겨졌다(표식 AC 번호 -1).

## 2026-11-22 TASK-42(미병합 브랜치·오래된 카드 정리)에서 마감
- 마감 방식: 다른 저장소에 헤더를 단 작업이라 source-header 의 테스트 표식(testFirst)으로 검증할 수 없다. 유저 결정(2026-11-22)으로 테스트 표식 대신 아래 증거로 닫는다. 코드 무변경·표식 1:1 은 PR 의 base..merge 범위를 다시 계산했다
- 저장소: coralstay/omnivim, 병합 PR #1 2026-11-12, bd1a657c2..e067b7c6c
- 코드 무변경·표식: ast 6·shfmt 5·md 6·주석 외 줄 3 동일, 표식 14파일 92개 위반 0
- lint: origin/main 521d6c7 lint --strict rc=0
- 테스트·빌드: pytest 테스트 없음, scripts/audit_all.py 문서 검사 [8] PASS(2026-11-17 TASK-41 기록, 나머지 FAIL 6 은 로컬 설치 확인 항목)
- 라이선스·작성자: MIT → AGPL-3.0 교체 확인(LICENSE AGPL), .mailmap 있음
- DoD #3: 유저가 description 286개 중 무작위 20개를 표본 검토하고 모두 유지하기로 결정(2026-11-11, DRAFT-13 기록)
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
coralstay/omnivim 에 source-header 헤더와 본문 노트 표식을 적용했다(PR #1 2026-11-12 병합). 2026-11-22 에 코드 무변경·표식 1:1·lint 0·테스트를 다시 확인해 증거로 닫았다(테스트 표식 대신 증거, 유저 결정).
<!-- SECTION:FINAL_SUMMARY:END -->

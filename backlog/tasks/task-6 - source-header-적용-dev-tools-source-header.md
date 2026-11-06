---
id: TASK-6
title: 'source-header 적용: dev-tools/source-header'
status: To Do
assignee: []
created_date: '2026-10-31T11:08:00Z'
updated_date: '2026-11-06T11:55:00Z'
labels:
  - source-header
  - rollout
dependencies: []
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
`~/githubs/dev-tools/source-header` (순서 그룹: 1-now)

## .source-header.json (초안)
```json
{"include": ["**"], "exclude": ["**/README.md", "**/CHANGELOG.md", "backlog/**", ".opensource/**", "contents/**", "content_data/**"]}
```

## 라이선스 조치
이미 AGPL-3.0

## 메모
도구 자신: .source-header.json·.mailmap·.githooks만 추가(헤더는 이미 있음).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [ ] #2 라이선스 조치를 마친다: 이미 AGPL-3.0
- [ ] #3 .source-header.json을 확정하고(제외 대상 재확인) source-header init으로 헤더를 넣고, 서브에이전트가 description 초안을 쓴다. source-header lint 오류 0
- [ ] #4 git-commit-tool --plugins source-header로 .githooks를 설치하고(core.hooksPath=.githooks) 헤더 없는 파일 커밋이 막히는 것을 실측한다
- [ ] #5 규격(source-header README '본문 노트 표식', TASK-23)에 따라 중요한 지점(진입점·불변식·비자명한 결정·외부 연동)의 줄 끝에 '---- N' 표식을 달고 파일 맨 아래 노트 구역에 설명을 쓴다. 이미 있는 주석(@file/@path/@book 배너, 설명 주석)은 변환 규칙(B4)으로 새 포맷에 옮기고 정보를 버리지 않는다. 번호는 파일마다 1부터 연속, 표식:노트 1:1. 주석·헤더 외 코드 줄은 바뀌지 않는다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 source-header lint . 오류 0 (출력을 Implementation Notes에 첨부)
- [ ] #2 저장소의 기존 테스트·빌드가 헤더 추가 후에도 통과
- [ ] #3 유저가 description diff를 검토
- [ ] #4 표식 번호가 파일마다 1부터 연속이고 표식:노트가 1:1임을 확인한 출력과, git diff에 주석·헤더 외 변경이 없음을 확인한 결과를 Implementation Notes에 첨부했다
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저(2026-11-06)가 GitHub에 올라간 저장소 전부의 소스에 프론트매터·라이선스·본문 노트 표식을 달기로 했다. 이 카드는 dev-tools/source-header 한 저장소를 헤더 적용(AC #1~#4)과 표식(AC #5)까지 한 번에 맡는다. 규격은 source-header README '본문 노트 표식'(TASK-23)이다.

### Objective
도구 자신. py 3(source-header.py·test_source_header.py 등)·sh 1. 소스에는 이미 헤더가 있다. 아직 .source-header.json·.mailmap·.githooks가 없다. 규격·템플릿은 TASK-23에서 끝났다(PR #1).

### Assessment
헤더는 이미 있으므로 init은 건너뛰고 설정 파일만 추가한다. 도구 파일에 표식을 달 때 테스트가 파일 내용을 읽는 곳(템플릿·README 검사)이 깨지지 않는지 확인한다. 커밋 훅이 전체 테스트를 돌려서 AC마다 테스트가 통과해야 커밋된다. 표식은 사람이 읽고 판단해야 해서 토큰이 많이 든다. 헤더 삽입(기계)과 표식(읽기)을 커밋으로 나누고, 표식은 디렉터리 단위 서브에이전트(새 컨텍스트)에 맡긴다.

### Plan
1. 인프라 커밋: .mailmap(전역 ~/.mailmap과 같은 매핑) · LICENSE 조치 · .source-header.json 확정 · .githooks 설치(core.hooksPath) (AC #1 #2 #4).
2. 헤더 삽입 커밋: source-header init → lint 오류 0 (AC #3).
3. description 커밋: 서브에이전트가 초안을 쓰고 유저가 diff를 검토한다 (AC #3, DoD #3).
4. 표식 커밋: 디렉터리 단위 서브에이전트가 파일을 읽고 중요한 지점에만 줄 끝 '---- N'과 하단 노트를 단다. 기존 주석은 B4로 변환한다 (AC #5).
5. 검증: lint --strict, 번호 연속·1:1 확인 스크립트, 기존 테스트·빌드, git diff에 주석·헤더 외 변경 없음.
<!-- SECTION:PLAN:END -->

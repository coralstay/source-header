---
id: TASK-24
title: 'source-header 적용: upkeep (헤더 + 본문 노트 표식)'
status: To Do
assignee: []
created_date: '2026-11-06T11:56:00Z'
updated_date: '2026-11-06T11:59:00Z'
labels:
  - source-header
  - rollout
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-11-06): GitHub에 올라간 저장소 전체에 프론트매터·라이선스·본문 노트 표식을 단다. 규격은 TASK-23(README '본문 노트 표식'). 저장소당 카드 1장에 헤더 적용과 표식을 합친다(커밋은 분리). 유저 결정: 이 카드는 source-header 백로그에 둔다.

## 대상 저장소
`~/githubs/upkeep` (GitHub coralstay/upkeep, private). 소스: sh 7(scripts/·scripts/identity/), py 1(runbooks/secretive-short-read), c 1(framing_demo.c), 그 밖 zshrc.snippet 등.

## .source-header.json (초안)
```json
{"include": ["scripts/**", "runbooks/**"], "exclude": ["**/README.md", "**/NOTES.md", "**/issue-577-comment.md", "backlog/**", "scripts/identity/zshrc.snippet"]}
```

## 라이선스 조치
LICENSE는 이미 AGPL-3.0. 헤더 license는 AGPL-3.0-only.

## 메모
- 로컬 브랜치 task/TASK-1(upkeep)에 push 안 한 커밋 53개가 있다. 이 카드는 그것과 별개이며, 그 브랜치가 정리된 뒤 main에서 시작하는 것이 안전하다.
- upkeep 운영 스크립트는 신원·키 설정을 다루므로 노트에 비밀값·개인 정보를 쓰지 않는다(커밋 전 확인).
- .c 파일의 접두사는 //, zshrc.snippet은 주석 접두사를 몰라 대상에서 뺀다.

## 완료 기준 (승격 후 --ac로 등록)
1. .mailmap을 저장소에 커밋해 authors가 coralstay로 나온다.
2. 라이선스 조치를 마친다(이미 AGPL, 표기 확인).
3. .source-header.json을 확정하고 source-header init으로 헤더를 넣고 description 초안을 쓴다. lint 오류 0.
4. .githooks로 source-header 플러그인을 설치하고 헤더 없는 파일 커밋이 막히는 것을 실측한다.
5. 규격에 따라 표식과 하단 노트를 달고 기존 주석은 변환 규칙으로 옮긴다. 번호 연속·1:1, 주석·헤더 외 코드 변경 없음.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .mailmap(전역 ~/.mailmap과 같은 매핑)을 저장소에 커밋해 다른 클론·CI에서도 authors가 coralstay로 나온다
- [ ] #2 라이선스 조치를 마친다: 이미 AGPL-3.0, 헤더 license는 AGPL-3.0-only로 표기 확인
- [ ] #3 .source-header.json을 확정하고(제외 대상 재확인) source-header init으로 헤더를 넣고, 서브에이전트가 description 초안을 쓴다. source-header lint 오류 0
- [ ] #4 git-commit-tool --plugins source-header로 .githooks를 설치하고(core.hooksPath=.githooks) 헤더 없는 파일 커밋이 막히는 것을 실측한다
- [ ] #5 규격(source-header README '본문 노트 표식', TASK-23)에 따라 중요한 지점(진입점·불변식·비자명한 결정·외부 연동)의 줄 끝에 '---- N' 표식을 달고 파일 맨 아래 노트 구역에 설명을 쓴다. 이미 있는 주석은 변환 규칙(B4)으로 새 포맷에 옮기고 정보를 버리지 않는다. 번호는 파일마다 1부터 연속, 표식:노트 1:1. 주석·헤더 외 코드 줄은 바뀌지 않는다
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
유저(2026-11-06)가 GitHub에 올라간 저장소 전부의 소스에 프론트매터·라이선스·본문 노트 표식을 달기로 했다. 이 카드는 upkeep 한 저장소를 헤더 적용(AC #1~#4)과 표식(AC #5)까지 한 번에 맡는다. 규격은 source-header README '본문 노트 표식'(TASK-23)이다.

### Objective
소스 sh 7(scripts/·scripts/identity/)·py 1·c 1(runbooks/secretive-short-read). LICENSE는 AGPL-3.0. .mailmap·.githooks 없음. GitHub main과 로컬 일치하나 로컬 task/TASK-1에 push 안 한 53커밋이 있다.

### Assessment
운영 스크립트가 신원·키 설정을 다루므로 노트에 비밀값·개인 정보를 쓰지 않는다(커밋 전 확인). upkeep의 task/TASK-1 브랜치가 정리된 뒤 main에서 시작하는 것이 안전하다. 표식은 사람이 읽고 판단해야 해서 토큰이 많이 든다. 헤더 삽입(기계)과 표식(읽기)을 커밋으로 나누고, 표식은 디렉터리 단위 서브에이전트(새 컨텍스트)에 맡긴다.

### Plan
1. 인프라 커밋: .mailmap(전역 ~/.mailmap과 같은 매핑) · LICENSE 조치 확인 · .source-header.json 확정 · .githooks 설치(core.hooksPath) (AC #1 #2 #4).
2. 헤더 삽입 커밋: source-header init → lint 오류 0 (AC #3).
3. description 커밋: 서브에이전트가 초안을 쓰고 유저가 diff를 검토한다 (AC #3, DoD #3).
4. 표식 커밋: 서브에이전트가 파일을 읽고 중요한 지점에만 줄 끝 '---- N'과 하단 노트를 단다. 기존 주석은 B4로 변환한다 (AC #5).
5. 검증: lint --strict, 번호 연속·1:1 확인 스크립트, 기존 테스트·빌드, git diff에 주석·헤더 외 변경 없음.
<!-- SECTION:PLAN:END -->

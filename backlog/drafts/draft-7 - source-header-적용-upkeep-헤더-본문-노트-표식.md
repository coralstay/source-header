---
id: DRAFT-7
title: 'source-header 적용: upkeep (헤더 + 본문 노트 표식)'
status: Draft
assignee: []
created_date: '2026-11-06T11:56:00Z'
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

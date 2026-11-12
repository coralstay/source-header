---
id: DRAFT-14
title: 'CI 최종 방어선: PR에서 source-header lint로 헤더 없는 파일 차단 (GitHub Actions)'
status: Draft
assignee: []
created_date: '2026-11-12T03:23:00Z'
labels:
  - source-header
  - ci
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
TASK-28 파일럿(2026-11-12)에서 로컬 git 훅만으로는 '항상 강제'가 되지 않음이 측정으로 확인됐다.
- source-header가 PATH에 없는 곳(Claude/서브에이전트의 셸, 다른 클론, CI)에서는 훅이 '명령을 찾지 못해 건너뜁니다 (강제는 CI가 맡습니다)'라고 경고만 하고 커밋을 통과시킨다.
- git commit --no-verify로 우회된다.
- 훅이 말하는 'CI'가 우리 저장소에는 없다. 그래서 헤더 없는 파일이 PR로 들어와도 막는 곳이 없다.

## 범위
각 저장소의 PR에서 'source-header lint --strict'(또는 --since origin/main)를 돌려 헤더 없는 파일·규칙 위반이 있으면 실패하게 한다. GitHub Actions 워크플로.

## 열린 설계 질문 (승격 전에 유저 결정 필요)
1. **CI가 도구를 어떻게 얻나**: source-header는 stdlib만 쓰는 단일 파일 Python이지만 저장소가 지금 private이라 다른 저장소의 Actions가 그냥 받아 올 수 없다.
   - (가) 각 저장소 워크플로가 coralstay/source-header를 토큰으로 체크아웃(읽기 전용 PAT 또는 배포 키 필요, 비밀값 관리 부담)
   - (나) 중앙 재사용 워크플로를 coralstay/coralstay에 두고 호출(private 재사용 워크플로는 저장소 설정에서 접근 허용이 필요). upkeep TASK-1·5가 같은 저장소에 중앙 점검 워크플로를 두려고 한다 — 같이 설계하는 것이 맞다.
   - (다) 도구 사본을 각 저장소에 고정 SHA·체크섬으로 넣기(사본이 늘어 SSOT가 깨진다).
   - (라) source-header를 먼저 공개해 raw URL로 받기(공개 전환과 연결됨, upkeep TASK-6).
2. **필수 검사로 걸지 여부**: main 보호 규칙(required status check)은 private 저장소에서는 GitHub Pro 없이 못 건다(rulesets API가 거부했다). 공개 전환 뒤에야 병합을 막을 수 있다.
3. **범위**: lint --strict 전체냐, 바뀐 파일만(--since origin/main)이냐. 처음에는 바뀐 파일만이 부담이 작다.

## 관련
- TASK-28(.githooks 설치): 이 카드가 훅의 구멍을 메운다.
- upkeep TASK-5: '보안 기준선 점검' 카드가 CI 최종 방어선(Plan-Approved·Manual-Verified 검증)을 만든다고 계획에 적었다. 같은 중앙 워크플로 설계를 공유할 수 있다.
- upkeep TASK-6: 공개 전환.

## 완료 기준 (승격 후 --ac로 등록)
1. 위 열린 질문에 대한 유저 결정이 카드에 기록되어 있다.
2. 파일럿 저장소(troubleshooting)에서 헤더 없는 파일을 넣은 PR이 실패하고 헤더를 고치면 통과하는 것을 실제 Actions 실행으로 확인한다.
3. 나머지 저장소로 확대하는 방법(복사/호출)을 문서화한다.
<!-- SECTION:DESCRIPTION:END -->

---
id: DRAFT-8
title: 기존 주석을 본문 노트 포맷으로 변환 (B4, 저장소별)
status: Draft
assignee: []
created_date: '2026-11-11T11:29:00Z'
labels:
  - source-header
  - followup
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
2026-11-06 적용 라운드에서 서브에이전트들은 기존 주석을 지우지 않고 표식·노트만 추가했다(정보 보존 우선). 기존 설명 주석을 새 포맷(줄 끝 `---- N` + 하단 노트)으로 옮기는 변환(source-header README '기존 주석 변환', B4)은 유저 결정으로 이번에서 뺐다.

## 규모 (실측)
- dev-toolchain: 파일 42개·9,174줄 중 주석 전용 3,529줄. scripts/lib.sh 1,566줄, scripts/install/00_select.sh 507줄에 몰려 있다. 나머지 40개 파일은 합쳐서 약 1,450줄.
- agent-orchestrator: Javadoc과 '// == AC/DoD ==' 구분 주석을 그대로 둠.
- omnivim, git-commit-tool 등: 일부 변환됨(git-commit-tool은 이미 약 190줄을 노트로 옮겼다).

## 범위
- 변환 대상은 표식이 달린 지점을 설명하는 주석뿐이다. 자명한 주석·구분선·지시 주석(noqa, type:)은 대상이 아니다.
- 코드 줄은 바뀌지 않는다(py는 ast, 셸은 shfmt -mn, Java는 빌드·테스트로 증명).
- 저장소·파일 단위로 쪼개 서브에이전트에 맡긴다. dev-toolchain의 두 큰 파일이 첫 후보.

## 선행
각 저장소의 적용 PR이 병합된 뒤(변환은 그 위에서 한다). DRAFT-6(양식)은 이 카드로 대체한다.

## 완료 기준 (승격 후 --ac로 등록)
1. 대상 저장소 목록과 파일별 변환 대상 범위를 정한다.
2. 변환 후 주석·헤더 외 코드가 바뀌지 않았음을 저장소별 방식으로 증명한다.
3. 정보 손실이 없음을 확인한다(제거된 주석의 내용이 노트에 있다).
<!-- SECTION:DESCRIPTION:END -->

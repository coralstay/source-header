---
id: TASK-16
title: '공개 전환 전 라이선스·저작권 정리: 이력 재생성 5곳 + LICENSE 보강'
status: In Progress
assignee: []
created_date: '2026-10-31T11:41:00Z'
updated_date: '2026-11-02T02:25:00Z'
labels:
  - license
  - public
dependencies: []
documentation:
  - ~/.claude/plans/giggly-kindling-snowglobe.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## 배경
유저 결정(2026-10-31): ~/githubs 저장소를 공개(Public)로 전환할 예정이므로, 헤더 적용보다 먼저 라이선스·저작권 문제를 정리한다. 공개되면 git 이력도 공개되므로, 이력에 제3자 저작물이 있는 저장소는 이력을 새로 만들고 GitHub 저장소를 삭제 후 같은 이름으로 다시 만든다(force-push만으로는 refs/pull·캐시 객체가 남음). 책 원문 등은 로컬에 남기고 .gitignore로 추적에서 뺀다.

## 감사 결과 (2026-10-31, Explore 서브에이전트 + 메인 표본 확인)
| 저장소 | 문제 | 조치 |
|---|---|---|
| freeride/handcrafted-cpp | practice/c-and-cpp/07_extreme_c·08_prof_cpp, practice/jongmanbook, practice/stone-lecture(책 원본 약 4,000+), googletest 복사본, 큰 .in/.zip/.pdf/.eps, 이력의 scripts/book*_data, README '.gitignore로 격리' 허위 문구 | ignore + README 수정 + re-init + GitHub 재생성 |
| freeride/coding-style-refactoring-principles | docs/.ocr-cache 233개(교보eBook 워터마크·구매 ID), 책 9권 전체 목차(contents-overview-tocs.md, docs/*TOC*.json, docs/TREE_METADATA.*, docs/TESTING_AND_REFACTORING_METADATA.*), 이력의 tracks/** | ignore + re-init + 재생성 |
| dev-tools/omnivim | official_sources/** (Practical Vim 공식 예제 137), MIT | ignore + MIT→AGPL + re-init + 재생성 |
| freeride/handcrafted-java | 이력의 jls-spec/*.pdf(Oracle JLS/JVMS), .gitignore의 build.gradle.kts 모순 | ignore + re-init + 재생성 |
| freeride/databases | 책별 장·페이지·개념 요약 데이터 scripts/content*_data(이력엔 book*_data) | 유저 결정: 책 기반 데이터 ignore + re-init + 재생성 |
| dev-tools/central-docs-collector, dev-tools/ebpf-wire-to-code-tracer, freeride(루트) | 문제 없음. LICENSE 없음, ebpf는 .opensource/가 info/exclude로만 무시 | LICENSE + .gitignore 보강 |
| backlog 저장소(devOps-LifeCycle TASK-208, toy-project TASK-68, dev-toolchain TASK-175, factory TASK-23, git-commit-tool GF-150) | MIT→AGPL(devOps, dev-toolchain), LICENSE 없음(toy), gitleaks 오탐(toy 11건), devOps 로컬 쓰레기 1.2GB | 각 저장소 헤더 카드의 '라이선스 조치' AC를 먼저 진행(훅상 그 저장소 task 브랜치에서만 커밋 가능) |
| 나중(진행 중 작업): agent-orchestrator, claude-code-agile-hooks, doctree | 이미 AGPL 또는 문제 없음(doctree 서재 목록은 유지 결정) | 각 헤더 카드에서 |

## 원칙
- 되돌릴 수 없는 작업(.git 삭제, GitHub 저장소 삭제) 전에 git bundle 전체 백업 + bundle verify
- 재생성한 GitHub 저장소는 일단 Private. 공개 전환은 모든 정리가 끝난 뒤 유저가 따로 결정
- 공개 전 마지막으로 gitleaks와 서드파티 경로 재검사
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 [수동 검증] 재생성·변경 대상 저장소 전부를 git bundle로 ~/githubs-backup/2026-10-31/에 백업하고 git bundle verify가 통과한다
- [x] #2 [수동 검증] handcrafted-cpp: 책 원본 트랙·googletest·데이터 파일을 .gitignore로 빼고(로컬 파일 유지) README 문구를 사실대로 고친 뒤 새 이력으로 다시 만들고, GitHub 저장소를 삭제 후 같은 이름(Private)으로 재생성해 push한다
- [x] #3 [수동 검증] coding-style: OCR 캐시와 책 목차 파생 파일을 빼고 같은 방식으로 재생성한다
- [x] #4 [수동 검증] omnivim: official_sources를 빼고 MIT→AGPL-3.0-only로 바꾼 뒤 같은 방식으로 재생성한다
- [x] #5 [수동 검증] handcrafted-java: jls-spec을 빼고 .gitignore 모순을 고친 뒤 같은 방식으로 재생성한다
- [x] #6 [수동 검증] databases: 책 기반 데이터(scripts/content*_data 등)를 빼고 같은 방식으로 재생성한다
- [x] #7 [수동 검증] central-docs-collector, ebpf-wire-to-code-tracer, freeride 루트에 AGPL-3.0 LICENSE와 .gitignore 보강을 커밋한다(ebpf의 미커밋 변경은 건드리지 않음)
- [x] #8 [수동 검증] 재생성한 5곳의 새 이력(git rev-list --objects --all)에 서드파티 경로·PDF가 0이고 gitleaks가 no leaks(또는 확인된 오탐만)임을 기록한다
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 [수동 검증] 모든 백업 bundle verify 통과 로그를 Implementation Notes에 첨부
- [x] #2 [수동 검증] 재생성 저장소마다 gh repo view로 Private·새 커밋 수를 확인
- [x] #3 [수동 검증] 로컬의 무시된 원본 파일(책 코드 등)이 삭제되지 않고 남아 있음을 확인
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
### Subjective
유저가 공개 전환을 전제로 라이선스 이슈를 헤더 적용보다 먼저 모두 정리하라고 했다. 필요하면 .git을 삭제하고 ignore하라고 승인했고, 이력 재생성 4곳은 GitHub 저장소를 삭제 후 같은 이름으로 재생성, databases도 재생성하기로 정했다(2026-10-31).

### Objective
감사 결과는 Description 표. 재생성 대상 5곳 모두 PR·태그·해시 참조가 0이고 커밋은 34/2/23/5/2개다. backlog 저장소는 pre_commit_check 때문에 그 저장소 task 브랜치에서만 커밋할 수 있다.

### Assessment
filter-repo로 경로 목록을 맞추는 것보다, 로컬 파일은 유지한 채 .gitignore로 빼고 새 init 하는 편이 단순하고 누락 위험이 낮다. 재생성 후 첫 커밋에 LICENSE·.gitignore·.mailmap을 함께 넣는다. 공개 전환 자체는 이 카드에서 하지 않는다.

### Plan
1. 대상 전체 git bundle 백업(~/githubs-backup/2026-10-31/) + verify
2. 재생성 5곳: .gitignore 보강 → README·LICENSE 정리 → 추적 대상 목록을 미리 출력해 서드파티 경로가 0인지 확인 → .git 삭제 → git init → 첫 커밋 → gh repo delete → gh repo create(Private) → push
3. 문제없는 3곳: LICENSE + .gitignore 커밋
4. 전체 gitleaks·서드파티 경로 재검사 → Implementation Notes
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## AC #1 백업 (2026-10-31)
~/githubs-backup/2026-10-31/ 에 8개 저장소의 git bundle(--all) + .git tgz + GitHub 메타데이터(json, 5개)
bundle verify: handcrafted-cpp(34 commits), coding-style(2), omnivim(23), handcrafted-java(5), databases(2), central-docs(3), ebpf(3), freeride(2) — 모두 "is okay"
GitHub 5개 저장소: 이슈·PR·릴리스 0

## AC #2~#6 로컬 이력 재생성 (완료) — GitHub 삭제·재생성·push는 유저 실행 대기
pre_git_safety_check가 gh repo delete와 main push를 금지 → 우회하지 않고 유저 명령으로 넘김
| 저장소 | 새 커밋 | 추적 파일 | 제외(.gitignore, 로컬 유지) |
|---|---|---|---|
| handcrafted-cpp | d7dccf3 | 54 | /practice/ 전체, *.pdf/eps/ps. README 허위 문구 정정, MIT→AGPL |
| coding-style | e0d2f68 | 1,616 | docs/.ocr-cache, docs/*METADATA*, contents-overview-tocs.md, scripts/contents_data |
| omnivim | c8348af | 597 | official_sources, scripts/data/all_tips.py, PRACTICAL_VIM_MAP.md, 공식 예제와 같은 tip119·120·121 실습. MIT→AGPL(README 배지·절, PROJECT_STRUCTURE) |
| handcrafted-java | 291b8bc | 100 | jls-spec, Books, *.pdf |
| databases | 5d30188 | 319 | scripts/content*_data, practice/16~18(기출) |
로컬 원본(책 코드·OCR·데이터) 남아 있음 확인: handcrafted-cpp practice/, coding-style docs/.ocr-cache, omnivim official_sources, databases scripts/content01_data.
참고: 공개본에서는 데이터가 빠져 일부 생성기(databases generate_all, omnivim generate_practice, coding-style 메타데이터 생성기)를 그대로 돌릴 수 없다(README에 명시).

## AC #7 LICENSE 보강 (로컬 커밋 완료, push 대기)
central-docs-collector 16355e6, ebpf-wire-to-code-tracer b6595cb(미커밋 변경 24건은 건드리지 않음), freeride 3365ed5(layout.yaml 변경은 건드리지 않음)

## AC #8 재검사
5곳 모두 gitleaks no leaks, 1MB 초과 blob 0, 서드파티 경로 0(패턴 일치는 global_data·organizing_data 디렉터리명과 generate_jongmanbook_full.py 스크립트명 오탐)

## GitHub (유저 실행, 2026-10-31)
github-recreate.sh 실행: 5개 저장소 삭제 → 같은 이름 Private 재생성 → push. 메인 확인: handcrafted-cpp·coding-style·omnivim·handcrafted-java·databases 모두 PRIVATE, 원격 커밋 1개, 토픽 복원. central-docs-collector·ebpf·freeride main push, 원격 LICENSE 존재 확인.

## 수동 검증 증거
- 증거: TASK-16#1 — ~/githubs-backup/2026-10-31/ bundle 8개 `git bundle verify` → 모두 'is okay'
- 증거: TASK-16#2~#6 — 재생성 5곳 새 커밋(cpp d7dccf3, coding-style e0d2f68, omnivim c8348af, java 291b8bc, databases 5d30188), `gh api repos/coralstay/<n>/commits` → 1개, visibility PRIVATE(handcrafted-cpp는 재실행 사고 후 복구 push로 1개)
- 증거: TASK-16#7 — central-docs 16355e6, ebpf b6595cb, freeride 3365ed5 push, 원격 LICENSE 존재(`gh api repos/.../contents/LICENSE`)
- 증거: TASK-16#8 — 5곳 gitleaks 'no leaks found', 1MB 초과 blob 0, 서드파티 경로 0
- 증거: TASK-16#D1 TASK-16#D2 TASK-16#D3 — 위 Notes의 verify 로그·gh 확인·로컬 원본 유지(ls) 기록
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
공개 전환 전 라이선스·저작권 정리를 마쳤다. 8개 저장소를 bundle·tgz로 백업하고, 제3자 저작물이 이력에 있던 5곳(handcrafted-cpp, coding-style, omnivim, handcrafted-java, databases)은 해당 자료를 .gitignore로 빼서(로컬 유지) 이력을 새로 만들고 GitHub 저장소를 같은 이름 Private으로 재생성했다(삭제·push는 훅 때문에 유저가 실행). omnivim·handcrafted-cpp는 MIT→AGPL-3.0-only, 나머지는 AGPL LICENSE 추가. 새 이력은 gitleaks no leaks, 서드파티 경로·대용량 blob 0. 공개 전환 자체와 backlog 저장소(devOps, dev-toolchain, toy-project, factory, git-commit-tool)의 라이선스 조치는 각 저장소 카드에서 이어간다.
<!-- SECTION:FINAL_SUMMARY:END -->

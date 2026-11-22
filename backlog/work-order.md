<!-- work-order-hash: 2b803444a076e6470d2400b9c0b01ba3a419106d4934500bac1ab3e23728ab1f -->
# 작업 순서

`work_order.py`가 backlog/tasks의 의존(`dependencies`)으로 만든 파일이다 — 직접 고치지 말고 다시 생성한다. 같은 단계의 태스크는 병렬로, 단계는 위에서 아래로 순차로 진행한다. Done 태스크와 없는 태스크에 대한 의존은 충족된 것으로 본다.

| 단계 | ID | 제목 |
|---|---|---|
| 1 | TASK-4 | source-header 적용: dev-tools/central-docs-collector |
| 1 | TASK-5 | source-header 적용: dev-tools/omnivim |
| 1 | TASK-6 | source-header 적용: dev-tools/source-header |
| 1 | TASK-12 | source-header 적용: coralstay-software-factory/components/agent-orchestrator |
| 1 | TASK-13 | source-header 적용: coralstay-software-factory/components/claude-code-agile-hooks |
| 1 | TASK-14 | source-header 적용: dev-tools/ebpf-wire-to-code-tracer |
| 1 | TASK-15 | source-header 적용: freeride/doctree |
| 1 | TASK-24 | source-header 적용: upkeep (헤더 + 본문 노트 표식) |
| 1 | TASK-25 | README: 헤더 주석이 ruff ERA001에 오탐되는 문제와 해결 안내 |
| 1 | TASK-26 | agile-hooks 잔여 표식: 소스 3개와 테스트 파일 정책 |
| 1 | TASK-27 | 기존 주석을 본문 노트 포맷으로 변환 — dev-toolchain 1차 (scripts/lib.sh, scripts/install/00_select.sh) |
| 1 | TASK-28 | 저장소별 .githooks 설치: source-header 플러그인으로 헤더 없는 커밋 차단 (파일럿 후 확대) |
| 1 | TASK-35 | source-header 적용 2차: handcrafted-python |
| 1 | TASK-36 | source-header 적용 2차: ebpf-wire-to-code-tracer (마지막) |
| 1 | TASK-42 | 미병합 브랜치(task/TASK-4·25·20) 병합과 오래된 카드 정리 |

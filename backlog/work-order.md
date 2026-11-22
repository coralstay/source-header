<!-- work-order-hash: c12100796eb28451483c31af54150bbb4985a5cf16fe64a5e21f428fa9b5887b -->
# 작업 순서

`work_order.py`가 backlog/tasks의 의존(`dependencies`)으로 만든 파일이다 — 직접 고치지 말고 다시 생성한다. 같은 단계의 태스크는 병렬로, 단계는 위에서 아래로 순차로 진행한다. Done 태스크와 없는 태스크에 대한 의존은 충족된 것으로 본다.

| 단계 | ID | 제목 |
|---|---|---|
| 1 | TASK-14 | source-header 적용: dev-tools/ebpf-wire-to-code-tracer |
| 1 | TASK-26 | agile-hooks 잔여 표식: 소스 3개와 테스트 파일 정책 |
| 1 | TASK-27 | 기존 주석을 본문 노트 포맷으로 변환 — dev-toolchain 1차 (scripts/lib.sh, scripts/install/00_select.sh) |
| 1 | TASK-28 | 저장소별 .githooks 설치: source-header 플러그인으로 헤더 없는 커밋 차단 (파일럿 후 확대) |
| 1 | TASK-35 | source-header 적용 2차: handcrafted-python |
| 1 | TASK-36 | source-header 적용 2차: ebpf-wire-to-code-tracer (마지막) |

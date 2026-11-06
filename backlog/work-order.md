<!-- work-order-hash: dbcc5e5969623e4b351674c2d3a0593a709b9435facc3bec73f023ad328c0a5a -->
# 작업 순서

`work_order.py`가 backlog/tasks의 의존(`dependencies`)으로 만든 파일이다 — 직접 고치지 말고 다시 생성한다. 같은 단계의 태스크는 병렬로, 단계는 위에서 아래로 순차로 진행한다. Done 태스크와 없는 태스크에 대한 의존은 충족된 것으로 본다.

| 단계 | ID | 제목 |
|---|---|---|
| 1 | TASK-3 | source-header 6단계: ~/githubs 기존 파일 전체에 헤더 적용 (조사·순서·저장소별 절차) |
| 1 | TASK-6 | source-header 적용: dev-tools/source-header |
| 1 | TASK-12 | source-header 적용: coralstay-software-factory/components/agent-orchestrator |
| 1 | TASK-13 | source-header 적용: coralstay-software-factory/components/claude-code-agile-hooks |
| 1 | TASK-15 | source-header 적용: freeride/doctree |
| 1 | TASK-16 | 공개 전환 전 라이선스·저작권 정리: 이력 재생성 5곳 + LICENSE 보강 |
| 1 | TASK-17 | 중앙 점검 워크플로: 모든 public 저장소의 main-protect 규칙 자동 적용·복구 |
| 1 | TASK-18 | 공개 전 민감정보 정리: Drive ID·책 데이터·로컬/VM 정보·실명·옛 이메일 |
| 1 | TASK-19 | 신원·키·계정 보안 재설계: 사람 키(Secure Enclave)·AI 키(Claude·Antigravity)·이메일 비공개 |
| 2 | TASK-4 | source-header 적용: dev-tools/central-docs-collector |
| 2 | TASK-5 | source-header 적용: dev-tools/omnivim |
| 2 | TASK-14 | source-header 적용: dev-tools/ebpf-wire-to-code-tracer |
| 2 | TASK-20 | 기존 이력 보관과 전 저장소 재초기화: coralstay-archive 이전 + 로컬 mirror + 새 첫 커밋 |
| 2 | TASK-21 | 보안 기준선 점검으로 확장: 비밀값 스캔·push 보호·Dependabot·Actions 권한·SECURITY.md |
| 3 | TASK-22 | 저장소별 공개 전환: 재검사·기준선 확인 후 하나씩 |

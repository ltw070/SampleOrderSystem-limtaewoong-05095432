# PLAN: SampleOrderSystem (Mission2)

## 목표

Mission1 PoC에서 검증된 레이어를 통합하여 **반도체 시료 생산주문관리 시스템** 전체를 완성한다.  
TDD + Verify Harness 방식으로 개발하며, 각 Phase마다 문서 정합성·테스트·준수성 검증을 거친다.

---

## Verify Harness 실행 흐름

```
[Phase 시작 전]
  SubAgent1(doc-verifier) → 문서 정합성 확인

[Phase 구현]
  SubAgent2(ai-action) → TDD (Red → Green → Refactor)
                       → git commit + push

[Phase 완료 후]
  SubAgent3(test-verify)  ‖  SubAgent4(compliance-verify)  [병렬]
  → Main Agent 종합 판정
  → PASS: 다음 Phase 진행
  → FAIL: SubAgent2에 재작업 지시
```

---

## 구현 순서 (TDD: Red → Green → Refactor)

---

### Phase 0 – 프로젝트 환경 설정

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Green | `requirements.txt` | pytest, pytest-cov, pytest-mock 추가 |
| Green | `pytest.ini` | `addopts = --basetemp=tmp_pytest` (Windows tmp_path 권한 우회) |
| Green | `.gitignore` | `data/`, `tmp_pytest/`, `__pycache__/`, `.coverage` 추가 |
| Green | `data/` | 런타임 JSON 저장 디렉토리 생성 |

---

### Phase 1 – 도메인 모델 (Mission1 PoC1 재사용)

> PoC1에서 검증된 모델을 그대로 이식한다.

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_model/test_enums.py` | OrderStatus 5개 멤버 테스트 |
| Red | `tests/test_model/test_sample.py` | id `S-\d{3}`, yield_rate 범위, stock 음수 방지 |
| Red | `tests/test_model/test_order.py` | order_no 형식, quantity 양수, status 타입 |
| Red | `tests/test_model/test_production.py` | `ceil(shortage / (yield_rate * 0.9))`, total_time 계산식 |
| Green | `app/model/enums.py` | OrderStatus Enum |
| Green | `app/model/sample.py` | Sample dataclass |
| Green | `app/model/order.py` | Order dataclass |
| Green | `app/model/production.py` | ProductionItem dataclass |
| Refactor | `app/model/` | 공통 유효성 검사 정리, `__init__.py` |

**Verify Harness**: SubAgent3 + SubAgent4 병렬 실행

---

### Phase 2 – Repository 레이어 (Mission1 PoC2 재사용)

> PoC2에서 검증된 Repository 인터페이스와 JSON 구현체를 이식한다.

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_repository/test_sample_repository.py` | save, find_by_id, update_stock, delete, persistence (5개) |
| Red | `tests/test_repository/test_order_repository.py` | save, find_by_status, update_status, persistence (4개) |
| Green | `app/repository/base_repository.py` | `BaseRepository(ABC, Generic[T])` |
| Green | `app/repository/sample_repository.py` | `SampleRepository` 인터페이스 |
| Green | `app/repository/order_repository.py` | `OrderRepository` 인터페이스 |
| Green | `app/repository/json/json_sample_repo.py` | JSON 구현체 (Atomic Write, Enum/datetime 직렬화) |
| Green | `app/repository/json/json_order_repo.py` | JSON 구현체 |
| Refactor | `app/repository/` | 직렬화 공통 헬퍼 분리, conftest.py fixture |

**JSON 구현 규칙**: Atomic Write(`os.replace`), `OrderStatus` 문자열, `datetime` ISO 8601

**Verify Harness**: SubAgent3 + SubAgent4 병렬 실행

---

### Phase 3 – Controller 레이어

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_controller/test_sample_controller.py` | register → list → search 흐름 |
| Red | `tests/test_controller/test_order_controller.py` | place → approve(재고 충분) → CONFIRMED |
| Red | `tests/test_controller/test_order_controller.py` | place → approve(재고 부족) → PRODUCING |
| Red | `tests/test_controller/test_order_controller.py` | reject → REJECTED |
| Red | `tests/test_controller/test_order_controller.py` | ship (CONFIRMED → RELEASE) |
| Red | `tests/test_controller/test_production_controller.py` | FIFO 큐 동작, complete_production (PRODUCING → CONFIRMED) |
| Green | `app/controller/base_controller.py` | `BaseController(ABC)`, `run()` 추상 메서드 |
| Green | `app/controller/sample_controller.py` | `register_sample`, `list_samples`, `search_samples` |
| Green | `app/controller/order_controller.py` | `place_order`, `list_reserved`, `approve_order`, `reject_order`, `ship_order` |
| Green | `app/controller/production_controller.py` | `get_current`, `get_queue`, `complete_production` |
| Refactor | `app/controller/` | 의존성 주입 통일 |

**approve_order 분기 로직**:
```
재고(stock) >= 주문량(quantity) → CONFIRMED
재고(stock) <  주문량(quantity) → ProductionItem 생성 → PRODUCING
```

**Verify Harness**: SubAgent3 + SubAgent4 병렬 실행

---

### Phase 4 – View 레이어

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_view/test_base_view.py` | `display()` str 반환, `get_input()` 인터페이스 |
| Red | `tests/test_view/test_main_view.py` | 시스템 현황 + 메뉴 문자열 반환 |
| Red | `tests/test_view/test_sample_view.py` | 시료 목록/등록/검색 화면 문자열 반환 |
| Red | `tests/test_view/test_order_view.py` | 주문 화면 문자열 반환 |
| Red | `tests/test_view/test_monitor_view.py` | 모니터링 화면 문자열 반환 |
| Red | `tests/test_view/test_production_view.py` | 생산라인 화면 문자열 반환 |
| Red | `tests/test_view/test_shipment_view.py` | 출고 화면 문자열 반환 |
| Green | `app/view/base_view.py` | `BaseView(ABC)`, `display() → str`, `get_input()` |
| Green | `app/view/main_view.py` | 메인 메뉴 (시스템 현황 포함) |
| Green | `app/view/sample_view.py` | 시료 관리 화면 |
| Green | `app/view/order_view.py` | 주문 화면 |
| Green | `app/view/monitor_view.py` | 모니터링 화면 |
| Green | `app/view/production_view.py` | 생산라인 화면 |
| Green | `app/view/shipment_view.py` | 출고 화면 |
| Refactor | `app/view/` | 공통 포맷팅 유틸 분리 (`formatters.py`) |

**설계 원칙**: 모든 `display()` 메서드는 `str` 반환. `print()` 직접 호출 금지.

**Verify Harness**: SubAgent3 + SubAgent4 병렬 실행

---

### Phase 5 – Monitor 통합 (Mission1 PoC3 재사용)

> PoC3에서 검증된 Aggregator + Formatter를 통합한다.

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_monitor/test_aggregator.py` | REJECTED 제외, 재고 상태 판단, 생산 요약 계산 |
| Red | `tests/test_monitor/test_formatter.py` | format 메서드 str 반환, 여유/부족/고갈 포함 |
| Green | `app/monitor/aggregator.py` | `MonitorAggregator`, `StockLevel`, `StockStatus`, `ProductionSummary` |
| Green | `app/monitor/formatter.py` | `MonitorFormatter` (4개 메서드 str 반환) |
| Refactor | `app/monitor/` | YIELD_CORRECTION_FACTOR = 0.9 상수화 |

**Verify Harness**: SubAgent3 + SubAgent4 병렬 실행

---

### Phase 6 – main.py 통합 및 최종 검증

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Green | `main.py` | 전체 MVC + Repository + Monitor 배선 및 메뉴 루프 |
| 검증 | — | `pytest tests/ -v --cov=app --cov-report=term-missing` |
| 검증 | — | SubAgent1 최종 문서 정합성 검증 |
| 검증 | — | SubAgent3 + SubAgent4 최종 병렬 검증 |

**main.py 메뉴 루프**:
```
MainView.display()
  [1] SampleController.run()
  [2] OrderController.run()       (주문 접수)
  [3] OrderController.run()       (승인/거절)
  [4] MonitorView + Aggregator + Formatter
  [5] ProductionController.run()
  [6] OrderController.run()       (출고 처리)
  [0] 종료
```

---

## 커밋 전략

| prefix | 시점 | 예시 |
|--------|------|------|
| `test:` | Red 단계 완료 | `test: Phase1 도메인 모델 테스트 작성` |
| `feat:` | Green 단계 완료 | `feat: Phase2 JSON Repository 구현` |
| `refactor:` | Refactor 단계 완료 | `refactor: Phase3 Controller 의존성 주입 통일` |
| `docs:` | 문서 업데이트 | `docs: PRD/PLAN.md 작성` |

커밋 후 `git push origin main` (루트 repo).

---

## 완료 기준

- [ ] 모든 테스트 통과 (`pytest`)
- [ ] 커버리지 80% 이상
- [ ] PRD 9가지 기능 메뉴 전부 동작
- [ ] `display()` 전부 str 반환 (print() 미사용)
- [ ] MVC 단방향 의존성 유지
- [ ] Repository Atomic Write 구현
- [ ] Verify Harness (SubAgent1~4) 전부 PASS
- [ ] REPORT.md 기록

---

## Phase별 검증 체크리스트

| Phase | SubAgent1 | SubAgent2 | SubAgent3 | SubAgent4 |
|-------|-----------|-----------|-----------|-----------|
| Phase 1 | PRD ↔ 모델 일치 | TDD 완료 | 테스트 통과 | 모델 규칙 준수 |
| Phase 2 | PLAN ↔ Repository | TDD 완료 | persistence 테스트 | Atomic Write |
| Phase 3 | PLAN ↔ Controller | TDD 완료 | 승인 분기 테스트 | 의존성 방향 |
| Phase 4 | PLAN ↔ View | TDD 완료 | display() str 반환 | print() 미사용 |
| Phase 5 | PLAN ↔ Monitor | TDD 완료 | REJECTED 제외 | 계산식 정확성 |
| Phase 6 | PRD ↔ 전체 코드 | 통합 완료 | 전체 커버리지 80%+ | 전체 컨벤션 |

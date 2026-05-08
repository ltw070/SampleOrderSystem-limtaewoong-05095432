# 반도체 시료 생산주문관리 시스템 (S-Semi)

> **Repository**: `SampleOrderSystem-limtaewoong-05095432`  
> **개발자**: limtaewoong (ltw070)

---

## 프로젝트 개요

S-Semi 반도체 회사의 시료 생산·주문 관리를 위한 **콘솔 기반 시스템**입니다.

- **패턴**: MVC (Model / Controller / View) + Repository 패턴
- **생산 스케줄링**: FIFO 단일 생산 라인
- **데이터 영속성**: JSON 파일 기반 (앱 재시작 후에도 유지)
- **개발 방식**: Agentic Engineering (TDD + Verify Harness)

**주문 상태 흐름**

```
RESERVED → PRODUCING → CONFIRMED → RELEASE
         ↘ REJECTED
```

---

## 개발 진행 상태

| 단계 | 상태 | 결과 |
|------|------|------|
| Mission1 PoC 4종 | ✅ 완료 | 322/322 테스트, 평균 커버리지 96% |
| Mission2 PRD / PLAN | ✅ 완료 | UI 예시·도메인 모델·Phase 0~6 계획 |
| Mission2 구현 | ✅ 완료 | **223/223 테스트, 커버리지 96%** |

---

## 폴더 구조

```
PersonalProject/                    # git root → SampleOrderSystem repo
├── mission1/                       # PoC 4종 ✅ 완료
│   ├── 01_ConsoleMVC/              # 131/131, 96%  (개별 repo)
│   ├── 02_DataPersistence/         # 107/107, 95%  (개별 repo)
│   ├── 03_DataMonitor/             #  41/ 41, 93%  (개별 repo)
│   ├── 04_DummyDataGenerator/      #  43/ 43, 100% (개별 repo)
│   └── REPORT.md
├── mission2/
│   └── SampleOrderSystem/          # 메인 시스템 ✅ 완료
│       ├── app/
│       │   ├── model/              # Sample, Order, ProductionItem, OrderStatus
│       │   ├── controller/         # SampleController, OrderController, ProductionController
│       │   ├── view/               # 7종 View (display()→str, print() 미사용)
│       │   ├── repository/         # ABC 인터페이스 + JSON 구현체 (Atomic Write)
│       │   └── monitor/            # MonitorAggregator, MonitorFormatter
│       ├── tests/                  # 223개 테스트 (커버리지 96%)
│       ├── data/                   # 런타임 JSON 저장 (.gitignore)
│       ├── main.py                 # 진입점 (MVC 전체 배선)
│       ├── PRD.md
│       ├── PLAN.md
│       └── REPORT.md               # Phase별 진행 이력
├── docs/
│   └── PRD.md
├── 0_Ref/                          # 과제 원본 참고 문서
├── README.md
└── CLAUDE.md
```

---

## Mission2 시스템 기능

| 메뉴 | 기능 |
|------|------|
| [1] 시료 관리 | 시료 등록 / 목록 조회 / 이름 검색 |
| [2] 시료 주문 | 고객 주문 접수 (RESERVED 생성) |
| [3] 주문 승인/거절 | 재고 자동 분기 — 충분: CONFIRMED / 부족: PRODUCING |
| [4] 모니터링 | 상태별 주문 건수 (REJECTED 제외) + 재고 여유/부족/고갈 |
| [5] 생산라인 조회 | FIFO 대기 큐 + 생산 완료 처리 (PRODUCING→CONFIRMED) |
| [6] 출고 처리 | CONFIRMED 주문 출고 (→RELEASE) |
| [0] 종료 | — |

---

## Mission2 실행 방법

```bash
cd mission2/SampleOrderSystem
pip install -r requirements.txt
python main.py
```

---

## Mission2 테스트

```bash
cd mission2/SampleOrderSystem
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Mission2 개발 방식 (Agentic Engineering)

```
SubAgent1 (m2-doc-verifier)       ← 문서 정합성 검증 (읽기 전용)
      ↓
SubAgent2 (m2-ai-action)          ← TDD 구현 (Red→Green→Refactor)
      ↓
SubAgent3 (m2-test-verify)   ‖   SubAgent4 (m2-compliance-verify)   ← 병렬 검증
      ↓
Main Agent 종합 판정 → PASS / FAIL
```

| Phase | 내용 | 테스트 수 |
|-------|------|---------|
| Phase 0 | 환경 설정 (pytest.ini, requirements.txt) | — |
| Phase 1 | 도메인 모델 (Model) | 41개 |
| Phase 2 | Repository 레이어 (JSON + Atomic Write) | 35개 |
| Phase 3 | Controller 레이어 (비즈니스 로직) | 27개 |
| Phase 4 | View 레이어 (display()→str) | 93개 |
| Phase 5 | Monitor 통합 (Aggregator + Formatter) | 27개 |
| Phase 6 | main.py 통합 | — |
| **합계** | | **223개 / 커버리지 96%** |

---

## Mission1 PoC 결과 요약

| PoC | 테스트 | 커버리지 | 개별 Repository |
|-----|--------|---------|----------------|
| ConsoleMVC | 131 / 131 | 96% | [ConsoleMVC-limtaewoong-05095432](https://github.com/ltw070/ConsoleMVC-limtaewoong-05095432) |
| DataPersistence | 107 / 107 | 95% | [DataPersistence-limtaewoong-05095432](https://github.com/ltw070/DataPersistence-limtaewoong-05095432) |
| DataMonitor | 41 / 41 | 93% | [DataMonitor-limtaewoong-05095432](https://github.com/ltw070/DataMonitor-limtaewoong-05095432) |
| DummyDataGenerator | 43 / 43 | 100% | [DummyDataGenerator-limtaewoong-05095432](https://github.com/ltw070/DummyDataGenerator-limtaewoong-05095432) |

> 각 PoC는 제출용 개별 Repository에서도 관리됩니다.

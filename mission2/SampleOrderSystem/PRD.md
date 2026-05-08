# PRD: 반도체 시료 생산주문관리 시스템 (SampleOrderSystem)

> **프로젝트명**: SampleOrderSystem  
> **대상 회사**: S-Semi (가상)  
> **시스템 유형**: 콘솔(CLI) 기반 관리 시스템  
> **개발 방식**: Agentic Engineering (TDD + Verify Harness)  
> **Repository**: `SampleOrderSystem-limtaewoong-05095432`

---

## 1. 배경 및 목적

가상의 반도체 회사 **S-Semi** 는 다양한 반도체 시료(Sample)를 생산하여 연구소, 팹리스(Fabless) 업체, 대학 연구실 등의 고객에게 납품합니다.

시료는 주문이 들어오면 웨이퍼 공정 설비를 통해 제작되고, 검수를 거쳐 고객에게 출고됩니다.

최근 주문량이 급증하면서 엑셀·메모장 기반 관리의 한계가 드러났습니다.

> "어, 이 주문 처리됐나요?"  
> "공정 예약을 했는데, 언제 완성되는지 모르겠어요."  
> "이미 충분한 시료 재고가 있는데, 왜 추가 공정이 돌아가고 있나요?"

이러한 문제를 해결하기 위해 **체계적인 반도체 시료 생산주문관리 시스템**을 개발합니다.

---

## 2. 이해관계자 및 역할

| 역할 | 설명 |
|------|------|
| 고객 | 필요한 시료를 이메일로 요청 |
| 주문 담당자 | 고객 요청에 맞게 주문서 작성 및 관리 |
| 생산 담당자 | 시료 등록, 주문 수신 후 승인 또는 거절 처리 |

**역할별 흐름**

```
고객 (시료 요청자)
  → [시료 요청]
주문 담당자 (주문서 관리)
  → [주문서 전달]
생산 담당자 (시료 생산·승인)
  → [승인 / 거절]
주문 담당자
```

---

## 3. 주문 상태 흐름

```
주문 등록 (RESERVED)
  ├─ [거절] → REJECTED
  └─ [승인]
       ├─ 재고 충분 → CONFIRMED → RELEASE
       └─ 재고 부족 → PRODUCING → CONFIRMED → RELEASE
```

| 상태 | 의미 |
|------|------|
| `RESERVED` | 주문 접수 |
| `REJECTED` | 주문 거절 (모니터링 집계 제외) |
| `PRODUCING` | 승인 완료, 재고 부족으로 생산 중 |
| `CONFIRMED` | 승인 완료, 출고 대기 중 |
| `RELEASE` | 출고 완료 |

---

## 4. 도메인 모델

> Mission1 PoC1에서 검증된 공통 인터페이스를 그대로 재사용한다.

### 4.1 Sample

```python
@dataclass
class Sample:
    id: str                      # 형식: "S-001" ~ "S-999"  (S-\d{3})
    name: str
    avg_production_time: float   # 단위: min/ea, 양수 (> 0)
    yield_rate: float            # 범위: 0 < yield_rate <= 1
    stock: int                   # 단위: ea, 0 이상
```

### 4.2 OrderStatus

```python
class OrderStatus(Enum):
    RESERVED  = "RESERVED"   # 주문 접수
    REJECTED  = "REJECTED"   # 주문 거절
    PRODUCING = "PRODUCING"  # 재고 부족, 생산 중
    CONFIRMED = "CONFIRMED"  # 출고 대기
    RELEASE   = "RELEASE"    # 출고 완료
```

### 4.3 Order

```python
@dataclass
class Order:
    order_no: str            # 형식: "ORD-YYYYMMDD-XXXX" (4자리 순번)
    sample_id: str           # Sample.id 참조
    customer_name: str
    quantity: int            # 양수 (> 0)
    status: OrderStatus      # 초기값: RESERVED
    created_at: datetime
```

### 4.4 ProductionItem

```python
@dataclass
class ProductionItem:
    order_no: str
    sample_id: str
    shortage: int            # 부족분 = 주문량 - 재고
    actual_qty: int          # 실 생산량 = ceil(shortage / (yield_rate * 0.9))
    total_time: float        # 총 생산 시간 = avg_production_time * actual_qty (min)
```

**생산량 계산식**

```
실 생산량   = ceil(부족분 / (수율 × 0.9))
총 생산시간 = 평균_생산시간(min/ea) × 실_생산량
```

---

## 5. 기능 명세

### 5.1 메인 메뉴

전체 시료 요약 정보를 표시하고 기능별 메뉴를 제공한다.

```
반도체 시료 생산주문관리 시스템
================================================================
시스템 현황   2026-04-16 09:32:15

등록 시료   12종      총 재고    2,840 ea
전체 주문   36건      생산라인   3건 대기

[1] 시료 관리                    [2] 시료 주문
[3] 주문 승인/거절               [4] 모니터링
[5] 생산라인 조회                [6] 출고 처리
[0] 종료

선택 > _
```

| 메뉴 | 기능 |
|------|------|
| [1] | 시료 관리 (등록 / 목록 / 검색) |
| [2] | 시료 주문 (주문 접수) |
| [3] | 주문 승인/거절 |
| [4] | 모니터링 (주문량 / 재고량) |
| [5] | 생산라인 조회 |
| [6] | 출고 처리 |
| [0] | 종료 |

---

### 5.2 시료 관리

시료(Sample)는 시스템의 기본 단위다. 등록된 시료만 주문 가능하다.

| 기능 | 설명 |
|------|------|
| 시료 등록 | 시료 ID, 이름, 평균 생산시간, 수율 입력 후 등록 |
| 시료 목록 조회 | 등록된 전체 시료와 현재 재고 수량 표시 (페이지 이동 지원) |
| 시료 검색 | 이름 등 속성으로 특정 시료 검색 |

```
================================================================
[1] 시료 관리

[1] 시료 등록   [2] 시료 목록   [3] 시료 검색   [0] 위로
선택 > 2

등록 시료 목록  (총 12종)
ID        시료명                  평균 생산시간   수율    현재 재고
S-001     실리콘 웨이퍼-8인치     0.5 min/ea     0.92    480 ea
S-002     GaN 에피택셜-4인치      0.3 min/ea     0.78    220 ea
S-003     SiC 파워기판-6인치      0.8 min/ea     0.92    30 ea
S-004     포토레지스트-PR7        0.2 min/ea     0.95    910 ea
S-005     산화막 웨이퍼-SiO2      0.6 min/ea     0.88    0 ea
...외 7종   [N] 다음페이지
선택 > _
```

---

### 5.3 시료 주문

고객이 시료를 요청하면 주문 담당자가 주문을 생성한다.

- 입력: 시료 ID, 고객명, 주문 수량
- 생성 시 주문 상태: `RESERVED`
- 주문번호 형식: `ORD-YYYYMMDD-XXXX`

```
================================================================
[2] 시료 주문

시료 ID     > S-003
고객명      > 삼성전자 파운드리
주문 수량   > 200

입력 내용 확인
시료        SiC 파워기판-6인치  (S-003)
고객        삼성전자 파운드리
수량        200 ea

[Y] 예약 접수   [N] 취소
선택 > Y

예약 접수 완료.

주문번호    ORD-20260416-0043
현재 상태   RESERVED

※ 재고 확인은 [3] 승인 메뉴에서 직접 진행하세요.
```

---

### 5.4 주문 승인/거절

`RESERVED` 상태 주문 목록을 확인하고 승인 또는 거절한다.

**승인 처리 (자동 분기)**

- 재고 충분 → 즉시 `CONFIRMED`
- 재고 부족 → 생산 라인 자동 등록 후 `PRODUCING`

**거절 처리**

- 즉시 `REJECTED`로 전환

```
================================================================
[3] 주문 승인/거절

승인 대기 중인 예약 목록  (RESERVED)
번호    주문번호           고객                시료                수량      상태
[1]     ORD-20260416-0041  LG이노텍            산화막 웨이퍼-SiO2   300 ea    RESERVED
[2]     ORD-20260416-0042  SK하이닉스          실리콘 웨이퍼-8인치  150 ea    RESERVED
[3]     ORD-20260416-0043  삼성전자 파운드리   SiC 파워기판-6인치  200 ea    RESERVED
승인할 번호 > 3

재고 확인 중...

시료        SiC 파워기판-6인치   현재 재고  30 ea
주문 수량   200 ea              부족분     170 ea  ← 이 수량만 생산

재고 부족.  부족분 170 ea 승인하시겠습니까?  (실생산량 206 ea / 165 min)

[Y] 승인   [N] 주문 거절
선택 > Y

승인 완료.

상태 변경    RESERVED → PRODUCING
주문번호     ORD-20260416-0043
```

---

### 5.5 모니터링

담당자가 시스템 현황을 한눈에 파악할 수 있도록 주문 상태별 집계와 재고 현황을 제공한다.

**주문량 확인**

- 상태별(`RESERVED` / `CONFIRMED` / `PRODUCING` / `RELEASE`) 주문 건수 표시
- `REJECTED`는 제외

**재고량 확인**

| 재고 상태 | 기준 |
|-----------|------|
| 여유 | `stock >= 활성 주문(CONFIRMED+PRODUCING) 총 주문량` |
| 부족 | `0 < stock < 활성 주문 총 주문량` |
| 고갈 | `stock == 0` |

```
================================================================
[4] 모니터링   2026-04-16 09:32:15

[1] 주문량 확인   [2] 재고량 확인   [0] 위로
선택 > 1

상태별 주문 현황
RESERVED     3건
CONFIRMED    8건
PRODUCING    3건
RELEASE     18건

재고 현황
시료명                재고       상태    잔여율
실리콘 웨이퍼-8인치   480 ea     여유     80%
GaN 에피택셜-4인치    220 ea     여유     44%
SiC 파워기판-6인치     30 ea     부족      6%
산화막 웨이퍼-SiO2      0 ea     고갈      0%
```

---

### 5.6 생산라인 조회

FIFO 방식의 단일 생산 라인 현황을 표시한다.

**생산량 계산식**

```
실 생산량   = ceil(부족분 / (수율 × 0.9))
총 생산시간 = 평균_생산시간 × 실_생산량  (단위: min)
```

- 생산 완료 처리 시 주문 상태: `PRODUCING` → `CONFIRMED`
- 생산 완료 시 재고 증가(생산량만큼) → 주문량 차감

```
================================================================
[5] 생산라인 조회   FIFO 방식

생산라인 1개 (단일 라인)

현재 처리 중
  주문번호  ORD-20260416-0038   시료  SiC 파워기판-6인치
  주문량    80 ea   재고 30 ea  →  부족 50 ea  →  실생산량 61 ea  (수율 0.92 / 49 min)

대기 중인 주문  (FIFO 순)
순서    주문번호           시료                  주문량     부족분    실생산량    예상시간
1       ORD-20260416-0040  산화막 웨이퍼-SiO2     150 ea     150 ea    190 ea      114 min
2       ORD-20260416-0043  SiC 파워기판-6인치     200 ea     170 ea    206 ea      165 min
3       ORD-20260416-0044  GaN 에피택셜-4인치     300 ea      80 ea    114 ea       34 min

* 실생산량 = ceil(부족분 / (수율 * 0.9)),  FIFO 방식
```

**생산 완료 처리**

- 현재 생산 중인 항목에 대해 "완료" 입력 → `PRODUCING` → `CONFIRMED` 전환
- 생산 큐에서 해당 항목 제거

---

### 5.7 출고 처리

`CONFIRMED` 상태 주문에 대해 출고를 처리한다.

- 출고 후 주문 상태 → `RELEASE`
- 출고 수량, 처리 일시 출력

```
================================================================
[6] 출고 처리

출고 가능 주문  (CONFIRMED)
번호    주문번호           고객           시료                  수량
[1]     ORD-20260416-0042  SK하이닉스     실리콘 웨이퍼-8인치    150 ea
[2]     ORD-20260416-0035  DB하이텍       포토레지스트-PR7       400 ea
출고할 번호 > 1

출고 처리 완료.

주문번호    ORD-20260416-0042
출고수량    150 ea
처리일시    2026-04-16 09:34:02
상태        CONFIRMED → RELEASE
```

---

## 6. 기술 아키텍처

### 6.1 레이어 구조 (MVC + Repository)

```
┌─────────────────────────────────────────────────────┐
│                     View Layer                       │
│  MainView / SampleView / OrderView / MonitorView     │
│  ProductionView / ShipmentView                       │
│  ※ display() → str 반환 (print() 직접 호출 금지)    │
└──────────────────┬──────────────────────────────────┘
                   │ (단방향 의존)
┌──────────────────▼──────────────────────────────────┐
│                  Controller Layer                    │
│  SampleController / OrderController                  │
│  ProductionController                                │
└──────────┬──────────────────┬───────────────────────┘
           │                  │
┌──────────▼──────┐  ┌────────▼────────────────────────┐
│   Model Layer   │  │       Repository Layer           │
│  Sample / Order │  │  SampleRepository (ABC)          │
│  ProductionItem │  │  OrderRepository (ABC)           │
│  OrderStatus    │  │  JsonSampleRepo / JsonOrderRepo  │
└─────────────────┘  └─────────────────────────────────┘
```

### 6.2 Mission1 PoC 재사용 현황

| 레이어 | 출처 | 재사용 여부 |
|-------|------|-----------|
| 도메인 모델 (Sample, Order, ProductionItem, Enum) | PoC1 | ✅ 재사용 |
| Repository 인터페이스 + JSON 구현체 | PoC2 | ✅ 재사용 |
| MonitorAggregator + MonitorFormatter | PoC3 | ✅ 재사용 |
| SampleGenerator + OrderGenerator + Seeder | PoC4 | 선택적 재사용 |

### 6.3 패키지 구조

```
mission2/SampleOrderSystem/
├── app/
│   ├── model/
│   │   ├── enums.py           # OrderStatus
│   │   ├── sample.py          # Sample dataclass
│   │   ├── order.py           # Order dataclass
│   │   └── production.py      # ProductionItem dataclass
│   ├── controller/
│   │   ├── base_controller.py
│   │   ├── sample_controller.py
│   │   ├── order_controller.py
│   │   └── production_controller.py
│   ├── view/
│   │   ├── base_view.py       # display() → str
│   │   ├── main_view.py
│   │   ├── sample_view.py
│   │   ├── order_view.py
│   │   ├── monitor_view.py
│   │   ├── production_view.py
│   │   └── shipment_view.py
│   ├── repository/
│   │   ├── base_repository.py
│   │   ├── sample_repository.py
│   │   ├── order_repository.py
│   │   └── json/
│   │       ├── json_sample_repo.py
│   │       └── json_order_repo.py
│   └── monitor/
│       ├── aggregator.py
│       └── formatter.py
├── tests/
│   ├── test_model/
│   ├── test_controller/
│   ├── test_view/
│   ├── test_repository/
│   └── test_monitor/
├── data/                      # 런타임 JSON (.gitignore)
├── main.py
├── requirements.txt
└── pytest.ini
```

---

## 7. 비기능 요구사항

| 항목 | 요구사항 |
|------|---------|
| 실행 방식 | 콘솔(CLI) 기반 |
| 데이터 영속성 | 앱 재시작 후에도 데이터 유지 (JSON 파일) |
| 테스트 커버리지 | 80% 이상 |
| 아키텍처 | MVC 패턴, Repository 패턴 |
| 코드 품질 | display() → str 반환, 단방향 의존성, 의존성 주입 |

---

## 8. 개발 방식 (Agentic Engineering)

### 8.1 Verify Harness 구조

```
SubAgent1 (doc-verifier)      ← 문서 정합성 검증
      ↓
SubAgent2 (ai-action)         ← TDD 구현 (Red→Green→Refactor)
      ↓
SubAgent3 (test-verify)  ‖  SubAgent4 (compliance-verify)   ← 병렬 검증
      ↓
Main Agent 종합 판정 → REPORT.md
```

### 8.2 커밋 전략

| prefix | 시점 |
|--------|------|
| `test:` | Red 단계 완료 (실패 테스트 작성) |
| `feat:` | Green 단계 완료 (구현 완료) |
| `refactor:` | Refactor 단계 완료 |
| `docs:` | 문서 업데이트 |

---

## 9. 검증 기준 (TDD)

| 테스트 | 검증 내용 |
|--------|----------|
| `test_sample_model` | id 형식, yield_rate 범위, stock 음수 방지 |
| `test_order_model` | order_no 형식, 상태 전이 유효성 |
| `test_production_item` | `ceil(shortage / (yield * 0.9))` 계산식 |
| `test_sample_controller` | register → list → search 흐름 |
| `test_order_controller` | approve(재고 충분) → CONFIRMED, approve(재고 부족) → PRODUCING |
| `test_production_controller` | FIFO 큐, complete_production → CONFIRMED |
| `test_view_display` | 모든 display() 가 str 반환 (print() 미사용) |
| `test_repository` | CRUD + 영속성 (tmp_path fixture) |
| `test_monitor_aggregator` | REJECTED 제외 집계, 재고 상태 판단 |
| `test_monitor_formatter` | 포맷 문자열 반환 |

커버리지 목표: **80% 이상**

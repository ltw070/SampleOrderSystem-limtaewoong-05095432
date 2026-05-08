---
name: poc3-data-monitor
description: Mission1 PoC3 - DataMonitor 개발 에이전트. 저장된 데이터 상태를 콘솔에서 실시간 조회하는 관리자 도구를 TDD 방식으로 구현할 때 사용한다. 작업 디렉토리는 mission1/03_DataMonitor.
---

## 역할

`mission1/03_DataMonitor` PoC를 TDD 방식으로 개발하는 전담 에이전트다.
목표는 현재 저장된 데이터(시료, 주문, 재고 등)를 **콘솔에서 실시간 조회**할 수 있는 관리자 도구를 구현하는 것이다.

## 작업 디렉토리

`C:\reviewer\PersonalProject\mission1\03_DataMonitor`

## 패키지 구조 목표

```
03_DataMonitor/
├── app/
│   ├── model/              # 조회 대상 도메인 객체
│   ├── repository/         # 데이터 읽기 레이어
│   └── monitor/
│       ├── formatter.py    # 콘솔 출력 포맷터
│       └── monitor.py      # 모니터링 로직 (집계, 필터)
├── tests/
│   ├── test_model/
│   ├── test_repository/
│   └── test_monitor/
├── data/                   # 샘플 데이터 (.gitignore)
├── main.py
└── requirements.txt
```

## TDD 사이클 (엄수)

1. **Red** — 실패하는 테스트를 먼저 작성한다 (`pytest` 실행 → 실패 확인)
2. **Green** — 테스트를 통과하는 최소한의 코드를 작성한다
3. **Refactor** — 중복 제거, 네이밍 정리 (테스트는 여전히 통과해야 함)

## 개발 규칙

- **출력 로직은 반드시 테스트 가능하게 설계한다**
  - `print()`를 직접 호출하지 않고 문자열을 반환하는 함수로 구현한다
  - 테스트에서 반환값을 검증한다
- 모니터링 항목별 독립 테스트를 작성한다
  - 상태별 주문 수 집계 (`RESERVED` / `CONFIRMED` / `PRODUCING` / `RELEASE`)
  - 시료별 재고 현황 및 상태 표기 (여유 / 부족 / 고갈)
  - 생산라인 대기 목록
- `unittest.mock` 또는 `pytest-mock`으로 저장소 레이어를 Mock 처리해 단위 테스트를 격리한다
- 테스트 커버리지 목표: **80% 이상**

## 검증 명령

```bash
cd C:\reviewer\PersonalProject\mission1\03_DataMonitor
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

## 커밋 규칙

- `test: ` — 테스트 추가 (Red 단계)
- `feat: ` — 기능 구현 (Green 단계)
- `refactor: ` — 리팩토링 (Refactor 단계)

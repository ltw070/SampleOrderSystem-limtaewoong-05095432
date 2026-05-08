---
name: poc2-data-persistence
description: Mission1 PoC2 - DataPersistence 개발 에이전트. 파일/JSON/DB 방식의 데이터 영속성 구조를 TDD 방식으로 구현할 때 사용한다. 작업 디렉토리는 mission1/02_DataPersistence.
---

## 역할

`mission1/02_DataPersistence` PoC를 TDD 방식으로 개발하는 전담 에이전트다.
목표는 애플리케이션 재시작 후에도 데이터를 유지할 수 있는 **영속성 레이어**를 구현하는 것이다.

## 작업 디렉토리

`C:\reviewer\PersonalProject\mission1\02_DataPersistence`

## 패키지 구조 목표

```
02_DataPersistence/
├── app/
│   ├── model/              # Sample, Order 도메인 객체
│   └── repository/         # 영속성 레이어 (CRUD 인터페이스 + 구현체)
│       ├── base.py         # 추상 Repository 인터페이스
│       ├── json_repo.py    # JSON 파일 기반 구현
│       └── db_repo.py      # SQLite 기반 구현 (선택)
├── tests/
│   ├── test_model/
│   └── test_repository/
├── data/                   # 영속성 저장 경로 (.gitignore)
├── main.py
└── requirements.txt
```

## TDD 사이클 (엄수)

1. **Red** — 실패하는 테스트를 먼저 작성한다 (`pytest` 실행 → 실패 확인)
2. **Green** — 테스트를 통과하는 최소한의 코드를 작성한다
3. **Refactor** — 중복 제거, 네이밍 정리 (테스트는 여전히 통과해야 함)

## 개발 규칙

- Repository 인터페이스(`base.py`)를 먼저 정의하고, 구현체를 작성한다
- CRUD 4가지 동작을 각각 독립 테스트로 검증한다
  - `create`: 데이터 저장 후 파일/DB에 실제로 기록되었는지 확인
  - `read`: 저장된 데이터를 정확히 불러오는지 확인
  - `update`: 기존 레코드가 올바르게 변경되는지 확인
  - `delete`: 삭제 후 조회 시 존재하지 않는지 확인
- 테스트는 임시 경로(`tmp_path` fixture)를 사용해 실제 데이터를 오염시키지 않는다
- **데이터 영속성 검증**: 인스턴스를 새로 생성해도 데이터가 유지되는지 반드시 테스트한다
- 테스트 커버리지 목표: **80% 이상**

## 검증 명령

```bash
cd C:\reviewer\PersonalProject\mission1\02_DataPersistence
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

## 커밋 규칙

- `test: ` — 테스트 추가 (Red 단계)
- `feat: ` — 기능 구현 (Green 단계)
- `refactor: ` — 리팩토링 (Refactor 단계)

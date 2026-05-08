# CLAUDE.md

## 프로젝트 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| PRD (전체) | `docs/PRD.md` | 반도체 시료 생산주문관리 시스템 제품 요구사항 문서 |
| **PRD - Mission2** | `mission2/SampleOrderSystem/PRD.md` | Mission2 전용 PRD (UI 예시·도메인 모델·기술 아키텍처 포함) |
| **PLAN - Mission2** | `mission2/SampleOrderSystem/PLAN.md` | Phase 0~6 TDD 구현 계획 + Verify Harness 체크포인트 |
| **REPORT - Mission2** | `mission2/SampleOrderSystem/REPORT.md` | Phase별 진행 이력·Verify Harness 결과 (223/223, 96%) |
| REPORT - Mission1 | `mission1/REPORT.md` | Mission1 PoC 개발 결과 보고서 (322/322, 평균 96%) |
| PRD - PoC1 | `mission1/01_ConsoleMVC/PRD.md` | MVC 스켈레톤 + 전체 공통 도메인 모델 · Interface 정의 |
| PRD - PoC2 | `mission1/02_DataPersistence/PRD.md` | Repository 인터페이스 + JSON 영속성 구현 명세 |
| PRD - PoC3 | `mission1/03_DataMonitor/PRD.md` | 집계(Aggregator) · 포맷터(Formatter) 인터페이스 명세 |
| PRD - PoC4 | `mission1/04_DummyDataGenerator/PRD.md` | Dummy 생성기 · Seeder 인터페이스 명세 |

---

## 프로젝트 개요

**프로젝트명**: 반도체 시료 생산주문관리 시스템 (S-Semi)  
**형태**: 콘솔(CLI) 기반  
**패턴**: MVC (Model / Controller / View) + Repository 패턴  
**생산 스케줄링**: FIFO 단일 생산 라인

### 주문 상태 흐름

```
RESERVED → PRODUCING → CONFIRMED → RELEASE
         ↘ REJECTED
```

---

## 폴더 구조

```
PersonalProject/                    # ← git root (SampleOrderSystem repo)
├── mission1/                       # PoC 개발 (4종) ✅ 완료
│   ├── 01_ConsoleMVC/              # MVC 스켈레톤 코드 (개별 repo, 131/131, 96%)
│   ├── 02_DataPersistence/         # 데이터 영속성 처리 (개별 repo, 107/107, 95%)
│   ├── 03_DataMonitor/             # 데이터 모니터링 Tool (개별 repo, 41/41, 93%)
│   ├── 04_DummyDataGenerator/      # Dummy 데이터 생성 Tool (개별 repo, 43/43, 100%)
│   └── REPORT.md                   # PoC 개발 결과 보고서
├── mission2/                       # 메인 프로젝트 ✅ 완료
│   └── SampleOrderSystem/
│       ├── app/
│       │   ├── model/              # Sample, Order, ProductionItem, OrderStatus
│       │   ├── controller/         # SampleController, OrderController, ProductionController
│       │   ├── view/               # 7종 View (display()→str, print() 미사용)
│       │   ├── repository/         # SampleRepository, OrderRepository + JSON 구현체
│       │   └── monitor/            # MonitorAggregator, MonitorFormatter
│       ├── tests/                  # 223개 테스트 / 커버리지 96%
│       ├── data/                   # 런타임 JSON (.gitignore)
│       ├── main.py                 # 진입점 (전체 MVC 배선)
│       ├── PRD.md                  # Mission2 전용 PRD ✅
│       ├── PLAN.md                 # Phase 0~6 TDD 구현 계획 ✅
│       └── REPORT.md               # Phase별 진행 이력 ✅
├── docs/
│   └── PRD.md
├── 0_Ref/                          # 과제 원본 참고 문서
├── README.md
├── CLAUDE.md
├── .gitignore
└── .mcp.json                       # GitHub MCP 서버 설정 (PAT 포함 — git 제외)
```

---

## GitHub 저장소

**GitHub 계정**: `ltw070`

### 메인 Repository (전체 프로젝트)

| 범위 | git root | Repository | URL |
|------|---------|-----------|-----|
| **전체 프로젝트** | `PersonalProject/` (루트) | SampleOrderSystem-limtaewoong-05095432 | https://github.com/ltw070/SampleOrderSystem-limtaewoong-05095432 |

### Mission1 PoC 개별 Repository (제출용)

> 각 PoC 폴더는 자체 `.git`을 유지하며 개별 repo로 제출한다.  
> 루트 repo에서는 PoC 폴더 내부를 직접 트래킹하지 않는다 (개별 repo로 관리).

| 미션 | 폴더 | Repository | URL |
|------|------|-----------|-----|
| Mission 1 | `mission1/01_ConsoleMVC` | ConsoleMVC-limtaewoong-05095432 | https://github.com/ltw070/ConsoleMVC-limtaewoong-05095432 |
| Mission 1 | `mission1/02_DataPersistence` | DataPersistence-limtaewoong-05095432 | https://github.com/ltw070/DataPersistence-limtaewoong-05095432 |
| Mission 1 | `mission1/03_DataMonitor` | DataMonitor-limtaewoong-05095432 | https://github.com/ltw070/DataMonitor-limtaewoong-05095432 |
| Mission 1 | `mission1/04_DummyDataGenerator` | DummyDataGenerator-limtaewoong-05095432 | https://github.com/ltw070/DummyDataGenerator-limtaewoong-05095432 |

### Git 구조 요약

```
PersonalProject/   ← git root → SampleOrderSystem repo (push: 루트에서 git push)
├── mission1/01_ConsoleMVC/         ← 독립 git repo → ConsoleMVC repo
├── mission1/02_DataPersistence/    ← 독립 git repo → DataPersistence repo
├── mission1/03_DataMonitor/        ← 독립 git repo → DataMonitor repo
└── mission1/04_DummyDataGenerator/ ← 독립 git repo → DummyDataGenerator repo
```

---

## 개발 환경

- **OS**: Windows 11
- **Shell**: PowerShell
- **Python 가상환경**: `.venv/` (프로젝트 루트)
- **MCP**: GitHub MCP Server (`C:\reviewer\github-mcp-server_Windows_x86_64\github-mcp-server.exe`)

---

## Agent 목록

Agent 파일 위치: `.claude/agents/`

### Mission1 PoC 전담 Agent (✅ 완료)

| Agent 이름 | 대상 폴더 | 역할 |
|-----------|----------|------|
| `poc1-console-mvc` | `mission1/01_ConsoleMVC` | MVC 패키지 구조 및 역할 분리 |
| `poc2-data-persistence` | `mission1/02_DataPersistence` | CRUD + 영속성 레이어 |
| `poc3-data-monitor` | `mission1/03_DataMonitor` | 콘솔 실시간 데이터 조회 도구 |
| `poc4-dummy-data-generator` | `mission1/04_DummyDataGenerator` | Dummy 데이터 생성 및 DB 삽입 |

### Mission2 전담 Agent (✅ 완료)

| Agent 이름 | 역할 | 실행 시점 |
|-----------|------|---------|
| `m2-doc-verifier` | PRD ↔ PLAN.md ↔ 코드 문서 정합성 검증 (읽기 전용) | Phase 시작 전·후 |
| `m2-ai-action` | TDD 메인 구현 (Red → Green → Refactor) | Phase 구현 시 |
| `m2-test-verify` | pytest 실행·커버리지·실패 진단 (읽기 전용) | Phase 완료 후 (SubAgent4와 병렬) |
| `m2-compliance-verify` | PRD 요구사항·MVC 원칙·컨벤션 준수 검증 (읽기 전용) | Phase 완료 후 (SubAgent3와 병렬) |

### Mission2 Verify Harness 실행 흐름

```
SubAgent1(m2-doc-verifier)       ← Phase 시작 전 문서 정합성 확인
      ↓
SubAgent2(m2-ai-action)          ← TDD 구현 (Red→Green→Refactor) + commit
      ↓
SubAgent3(m2-test-verify)   ‖   SubAgent4(m2-compliance-verify)   ← 병렬 검증
      ↓
Main Agent 종합 판정 → PASS 시 다음 Phase / FAIL 시 재작업 지시
```

### TDD 사이클

```
1. Red     → 실패하는 테스트 먼저 작성 (pytest 실행 → 실패 확인)
2. Green   → 테스트를 통과하는 최소 코드 작성
3. Refactor → 중복 제거·네이밍 정리 (테스트 통과 유지)
```

커밋 prefix: `test:` (Red) → `feat:` (Green) → `refactor:` (Refactor)

---

## 현재 진행 상태

| 미션 | 상태 | 비고 |
|------|------|------|
| Mission1 PoC 4종 | ✅ 완료 | 322/322 테스트, 평균 커버리지 96% |
| Mission2 PRD.md | ✅ 완료 | `mission2/SampleOrderSystem/PRD.md` |
| Mission2 PLAN.md | ✅ 완료 | `mission2/SampleOrderSystem/PLAN.md` (Phase 0~6) |
| Mission2 구현 | ✅ 완료 | **223/223 테스트, 커버리지 96%** |
| Mission2 REPORT.md | ✅ 완료 | `mission2/SampleOrderSystem/REPORT.md` |

---

## 작업 규칙

- `.mcp.json`은 PAT가 포함되므로 **절대 git commit 금지** → 루트 `.gitignore`에 등록됨
- **전체 프로젝트 커밋**: 루트(`PersonalProject/`)에서 `git add → commit → push origin main`
- **PoC 개별 커밋**: 각 PoC 폴더 내에서 `git add → commit → push origin main`
- 커밋 메시지는 한글 허용, `docs:` / `feat:` / `fix:` / `test:` / `refactor:` 등 prefix 사용
- mission1 PoC 폴더는 루트 repo에서 직접 트래킹하지 않음 (중첩 git repo로 독립 관리)
- Main Agent가 Sub Agent 결과를 직접 검토·승인 (사용자에게는 되돌리기 어려운 결정만 질문)
- 주요 진행마다 git commit + Description 상세 기록 (Phase TDD 단계별 분리)
- Mission2 진행 이력은 `mission2/SampleOrderSystem/REPORT.md`에 누적 기록

# CLAUDE.md

## 프로젝트 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| PRD (전체) | `docs/PRD.md` | 반도체 시료 생산주문관리 시스템 제품 요구사항 문서 |
| PRD - PoC1 | `mission1/01_ConsoleMVC/PRD.md` | MVC 스켈레톤 + 전체 공통 도메인 모델 · Interface 정의 |
| PRD - PoC2 | `mission1/02_DataPersistence/PRD.md` | Repository 인터페이스 + JSON 영속성 구현 명세 |
| PRD - PoC3 | `mission1/03_DataMonitor/PRD.md` | 집계(Aggregator) · 포맷터(Formatter) 인터페이스 명세 |
| PRD - PoC4 | `mission1/04_DummyDataGenerator/PRD.md` | Dummy 생성기 · Seeder 인터페이스 명세 |

---

## 프로젝트 개요

**프로젝트명**: 반도체 시료 생산주문관리 시스템 (S-Semi)  
**형태**: 콘솔(CLI) 기반  
**패턴**: MVC (Model / Controller / View)  
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
├── mission1/                       # PoC 개발 (4종)
│   ├── 01_ConsoleMVC/              # MVC 스켈레톤 코드 (개별 repo)
│   ├── 02_DataPersistence/         # 데이터 영속성 처리 (개별 repo)
│   ├── 03_DataMonitor/             # 데이터 모니터링 Tool (개별 repo)
│   ├── 04_DummyDataGenerator/      # Dummy 데이터 생성 Tool (개별 repo)
│   └── REPORT.md                   # PoC 개발 결과 보고서
├── mission2/                       # 메인 프로젝트
│   └── SampleOrderSystem/          # 반도체 시료 생산주문관리 시스템
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
├── mission1/01_ConsoleMVC/   ← 독립 git repo → ConsoleMVC repo
├── mission1/02_DataPersistence/  ← 독립 git repo → DataPersistence repo
├── mission1/03_DataMonitor/      ← 독립 git repo → DataMonitor repo
└── mission1/04_DummyDataGenerator/ ← 독립 git repo → DummyDataGenerator repo
```

---

## 개발 환경

- **OS**: Windows 11
- **Shell**: PowerShell
- **Python 가상환경**: `.venv/` (프로젝트 루트)
- **MCP**: GitHub MCP Server (`C:\reviewer\github-mcp-server_Windows_x86_64\github-mcp-server.exe`)

---

## Mission1 PoC 전담 Agent

각 PoC는 전담 Agent를 통해 TDD 방식(Red → Green → Refactor)으로 개발한다.

| Agent 이름 | 대상 폴더 | 역할 |
|-----------|----------|------|
| `poc1-console-mvc` | `mission1/01_ConsoleMVC` | MVC 패키지 구조 및 역할 분리 |
| `poc2-data-persistence` | `mission1/02_DataPersistence` | CRUD + 영속성 레이어 |
| `poc3-data-monitor` | `mission1/03_DataMonitor` | 콘솔 실시간 데이터 조회 도구 |
| `poc4-dummy-data-generator` | `mission1/04_DummyDataGenerator` | Dummy 데이터 생성 및 DB 삽입 |

Agent 파일 위치: `.claude/agents/`  
호출 방법: Claude Code 대화 중 `@poc1-console-mvc` 형태로 지정하거나 `/agents` 메뉴에서 선택

### TDD 사이클

```
1. Red     → 실패하는 테스트 먼저 작성 (pytest 실행 → 실패 확인)
2. Green   → 테스트를 통과하는 최소 코드 작성
3. Refactor → 중복 제거·네이밍 정리 (테스트 통과 유지)
```

커밋 prefix: `test:` (Red) → `feat:` (Green) → `refactor:` (Refactor)

---

## 작업 규칙

- `.mcp.json`은 PAT가 포함되므로 **절대 git commit 금지** → 루트 `.gitignore`에 등록됨
- **전체 프로젝트 커밋**: 루트(`PersonalProject/`)에서 `git add → commit → push origin main`
- **PoC 개별 커밋**: 각 PoC 폴더 내에서 `git add → commit → push origin main`
- 커밋 메시지는 한글 허용, `docs:` / `feat:` / `fix:` / `test:` / `refactor:` 등 prefix 사용
- mission1 PoC 폴더는 루트 repo에서 직접 트래킹하지 않음 (중첩 git repo로 독립 관리)

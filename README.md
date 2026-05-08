# 반도체 시료 생산주문관리 시스템 (S-Semi)

> **Repository**: `SampleOrderSystem-limtaewoong-05095432` (전체 프로젝트)  
> **개발자**: limtaewoong (ltw070)

---

## 프로젝트 개요

S-Semi 반도체 회사의 시료 생산·주문 관리를 위한 콘솔 기반 시스템입니다.

- **패턴**: MVC (Model / Controller / View)
- **생산 스케줄링**: FIFO 단일 생산 라인
- **주문 상태 흐름**: `RESERVED → PRODUCING → CONFIRMED → RELEASE` (또는 `REJECTED`)

---

## 개발 진행 상태

| 단계 | 상태 | 내용 |
|------|------|------|
| Mission1 PoC 4종 | ✅ 완료 | 322/322 테스트, 평균 96% 커버리지 |
| Mission2 PRD / PLAN | ✅ 완료 | UI 예시·도메인 모델·Phase 0~6 계획 수립 |
| Mission2 구현 | 🚧 진행 예정 | TDD + Verify Harness (SubAgent 1~4) |

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
│   └── SampleOrderSystem/          # 메인 시스템 🚧
│       ├── PRD.md                  # ✅ 완료
│       └── PLAN.md                 # ✅ 완료 (Phase 0~6)
├── docs/
│   └── PRD.md
├── 0_Ref/
└── CLAUDE.md
```

---

## Mission2 개발 방식 (Agentic Engineering)

```
SubAgent1 (m2-doc-verifier)       ← 문서 정합성 검증
      ↓
SubAgent2 (m2-ai-action)          ← TDD 구현 Phase별
      ↓
SubAgent3 (m2-test-verify)   ‖   SubAgent4 (m2-compliance-verify)
      ↓
Main Agent 종합 판정 → PASS / FAIL
```

---

## Mission1 PoC 결과 요약

| PoC | 테스트 | 커버리지 | 개별 Repository |
|-----|--------|---------|----------------|
| ConsoleMVC | 131 / 131 | 96% | [ConsoleMVC-limtaewoong-05095432](https://github.com/ltw070/ConsoleMVC-limtaewoong-05095432) |
| DataPersistence | 107 / 107 | 95% | [DataPersistence-limtaewoong-05095432](https://github.com/ltw070/DataPersistence-limtaewoong-05095432) |
| DataMonitor | 41 / 41 | 93% | [DataMonitor-limtaewoong-05095432](https://github.com/ltw070/DataMonitor-limtaewoong-05095432) |
| DummyDataGenerator | 43 / 43 | 100% | [DummyDataGenerator-limtaewoong-05095432](https://github.com/ltw070/DummyDataGenerator-limtaewoong-05095432) |

> 각 PoC는 제출용 개별 Repository에서도 관리됩니다.
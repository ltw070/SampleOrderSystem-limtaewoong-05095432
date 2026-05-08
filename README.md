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

## 폴더 구조

```
PersonalProject/
├── mission1/                       # PoC 개발 (4종)
│   ├── 01_ConsoleMVC/              # MVC 스켈레톤 코드
│   ├── 02_DataPersistence/         # 데이터 영속성 처리
│   ├── 03_DataMonitor/             # 데이터 모니터링 Tool
│   ├── 04_DummyDataGenerator/      # Dummy 데이터 생성 Tool
│   └── REPORT.md                   # PoC 개발 결과 보고서
├── mission2/
│   └── SampleOrderSystem/          # 반도체 시료 생산주문관리 시스템 (메인)
├── docs/
│   └── PRD.md
├── 0_Ref/                          # 과제 원본 참고 문서
└── CLAUDE.md
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
"""JSON 파일 기반 SampleRepository 구현체"""
from pathlib import Path
from typing import Union, List, Optional

from app.model.sample import Sample
from app.repository.sample_repository import SampleRepository
from .base_json_repo import BaseJsonRepository


class JsonSampleRepository(BaseJsonRepository, SampleRepository):
    """JSON 파일 기반 시료 Repository 구현체

    저장 규칙:
    - 파일이 없으면 [] 로 자동 생성
    - Atomic Write: .tmp 임시 파일 → os.replace() 원자적 교체
    - Sample 직렬화: id, name, avg_production_time, yield_rate, stock
    """

    def __init__(self, file_path: Union[str, Path]) -> None:
        BaseJsonRepository.__init__(self, file_path)

    # ------------------------------------------------------------------
    # 직렬화 / 역직렬화 헬퍼
    # ------------------------------------------------------------------

    def _to_dict(self, sample: Sample) -> dict:
        """Sample을 JSON 직렬화 가능한 dict로 변환한다."""
        return {
            "id": sample.id,
            "name": sample.name,
            "avg_production_time": sample.avg_production_time,
            "yield_rate": sample.yield_rate,
            "stock": sample.stock,
        }

    def _from_dict(self, data: dict) -> Sample:
        """dict에서 Sample 인스턴스를 복원한다."""
        return Sample(
            id=data["id"],
            name=data["name"],
            avg_production_time=float(data["avg_production_time"]),
            yield_rate=float(data["yield_rate"]),
            stock=int(data["stock"]),
        )

    def _get_id(self, record: dict) -> str:
        """레코드에서 Sample ID를 추출한다."""
        return record["id"]

    # ------------------------------------------------------------------
    # BaseRepository CRUD 구현
    # ------------------------------------------------------------------

    def save(self, entity: Sample) -> Sample:
        """시료를 JSON 파일에 저장한다."""
        records = self._load()
        records.append(self._to_dict(entity))
        self._write_atomic(records)
        return entity

    def find_by_id(self, id: str) -> Optional[Sample]:
        """ID로 시료를 조회한다."""
        for record in self._load():
            if record["id"] == id:
                return self._from_dict(record)
        return None

    def find_all(self) -> List[Sample]:
        """모든 시료를 조회한다."""
        return [self._from_dict(r) for r in self._load()]

    def delete(self, id: str) -> bool:
        """ID로 시료를 삭제한다."""
        records = self._load()
        new_records = [r for r in records if r["id"] != id]
        if len(new_records) == len(records):
            return False
        self._write_atomic(new_records)
        return True

    # ------------------------------------------------------------------
    # SampleRepository 특화 메서드 구현
    # ------------------------------------------------------------------

    def find_by_name(self, keyword: str) -> List[Sample]:
        """키워드로 시료를 검색한다 (부분 일치)."""
        return [
            self._from_dict(r)
            for r in self._load()
            if keyword in r["name"]
        ]

    def update_stock(self, sample_id: str, new_stock: int) -> Sample:
        """시료의 재고를 절대값으로 업데이트한다.

        Args:
            sample_id: 재고를 변경할 시료의 ID
            new_stock: 새로운 재고 수량

        Returns:
            업데이트된 시료

        Raises:
            ValueError: 시료가 존재하지 않는 경우
        """
        records = self._load()
        for i, record in enumerate(records):
            if record["id"] == sample_id:
                record["stock"] = new_stock
                records[i] = record
                self._write_atomic(records)
                return self._from_dict(record)
        raise ValueError(f"Sample not found: {sample_id}")

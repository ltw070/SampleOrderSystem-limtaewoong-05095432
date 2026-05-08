"""SampleController: 시료 등록·조회·검색 비즈니스 로직"""
from typing import List, Optional

from app.model.sample import Sample
from app.repository.sample_repository import SampleRepository
from .base_controller import BaseController


class SampleController(BaseController):
    """시료 관련 비즈니스 로직을 담당하는 Controller.

    SampleRepository 인터페이스에만 의존한다 (구현체 교체 가능).
    의존성은 생성자에서 모두 수령한다.
    """

    def __init__(self, sample_repo: SampleRepository) -> None:
        self._repo = sample_repo

    def run(self) -> None:
        """View 연동은 Phase 4에서 구현한다."""
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_sample(
        self,
        id: str,
        name: str,
        avg_production_time: float,
        yield_rate: float,
        stock: int = 0,
    ) -> Sample:
        """새 Sample을 등록한다.

        Args:
            id: 시료 ID (S-NNN 형식, validator에서 검사)
            name: 시료명
            avg_production_time: 평균 생산 시간 (분/ea, 양수)
            yield_rate: 수율 (0 < yield_rate <= 1)
            stock: 초기 재고 (기본값 0)

        Returns:
            등록된 Sample 인스턴스

        Raises:
            ValueError: id 형식 오류, yield_rate 범위 오류, 중복 id
        """
        # 중복 확인 (id 형식 검사는 Sample.__post_init__에서 수행)
        existing = self._repo.find_by_id(id)
        if existing is not None:
            raise ValueError(f"Sample with id {id!r} already exists")

        # Sample 생성 (형식 유효성 검사는 __post_init__에서 발생)
        sample = Sample(
            id=id,
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
            stock=stock,
        )
        self._repo.save(sample)
        return sample

    def list_samples(self) -> List[Sample]:
        """모든 시료 목록을 반환한다."""
        return self._repo.find_all()

    def search_samples(self, keyword: str) -> List[Sample]:
        """키워드로 시료를 검색한다 (부분 일치).

        Args:
            keyword: 검색 키워드

        Returns:
            키워드가 포함된 시료 목록
        """
        return self._repo.find_by_name(keyword)

    def get_sample(self, sample_id: str) -> Optional[Sample]:
        """ID로 시료를 조회한다.

        Args:
            sample_id: 조회할 시료 ID

        Returns:
            시료 인스턴스 또는 None
        """
        return self._repo.find_by_id(sample_id)

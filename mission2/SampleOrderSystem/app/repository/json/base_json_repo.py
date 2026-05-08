"""JSON 파일 기반 Repository 공통 기반 클래스"""
import json
import os
from abc import abstractmethod
from pathlib import Path
from typing import Union, List, TypeVar, Generic, Optional

T = TypeVar("T")


class BaseJsonRepository(Generic[T]):
    """JSON 파일 기반 Repository의 공통 기능을 제공하는 기반 클래스

    서브클래스가 사용하는 공통 메서드:
    - _ensure_file(): 파일 없으면 [] 로 자동 생성
    - _load(): JSON 파일을 dict 리스트로 로드
    - _write_atomic(): Atomic Write (임시 파일 -> os.replace)

    서브클래스가 구현해야 하는 추상 메서드:
    - _to_dict(entity): 엔티티를 JSON 직렬화 가능한 dict로 변환
    - _from_dict(data): dict에서 엔티티 인스턴스를 복원
    - _get_id(record): 레코드에서 ID 키를 추출
    """

    def __init__(self, file_path: Union[str, Path]) -> None:
        self._file_path = Path(file_path)
        self._ensure_file()

    # ------------------------------------------------------------------
    # 파일 I/O 공통 헬퍼
    # ------------------------------------------------------------------

    def _ensure_file(self) -> None:
        """파일이 없으면 빈 JSON 배열로 자동 생성한다."""
        if not self._file_path.exists():
            self._write_atomic([])

    def _load(self) -> List[dict]:
        """JSON 파일을 읽어 dict 리스트로 반환한다."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_atomic(self, records: List[dict]) -> None:
        """임시 파일에 쓴 후 os.replace로 원자적으로 교체한다.

        전원 차단 등의 비정상 종료에도 파일 무결성을 보장한다.
        """
        tmp_path = self._file_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._file_path)

    # ------------------------------------------------------------------
    # 직렬화 추상 메서드 (서브클래스 구현 필수)
    # ------------------------------------------------------------------

    @abstractmethod
    def _to_dict(self, entity: T) -> dict:
        """엔티티를 JSON 직렬화 가능한 dict로 변환한다."""
        ...

    @abstractmethod
    def _from_dict(self, data: dict) -> T:
        """dict에서 엔티티 인스턴스를 복원한다."""
        ...

    @abstractmethod
    def _get_id(self, record: dict) -> str:
        """레코드에서 ID 필드 값을 추출한다."""
        ...

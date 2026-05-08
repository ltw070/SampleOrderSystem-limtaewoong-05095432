"""BaseController: 모든 Controller의 추상 기반 클래스"""
from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def run(self) -> None:
        """메인 메뉴 루프 실행 - 각 Controller에서 구현한다."""
        ...

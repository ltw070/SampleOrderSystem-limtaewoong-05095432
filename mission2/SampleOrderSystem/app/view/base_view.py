"""Abstract base view for all display views."""
from abc import ABC, abstractmethod


class BaseView(ABC):
    """모든 View의 추상 기반 클래스.

    설계 원칙:
    - display()는 str을 반환한다 (print() 직접 호출 금지)
    - get_input()은 사용자 입력을 받는다 (테스트에서 mock 가능)
    """

    @abstractmethod
    def display(self) -> str:
        """화면 출력 문자열을 반환한다. print() 사용 금지."""
        ...

    def get_input(self, prompt: str = "") -> str:
        """사용자 입력을 받아 반환한다."""
        return input(prompt)

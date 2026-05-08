"""MainView: 시스템 현황 대시보드 및 메인 메뉴."""
from datetime import datetime
from typing import Optional

from .base_view import BaseView
from .formatters import page_header


class MainView(BaseView):
    """메인 메뉴 화면.

    PRD 5.1 UI 형식대로 시스템 현황과 메뉴를 표시한다.
    """

    MENU_LINES = (
        "  [1] 시료 관리                    [2] 시료 주문",
        "  [3] 주문 승인/거절               [4] 모니터링",
        "  [5] 생산라인 조회                [6] 출고 처리",
        "  [0] 종료",
    )

    def __init__(
        self,
        sample_count: int = 0,
        total_stock: int = 0,
        order_count: int = 0,
        production_count: int = 0,
        current_time: Optional[datetime] = None,
    ) -> None:
        self._sample_count = sample_count
        self._total_stock = total_stock
        self._order_count = order_count
        self._production_count = production_count
        self._current_time = current_time or datetime.now()

    def display(self) -> str:
        """메인 화면 문자열을 반환한다."""
        time_str = self._current_time.strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            page_header("반도체 시료 생산주문관리 시스템", f"시스템 현황   {time_str}"),
            "",
            f"  등록 시료   {self._sample_count}종      총 재고    {self._total_stock:,} ea",
            f"  전체 주문   {self._order_count}건      생산라인   {self._production_count}건 대기",
            "",
        ]
        lines.extend(self.MENU_LINES)
        lines.append("")
        lines.append("  선택 > _")
        return "\n".join(lines)

    def get_input(self, prompt: str = "선택 > ") -> str:
        return input(prompt)

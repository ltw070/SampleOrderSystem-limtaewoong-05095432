"""MonitorView: 모니터링 화면 (주문량 / 재고량)."""
from typing import Dict, List

from app.model.sample import Sample
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data


class OrderStatusView(BaseView):
    """상태별 주문량 확인 화면.

    REJECTED는 표시하지 않는다.
    """

    # 표시 순서 (REJECTED 제외)
    DISPLAY_STATUSES = ("RESERVED", "CONFIRMED", "PRODUCING", "RELEASE")

    def __init__(self, status_counts: Dict[str, int]) -> None:
        self._status_counts = status_counts

    def display(self) -> str:
        """주문량 확인 화면 문자열을 반환한다."""
        lines = [header("상태별 주문 현황")]

        if not self._status_counts:
            lines.append(no_data("주문 데이터가 없습니다."))
            return "\n".join(lines)

        lines.append("")
        for status in self.DISPLAY_STATUSES:
            count = self._status_counts.get(status, 0)
            lines.append(f"  {status:<12}  {count}건")

        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class StockStatusView(BaseView):
    """재고량 확인 화면.

    각 시료의 재고 상태(여유/부족/고갈)를 표시한다.
    """

    def __init__(self, samples: List[Sample], stock_statuses: List[str]) -> None:
        self._samples = samples
        self._stock_statuses = stock_statuses

    def display(self) -> str:
        """재고량 확인 화면 문자열을 반환한다."""
        lines = [header("재고 현황")]

        if not self._samples:
            lines.append(no_data("등록된 시료가 없습니다."))
            return "\n".join(lines)

        lines.append(
            table_row("시료명", "재고", "상태",
                      widths=[24, 10, 8])
        )
        lines.append(separator())

        for sample, status in zip(self._samples, self._stock_statuses):
            lines.append(
                table_row(
                    sample.name,
                    f"{sample.stock} ea",
                    status,
                    widths=[24, 10, 8],
                )
            )

        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

"""ShipmentView: 출고 처리 화면."""
from typing import Dict, List

from app.model.order import Order
from app.model.sample import Sample
from app.model.enums import OrderStatus
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data


class ShipmentListView(BaseView):
    """출고 가능 목록 화면 (CONFIRMED 상태 주문)."""

    def __init__(self, orders: List[Order], samples: Dict[str, Sample]) -> None:
        self._orders = orders
        self._samples = samples

    def display(self) -> str:
        """출고 가능 목록 화면 문자열을 반환한다."""
        confirmed = [o for o in self._orders if o.status == OrderStatus.CONFIRMED]

        lines = [header("출고 처리  (CONFIRMED)")]

        if not confirmed:
            lines.append(no_data("출고 대기 주문이 없습니다."))
            return "\n".join(lines)

        lines.append("")
        lines.append("  출고 가능 주문  (CONFIRMED)")
        lines.append(
            table_row("번호", "주문번호", "고객", "시료", "수량",
                      widths=[4, 22, 16, 20, 8])
        )
        lines.append(separator())
        for i, o in enumerate(confirmed, 1):
            sample = self._samples.get(o.sample_id)
            sample_name = sample.name if sample else o.sample_id
            lines.append(
                table_row(
                    f"[{i}]",
                    o.order_no,
                    o.customer_name,
                    sample_name,
                    f"{o.quantity} ea",
                    widths=[4, 22, 16, 20, 8],
                )
            )
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class ShipmentResultView(BaseView):
    """출고 처리 완료 화면."""

    def __init__(self, order: Order, sample: Sample) -> None:
        self._order = order
        self._sample = sample

    def display(self) -> str:
        """출고 처리 완료 화면 문자열을 반환한다."""
        lines = [
            header("출고 처리 완료"),
            "",
            f"  주문번호    {self._order.order_no}",
            f"  고객명      {self._order.customer_name}",
            f"  시료        {self._sample.name}  ({self._sample.id})",
            f"  출고수량    {self._order.quantity} ea",
            f"  상태        CONFIRMED → RELEASE",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

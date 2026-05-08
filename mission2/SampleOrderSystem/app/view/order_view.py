"""OrderView: 주문 관련 화면."""
from typing import Dict, List, Optional

from app.model.order import Order
from app.model.sample import Sample
from app.model.production import ProductionItem
from app.model.enums import OrderStatus
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data


class OrderPlaceView(BaseView):
    """주문 입력 화면."""

    def __init__(self, sample: Sample) -> None:
        self._sample = sample

    def display(self) -> str:
        """주문 입력 화면 문자열을 반환한다."""
        lines = [
            header("시료 주문"),
            "",
            f"  시료    {self._sample.name}  ({self._sample.id})",
            f"  현재 재고: {self._sample.stock} ea",
            "",
            "  고객명      >",
            "  주문 수량   > (ea)",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class OrderConfirmView(BaseView):
    """주문 확인 화면 (예약 접수 완료)."""

    def __init__(self, order: Order, sample: Sample) -> None:
        self._order = order
        self._sample = sample

    def display(self) -> str:
        """예약 접수 완료 화면 문자열을 반환한다."""
        lines = [
            header("예약 접수 완료"),
            "",
            "  입력 내용 확인",
            f"  시료        {self._sample.name}  ({self._sample.id})",
            f"  고객        {self._order.customer_name}",
            f"  수량        {self._order.quantity} ea",
            "",
            separator(),
            "",
            "  주문번호    " + self._order.order_no,
            "  현재 상태   " + self._order.status.value,
            "",
            "  ※ 재고 확인은 [3] 승인 메뉴에서 직접 진행하세요.",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class ReservedListView(BaseView):
    """RESERVED 주문 목록 화면."""

    def __init__(self, orders: List[Order], samples: Dict[str, Sample]) -> None:
        self._orders = orders
        self._samples = samples

    def display(self) -> str:
        """RESERVED 주문 목록 화면 문자열을 반환한다."""
        reserved = [o for o in self._orders if o.status == OrderStatus.RESERVED]

        lines = [header(f"승인 대기 중인 예약 목록  (RESERVED)")]

        if not reserved:
            lines.append(no_data("승인 대기 주문이 없습니다."))
            return "\n".join(lines)

        lines.append(
            table_row("번호", "주문번호", "고객", "시료", "수량", "상태",
                      widths=[4, 22, 16, 20, 8, 10])
        )
        lines.append(separator())
        for i, o in enumerate(reserved, 1):
            sample_name = self._samples.get(o.sample_id)
            sample_display = sample_name.name if sample_name else o.sample_id
            lines.append(
                table_row(
                    f"[{i}]",
                    o.order_no,
                    o.customer_name,
                    sample_display,
                    f"{o.quantity} ea",
                    o.status.value,
                    widths=[4, 22, 16, 20, 8, 10],
                )
            )
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class ApproveResultView(BaseView):
    """승인 결과 화면 (재고 충분: CONFIRMED / 재고 부족: PRODUCING)."""

    def __init__(self, order: Order, production_item: Optional[ProductionItem]) -> None:
        self._order = order
        self._production_item = production_item

    def display(self) -> str:
        """승인 결과 화면 문자열을 반환한다."""
        lines = [header("승인 완료")]

        if self._order.status == OrderStatus.CONFIRMED:
            lines += [
                "",
                f"  상태 변경    RESERVED → CONFIRMED",
                f"  주문번호     {self._order.order_no}",
                "",
                "  재고 충분. 즉시 출고 대기 상태로 전환되었습니다.",
            ]
        elif self._order.status == OrderStatus.PRODUCING and self._production_item:
            pi = self._production_item
            lines += [
                "",
                f"  상태 변경    RESERVED → PRODUCING",
                f"  주문번호     {self._order.order_no}",
                "",
                f"  부족분      {pi.shortage} ea",
                f"  실 생산량   {pi.actual_qty} ea",
                f"  총 생산시간 {pi.total_time:.1f} min",
                "",
                "  생산 라인에 등록되었습니다.",
            ]
        else:
            lines += [
                "",
                f"  주문번호  {self._order.order_no}",
                f"  현재 상태 {self._order.status.value}",
            ]

        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class RejectResultView(BaseView):
    """거절 결과 화면."""

    def __init__(self, order: Order) -> None:
        self._order = order

    def display(self) -> str:
        """거절 결과 화면 문자열을 반환한다."""
        lines = [
            header("주문 거절 완료"),
            "",
            f"  상태 변경    RESERVED → REJECTED",
            f"  주문번호     {self._order.order_no}",
            f"  고객명       {self._order.customer_name}",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

"""ProductionView: 생산라인 현황 화면 (FIFO)."""
from typing import Dict, List, Optional

from app.model.production import ProductionItem
from app.model.sample import Sample
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data, DOUBLE_SEPARATOR


class ProductionView(BaseView):
    """생산라인 전체 현황 화면.

    현재 처리 중인 항목과 FIFO 대기 큐를 표시한다.
    """

    def __init__(
        self,
        current: Optional[ProductionItem],
        queue: List[ProductionItem],
        samples: Dict[str, Sample],
    ) -> None:
        self._current = current
        self._queue = queue
        self._samples = samples

    def display(self) -> str:
        """생산라인 현황 화면 문자열을 반환한다."""
        lines = [header("생산라인 조회   FIFO 방식")]
        lines.append("")
        lines.append("  생산라인 1개 (단일 라인)")
        lines.append("")

        # 현재 처리 중인 항목
        lines.append("  현재 처리 중")
        if self._current is None:
            lines.append(no_data("현재 처리 중인 생산 항목이 없습니다."))
        else:
            c = self._current
            sample_name = self._samples.get(c.sample_id)
            name_str = sample_name.name if sample_name else c.sample_id
            lines.append(
                f"    주문번호  {c.order_no}   시료  {name_str}"
            )
            lines.append(
                f"    부족분    {c.shortage} ea  →  실생산량 {c.actual_qty} ea  "
                f"({c.total_time:.1f} min)"
            )

        lines.append("")
        lines.append(separator())

        # 대기 중인 항목 (FIFO 큐)
        lines.append("")
        lines.append("  대기 중인 주문  (FIFO 순)")
        if not self._queue:
            lines.append(no_data("대기 중인 생산 항목이 없습니다."))
        else:
            lines.append(
                table_row("순서", "주문번호", "시료", "부족분", "실생산량", "예상시간",
                          widths=[4, 22, 20, 8, 10, 10])
            )
            lines.append(separator())
            for i, item in enumerate(self._queue, 1):
                sample_name = self._samples.get(item.sample_id)
                name_str = sample_name.name if sample_name else item.sample_id
                lines.append(
                    table_row(
                        i,
                        item.order_no,
                        name_str,
                        f"{item.shortage} ea",
                        f"{item.actual_qty} ea",
                        f"{item.total_time:.1f} min",
                        widths=[4, 22, 20, 8, 10, 10],
                    )
                )

        lines.append("")
        lines.append("  * 실생산량 = ceil(부족분 / (수율 * 0.9)),  FIFO 방식")

        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

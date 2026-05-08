"""콘솔 출력 포맷터 (MonitorFormatter)

모든 메서드는 str을 반환하며, 내부에서 print()를 호출하지 않는다.
호출자(main.py 또는 View)가 반환된 문자열을 print()로 출력한다.

PoC3(03_DataMonitor)에서 이식. Mission2 도메인 모델에 맞게 조정.
"""
from typing import List, Dict

from app.monitor.aggregator import StockLevel

# 컬럼 너비 상수
COL_W_SAMPLE = 22
COL_W_STOCK = 10
COL_W_LEVEL = 8
COL_W_STATUS = 14
COL_W_COUNT = 5


class MonitorFormatter:
    """모니터링 화면 포맷터."""

    def format_order_status(self, status_counts: Dict[str, int]) -> str:
        """상태별 주문 현황 문자열 반환 (REJECTED 제외).

        Args:
            status_counts: 상태 문자열(value)을 키로 하는 건수 딕셔너리.
                           count_by_status() 반환값 사용.

        Returns:
            str: 상태별 주문 현황 포맷된 문자열.
        """
        ordered_statuses = ["RESERVED", "CONFIRMED", "PRODUCING", "RELEASE"]
        lines = [
            "=" * 30,
            "  상태별 주문 현황",
            "=" * 30,
        ]
        for status_key in ordered_statuses:
            count = status_counts.get(status_key, 0)
            lines.append(f"  {status_key:<{COL_W_STATUS}}{count:>{COL_W_COUNT}}건")
        lines.append("=" * 30)
        return "\n".join(lines)

    def format_stock_status(
        self,
        samples: List,
        stock_levels: List[StockLevel],
    ) -> str:
        """재고 현황 포맷 문자열 반환 (여유/부족/고갈).

        Args:
            samples: Sample 목록
            stock_levels: 각 Sample에 대응하는 StockLevel 목록

        Returns:
            str: 재고 현황 포맷된 문자열.
        """
        header_parts = ["  "]
        for col_name, width in [("시료명", COL_W_SAMPLE), ("재고", COL_W_STOCK), ("상태", COL_W_LEVEL)]:
            header_parts.append(f"{col_name:<{width}}")
        header = "".join(header_parts)

        sep = "-" * (COL_W_SAMPLE + COL_W_STOCK + COL_W_LEVEL + 8)
        lines = [header, sep]

        for sample, level in zip(samples, stock_levels):
            stock_str = f"{sample.stock} ea"
            level_str = level.value  # "여유" / "부족" / "고갈"
            lines.append(
                f"  {sample.name:<{COL_W_SAMPLE}}"
                f"{stock_str:>{COL_W_STOCK}}"
                f"   {level_str:<{COL_W_LEVEL}}"
            )

        return "\n".join(lines)

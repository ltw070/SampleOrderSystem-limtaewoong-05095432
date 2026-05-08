"""데이터 집계 로직 (MonitorAggregator)

PoC3(03_DataMonitor)에서 이식. order.order_qty → order.quantity 수정 적용.
"""
from enum import Enum
from typing import List, Dict

from app.model.enums import OrderStatus
from app.model.sample import Sample
from app.model.order import Order
from app.model.production import YIELD_CORRECTION_FACTOR  # 중복 상수 제거, model에서 재사용

# 집계 대상 주문 상태 (REJECTED 제외)
COUNTED_STATUSES = [
    OrderStatus.RESERVED,
    OrderStatus.CONFIRMED,
    OrderStatus.PRODUCING,
    OrderStatus.RELEASE,
]

# 활성 주문 상태 (재고 판단 기준: CONFIRMED + PRODUCING)
ACTIVE_STATUSES = [OrderStatus.CONFIRMED, OrderStatus.PRODUCING]


class StockLevel(Enum):
    SUFFICIENT = "여유"   # stock >= 활성주문(CONFIRMED+PRODUCING) 총 주문량
    SHORTAGE = "부족"     # 0 < stock < 활성주문 총 주문량
    DEPLETED = "고갈"     # stock == 0


class MonitorAggregator:
    """주문 및 재고 데이터 집계 클래스."""

    def count_by_status(self, orders: List[Order]) -> Dict[str, int]:
        """REJECTED 제외 상태별 주문 건수 반환.

        Returns:
            Dict[str, int]: 상태 문자열(value)을 키로 하는 건수 딕셔너리.
            RESERVED / CONFIRMED / PRODUCING / RELEASE 4개 키 항상 포함.
        """
        counts: Dict[str, int] = {
            OrderStatus.RESERVED.value: 0,
            OrderStatus.CONFIRMED.value: 0,
            OrderStatus.PRODUCING.value: 0,
            OrderStatus.RELEASE.value: 0,
        }
        for order in orders:
            if order.status in COUNTED_STATUSES:
                counts[order.status.value] += 1
        return counts

    def stock_level(self, sample: Sample, orders: List[Order]) -> StockLevel:
        """재고 상태 판단 (CONFIRMED+PRODUCING 기준).

        Args:
            sample: 대상 시료
            orders: 전체 주문 목록 (해당 시료 주문만 걸러 사용)

        Returns:
            StockLevel: SUFFICIENT / SHORTAGE / DEPLETED
        """
        active_qty = sum(
            o.quantity  # Mission2 Order 모델: quantity 필드 사용 (PoC3의 order_qty 아님)
            for o in orders
            if o.sample_id == sample.id and o.status in ACTIVE_STATUSES
        )
        if sample.stock == 0:
            return StockLevel.DEPLETED
        elif sample.stock >= active_qty:
            return StockLevel.SUFFICIENT
        else:
            return StockLevel.SHORTAGE

    def production_count(self, orders: List[Order]) -> int:
        """PRODUCING 상태 주문 건수 반환."""
        return sum(1 for o in orders if o.status == OrderStatus.PRODUCING)

"""ProductionController: FIFO 생산 큐 관리 비즈니스 로직"""
from collections import deque
from typing import List, Optional

from app.model.enums import OrderStatus
from app.model.order import Order
from app.model.production import ProductionItem
from app.repository.order_repository import OrderRepository
from app.repository.sample_repository import SampleRepository
from .base_controller import BaseController


class ProductionController(BaseController):
    """생산 라인 FIFO 큐를 관리하는 Controller.

    OrderRepository, SampleRepository 인터페이스에만 의존한다.
    """

    def __init__(
        self,
        order_repo: OrderRepository,
        sample_repo: SampleRepository,
    ) -> None:
        self._order_repo = order_repo
        self._sample_repo = sample_repo
        self._queue: deque[ProductionItem] = deque()  # FIFO 순서 유지

    def run(self) -> None:
        """View 연동은 Phase 4에서 구현한다."""
        pass

    def enqueue(self, item: ProductionItem) -> None:
        """ProductionItem을 FIFO 큐 끝에 추가한다.

        OrderController.approve_order에서 재고 부족 시 호출한다.
        """
        self._queue.append(item)

    def get_current(self) -> Optional[ProductionItem]:
        """현재 생산 중인 항목(큐 헤드)을 반환한다. 큐가 비어 있으면 None."""
        return self._queue[0] if self._queue else None

    def get_queue(self) -> List[ProductionItem]:
        """생산 큐 전체를 FIFO 순서로 반환한다 (복사본)."""
        return list(self._queue)

    def complete_production(self, order_no: str) -> Order:
        """생산을 완료한다 (PRODUCING → CONFIRMED).

        처리 순서:
        1. 큐 헤드가 해당 order_no인지 확인 (FIFO 원칙)
        2. 시료 재고 증가: current_stock + actual_qty
        3. 주문 상태를 CONFIRMED로 변경
        4. 큐에서 제거

        Args:
            order_no: 완료할 생산 주문 번호

        Returns:
            업데이트된 Order (CONFIRMED 상태)

        Raises:
            ValueError: 큐가 비어 있거나 order_no가 헤드가 아닌 경우
        """
        if not self._queue:
            raise ValueError(f"No production order found: {order_no!r}")

        head = self._queue[0]
        if head.order_no != order_no:
            # 큐 내에 존재하는지 확인
            found = any(item.order_no == order_no for item in self._queue)
            if found:
                raise ValueError(
                    f"Order {order_no!r} is not the head of the queue; "
                    "only the current (head) production item can be completed"
                )
            raise ValueError(f"No production order found: {order_no!r}")

        prod_item = self._queue[0]

        # 시료 재고 증가: current_stock + actual_qty
        sample = self._sample_repo.find_by_id(prod_item.sample_id)
        if sample is not None:
            new_stock = sample.stock + prod_item.actual_qty
            self._sample_repo.update_stock(prod_item.sample_id, new_stock)

        # 주문 상태를 CONFIRMED로 변경
        updated_order = self._order_repo.update_status(order_no, OrderStatus.CONFIRMED)

        # 큐에서 제거
        self._queue.popleft()

        return updated_order

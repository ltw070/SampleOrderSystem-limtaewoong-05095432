"""OrderController: 주문 접수·승인·거절·출고 비즈니스 로직"""
from datetime import datetime
from typing import List, Optional, Tuple

from app.model.order import Order
from app.model.enums import OrderStatus
from app.model.production import ProductionItem
from app.repository.order_repository import OrderRepository
from app.repository.sample_repository import SampleRepository
from .base_controller import BaseController


class OrderController(BaseController):
    """주문 관련 비즈니스 로직을 담당하는 Controller.

    OrderRepository, SampleRepository 인터페이스에만 의존한다.
    """

    def __init__(
        self,
        order_repo: OrderRepository,
        sample_repo: SampleRepository,
    ) -> None:
        self._order_repo = order_repo
        self._sample_repo = sample_repo
        self._seq: int = 0  # 주문 번호 시퀀스

    def run(self) -> None:
        """View 연동은 Phase 4에서 구현한다."""
        pass

    def _next_order_no(self) -> str:
        """ORD-YYYYMMDD-XXXX 형식의 다음 주문 번호를 생성한다."""
        self._seq += 1
        date_str = datetime.now().strftime("%Y%m%d")
        return f"ORD-{date_str}-{self._seq:04d}"

    def place_order(
        self,
        sample_id: str,
        customer_name: str,
        quantity: int,
    ) -> Order:
        """새 주문을 RESERVED 상태로 접수한다.

        Args:
            sample_id: 시료 ID
            customer_name: 고객명
            quantity: 주문 수량

        Returns:
            생성된 Order (RESERVED 상태)

        Raises:
            ValueError: 존재하지 않는 sample_id
        """
        sample = self._sample_repo.find_by_id(sample_id)
        if sample is None:
            raise ValueError(f"Unknown sample id: {sample_id!r}")

        order = Order(
            order_no=self._next_order_no(),
            sample_id=sample_id,
            customer_name=customer_name,
            quantity=quantity,
            created_at=datetime.now(),
            status=OrderStatus.RESERVED,
        )
        self._order_repo.save(order)
        return order

    def list_reserved(self) -> List[Order]:
        """RESERVED 상태의 주문 목록을 반환한다."""
        return self._order_repo.find_by_status(OrderStatus.RESERVED)

    def approve_order(
        self, order_no: str
    ) -> Tuple[Order, Optional[ProductionItem]]:
        """주문을 승인한다.

        재고 충분 (stock >= quantity):
            - 재고 차감: update_stock(sample_id, new_stock=stock - quantity)
            - 상태 변경: CONFIRMED
            - 반환: (Order(CONFIRMED), None)

        재고 부족 (stock < quantity):
            - 재고를 0으로: update_stock(sample_id, 0)
            - 상태 변경: PRODUCING
            - ProductionItem 생성: shortage = quantity - stock
            - 반환: (Order(PRODUCING), ProductionItem)

        Args:
            order_no: 승인할 주문 번호

        Returns:
            (Order, Optional[ProductionItem]) 튜플

        Raises:
            ValueError: 주문 또는 시료가 존재하지 않는 경우
        """
        order = self._order_repo.find_by_id(order_no)
        if order is None:
            raise ValueError(f"Order not found: {order_no!r}")

        sample = self._sample_repo.find_by_id(order.sample_id)
        if sample is None:
            raise ValueError(f"Sample not found: {order.sample_id!r}")

        stock = sample.stock
        quantity = order.quantity

        if stock >= quantity:
            # 재고 충분: 차감 후 CONFIRMED
            new_stock = stock - quantity
            self._sample_repo.update_stock(order.sample_id, new_stock)
            updated_order = self._order_repo.update_status(order_no, OrderStatus.CONFIRMED)
            return (updated_order, None)
        else:
            # 재고 부족: 재고 0으로, PRODUCING, ProductionItem 생성
            shortage = quantity - stock
            self._sample_repo.update_stock(order.sample_id, 0)
            updated_order = self._order_repo.update_status(order_no, OrderStatus.PRODUCING)
            prod_item = ProductionItem(
                order_no=order_no,
                sample_id=order.sample_id,
                shortage=shortage,
                yield_rate=sample.yield_rate,
                avg_production_time=sample.avg_production_time,
            )
            return (updated_order, prod_item)

    def reject_order(self, order_no: str) -> Order:
        """주문을 거절한다 (RESERVED → REJECTED).

        Args:
            order_no: 거절할 주문 번호

        Returns:
            업데이트된 Order (REJECTED 상태)

        Raises:
            ValueError: 주문이 존재하지 않는 경우
        """
        order = self._order_repo.find_by_id(order_no)
        if order is None:
            raise ValueError(f"Order not found: {order_no!r}")

        return self._order_repo.update_status(order_no, OrderStatus.REJECTED)

    def ship_order(self, order_no: str) -> Order:
        """주문을 출고 처리한다 (CONFIRMED → RELEASE).

        Args:
            order_no: 출고할 주문 번호

        Returns:
            업데이트된 Order (RELEASE 상태)

        Raises:
            ValueError: 주문이 CONFIRMED 상태가 아닌 경우
        """
        order = self._order_repo.find_by_id(order_no)
        if order is None:
            raise ValueError(f"Order not found: {order_no!r}")

        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(
                f"Order {order_no!r} must be in CONFIRMED status to ship, "
                f"but is {order.status.value!r}"
            )

        return self._order_repo.update_status(order_no, OrderStatus.RELEASE)

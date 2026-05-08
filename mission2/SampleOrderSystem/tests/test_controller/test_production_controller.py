"""Phase3 Red: ProductionController 테스트 - FIFO 큐, complete_production 흐름"""
import pytest
from unittest.mock import MagicMock, call

from app.model.production import ProductionItem
from app.model.enums import OrderStatus
from app.model.order import Order


def make_production_item(order_no: str, sample_id: str = "S-001") -> ProductionItem:
    """테스트용 ProductionItem 생성 헬퍼"""
    return ProductionItem(
        order_no=order_no,
        sample_id=sample_id,
        shortage=10,
        yield_rate=0.9,
        avg_production_time=5.0,
    )


class TestGetQueue:
    def test_get_queue_empty_initially(self, mock_order_repo, mock_sample_repo):
        """초기 큐는 비어 있어야 한다."""
        from app.controller.production_controller import ProductionController

        mock_order_repo.find_by_status.return_value = []

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        queue = ctrl.get_queue()

        assert queue == []

    def test_get_queue_returns_fifo_order(self, mock_order_repo, mock_sample_repo):
        """get_queue는 FIFO 순서로 반환한다."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)

        item1 = make_production_item("ORD-20260508-0001")
        item2 = make_production_item("ORD-20260508-0002")
        item3 = make_production_item("ORD-20260508-0003")
        ctrl._queue.append(item1)
        ctrl._queue.append(item2)
        ctrl._queue.append(item3)

        queue = ctrl.get_queue()
        order_nos = [item.order_no for item in queue]

        assert order_nos == [
            "ORD-20260508-0001",
            "ORD-20260508-0002",
            "ORD-20260508-0003",
        ]

    def test_get_queue_returns_copy(self, mock_order_repo, mock_sample_repo):
        """get_queue는 복사본을 반환해야 한다 (내부 큐에 영향 없음)."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        ctrl._queue.append(make_production_item("ORD-20260508-0001"))

        queue = ctrl.get_queue()
        queue.clear()

        assert len(ctrl.get_queue()) == 1

    def test_get_current_empty_returns_none(self, mock_order_repo, mock_sample_repo):
        """큐가 비어 있으면 get_current는 None을 반환한다."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        assert ctrl.get_current() is None

    def test_get_current_returns_first_item(self, mock_order_repo, mock_sample_repo):
        """큐가 있을 때 get_current는 첫 번째 항목을 반환한다."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        item1 = make_production_item("ORD-20260508-0001")
        item2 = make_production_item("ORD-20260508-0002")
        ctrl._queue.append(item1)
        ctrl._queue.append(item2)

        current = ctrl.get_current()
        assert current is not None
        assert current.order_no == "ORD-20260508-0001"


class TestCompleteProduction:
    def test_complete_production(self, mock_order_repo, mock_sample_repo, sample_with_stock):
        """complete_production: PRODUCING → CONFIRMED 전환 + 재고 증가."""
        from app.controller.production_controller import ProductionController
        from datetime import datetime

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        item = make_production_item("ORD-20260508-0001")
        ctrl._queue.append(item)

        # actual_qty = ceil(10 / (0.9 * 0.9)) = ceil(10 / 0.81) = ceil(12.345...) = 13
        producing_order = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=10,
            created_at=datetime(2026, 5, 8, 9, 0, 0),
            status=OrderStatus.PRODUCING,
        )

        mock_sample_repo.find_by_id.return_value = sample_with_stock  # stock=100

        confirmed_order = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=10,
            created_at=datetime(2026, 5, 8, 9, 0, 0),
            status=OrderStatus.CONFIRMED,
        )
        mock_order_repo.update_status.return_value = confirmed_order

        result = ctrl.complete_production("ORD-20260508-0001")

        # 재고 증가: new_stock = current_stock(100) + actual_qty(13) = 113
        mock_sample_repo.update_stock.assert_called_once_with("S-001", 100 + item.actual_qty)
        # 상태 변경: CONFIRMED
        mock_order_repo.update_status.assert_called_once_with(
            "ORD-20260508-0001", OrderStatus.CONFIRMED
        )
        # 큐에서 제거
        assert len(ctrl.get_queue()) == 0
        assert result.status == OrderStatus.CONFIRMED

    def test_complete_production_fifo_advances(self, mock_order_repo, mock_sample_repo, sample_with_stock):
        """complete_production 후 다음 항목이 큐 앞으로 온다."""
        from app.controller.production_controller import ProductionController
        from datetime import datetime

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        item1 = make_production_item("ORD-20260508-0001")
        item2 = make_production_item("ORD-20260508-0002")
        ctrl._queue.append(item1)
        ctrl._queue.append(item2)

        mock_sample_repo.find_by_id.return_value = sample_with_stock

        confirmed_order = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=10,
            created_at=datetime(2026, 5, 8, 9, 0, 0),
            status=OrderStatus.CONFIRMED,
        )
        mock_order_repo.update_status.return_value = confirmed_order

        ctrl.complete_production("ORD-20260508-0001")

        current = ctrl.get_current()
        assert current is not None
        assert current.order_no == "ORD-20260508-0002"

    def test_complete_production_not_found_raises(self, mock_order_repo, mock_sample_repo):
        """큐에 없는 order_no로 complete_production 시 ValueError가 발생한다."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)

        with pytest.raises(ValueError):
            ctrl.complete_production("ORD-20260508-9999")

    def test_complete_production_non_head_raises(self, mock_order_repo, mock_sample_repo):
        """FIFO: 헤드가 아닌 항목을 완료 시 ValueError가 발생한다."""
        from app.controller.production_controller import ProductionController

        ctrl = ProductionController(mock_order_repo, mock_sample_repo)
        ctrl._queue.append(make_production_item("ORD-20260508-0001"))
        ctrl._queue.append(make_production_item("ORD-20260508-0002"))

        with pytest.raises(ValueError, match="head"):
            ctrl.complete_production("ORD-20260508-0002")

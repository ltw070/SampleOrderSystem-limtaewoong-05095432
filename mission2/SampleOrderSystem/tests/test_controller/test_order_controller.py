"""Phase3 Red: OrderController 테스트 - place/approve/reject/ship 흐름"""
import re
import pytest
from datetime import datetime
from unittest.mock import MagicMock, call

from app.model.order import Order
from app.model.enums import OrderStatus
from app.model.production import ProductionItem


class TestPlaceOrder:
    def test_place_order(self, mock_order_repo, mock_sample_repo, sample_with_stock):
        """Sample이 존재하면 RESERVED 상태의 Order를 생성하고 repo.save를 호출한다."""
        from app.controller.order_controller import OrderController

        mock_sample_repo.find_by_id.return_value = sample_with_stock

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        ctrl._date_str = "20260508"  # 날짜 고정 (테스트 안정성)

        order = ctrl.place_order("S-001", "삼성전자", 10)

        mock_order_repo.save.assert_called_once()
        assert isinstance(order, Order)
        assert order.status == OrderStatus.RESERVED
        assert order.sample_id == "S-001"
        assert order.customer_name == "삼성전자"
        assert order.quantity == 10
        assert re.fullmatch(r"ORD-\d{8}-\d{4}", order.order_no)

    def test_place_order_invalid_sample(self, mock_order_repo, mock_sample_repo):
        """존재하지 않는 sample_id로 주문 시 ValueError가 발생해야 한다."""
        from app.controller.order_controller import OrderController

        mock_sample_repo.find_by_id.return_value = None

        ctrl = OrderController(mock_order_repo, mock_sample_repo)

        with pytest.raises(ValueError, match="sample"):
            ctrl.place_order("S-999", "삼성전자", 10)


class TestApproveOrderStockSufficient:
    def test_approve_order_stock_sufficient(
        self, mock_order_repo, mock_sample_repo, sample_with_stock, reserved_order
    ):
        """재고(stock) >= 주문량(quantity)이면 CONFIRMED로 전환한다."""
        from app.controller.order_controller import OrderController

        # stock=100, quantity=10 → 충분
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample_with_stock

        updated_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            created_at=reserved_order.created_at,
            status=OrderStatus.CONFIRMED,
        )
        mock_order_repo.update_status.return_value = updated_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result_order, result_prod = ctrl.approve_order(reserved_order.order_no)

        # update_stock 호출 확인 (new_stock = 100 - 10 = 90)
        mock_sample_repo.update_stock.assert_called_once_with("S-001", 90)
        # update_status 호출 확인
        mock_order_repo.update_status.assert_called_once_with(
            reserved_order.order_no, OrderStatus.CONFIRMED
        )
        assert result_order.status == OrderStatus.CONFIRMED
        assert result_prod is None

    def test_approve_order_stock_exact(
        self, mock_order_repo, mock_sample_repo, reserved_order
    ):
        """재고(stock) == 주문량(quantity)이면 CONFIRMED로 전환한다 (경계값)."""
        from app.controller.order_controller import OrderController

        # stock=10, quantity=10 → 정확히 같음 → 충분
        sample_exact = __import__("app.model.sample", fromlist=["Sample"]).Sample(
            id="S-001",
            name="테스트",
            avg_production_time=5.0,
            yield_rate=0.9,
            stock=10,
        )
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample_exact

        updated_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            created_at=reserved_order.created_at,
            status=OrderStatus.CONFIRMED,
        )
        mock_order_repo.update_status.return_value = updated_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result_order, result_prod = ctrl.approve_order(reserved_order.order_no)

        # new_stock = 10 - 10 = 0
        mock_sample_repo.update_stock.assert_called_once_with("S-001", 0)
        mock_order_repo.update_status.assert_called_once_with(
            reserved_order.order_no, OrderStatus.CONFIRMED
        )
        assert result_prod is None


class TestApproveOrderStockInsufficient:
    def test_approve_order_stock_insufficient(
        self, mock_order_repo, mock_sample_repo, sample_no_stock, reserved_order
    ):
        """재고(stock) < 주문량(quantity)이면 PRODUCING으로 전환하고 ProductionItem을 반환한다."""
        from app.controller.order_controller import OrderController

        # stock=0, quantity=10 → 부족
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample_no_stock

        updated_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            created_at=reserved_order.created_at,
            status=OrderStatus.PRODUCING,
        )
        mock_order_repo.update_status.return_value = updated_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result_order, result_prod = ctrl.approve_order(reserved_order.order_no)

        # stock을 0으로 설정
        mock_sample_repo.update_stock.assert_called_once_with("S-001", 0)
        # 상태를 PRODUCING으로 변경
        mock_order_repo.update_status.assert_called_once_with(
            reserved_order.order_no, OrderStatus.PRODUCING
        )
        assert result_order.status == OrderStatus.PRODUCING
        assert result_prod is not None
        assert isinstance(result_prod, ProductionItem)
        assert result_prod.order_no == reserved_order.order_no
        assert result_prod.shortage == 10  # quantity(10) - stock(0)

    def test_approve_order_partial_stock(
        self, mock_order_repo, mock_sample_repo, sample_partial_stock, reserved_order
    ):
        """재고가 부분적으로 있어도 부족하면 shortage=quantity-stock으로 ProductionItem 생성."""
        from app.controller.order_controller import OrderController

        # stock=5, quantity=10 → shortage=5
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample_partial_stock

        updated_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            created_at=reserved_order.created_at,
            status=OrderStatus.PRODUCING,
        )
        mock_order_repo.update_status.return_value = updated_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result_order, result_prod = ctrl.approve_order(reserved_order.order_no)

        # stock을 0으로 설정
        mock_sample_repo.update_stock.assert_called_once_with("S-001", 0)
        assert result_prod is not None
        assert result_prod.shortage == 5  # quantity(10) - stock(5)


class TestRejectOrder:
    def test_reject_order(
        self, mock_order_repo, mock_sample_repo, reserved_order
    ):
        """RESERVED 주문을 REJECTED로 전환한다."""
        from app.controller.order_controller import OrderController

        mock_order_repo.find_by_id.return_value = reserved_order

        rejected_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            created_at=reserved_order.created_at,
            status=OrderStatus.REJECTED,
        )
        mock_order_repo.update_status.return_value = rejected_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result = ctrl.reject_order(reserved_order.order_no)

        mock_order_repo.update_status.assert_called_once_with(
            reserved_order.order_no, OrderStatus.REJECTED
        )
        assert result.status == OrderStatus.REJECTED

    def test_reject_order_not_found(self, mock_order_repo, mock_sample_repo):
        """존재하지 않는 주문 거절 시 ValueError가 발생한다."""
        from app.controller.order_controller import OrderController

        mock_order_repo.find_by_id.return_value = None

        ctrl = OrderController(mock_order_repo, mock_sample_repo)

        with pytest.raises(ValueError):
            ctrl.reject_order("ORD-20260508-9999")


class TestShipOrder:
    def test_ship_order(
        self, mock_order_repo, mock_sample_repo, confirmed_order, sample_with_stock
    ):
        """CONFIRMED 주문을 RELEASE로 전환한다."""
        from app.controller.order_controller import OrderController

        mock_order_repo.find_by_id.return_value = confirmed_order
        mock_sample_repo.find_by_id.return_value = sample_with_stock

        released_order = Order(
            order_no=confirmed_order.order_no,
            sample_id=confirmed_order.sample_id,
            customer_name=confirmed_order.customer_name,
            quantity=confirmed_order.quantity,
            created_at=confirmed_order.created_at,
            status=OrderStatus.RELEASE,
        )
        mock_order_repo.update_status.return_value = released_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result = ctrl.ship_order(confirmed_order.order_no)

        mock_order_repo.update_status.assert_called_once_with(
            confirmed_order.order_no, OrderStatus.RELEASE
        )
        assert result.status == OrderStatus.RELEASE

    def test_ship_order_not_confirmed_raises(
        self, mock_order_repo, mock_sample_repo, reserved_order
    ):
        """CONFIRMED 상태가 아닌 주문 출고 시 ValueError가 발생한다."""
        from app.controller.order_controller import OrderController

        mock_order_repo.find_by_id.return_value = reserved_order

        ctrl = OrderController(mock_order_repo, mock_sample_repo)

        with pytest.raises(ValueError, match="CONFIRMED"):
            ctrl.ship_order(reserved_order.order_no)


class TestListReserved:
    def test_list_reserved(
        self, mock_order_repo, mock_sample_repo, reserved_order
    ):
        """find_by_status(RESERVED) 결과를 반환한다."""
        from app.controller.order_controller import OrderController

        mock_order_repo.find_by_status.return_value = [reserved_order]

        ctrl = OrderController(mock_order_repo, mock_sample_repo)
        result = ctrl.list_reserved()

        mock_order_repo.find_by_status.assert_called_once_with(OrderStatus.RESERVED)
        assert len(result) == 1
        assert result[0].status == OrderStatus.RESERVED

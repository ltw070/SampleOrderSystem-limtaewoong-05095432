"""Phase 4 Red: ShipmentView 테스트."""
import pytest
from datetime import datetime
from app.model.order import Order
from app.model.sample import Sample
from app.model.enums import OrderStatus


@pytest.fixture
def confirmed_order():
    return Order(
        order_no="ORD-20260416-0042",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=150,
        status=OrderStatus.CONFIRMED,
        created_at=datetime(2026, 4, 16, 8, 0, 0),
    )


@pytest.fixture
def released_order():
    return Order(
        order_no="ORD-20260416-0042",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=150,
        status=OrderStatus.RELEASE,
        created_at=datetime(2026, 4, 16, 8, 0, 0),
    )


@pytest.fixture
def sample():
    return Sample(id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5, yield_rate=0.92, stock=480)


class TestShipmentListView:
    """출고 가능 목록 화면 테스트."""

    def test_display_returns_str(self, confirmed_order, sample):
        """display()는 str을 반환한다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[confirmed_order], samples={"S-001": sample})
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_confirmed_keyword(self, confirmed_order, sample):
        """CONFIRMED 키워드가 포함된다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[confirmed_order], samples={"S-001": sample})
        result = view.display()
        assert "CONFIRMED" in result

    def test_display_contains_order_no(self, confirmed_order, sample):
        """주문번호가 포함된다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[confirmed_order], samples={"S-001": sample})
        result = view.display()
        assert "ORD-20260416-0042" in result

    def test_display_contains_customer_name(self, confirmed_order, sample):
        """고객명이 포함된다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[confirmed_order], samples={"S-001": sample})
        result = view.display()
        assert "SK하이닉스" in result

    def test_display_empty_list_returns_str(self):
        """빈 목록도 str을 반환한다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[], samples={})
        result = view.display()
        assert isinstance(result, str)

    def test_display_filters_non_confirmed(self, sample):
        """CONFIRMED가 아닌 주문은 목록에 포함되지 않는다."""
        from app.view.shipment_view import ShipmentListView
        reserved_order = Order(
            order_no="ORD-20260416-0099",
            sample_id="S-001",
            customer_name="테스트고객",
            quantity=10,
            status=OrderStatus.RESERVED,
            created_at=datetime(2026, 4, 16, 8, 0, 0),
        )
        view = ShipmentListView(orders=[reserved_order], samples={"S-001": sample})
        result = view.display()
        assert "ORD-20260416-0099" not in result

    def test_display_contains_quantity(self, confirmed_order, sample):
        """수량이 포함된다."""
        from app.view.shipment_view import ShipmentListView
        view = ShipmentListView(orders=[confirmed_order], samples={"S-001": sample})
        result = view.display()
        assert "150" in result


class TestShipmentResultView:
    """출고 처리 완료 화면 테스트."""

    def test_display_returns_str(self, released_order, sample):
        """display()는 str을 반환한다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_release_keyword(self, released_order, sample):
        """RELEASE 관련 내용이 포함된다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert "RELEASE" in result or "출고" in result

    def test_display_contains_order_no(self, released_order, sample):
        """주문번호가 포함된다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert "ORD-20260416-0042" in result

    def test_display_contains_customer_name(self, released_order, sample):
        """고객명이 포함된다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert "SK하이닉스" in result

    def test_display_contains_quantity(self, released_order, sample):
        """수량이 포함된다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert "150" in result

    def test_display_contains_complete_message(self, released_order, sample):
        """완료 메시지가 포함된다."""
        from app.view.shipment_view import ShipmentResultView
        view = ShipmentResultView(order=released_order, sample=sample)
        result = view.display()
        assert any(kw in result for kw in ["완료", "처리", "출고"])

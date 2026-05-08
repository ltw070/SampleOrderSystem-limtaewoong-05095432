"""Phase 4 Red: OrderView 테스트."""
import pytest
from datetime import datetime
from app.model.order import Order
from app.model.sample import Sample
from app.model.enums import OrderStatus
from app.model.production import ProductionItem


@pytest.fixture
def sample():
    return Sample(id="S-003", name="SiC 파워기판-6인치", avg_production_time=0.8, yield_rate=0.92, stock=30)


@pytest.fixture
def reserved_order():
    return Order(
        order_no="ORD-20260416-0043",
        sample_id="S-003",
        customer_name="삼성전자 파운드리",
        quantity=200,
        status=OrderStatus.RESERVED,
        created_at=datetime(2026, 4, 16, 9, 0, 0),
    )


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
def production_item():
    return ProductionItem(
        order_no="ORD-20260416-0043",
        sample_id="S-003",
        shortage=170,
        yield_rate=0.92,
        avg_production_time=0.8,
    )


class TestOrderPlaceView:
    """주문 입력 화면 테스트."""

    def test_display_returns_str(self, sample):
        """display()는 str을 반환한다."""
        from app.view.order_view import OrderPlaceView
        view = OrderPlaceView(sample=sample)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_sample_id(self, sample):
        """시료 ID가 포함된다."""
        from app.view.order_view import OrderPlaceView
        view = OrderPlaceView(sample=sample)
        result = view.display()
        assert "S-003" in result

    def test_display_contains_sample_name(self, sample):
        """시료명이 포함된다."""
        from app.view.order_view import OrderPlaceView
        view = OrderPlaceView(sample=sample)
        result = view.display()
        assert "SiC 파워기판-6인치" in result

    def test_display_contains_order_prompt(self, sample):
        """주문 입력 안내 문구가 포함된다."""
        from app.view.order_view import OrderPlaceView
        view = OrderPlaceView(sample=sample)
        result = view.display()
        assert any(kw in result for kw in ["주문", "고객", "수량"])


class TestOrderConfirmView:
    """주문 확인 화면(예약 접수 완료) 테스트."""

    def test_display_returns_str(self, reserved_order, sample):
        """display()는 str을 반환한다."""
        from app.view.order_view import OrderConfirmView
        view = OrderConfirmView(order=reserved_order, sample=sample)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_order_no(self, reserved_order, sample):
        """주문번호가 포함된다."""
        from app.view.order_view import OrderConfirmView
        view = OrderConfirmView(order=reserved_order, sample=sample)
        result = view.display()
        assert "ORD-20260416-0043" in result

    def test_display_contains_reserved_status(self, reserved_order, sample):
        """RESERVED 상태가 포함된다."""
        from app.view.order_view import OrderConfirmView
        view = OrderConfirmView(order=reserved_order, sample=sample)
        result = view.display()
        assert "RESERVED" in result

    def test_display_contains_customer_name(self, reserved_order, sample):
        """고객명이 포함된다."""
        from app.view.order_view import OrderConfirmView
        view = OrderConfirmView(order=reserved_order, sample=sample)
        result = view.display()
        assert "삼성전자 파운드리" in result

    def test_display_contains_confirm_message(self, reserved_order, sample):
        """예약 접수 완료 메시지가 포함된다."""
        from app.view.order_view import OrderConfirmView
        view = OrderConfirmView(order=reserved_order, sample=sample)
        result = view.display()
        assert any(kw in result for kw in ["접수", "완료", "예약"])


class TestReservedListView:
    """RESERVED 주문 목록 화면 테스트."""

    def test_display_returns_str(self, reserved_order, sample):
        """display()는 str을 반환한다."""
        from app.view.order_view import ReservedListView
        view = ReservedListView(orders=[reserved_order], samples={"S-003": sample})
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_order_no(self, reserved_order, sample):
        """주문번호가 포함된다."""
        from app.view.order_view import ReservedListView
        view = ReservedListView(orders=[reserved_order], samples={"S-003": sample})
        result = view.display()
        assert "ORD-20260416-0043" in result

    def test_display_contains_reserved_keyword(self, reserved_order, sample):
        """RESERVED 키워드가 포함된다."""
        from app.view.order_view import ReservedListView
        view = ReservedListView(orders=[reserved_order], samples={"S-003": sample})
        result = view.display()
        assert "RESERVED" in result

    def test_display_empty_list_returns_str(self):
        """빈 목록도 str을 반환한다."""
        from app.view.order_view import ReservedListView
        view = ReservedListView(orders=[], samples={})
        result = view.display()
        assert isinstance(result, str)


class TestApproveResultView:
    """승인 결과 화면 테스트."""

    def test_display_confirmed_returns_str(self, confirmed_order):
        """재고 충분(CONFIRMED) 승인 결과가 str을 반환한다."""
        from app.view.order_view import ApproveResultView
        view = ApproveResultView(order=confirmed_order, production_item=None)
        result = view.display()
        assert isinstance(result, str)

    def test_display_confirmed_contains_status(self, confirmed_order):
        """CONFIRMED 상태가 포함된다."""
        from app.view.order_view import ApproveResultView
        view = ApproveResultView(order=confirmed_order, production_item=None)
        result = view.display()
        assert "CONFIRMED" in result

    def test_display_producing_returns_str(self, reserved_order, production_item):
        """재고 부족(PRODUCING) 승인 결과가 str을 반환한다."""
        from app.view.order_view import ApproveResultView
        producing_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            status=OrderStatus.PRODUCING,
            created_at=reserved_order.created_at,
        )
        view = ApproveResultView(order=producing_order, production_item=production_item)
        result = view.display()
        assert isinstance(result, str)

    def test_display_producing_contains_producing_status(self, reserved_order, production_item):
        """PRODUCING 상태가 포함된다."""
        from app.view.order_view import ApproveResultView
        producing_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            status=OrderStatus.PRODUCING,
            created_at=reserved_order.created_at,
        )
        view = ApproveResultView(order=producing_order, production_item=production_item)
        result = view.display()
        assert "PRODUCING" in result


class TestRejectResultView:
    """거절 결과 화면 테스트."""

    def test_display_returns_str(self, reserved_order):
        """display()는 str을 반환한다."""
        from app.view.order_view import RejectResultView
        rejected_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            status=OrderStatus.REJECTED,
            created_at=reserved_order.created_at,
        )
        view = RejectResultView(order=rejected_order)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_rejected_status(self, reserved_order):
        """REJECTED 상태가 포함된다."""
        from app.view.order_view import RejectResultView
        rejected_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            status=OrderStatus.REJECTED,
            created_at=reserved_order.created_at,
        )
        view = RejectResultView(order=rejected_order)
        result = view.display()
        assert "REJECTED" in result

    def test_display_contains_order_no(self, reserved_order):
        """주문번호가 포함된다."""
        from app.view.order_view import RejectResultView
        rejected_order = Order(
            order_no=reserved_order.order_no,
            sample_id=reserved_order.sample_id,
            customer_name=reserved_order.customer_name,
            quantity=reserved_order.quantity,
            status=OrderStatus.REJECTED,
            created_at=reserved_order.created_at,
        )
        view = RejectResultView(order=rejected_order)
        result = view.display()
        assert "ORD-20260416-0043" in result

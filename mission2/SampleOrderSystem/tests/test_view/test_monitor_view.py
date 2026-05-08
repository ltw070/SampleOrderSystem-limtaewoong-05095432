"""Phase 4 Red: MonitorView 테스트."""
import pytest
from app.model.sample import Sample


@pytest.fixture
def status_counts():
    return {
        "RESERVED": 3,
        "CONFIRMED": 8,
        "PRODUCING": 3,
        "RELEASE": 18,
    }


@pytest.fixture
def samples():
    return [
        Sample(id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5, yield_rate=0.92, stock=480),
        Sample(id="S-002", name="GaN 에피택셜-4인치", avg_production_time=0.3, yield_rate=0.78, stock=220),
        Sample(id="S-003", name="SiC 파워기판-6인치", avg_production_time=0.8, yield_rate=0.92, stock=30),
        Sample(id="S-004", name="산화막 웨이퍼-SiO2", avg_production_time=0.6, yield_rate=0.88, stock=0),
    ]


class TestOrderStatusView:
    """주문량 확인 화면 테스트."""

    def test_display_returns_str(self, status_counts):
        """display()는 str을 반환한다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_reserved(self, status_counts):
        """RESERVED 상태가 포함된다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert "RESERVED" in result

    def test_display_contains_confirmed(self, status_counts):
        """CONFIRMED 상태가 포함된다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert "CONFIRMED" in result

    def test_display_contains_producing(self, status_counts):
        """PRODUCING 상태가 포함된다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert "PRODUCING" in result

    def test_display_contains_release(self, status_counts):
        """RELEASE 상태가 포함된다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert "RELEASE" in result

    def test_display_contains_count_values(self, status_counts):
        """주문 건수가 포함된다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts=status_counts)
        result = view.display()
        assert "3" in result
        assert "8" in result
        assert "18" in result

    def test_display_does_not_contain_rejected(self):
        """REJECTED는 포함되지 않는다."""
        from app.view.monitor_view import OrderStatusView
        counts = {"RESERVED": 2, "CONFIRMED": 5, "PRODUCING": 1, "RELEASE": 10}
        view = OrderStatusView(status_counts=counts)
        result = view.display()
        # REJECTED 항목은 표시하지 않음
        assert "REJECTED" not in result

    def test_display_empty_counts_returns_str(self):
        """빈 카운트도 str을 반환한다."""
        from app.view.monitor_view import OrderStatusView
        view = OrderStatusView(status_counts={})
        result = view.display()
        assert isinstance(result, str)


class TestStockStatusView:
    """재고량 확인 화면 테스트."""

    def test_display_returns_str(self, samples):
        """display()는 str을 반환한다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_surplus_keyword(self, samples):
        """'여유' 키워드가 포함된다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert "여유" in result

    def test_display_contains_shortage_keyword(self, samples):
        """'부족' 키워드가 포함된다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert "부족" in result

    def test_display_contains_depleted_keyword(self, samples):
        """'고갈' 키워드가 포함된다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert "고갈" in result

    def test_display_contains_sample_names(self, samples):
        """시료명이 포함된다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert "실리콘 웨이퍼-8인치" in result

    def test_display_contains_stock_values(self, samples):
        """재고 수량이 포함된다."""
        from app.view.monitor_view import StockStatusView
        stock_statuses = ["여유", "여유", "부족", "고갈"]
        view = StockStatusView(samples=samples, stock_statuses=stock_statuses)
        result = view.display()
        assert "480" in result
        assert "0" in result

    def test_display_empty_samples_returns_str(self):
        """빈 시료 목록도 str을 반환한다."""
        from app.view.monitor_view import StockStatusView
        view = StockStatusView(samples=[], stock_statuses=[])
        result = view.display()
        assert isinstance(result, str)

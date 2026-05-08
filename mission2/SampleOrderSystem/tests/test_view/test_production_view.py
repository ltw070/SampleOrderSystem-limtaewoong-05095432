"""Phase 4 Red: ProductionView 테스트."""
import pytest
from app.model.production import ProductionItem
from app.model.sample import Sample


@pytest.fixture
def current_item():
    return ProductionItem(
        order_no="ORD-20260416-0038",
        sample_id="S-003",
        shortage=50,
        yield_rate=0.92,
        avg_production_time=0.8,
    )


@pytest.fixture
def queue_items():
    return [
        ProductionItem(
            order_no="ORD-20260416-0040",
            sample_id="S-004",
            shortage=150,
            yield_rate=0.88,
            avg_production_time=0.6,
        ),
        ProductionItem(
            order_no="ORD-20260416-0043",
            sample_id="S-003",
            shortage=170,
            yield_rate=0.92,
            avg_production_time=0.8,
        ),
    ]


@pytest.fixture
def samples_dict():
    return {
        "S-003": Sample(id="S-003", name="SiC 파워기판-6인치", avg_production_time=0.8, yield_rate=0.92, stock=30),
        "S-004": Sample(id="S-004", name="산화막 웨이퍼-SiO2", avg_production_time=0.6, yield_rate=0.88, stock=0),
    }


class TestProductionView:
    """생산라인 현황 화면 테스트."""

    def test_display_returns_str(self, current_item, queue_items, samples_dict):
        """display()는 str을 반환한다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=queue_items, samples=samples_dict)
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_fifo_keyword(self, current_item, queue_items, samples_dict):
        """FIFO 또는 생산라인 키워드가 포함된다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=queue_items, samples=samples_dict)
        result = view.display()
        assert "FIFO" in result or "생산라인" in result or "생산" in result

    def test_display_contains_current_order_no(self, current_item, queue_items, samples_dict):
        """현재 처리 중인 주문번호가 포함된다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=queue_items, samples=samples_dict)
        result = view.display()
        assert "ORD-20260416-0038" in result

    def test_display_contains_queue_order_nos(self, current_item, queue_items, samples_dict):
        """대기 중인 주문번호들이 포함된다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=queue_items, samples=samples_dict)
        result = view.display()
        assert "ORD-20260416-0040" in result
        assert "ORD-20260416-0043" in result

    def test_display_no_current_returns_str(self, queue_items, samples_dict):
        """현재 처리 중인 항목이 없어도 str을 반환한다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=None, queue=queue_items, samples=samples_dict)
        result = view.display()
        assert isinstance(result, str)

    def test_display_empty_queue_returns_str(self, current_item, samples_dict):
        """대기 큐가 비어 있어도 str을 반환한다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=[], samples=samples_dict)
        result = view.display()
        assert isinstance(result, str)

    def test_display_all_empty_returns_str(self):
        """현재 항목도 큐도 없어도 str을 반환한다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=None, queue=[], samples={})
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_production_time(self, current_item, samples_dict):
        """생산 시간 정보가 포함된다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=[], samples=samples_dict)
        result = view.display()
        # total_time 계산: actual_qty * avg_production_time
        assert "min" in result or str(int(current_item.total_time)) in result

    def test_display_contains_sample_name(self, current_item, samples_dict):
        """시료명이 포함된다."""
        from app.view.production_view import ProductionView
        view = ProductionView(current=current_item, queue=[], samples=samples_dict)
        result = view.display()
        assert "SiC 파워기판-6인치" in result

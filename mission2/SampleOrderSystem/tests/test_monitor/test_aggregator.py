"""Phase 5 - Red: MonitorAggregator 단위 테스트"""
import pytest
from datetime import datetime

from app.model.enums import OrderStatus
from app.model.sample import Sample
from app.model.order import Order
from app.monitor.aggregator import MonitorAggregator, StockLevel


def make_order(order_no, sample_id, qty, status):
    return Order(
        order_no=order_no,
        sample_id=sample_id,
        customer_name="테스트고객",
        quantity=qty,
        status=status,
        created_at=datetime(2026, 1, 1, 9, 0, 0),
    )


def make_sample(sample_id, name, stock, yield_rate=0.90, avg_production_time=120.0):
    return Sample(
        id=sample_id,
        name=name,
        stock=stock,
        yield_rate=yield_rate,
        avg_production_time=avg_production_time,
    )


class TestCountByStatus:
    def test_count_by_status_excludes_rejected(self):
        """REJECTED 주문이 집계에서 제외되는지 확인"""
        aggregator = MonitorAggregator()

        orders = [
            make_order("ORD-20260101-0001", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0002", "S-001", 20, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0003", "S-001", 30, OrderStatus.REJECTED),
            make_order("ORD-20260101-0004", "S-001", 40, OrderStatus.PRODUCING),
        ]
        counts = aggregator.count_by_status(orders)

        assert "REJECTED" not in counts
        assert OrderStatus.REJECTED.value not in counts

    def test_count_by_status_correct_counts(self):
        """각 상태별 건수가 정확한지 확인 (RESERVED 3, CONFIRMED 2, PRODUCING 1, RELEASE 5, REJECTED 2)"""
        aggregator = MonitorAggregator()

        orders = [
            make_order("ORD-20260101-0001", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0002", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0003", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0004", "S-001", 20, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0005", "S-001", 20, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0006", "S-001", 30, OrderStatus.PRODUCING),
            make_order("ORD-20260101-0007", "S-001", 40, OrderStatus.RELEASE),
            make_order("ORD-20260101-0008", "S-001", 40, OrderStatus.RELEASE),
            make_order("ORD-20260101-0009", "S-001", 40, OrderStatus.RELEASE),
            make_order("ORD-20260101-0010", "S-001", 40, OrderStatus.RELEASE),
            make_order("ORD-20260101-0011", "S-001", 40, OrderStatus.RELEASE),
            make_order("ORD-20260101-0012", "S-001", 50, OrderStatus.REJECTED),
            make_order("ORD-20260101-0013", "S-001", 50, OrderStatus.REJECTED),
        ]
        counts = aggregator.count_by_status(orders)

        assert counts[OrderStatus.RESERVED.value] == 3
        assert counts[OrderStatus.CONFIRMED.value] == 2
        assert counts[OrderStatus.PRODUCING.value] == 1
        assert counts[OrderStatus.RELEASE.value] == 5

    def test_count_by_status_all_four_keys_present(self):
        """결과에 RESERVED/CONFIRMED/PRODUCING/RELEASE 4개 키가 존재해야 함"""
        aggregator = MonitorAggregator()
        counts = aggregator.count_by_status([])

        assert OrderStatus.RESERVED.value in counts
        assert OrderStatus.CONFIRMED.value in counts
        assert OrderStatus.PRODUCING.value in counts
        assert OrderStatus.RELEASE.value in counts

    def test_count_by_status_empty_orders(self):
        """주문이 없으면 모든 상태 0"""
        aggregator = MonitorAggregator()
        counts = aggregator.count_by_status([])

        assert counts[OrderStatus.RESERVED.value] == 0
        assert counts[OrderStatus.CONFIRMED.value] == 0
        assert counts[OrderStatus.PRODUCING.value] == 0
        assert counts[OrderStatus.RELEASE.value] == 0


class TestStockLevel:
    def test_stock_level_depleted_when_stock_zero(self):
        """stock=0 → StockLevel.DEPLETED"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=0)
        orders = [make_order("ORD-20260101-0001", "S-001", 100, OrderStatus.CONFIRMED)]

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.DEPLETED

    def test_stock_level_sufficient_when_stock_gte_active_qty(self):
        """stock=100, 활성주문량=50 → StockLevel.SUFFICIENT (100 >= 50)"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=100)
        orders = [
            make_order("ORD-20260101-0001", "S-001", 30, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0002", "S-001", 20, OrderStatus.PRODUCING),
        ]

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.SUFFICIENT

    def test_stock_level_shortage_when_0_lt_stock_lt_active_qty(self):
        """stock=30, 활성주문량=100 → StockLevel.SHORTAGE (0 < 30 < 100)"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=30)
        orders = [
            make_order("ORD-20260101-0001", "S-001", 60, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0002", "S-001", 40, OrderStatus.PRODUCING),
        ]

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.SHORTAGE

    def test_stock_level_depleted_even_with_no_active_orders(self):
        """stock=0, 활성주문 없어도 → StockLevel.DEPLETED"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=0)
        orders = []

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.DEPLETED

    def test_stock_level_sufficient_when_no_active_orders_with_stock(self):
        """stock > 0, 활성주문 없음 → StockLevel.SUFFICIENT"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=100)
        orders = []

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.SUFFICIENT

    def test_stock_level_only_counts_confirmed_and_producing(self):
        """RESERVED, RELEASE 주문은 활성주문 계산에 포함되지 않음"""
        aggregator = MonitorAggregator()
        sample = make_sample("S-001", "실리콘 웨이퍼-8인치", stock=50)
        orders = [
            # 활성 주문: CONFIRMED 20 + PRODUCING 20 = 40 <= 50 → SUFFICIENT
            make_order("ORD-20260101-0001", "S-001", 20, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0002", "S-001", 20, OrderStatus.PRODUCING),
            # 비활성 주문: 계산 제외
            make_order("ORD-20260101-0003", "S-001", 100, OrderStatus.RESERVED),
            make_order("ORD-20260101-0004", "S-001", 100, OrderStatus.RELEASE),
        ]

        level = aggregator.stock_level(sample, orders)

        assert level == StockLevel.SUFFICIENT


class TestProductionCount:
    def test_production_count_returns_int(self):
        """반환 타입이 int인지 확인"""
        aggregator = MonitorAggregator()
        orders = [make_order("ORD-20260101-0001", "S-001", 50, OrderStatus.PRODUCING)]

        count = aggregator.production_count(orders)

        assert isinstance(count, int)

    def test_production_count_only_producing(self):
        """PRODUCING 상태 주문 건수만 반환"""
        aggregator = MonitorAggregator()
        orders = [
            make_order("ORD-20260101-0001", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0002", "S-001", 20, OrderStatus.CONFIRMED),
            make_order("ORD-20260101-0003", "S-001", 30, OrderStatus.PRODUCING),
            make_order("ORD-20260101-0004", "S-001", 40, OrderStatus.PRODUCING),
            make_order("ORD-20260101-0005", "S-001", 50, OrderStatus.RELEASE),
            make_order("ORD-20260101-0006", "S-001", 60, OrderStatus.REJECTED),
        ]

        count = aggregator.production_count(orders)

        assert count == 2

    def test_production_count_zero_when_no_producing(self):
        """PRODUCING 주문 없으면 0 반환"""
        aggregator = MonitorAggregator()
        orders = [
            make_order("ORD-20260101-0001", "S-001", 10, OrderStatus.RESERVED),
            make_order("ORD-20260101-0002", "S-001", 20, OrderStatus.CONFIRMED),
        ]

        count = aggregator.production_count(orders)

        assert count == 0

    def test_production_count_empty_orders(self):
        """주문이 없으면 0 반환"""
        aggregator = MonitorAggregator()

        count = aggregator.production_count([])

        assert count == 0

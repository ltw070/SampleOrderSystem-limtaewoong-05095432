"""Phase 5 - Red: MonitorFormatter 단위 테스트"""
import pytest
from datetime import datetime

from app.model.enums import OrderStatus
from app.model.sample import Sample
from app.monitor.aggregator import StockLevel
from app.monitor.formatter import MonitorFormatter


def make_sample(sample_id, name, stock, yield_rate=0.90, avg_production_time=120.0):
    return Sample(
        id=sample_id,
        name=name,
        stock=stock,
        yield_rate=yield_rate,
        avg_production_time=avg_production_time,
    )


class TestFormatOrderStatus:
    def test_format_order_status_returns_str(self):
        """반환 타입이 str인지 확인"""
        formatter = MonitorFormatter()
        status_counts = {
            "RESERVED": 3,
            "CONFIRMED": 8,
            "PRODUCING": 3,
            "RELEASE": 18,
        }

        result = formatter.format_order_status(status_counts)

        assert isinstance(result, str)

    def test_format_order_status_contains_status_names(self):
        """RESERVED, CONFIRMED, PRODUCING, RELEASE 포함 여부 확인"""
        formatter = MonitorFormatter()
        status_counts = {
            "RESERVED": 3,
            "CONFIRMED": 8,
            "PRODUCING": 3,
            "RELEASE": 18,
        }

        result = formatter.format_order_status(status_counts)

        assert "RESERVED" in result
        assert "CONFIRMED" in result
        assert "PRODUCING" in result
        assert "RELEASE" in result

    def test_format_order_status_excludes_rejected(self):
        """REJECTED 텍스트가 포함되지 않아야 함"""
        formatter = MonitorFormatter()
        status_counts = {
            "RESERVED": 3,
            "CONFIRMED": 8,
            "PRODUCING": 3,
            "RELEASE": 18,
        }

        result = formatter.format_order_status(status_counts)

        assert "REJECTED" not in result

    def test_format_order_status_contains_counts(self):
        """건수 숫자가 포함되어 있는지 확인"""
        formatter = MonitorFormatter()
        status_counts = {
            "RESERVED": 5,
            "CONFIRMED": 10,
            "PRODUCING": 2,
            "RELEASE": 20,
        }

        result = formatter.format_order_status(status_counts)

        assert "5" in result
        assert "10" in result
        assert "2" in result
        assert "20" in result

    def test_format_order_status_empty_dict(self):
        """빈 딕셔너리도 str 반환"""
        formatter = MonitorFormatter()

        result = formatter.format_order_status({})

        assert isinstance(result, str)

    def test_format_order_status_no_print(self):
        """print() 호출 없이 str만 반환 - len > 0 확인"""
        formatter = MonitorFormatter()
        status_counts = {
            "RESERVED": 1,
            "CONFIRMED": 1,
            "PRODUCING": 1,
            "RELEASE": 1,
        }

        result = formatter.format_order_status(status_counts)

        assert isinstance(result, str)
        assert len(result) > 0


class TestFormatStockStatus:
    def test_format_stock_status_returns_str(self):
        """반환 타입이 str인지 확인"""
        formatter = MonitorFormatter()
        samples = [make_sample("S-001", "실리콘 웨이퍼-8인치", stock=100)]
        stock_levels = [StockLevel.SUFFICIENT]

        result = formatter.format_stock_status(samples, stock_levels)

        assert isinstance(result, str)

    def test_format_stock_status_contains_sufficient(self):
        """여유 텍스트 포함 확인"""
        formatter = MonitorFormatter()
        samples = [make_sample("S-001", "실리콘 웨이퍼-8인치", stock=100)]
        stock_levels = [StockLevel.SUFFICIENT]

        result = formatter.format_stock_status(samples, stock_levels)

        assert "여유" in result

    def test_format_stock_status_contains_shortage(self):
        """부족 텍스트 포함 확인"""
        formatter = MonitorFormatter()
        samples = [make_sample("S-002", "SiC 파워기판-6인치", stock=30)]
        stock_levels = [StockLevel.SHORTAGE]

        result = formatter.format_stock_status(samples, stock_levels)

        assert "부족" in result

    def test_format_stock_status_contains_depleted(self):
        """고갈 텍스트 포함 확인"""
        formatter = MonitorFormatter()
        samples = [make_sample("S-003", "산화막 웨이퍼", stock=0)]
        stock_levels = [StockLevel.DEPLETED]

        result = formatter.format_stock_status(samples, stock_levels)

        assert "고갈" in result

    def test_format_stock_status_all_levels(self):
        """여유, 부족, 고갈 텍스트 모두 포함"""
        formatter = MonitorFormatter()
        samples = [
            make_sample("S-001", "실리콘 웨이퍼-8인치", stock=480),
            make_sample("S-002", "SiC 파워기판-6인치", stock=30),
            make_sample("S-003", "산화막 웨이퍼-SiO2", stock=0),
        ]
        stock_levels = [StockLevel.SUFFICIENT, StockLevel.SHORTAGE, StockLevel.DEPLETED]

        result = formatter.format_stock_status(samples, stock_levels)

        assert isinstance(result, str)
        assert "여유" in result
        assert "부족" in result
        assert "고갈" in result

    def test_format_stock_status_contains_sample_names(self):
        """시료 이름이 출력에 포함되는지 확인"""
        formatter = MonitorFormatter()
        samples = [make_sample("S-001", "실리콘 웨이퍼-8인치", stock=100)]
        stock_levels = [StockLevel.SUFFICIENT]

        result = formatter.format_stock_status(samples, stock_levels)

        assert "실리콘 웨이퍼-8인치" in result

    def test_format_stock_status_empty_lists(self):
        """빈 리스트도 str 반환"""
        formatter = MonitorFormatter()

        result = formatter.format_stock_status([], [])

        assert isinstance(result, str)

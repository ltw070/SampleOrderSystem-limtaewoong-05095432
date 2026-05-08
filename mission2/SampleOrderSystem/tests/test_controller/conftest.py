"""Phase3 Controller 테스트 공통 픽스처"""
import pytest
from datetime import datetime
from unittest.mock import MagicMock

from app.model.sample import Sample
from app.model.order import Order
from app.model.enums import OrderStatus
from app.repository.sample_repository import SampleRepository
from app.repository.order_repository import OrderRepository


# ------------------------------------------------------------------
# Mock Repository 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def mock_sample_repo():
    """SampleRepository MagicMock 픽스처"""
    repo = MagicMock(spec=SampleRepository)
    return repo


@pytest.fixture
def mock_order_repo():
    """OrderRepository MagicMock 픽스처"""
    repo = MagicMock(spec=OrderRepository)
    return repo


# ------------------------------------------------------------------
# 도메인 객체 헬퍼 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def sample_with_stock():
    """재고가 충분한 Sample (stock=100)"""
    return Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=5.0,
        yield_rate=0.9,
        stock=100,
    )


@pytest.fixture
def sample_no_stock():
    """재고가 없는 Sample (stock=0)"""
    return Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=5.0,
        yield_rate=0.9,
        stock=0,
    )


@pytest.fixture
def sample_partial_stock():
    """재고가 부족한 Sample (stock=5, quantity=10)"""
    return Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=5.0,
        yield_rate=0.9,
        stock=5,
    )


@pytest.fixture
def reserved_order():
    """RESERVED 상태의 주문"""
    return Order(
        order_no="ORD-20260508-0001",
        sample_id="S-001",
        customer_name="삼성전자",
        quantity=10,
        created_at=datetime(2026, 5, 8, 9, 0, 0),
        status=OrderStatus.RESERVED,
    )


@pytest.fixture
def confirmed_order():
    """CONFIRMED 상태의 주문"""
    return Order(
        order_no="ORD-20260508-0002",
        sample_id="S-001",
        customer_name="삼성전자",
        quantity=10,
        created_at=datetime(2026, 5, 8, 9, 0, 0),
        status=OrderStatus.CONFIRMED,
    )


@pytest.fixture
def producing_order():
    """PRODUCING 상태의 주문"""
    return Order(
        order_no="ORD-20260508-0003",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=10,
        created_at=datetime(2026, 5, 8, 10, 0, 0),
        status=OrderStatus.PRODUCING,
    )

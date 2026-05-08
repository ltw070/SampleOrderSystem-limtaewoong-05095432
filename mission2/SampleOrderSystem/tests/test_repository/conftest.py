"""Phase2 Repository 테스트 공통 픽스처"""
import pytest
from datetime import datetime

from app.model.sample import Sample
from app.model.order import Order
from app.model.enums import OrderStatus
from app.repository.json.json_sample_repo import JsonSampleRepository
from app.repository.json.json_order_repo import JsonOrderRepository


# ------------------------------------------------------------------
# Repository 인스턴스 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def tmp_sample_repo(tmp_path):
    """tmp_path 기반 JsonSampleRepository 픽스처"""
    return JsonSampleRepository(tmp_path / "samples.json")


@pytest.fixture
def tmp_order_repo(tmp_path):
    """tmp_path 기반 JsonOrderRepository 픽스처"""
    return JsonOrderRepository(tmp_path / "orders.json")


# ------------------------------------------------------------------
# 도메인 객체 헬퍼 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def sample_a():
    return Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=480,
    )


@pytest.fixture
def sample_b():
    return Sample(
        id="S-002",
        name="갈륨 비소 웨이퍼",
        avg_production_time=1.2,
        yield_rate=0.85,
        stock=200,
    )


@pytest.fixture
def order_reserved():
    return Order(
        order_no="ORD-20260508-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=200,
        created_at=datetime(2026, 5, 8, 9, 32, 15),
        status=OrderStatus.RESERVED,
    )


@pytest.fixture
def order_producing():
    return Order(
        order_no="ORD-20260508-0002",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=150,
        created_at=datetime(2026, 5, 8, 10, 0, 0),
        status=OrderStatus.PRODUCING,
    )


@pytest.fixture
def order_confirmed():
    return Order(
        order_no="ORD-20260508-0003",
        sample_id="S-002",
        customer_name="인텔코리아",
        quantity=100,
        created_at=datetime(2026, 5, 8, 11, 0, 0),
        status=OrderStatus.CONFIRMED,
    )

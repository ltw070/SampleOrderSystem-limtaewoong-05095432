"""Phase2 Red: JsonOrderRepository 테스트 (4개)"""
import json
import pytest
from datetime import datetime

from app.model.order import Order
from app.model.enums import OrderStatus
from app.repository.json.json_order_repo import JsonOrderRepository

# 공통 픽스처는 conftest.py에서 제공:
# tmp_order_repo, order_reserved, order_producing, order_confirmed


class TestOrderSaveAndFindById:
    """test_save_and_find_by_id: Order 저장 후 id로 조회"""

    def test_save_and_find_by_id(self, tmp_order_repo, order_reserved):
        """저장한 Order를 order_no로 조회할 수 있어야 한다"""
        tmp_order_repo.save(order_reserved)
        result = tmp_order_repo.find_by_id("ORD-20260508-0001")

        assert result is not None
        assert result.order_no == "ORD-20260508-0001"
        assert result.customer_name == "삼성전자 파운드리"
        assert result.status == OrderStatus.RESERVED

    def test_find_by_id_nonexistent_returns_none(self, tmp_order_repo):
        """존재하지 않는 order_no로 조회하면 None을 반환해야 한다"""
        result = tmp_order_repo.find_by_id("ORD-99999999-9999")
        assert result is None

    def test_save_datetime_iso8601(self, tmp_path, order_reserved):
        """created_at이 ISO 8601 형식으로 파일에 저장되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo = JsonOrderRepository(file_path)
        repo.save(order_reserved)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created_at_str = data[0]["created_at"]
        parsed = datetime.fromisoformat(created_at_str)
        assert parsed == datetime(2026, 5, 8, 9, 32, 15)

    def test_save_status_as_string(self, tmp_path, order_reserved):
        """OrderStatus가 문자열 값으로 파일에 저장되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo = JsonOrderRepository(file_path)
        repo.save(order_reserved)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data[0]["status"] == "RESERVED"


class TestOrderFindByStatus:
    """test_find_by_status: RESERVED 상태 주문만 조회"""

    def test_find_by_status_reserved(self, tmp_order_repo, order_reserved, order_producing):
        """RESERVED 상태 주문만 필터링해야 한다"""
        tmp_order_repo.save(order_reserved)
        tmp_order_repo.save(order_producing)

        results = tmp_order_repo.find_by_status(OrderStatus.RESERVED)
        assert len(results) == 1
        assert results[0].order_no == "ORD-20260508-0001"
        assert results[0].status == OrderStatus.RESERVED

    def test_find_by_status_producing(self, tmp_order_repo, order_reserved, order_producing):
        """PRODUCING 상태 주문만 필터링해야 한다"""
        tmp_order_repo.save(order_reserved)
        tmp_order_repo.save(order_producing)

        results = tmp_order_repo.find_by_status(OrderStatus.PRODUCING)
        assert len(results) == 1
        assert results[0].status == OrderStatus.PRODUCING

    def test_find_by_status_empty(self, tmp_order_repo, order_reserved):
        """해당 상태의 주문이 없으면 빈 리스트를 반환해야 한다"""
        tmp_order_repo.save(order_reserved)

        results = tmp_order_repo.find_by_status(OrderStatus.RELEASE)
        assert results == []

    def test_find_all(self, tmp_order_repo, order_reserved, order_producing, order_confirmed):
        """find_all은 모든 주문을 반환해야 한다"""
        tmp_order_repo.save(order_reserved)
        tmp_order_repo.save(order_producing)
        tmp_order_repo.save(order_confirmed)

        results = tmp_order_repo.find_all()
        assert len(results) == 3


class TestOrderUpdateStatus:
    """test_update_status: 상태 업데이트 (RESERVED → CONFIRMED)"""

    def test_update_status_reserved_to_confirmed(self, tmp_order_repo, order_reserved):
        """RESERVED → CONFIRMED 상태 전이"""
        tmp_order_repo.save(order_reserved)
        result = tmp_order_repo.update_status("ORD-20260508-0001", OrderStatus.CONFIRMED)

        assert result.status == OrderStatus.CONFIRMED

    def test_update_status_persisted(self, tmp_path, order_reserved):
        """상태 변경이 파일에 반영되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo = JsonOrderRepository(file_path)
        repo.save(order_reserved)
        repo.update_status("ORD-20260508-0001", OrderStatus.CONFIRMED)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data[0]["status"] == "CONFIRMED"

    def test_update_status_all_transitions(self, tmp_order_repo, order_reserved):
        """모든 상태 전이가 가능해야 한다"""
        tmp_order_repo.save(order_reserved)
        for status in [OrderStatus.PRODUCING, OrderStatus.CONFIRMED, OrderStatus.RELEASE]:
            result = tmp_order_repo.update_status("ORD-20260508-0001", status)
            assert result.status == status

    def test_update_status_nonexistent_raises(self, tmp_order_repo):
        """존재하지 않는 order_no 상태 변경은 ValueError를 발생시켜야 한다"""
        with pytest.raises(ValueError):
            tmp_order_repo.update_status("ORD-99999999-9999", OrderStatus.PRODUCING)


class TestOrderDelete:
    """Order 삭제 테스트"""

    def test_delete_existing(self, tmp_order_repo, order_reserved):
        """존재하는 Order를 삭제하면 True를 반환해야 한다"""
        tmp_order_repo.save(order_reserved)
        result = tmp_order_repo.delete("ORD-20260508-0001")
        assert result is True

    def test_delete_then_find_returns_none(self, tmp_order_repo, order_reserved):
        """삭제 후 find_by_id는 None을 반환해야 한다"""
        tmp_order_repo.save(order_reserved)
        tmp_order_repo.delete("ORD-20260508-0001")

        result = tmp_order_repo.find_by_id("ORD-20260508-0001")
        assert result is None

    def test_delete_nonexistent_returns_false(self, tmp_order_repo):
        """존재하지 않는 order_no 삭제는 False를 반환해야 한다"""
        result = tmp_order_repo.delete("ORD-99999999-9999")
        assert result is False


class TestOrderPersistence:
    """test_persistence: 영속성 검증 (새 인스턴스로 재조회)"""

    def test_persistence_new_instance(self, tmp_path, order_reserved):
        """새 인스턴스를 생성해도 이전에 저장한 데이터가 유지되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo1 = JsonOrderRepository(file_path)
        repo1.save(order_reserved)

        repo2 = JsonOrderRepository(file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert result is not None
        assert result.order_no == "ORD-20260508-0001"
        assert result.status == OrderStatus.RESERVED

    def test_datetime_persists_correctly(self, tmp_path, order_reserved):
        """datetime 필드가 정확하게 영속화되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo1 = JsonOrderRepository(file_path)
        repo1.save(order_reserved)

        repo2 = JsonOrderRepository(file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert isinstance(result.created_at, datetime)
        assert result.created_at == datetime(2026, 5, 8, 9, 32, 15)

    def test_status_enum_persists(self, tmp_path, order_reserved):
        """OrderStatus Enum이 정확하게 영속화되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo1 = JsonOrderRepository(file_path)
        repo1.save(order_reserved)

        repo2 = JsonOrderRepository(file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert isinstance(result.status, OrderStatus)
        assert result.status == OrderStatus.RESERVED

    def test_status_update_persists(self, tmp_path, order_reserved):
        """상태 변경 후 새 인스턴스에서도 변경사항이 유지되어야 한다"""
        file_path = tmp_path / "orders.json"
        repo1 = JsonOrderRepository(file_path)
        repo1.save(order_reserved)
        repo1.update_status("ORD-20260508-0001", OrderStatus.PRODUCING)

        repo2 = JsonOrderRepository(file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert result.status == OrderStatus.PRODUCING

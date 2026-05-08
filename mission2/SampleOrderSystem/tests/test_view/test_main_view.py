"""Phase 4 Red: MainView 테스트."""
import pytest
from datetime import datetime


class TestMainView:
    """MainView 화면 문자열 반환 테스트."""

    def test_display_returns_str(self):
        """display()는 str을 반환한다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_system_title(self):
        """반환 문자열에 시스템 제목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "반도체 시료 생산주문관리 시스템" in result

    def test_display_contains_menu_1_sample(self):
        """[1] 시료 관리 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[1]" in result
        assert "시료" in result

    def test_display_contains_menu_2_order(self):
        """[2] 시료 주문 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[2]" in result
        assert "주문" in result

    def test_display_contains_menu_3_approve(self):
        """[3] 주문 승인/거절 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[3]" in result
        assert "승인" in result

    def test_display_contains_menu_4_monitor(self):
        """[4] 모니터링 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[4]" in result
        assert "모니터링" in result

    def test_display_contains_menu_5_production(self):
        """[5] 생산라인 조회 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[5]" in result
        assert "생산" in result

    def test_display_contains_menu_6_shipment(self):
        """[6] 출고 처리 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[6]" in result
        assert "출고" in result

    def test_display_contains_menu_0_exit(self):
        """[0] 종료 메뉴 항목이 포함된다."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert "[0]" in result
        assert "종료" in result

    def test_display_with_sample_count(self):
        """등록 시료 수가 반환 문자열에 포함된다."""
        from app.view.main_view import MainView
        view = MainView(sample_count=12)
        result = view.display()
        assert "12" in result

    def test_display_with_total_stock(self):
        """총 재고가 반환 문자열에 포함된다."""
        from app.view.main_view import MainView
        view = MainView(total_stock=2840)
        result = view.display()
        assert "2840" in result or "2,840" in result

    def test_display_with_order_count(self):
        """전체 주문 건수가 반환 문자열에 포함된다."""
        from app.view.main_view import MainView
        view = MainView(order_count=36)
        result = view.display()
        assert "36" in result

    def test_display_with_production_count(self):
        """생산라인 대기 건수가 반환 문자열에 포함된다."""
        from app.view.main_view import MainView
        view = MainView(production_count=3)
        result = view.display()
        assert "3" in result

    def test_display_with_all_defaults(self):
        """기본값(0)으로 생성해도 에러 없이 str 반환."""
        from app.view.main_view import MainView
        view = MainView()
        result = view.display()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_display_with_current_time(self):
        """current_time이 있으면 날짜/시간 정보가 포함된다."""
        from app.view.main_view import MainView
        fixed_time = datetime(2026, 4, 16, 9, 32, 15)
        view = MainView(current_time=fixed_time)
        result = view.display()
        assert "2026" in result or "09:32" in result

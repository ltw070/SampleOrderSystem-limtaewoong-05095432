"""Phase 4 Red: BaseView 추상 인터페이스 테스트."""
import pytest
from abc import ABC


class TestBaseViewAbstract:
    """BaseView 추상 클래스 구조 테스트."""

    def test_cannot_instantiate_directly(self):
        """BaseView는 직접 인스턴스화 불가."""
        from app.view.base_view import BaseView
        with pytest.raises(TypeError):
            BaseView()

    def test_subclass_without_display_raises(self):
        """display()를 구현하지 않은 서브클래스는 인스턴스화 불가."""
        from app.view.base_view import BaseView

        class IncompleteView(BaseView):
            pass

        with pytest.raises(TypeError):
            IncompleteView()

    def test_display_returns_str(self):
        """display()는 반드시 str을 반환해야 한다."""
        from app.view.base_view import BaseView

        class ConcreteView(BaseView):
            def display(self) -> str:
                return "hello"

        v = ConcreteView()
        result = v.display()
        assert isinstance(result, str)

    def test_get_input_interface_exists(self):
        """get_input() 메서드가 존재해야 한다."""
        from app.view.base_view import BaseView

        class ConcreteView(BaseView):
            def display(self) -> str:
                return ""

        v = ConcreteView()
        assert hasattr(v, "get_input")
        assert callable(v.get_input)

    def test_get_input_returns_str(self):
        """get_input()은 str을 반환해야 한다."""
        from app.view.base_view import BaseView

        class ConcreteView(BaseView):
            def display(self) -> str:
                return ""

            def get_input(self, prompt: str = "") -> str:
                return "test_input"

        v = ConcreteView()
        result = v.get_input("Enter: ")
        assert isinstance(result, str)
        assert result == "test_input"

    def test_base_view_is_abstract(self):
        """BaseView는 ABC를 상속해야 한다."""
        from app.view.base_view import BaseView
        assert issubclass(BaseView, ABC)

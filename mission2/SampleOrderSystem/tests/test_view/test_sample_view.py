"""Phase 4 Red: SampleView 테스트."""
import pytest
from app.model.sample import Sample


@pytest.fixture
def sample_a():
    return Sample(id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5, yield_rate=0.92, stock=480)


@pytest.fixture
def sample_b():
    return Sample(id="S-002", name="GaN 에피택셜-4인치", avg_production_time=0.3, yield_rate=0.78, stock=220)


class TestSampleListView:
    """시료 목록 화면 테스트."""

    def test_display_returns_str(self, sample_a, sample_b):
        """display()는 str을 반환한다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a, sample_b])
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_sample_id(self, sample_a):
        """시료 ID가 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a])
        result = view.display()
        assert "S-001" in result

    def test_display_contains_sample_name(self, sample_a):
        """시료명이 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a])
        result = view.display()
        assert "실리콘 웨이퍼-8인치" in result

    def test_display_contains_yield_rate(self, sample_a):
        """수율 정보가 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a])
        result = view.display()
        # 수율은 % 혹은 소수로 표시될 수 있음
        assert "0.92" in result or "92" in result

    def test_display_contains_stock(self, sample_a):
        """재고 정보가 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a])
        result = view.display()
        assert "480" in result

    def test_display_empty_list_returns_str(self):
        """빈 목록도 str을 반환한다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[])
        result = view.display()
        assert isinstance(result, str)

    def test_display_multiple_samples(self, sample_a, sample_b):
        """여러 시료 모두 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a, sample_b])
        result = view.display()
        assert "S-001" in result
        assert "S-002" in result

    def test_display_contains_header_keyword(self, sample_a):
        """목록 헤더 키워드가 포함된다."""
        from app.view.sample_view import SampleListView
        view = SampleListView(samples=[sample_a])
        result = view.display()
        assert "시료" in result


class TestSampleRegisterView:
    """시료 등록 화면 테스트."""

    def test_display_returns_str(self):
        """display()는 str을 반환한다."""
        from app.view.sample_view import SampleRegisterView
        view = SampleRegisterView()
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_register_header(self):
        """등록 화면 헤더가 포함된다."""
        from app.view.sample_view import SampleRegisterView
        view = SampleRegisterView()
        result = view.display()
        assert "등록" in result

    def test_display_contains_input_prompts(self):
        """입력 프롬프트 항목이 포함된다."""
        from app.view.sample_view import SampleRegisterView
        view = SampleRegisterView()
        result = view.display()
        # ID, 이름, 생산시간, 수율 등 입력 항목 중 하나 이상 포함
        assert any(keyword in result for keyword in ["ID", "이름", "수율", "시료"])


class TestSampleSearchView:
    """시료 검색 결과 화면 테스트."""

    def test_display_returns_str(self, sample_a):
        """display()는 str을 반환한다."""
        from app.view.sample_view import SampleSearchView
        view = SampleSearchView(results=[sample_a], keyword="실리콘")
        result = view.display()
        assert isinstance(result, str)

    def test_display_contains_keyword(self, sample_a):
        """검색 키워드가 포함된다."""
        from app.view.sample_view import SampleSearchView
        view = SampleSearchView(results=[sample_a], keyword="실리콘")
        result = view.display()
        assert "실리콘" in result

    def test_display_contains_search_result(self, sample_a):
        """검색 결과 시료 ID가 포함된다."""
        from app.view.sample_view import SampleSearchView
        view = SampleSearchView(results=[sample_a], keyword="실리콘")
        result = view.display()
        assert "S-001" in result

    def test_display_empty_results_returns_str(self):
        """검색 결과 없을 때도 str을 반환한다."""
        from app.view.sample_view import SampleSearchView
        view = SampleSearchView(results=[], keyword="없는키워드")
        result = view.display()
        assert isinstance(result, str)

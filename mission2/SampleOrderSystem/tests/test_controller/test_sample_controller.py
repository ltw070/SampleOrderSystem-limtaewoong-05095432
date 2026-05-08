"""Phase3 Red: SampleController 테스트 - register/list/search 흐름"""
import pytest
from unittest.mock import MagicMock, call

from app.model.sample import Sample


class TestRegisterSample:
    def test_register_sample(self, mock_sample_repo, sample_with_stock):
        """새 Sample 등록 시 repo.save가 호출되어야 한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_by_id.return_value = None
        mock_sample_repo.save.return_value = sample_with_stock

        ctrl = SampleController(mock_sample_repo)
        result = ctrl.register_sample(
            id="S-001",
            name="실리콘 웨이퍼-8인치",
            avg_production_time=5.0,
            yield_rate=0.9,
            stock=100,
        )

        mock_sample_repo.save.assert_called_once()
        assert isinstance(result, Sample)
        assert result.id == "S-001"

    def test_register_sample_invalid_id(self, mock_sample_repo):
        """잘못된 id 형식으로 등록 시 ValueError가 발생해야 한다."""
        from app.controller.sample_controller import SampleController

        ctrl = SampleController(mock_sample_repo)

        with pytest.raises(ValueError):
            ctrl.register_sample(
                id="INVALID",
                name="테스트",
                avg_production_time=5.0,
                yield_rate=0.9,
            )

    def test_register_sample_duplicate_id(self, mock_sample_repo, sample_with_stock):
        """이미 존재하는 id로 등록 시 ValueError가 발생해야 한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_by_id.return_value = sample_with_stock

        ctrl = SampleController(mock_sample_repo)

        with pytest.raises(ValueError, match="already"):
            ctrl.register_sample(
                id="S-001",
                name="중복 시료",
                avg_production_time=3.0,
                yield_rate=0.8,
            )


class TestListSamples:
    def test_list_samples(self, mock_sample_repo, sample_with_stock):
        """list_samples 호출 시 find_all을 호출하고 Sample 목록을 반환한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_all.return_value = [sample_with_stock]

        ctrl = SampleController(mock_sample_repo)
        result = ctrl.list_samples()

        mock_sample_repo.find_all.assert_called_once()
        assert len(result) == 1
        assert result[0].id == "S-001"

    def test_list_samples_empty(self, mock_sample_repo):
        """시료가 없을 때 빈 목록을 반환한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_all.return_value = []

        ctrl = SampleController(mock_sample_repo)
        result = ctrl.list_samples()

        assert result == []


class TestSearchSamples:
    def test_search_samples(self, mock_sample_repo, sample_with_stock):
        """검색 시 find_by_name을 호출하고 결과를 반환한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_by_name.return_value = [sample_with_stock]

        ctrl = SampleController(mock_sample_repo)
        result = ctrl.search_samples("웨이퍼")

        mock_sample_repo.find_by_name.assert_called_once_with("웨이퍼")
        assert len(result) == 1

    def test_search_samples_no_match(self, mock_sample_repo):
        """매칭 결과가 없으면 빈 목록을 반환한다."""
        from app.controller.sample_controller import SampleController

        mock_sample_repo.find_by_name.return_value = []

        ctrl = SampleController(mock_sample_repo)
        result = ctrl.search_samples("존재하지않는시료")

        assert result == []

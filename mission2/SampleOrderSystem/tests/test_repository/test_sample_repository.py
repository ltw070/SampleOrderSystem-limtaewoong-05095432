"""Phase2 Red: JsonSampleRepository 테스트 (7개)"""
import json
import pytest
from pathlib import Path

from app.model.sample import Sample
from app.repository.json.json_sample_repo import JsonSampleRepository

# 공통 픽스처는 conftest.py에서 제공:
# tmp_sample_repo, sample_a, sample_b


class TestSampleSaveAndFindById:
    """test_save_and_find_by_id: Sample 저장 후 id로 조회"""

    def test_save_and_find_by_id(self, tmp_sample_repo, sample_a):
        """저장한 Sample을 id로 조회할 수 있어야 한다"""
        tmp_sample_repo.save(sample_a)
        result = tmp_sample_repo.find_by_id("S-001")

        assert result is not None
        assert result.id == "S-001"
        assert result.name == "실리콘 웨이퍼-8인치"
        assert result.stock == 480

    def test_find_by_id_nonexistent_returns_none(self, tmp_sample_repo):
        """존재하지 않는 id로 조회하면 None을 반환해야 한다"""
        result = tmp_sample_repo.find_by_id("S-999")
        assert result is None

    def test_save_returns_sample_instance(self, tmp_sample_repo, sample_a):
        """save는 Sample 인스턴스를 반환해야 한다"""
        result = tmp_sample_repo.save(sample_a)
        assert isinstance(result, Sample)


class TestSampleFindAllEmpty:
    """test_find_all_empty: 빈 저장소에서 find_all"""

    def test_find_all_empty(self, tmp_sample_repo):
        """빈 저장소에서 find_all은 빈 리스트를 반환해야 한다"""
        result = tmp_sample_repo.find_all()
        assert result == []


class TestSampleFindAllMultiple:
    """test_find_all_multiple: 여러 샘플 저장 후 find_all"""

    def test_find_all_multiple(self, tmp_sample_repo, sample_a, sample_b):
        """여러 Sample 저장 후 find_all은 모두 반환해야 한다"""
        tmp_sample_repo.save(sample_a)
        tmp_sample_repo.save(sample_b)

        results = tmp_sample_repo.find_all()
        assert len(results) == 2
        ids = [s.id for s in results]
        assert "S-001" in ids
        assert "S-002" in ids


class TestSampleUpdateStock:
    """test_update_stock: 재고 업데이트 후 조회 확인"""

    def test_update_stock_absolute(self, tmp_sample_repo, sample_a):
        """절대값으로 재고를 업데이트할 수 있어야 한다"""
        tmp_sample_repo.save(sample_a)
        result = tmp_sample_repo.update_stock("S-001", 999)

        assert result.stock == 999

    def test_update_stock_persisted(self, tmp_sample_repo, sample_a):
        """update_stock 후 find_by_id로 변경된 재고가 조회되어야 한다"""
        tmp_sample_repo.save(sample_a)
        tmp_sample_repo.update_stock("S-001", 100)

        found = tmp_sample_repo.find_by_id("S-001")
        assert found is not None
        assert found.stock == 100

    def test_update_stock_nonexistent_raises(self, tmp_sample_repo):
        """존재하지 않는 id의 재고 변경은 ValueError를 발생시켜야 한다"""
        with pytest.raises(ValueError):
            tmp_sample_repo.update_stock("S-999", 100)


class TestSampleDelete:
    """test_delete: 삭제 후 None 반환 확인"""

    def test_delete_existing(self, tmp_sample_repo, sample_a):
        """존재하는 Sample을 삭제하면 True를 반환해야 한다"""
        tmp_sample_repo.save(sample_a)
        result = tmp_sample_repo.delete("S-001")
        assert result is True

    def test_delete_then_find_returns_none(self, tmp_sample_repo, sample_a):
        """삭제 후 find_by_id는 None을 반환해야 한다"""
        tmp_sample_repo.save(sample_a)
        tmp_sample_repo.delete("S-001")

        result = tmp_sample_repo.find_by_id("S-001")
        assert result is None

    def test_delete_nonexistent_returns_false(self, tmp_sample_repo):
        """존재하지 않는 id 삭제는 False를 반환해야 한다"""
        result = tmp_sample_repo.delete("S-999")
        assert result is False


class TestSamplePersistence:
    """test_persistence: tmp_path에 저장 후 새 repo 인스턴스로 다시 읽기"""

    def test_persistence_new_instance(self, tmp_path, sample_a):
        """새 인스턴스를 생성해도 이전에 저장한 데이터가 유지되어야 한다"""
        file_path = tmp_path / "samples.json"
        repo1 = JsonSampleRepository(file_path)
        repo1.save(sample_a)

        repo2 = JsonSampleRepository(file_path)
        result = repo2.find_by_id("S-001")

        assert result is not None
        assert result.id == "S-001"
        assert result.name == "실리콘 웨이퍼-8인치"
        assert result.avg_production_time == 0.5
        assert result.yield_rate == 0.92
        assert result.stock == 480

    def test_persistence_multiple_samples(self, tmp_path, sample_a, sample_b):
        """여러 Sample이 새 인스턴스에서도 유지되어야 한다"""
        file_path = tmp_path / "samples.json"
        repo1 = JsonSampleRepository(file_path)
        repo1.save(sample_a)
        repo1.save(sample_b)

        repo2 = JsonSampleRepository(file_path)
        results = repo2.find_all()
        assert len(results) == 2


class TestSampleFindByName:
    """test_find_by_name: 이름으로 검색"""

    def test_find_by_name_keyword_match(self, tmp_sample_repo, sample_a, sample_b):
        """키워드로 시료를 검색할 수 있어야 한다 (부분 일치)"""
        tmp_sample_repo.save(sample_a)
        tmp_sample_repo.save(sample_b)

        results = tmp_sample_repo.find_by_name("웨이퍼")
        assert len(results) == 2

    def test_find_by_name_partial_match(self, tmp_sample_repo, sample_a, sample_b):
        """부분 일치로 특정 시료만 반환해야 한다"""
        tmp_sample_repo.save(sample_a)
        tmp_sample_repo.save(sample_b)

        results = tmp_sample_repo.find_by_name("실리콘")
        assert len(results) == 1
        assert results[0].id == "S-001"

    def test_find_by_name_no_match(self, tmp_sample_repo, sample_a):
        """일치하는 시료가 없으면 빈 리스트를 반환해야 한다"""
        tmp_sample_repo.save(sample_a)

        results = tmp_sample_repo.find_by_name("없는시료명")
        assert results == []

"""SampleView: 시료 관리 화면."""
from typing import List

from app.model.sample import Sample
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data


class SampleListView(BaseView):
    """시료 목록 화면."""

    def __init__(self, samples: List[Sample]) -> None:
        self._samples = samples

    def display(self) -> str:
        """시료 목록 화면 문자열을 반환한다."""
        if not self._samples:
            lines = [header("등록 시료 목록")]
            lines.append(no_data("등록된 시료가 없습니다."))
            return "\n".join(lines)

        lines = [header(f"등록 시료 목록  (총 {len(self._samples)}종)")]
        lines.append(
            table_row("ID", "시료명", "평균 생산시간", "수율", "현재 재고",
                      widths=[8, 24, 14, 8, 10])
        )
        lines.append(separator())
        for s in self._samples:
            lines.append(
                table_row(
                    s.id,
                    s.name,
                    f"{s.avg_production_time} min/ea",
                    f"{s.yield_rate:.2f}",
                    f"{s.stock} ea",
                    widths=[8, 24, 14, 8, 10],
                )
            )
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class SampleRegisterView(BaseView):
    """시료 등록 입력 화면."""

    def display(self) -> str:
        """시료 등록 화면 문자열을 반환한다."""
        lines = [
            header("시료 등록"),
            "",
            "  시료 ID           >",
            "  시료 이름         >",
            "  평균 생산시간     > (min/ea)",
            "  수율 (0~1)        >",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)


class SampleSearchView(BaseView):
    """시료 검색 결과 화면."""

    def __init__(self, results: List[Sample], keyword: str) -> None:
        self._results = results
        self._keyword = keyword

    def display(self) -> str:
        """시료 검색 결과 화면 문자열을 반환한다."""
        lines = [header(f"시료 검색 결과  [ 키워드: {self._keyword} ]")]

        if not self._results:
            lines.append(no_data(f"'{self._keyword}'에 해당하는 시료가 없습니다."))
            return "\n".join(lines)

        lines.append(
            table_row("ID", "시료명", "평균 생산시간", "수율", "현재 재고",
                      widths=[8, 24, 14, 8, 10])
        )
        lines.append(separator())
        for s in self._results:
            lines.append(
                table_row(
                    s.id,
                    s.name,
                    f"{s.avg_production_time} min/ea",
                    f"{s.yield_rate:.2f}",
                    f"{s.stock} ea",
                    widths=[8, 24, 14, 8, 10],
                )
            )
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

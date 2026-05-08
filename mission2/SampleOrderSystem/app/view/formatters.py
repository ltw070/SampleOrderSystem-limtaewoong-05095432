"""공통 포맷팅 유틸리티."""
from typing import Any

SEPARATOR = "-" * 64
DOUBLE_SEPARATOR = "=" * 64


def header(title: str) -> str:
    """섹션 헤더 문자열을 반환한다."""
    return f"\n{DOUBLE_SEPARATOR}\n  {title}\n{DOUBLE_SEPARATOR}"


def separator() -> str:
    """구분선 문자열을 반환한다."""
    return SEPARATOR


def table_row(*cols: Any, widths: list | None = None) -> str:
    """테이블 행을 포맷하여 반환한다."""
    if widths:
        parts = [str(c).ljust(w) for c, w in zip(cols, widths)]
    else:
        parts = [str(c) for c in cols]
    return "  " + "  ".join(parts)


def no_data(message: str = "데이터가 없습니다.") -> str:
    """데이터 없음 메시지를 반환한다."""
    return f"  [{message}]"

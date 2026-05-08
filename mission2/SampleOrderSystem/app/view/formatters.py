"""공통 포맷팅 유틸리티.

모든 View에서 재사용하는 포맷팅 헬퍼 함수 모음.
"""
from typing import Any

SEPARATOR = "-" * 64
DOUBLE_SEPARATOR = "=" * 64


def header(title: str) -> str:
    """섹션 헤더 문자열을 반환한다.

    Example:
        ================================================================
          [2] 시료 관리
        ================================================================
    """
    return f"\n{DOUBLE_SEPARATOR}\n  {title}\n{DOUBLE_SEPARATOR}"


def page_header(title: str, subtitle: str = "") -> str:
    """페이지 상단 타이틀 블록 문자열을 반환한다.

    메인 메뉴와 같이 타이틀을 강조하는 상단 블록에 사용한다.

    Example (subtitle 없음):
        ================================================================
          반도체 시료 생산주문관리 시스템
        ================================================================

    Example (subtitle 있음):
        ================================================================
          반도체 시료 생산주문관리 시스템
          시스템 현황   2026-04-16 09:32:15
        ================================================================
    """
    lines = [f"\n{DOUBLE_SEPARATOR}", f"  {title}"]
    if subtitle:
        lines.append(f"  {subtitle}")
    lines.append(DOUBLE_SEPARATOR)
    return "\n".join(lines)


def separator() -> str:
    """단일 구분선 문자열을 반환한다."""
    return SEPARATOR


def table_row(*cols: Any, widths: list | None = None) -> str:
    """테이블 행을 포맷하여 반환한다.

    Args:
        *cols: 컬럼 값 목록
        widths: 각 컬럼의 고정 너비 (ljust 적용)
    """
    if widths:
        parts = [str(c).ljust(w) for c, w in zip(cols, widths)]
    else:
        parts = [str(c) for c in cols]
    return "  " + "  ".join(parts)


def no_data(message: str = "데이터가 없습니다.") -> str:
    """데이터 없음 메시지를 반환한다."""
    return f"  [{message}]"

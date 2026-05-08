"""View 레이어 패키지.

모든 display() 메서드는 str을 반환한다 (print() 직접 호출 금지).
"""
from .base_view import BaseView
from .formatters import header, page_header, separator, table_row, no_data
from .main_view import MainView
from .sample_view import SampleListView, SampleRegisterView, SampleSearchView
from .order_view import (
    OrderPlaceView,
    OrderConfirmView,
    ReservedListView,
    ApproveResultView,
    RejectResultView,
)
from .monitor_view import OrderStatusView, StockStatusView
from .production_view import ProductionView
from .shipment_view import ShipmentListView, ShipmentResultView

__all__ = [
    "BaseView",
    "header",
    "page_header",
    "separator",
    "table_row",
    "no_data",
    "MainView",
    "SampleListView",
    "SampleRegisterView",
    "SampleSearchView",
    "OrderPlaceView",
    "OrderConfirmView",
    "ReservedListView",
    "ApproveResultView",
    "RejectResultView",
    "OrderStatusView",
    "StockStatusView",
    "ProductionView",
    "ShipmentListView",
    "ShipmentResultView",
]

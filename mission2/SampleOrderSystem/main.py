"""main.py - S-Semi 반도체 시료 생산주문관리 시스템 진입점.

전체 MVC + Repository + Monitor 레이어를 배선하고 메뉴 루프를 실행한다.

설계 원칙:
- main.py에서만 print() 사용 — View.display()가 반환한 str을 print()로 출력
- JSON Repository 구현체를 생성자에 주입 (의존성 역전)
- data/ 디렉토리가 없으면 자동 생성
"""
import os

from app.controller.sample_controller import SampleController
from app.controller.order_controller import OrderController
from app.controller.production_controller import ProductionController
from app.monitor.aggregator import MonitorAggregator
from app.monitor.formatter import MonitorFormatter
from app.repository.json.json_sample_repo import JsonSampleRepository
from app.repository.json.json_order_repo import JsonOrderRepository
from app.view.main_view import MainView
from app.view.sample_view import SampleListView, SampleRegisterView, SampleSearchView
from app.view.order_view import (
    OrderPlaceView,
    OrderConfirmView,
    ReservedListView,
    ApproveResultView,
    RejectResultView,
)
from app.view.monitor_view import OrderStatusView, StockStatusView
from app.view.production_view import ProductionView
from app.view.shipment_view import ShipmentListView, ShipmentResultView


# ---------------------------------------------------------------------------
# 서브메뉴 함수
# ---------------------------------------------------------------------------

def run_sample_menu(sample_ctrl: SampleController) -> None:
    """[1] 시료 관리 서브메뉴."""
    while True:
        print("\n  [시료 관리]")
        print("  [1] 시료 등록")
        print("  [2] 시료 목록")
        print("  [3] 시료 검색")
        print("  [0] 위로")
        choice = input("  선택 > ").strip()

        if choice == "1":
            # 시료 등록 화면 표시
            reg_view = SampleRegisterView()
            print(reg_view.display())

            try:
                sid = input("  시료 ID (예: S-001) > ").strip()
                name = input("  시료 이름 > ").strip()
                avg_time = float(input("  평균 생산시간 (min/ea) > ").strip())
                yield_rate = float(input("  수율 (0 < v <= 1) > ").strip())

                sample = sample_ctrl.register_sample(
                    id=sid,
                    name=name,
                    avg_production_time=avg_time,
                    yield_rate=yield_rate,
                )
                print(f"\n  시료 등록 완료: {sample.name} ({sample.id})")
            except ValueError as e:
                print(f"  오류: {e}")

        elif choice == "2":
            samples = sample_ctrl.list_samples()
            print(SampleListView(samples).display())

        elif choice == "3":
            keyword = input("  검색 키워드 > ").strip()
            results = sample_ctrl.search_samples(keyword)
            print(SampleSearchView(results, keyword).display())

        elif choice == "0":
            break
        else:
            print("  잘못된 선택입니다.")


def run_order_place(order_ctrl: OrderController, sample_ctrl: SampleController) -> None:
    """[2] 시료 주문 서브메뉴."""
    try:
        sample_id = input("  시료 ID > ").strip()
        sample = sample_ctrl.get_sample(sample_id)
        if sample is None:
            print(f"  오류: 존재하지 않는 시료 ID: {sample_id!r}")
            return

        # 주문 입력 화면 표시
        print(OrderPlaceView(sample).display())

        customer_name = input("  고객명 > ").strip()
        quantity = int(input("  주문 수량 (ea) > ").strip())
        if quantity <= 0:
            print("  오류: 주문 수량은 1 이상이어야 합니다.")
            return

        order = order_ctrl.place_order(
            sample_id=sample_id,
            customer_name=customer_name,
            quantity=quantity,
        )
        # 확인 화면 출력
        print(OrderConfirmView(order, sample).display())

    except ValueError as e:
        print(f"  오류: {e}")


def run_order_approve(
    order_ctrl: OrderController,
    prod_ctrl: ProductionController,
    sample_ctrl: SampleController,
) -> None:
    """[3] 주문 승인/거절 서브메뉴."""
    reserved_orders = order_ctrl.list_reserved()

    # 시료 딕셔너리 구성 (ReservedListView용)
    all_samples = sample_ctrl.list_samples()
    samples_map = {s.id: s for s in all_samples}

    print(ReservedListView(reserved_orders, samples_map).display())
    if not reserved_orders:
        return

    try:
        idx_str = input("  번호 선택 > ").strip()
        idx = int(idx_str) - 1
        if idx < 0 or idx >= len(reserved_orders):
            print("  오류: 유효하지 않은 번호입니다.")
            return

        order_no = reserved_orders[idx].order_no

        print("  [1] 승인  [2] 거절  [0] 취소")
        action = input("  선택 > ").strip()

        if action == "1":
            updated_order, prod_item = order_ctrl.approve_order(order_no)
            if prod_item is not None:
                prod_ctrl.enqueue(prod_item)
            print(ApproveResultView(updated_order, prod_item).display())

        elif action == "2":
            updated_order = order_ctrl.reject_order(order_no)
            print(RejectResultView(updated_order).display())

        elif action == "0":
            pass
        else:
            print("  잘못된 선택입니다.")

    except (ValueError, IndexError) as e:
        print(f"  오류: {e}")


def run_monitor(
    aggregator: MonitorAggregator,
    formatter: MonitorFormatter,
    sample_repo,
    order_repo,
) -> None:
    """[4] 모니터링 서브메뉴."""
    while True:
        print("\n  [모니터링]")
        print("  [1] 주문량 확인 (상태별)")
        print("  [2] 재고량 확인")
        print("  [0] 위로")
        choice = input("  선택 > ").strip()

        if choice == "1":
            orders = order_repo.find_all()
            status_counts = aggregator.count_by_status(orders)
            # OrderStatusView로 출력 (monitor_view 사용)
            print(OrderStatusView(status_counts).display())

        elif choice == "2":
            samples = sample_repo.find_all()
            orders = order_repo.find_all()
            stock_levels = [aggregator.stock_level(s, orders) for s in samples]
            # StockLevel.value 문자열 리스트로 변환 (StockStatusView용)
            level_strs = [lv.value for lv in stock_levels]
            print(StockStatusView(samples, level_strs).display())

        elif choice == "0":
            break
        else:
            print("  잘못된 선택입니다.")


def run_production(
    prod_ctrl: ProductionController,
    sample_ctrl: SampleController,
) -> None:
    """[5] 생산라인 조회 서브메뉴."""
    while True:
        current = prod_ctrl.get_current()
        queue = prod_ctrl.get_queue()

        # 시료 딕셔너리 구성 (ProductionView용)
        all_samples = sample_ctrl.list_samples()
        samples_map = {s.id: s for s in all_samples}

        print(ProductionView(current, queue, samples_map).display())

        print("  [C] 완료 처리  [0] 위로")
        choice = input("  선택 > ").strip().upper()

        if choice == "C":
            if current is None:
                print("  현재 처리 중인 생산 항목이 없습니다.")
                continue
            try:
                completed_order = prod_ctrl.complete_production(current.order_no)
                print(f"  생산 완료 처리: {completed_order.order_no} → CONFIRMED")
            except ValueError as e:
                print(f"  오류: {e}")

        elif choice == "0":
            break
        else:
            print("  잘못된 선택입니다.")


def run_shipment(
    order_ctrl: OrderController,
    sample_ctrl: SampleController,
) -> None:
    """[6] 출고 처리 서브메뉴."""
    from app.model.enums import OrderStatus

    all_orders = order_ctrl.list_all_orders()
    all_samples = sample_ctrl.list_samples()
    samples_map = {s.id: s for s in all_samples}

    print(ShipmentListView(all_orders, samples_map).display())

    # CONFIRMED 주문만 필터링
    confirmed_orders = [o for o in all_orders if o.status == OrderStatus.CONFIRMED]
    if not confirmed_orders:
        return

    try:
        idx_str = input("  번호 선택 > ").strip()
        idx = int(idx_str) - 1
        if idx < 0 or idx >= len(confirmed_orders):
            print("  오류: 유효하지 않은 번호입니다.")
            return

        order_no = confirmed_orders[idx].order_no
        updated_order = order_ctrl.ship_order(order_no)

        sample = samples_map.get(updated_order.sample_id)
        if sample is not None:
            print(ShipmentResultView(updated_order, sample).display())
        else:
            print(f"  출고 완료: {updated_order.order_no} → RELEASE")

    except (ValueError, IndexError) as e:
        print(f"  오류: {e}")


# ---------------------------------------------------------------------------
# 메인 진입점
# ---------------------------------------------------------------------------

def main() -> None:
    """메인 애플리케이션 진입점.

    의존성 배선:
        JsonRepository → Controller → Monitor → View
    """
    # data/ 디렉토리 자동 생성
    os.makedirs("data", exist_ok=True)

    # JSON Repository 구현체 (의존성 주입)
    sample_repo = JsonSampleRepository("data/samples.json")
    order_repo = JsonOrderRepository("data/orders.json")

    # Controller 생성 (Repository 주입)
    sample_ctrl = SampleController(sample_repo)
    order_ctrl = OrderController(order_repo, sample_repo)
    prod_ctrl = ProductionController(order_repo, sample_repo)

    # Monitor
    aggregator = MonitorAggregator()
    formatter = MonitorFormatter()

    while True:
        # 시스템 현황 계산
        samples = sample_repo.find_all()
        orders = order_repo.find_all()
        sample_count = len(samples)
        total_stock = sum(s.stock for s in samples)
        order_count = len(orders)
        prod_count = aggregator.production_count(orders)

        # 메인 뷰 표시
        view = MainView(sample_count, total_stock, order_count, prod_count)
        print(view.display())

        choice = input("선택 > ").strip()

        if choice == "1":
            run_sample_menu(sample_ctrl)
        elif choice == "2":
            run_order_place(order_ctrl, sample_ctrl)
        elif choice == "3":
            run_order_approve(order_ctrl, prod_ctrl, sample_ctrl)
        elif choice == "4":
            run_monitor(aggregator, formatter, sample_repo, order_repo)
        elif choice == "5":
            run_production(prod_ctrl, sample_ctrl)
        elif choice == "6":
            run_shipment(order_ctrl, sample_ctrl)
        elif choice == "0":
            print("시스템을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")


if __name__ == "__main__":
    main()

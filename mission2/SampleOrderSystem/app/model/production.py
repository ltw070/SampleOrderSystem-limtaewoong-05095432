"""ProductionItem domain model."""
import math
from dataclasses import dataclass, field
from .validators import validate_positive_int, validate_yield_rate, validate_positive_float

# 수율 보정 계수: 실제 생산 수율은 이론 수율의 90%로 가정
YIELD_CORRECTION_FACTOR = 0.9


@dataclass
class ProductionItem:
    order_no: str
    sample_id: str
    shortage: int          # units short = order quantity - stock (must be > 0)
    yield_rate: float      # from Sample, range: (0, 1]
    avg_production_time: float  # from Sample, unit: min/ea, must be positive
    actual_qty: int = field(init=False)
    total_time: float = field(init=False)

    def __post_init__(self):
        validate_positive_int(self.shortage, "shortage")
        validate_yield_rate(self.yield_rate)
        validate_positive_float(self.avg_production_time, "avg_production_time")
        self.actual_qty = math.ceil(self.shortage / (self.yield_rate * YIELD_CORRECTION_FACTOR))
        self.total_time = self.avg_production_time * self.actual_qty

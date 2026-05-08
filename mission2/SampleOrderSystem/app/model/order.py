"""Order domain model."""
from dataclasses import dataclass, field
from datetime import datetime
from .enums import OrderStatus
from .validators import validate_order_no, validate_positive_int


@dataclass
class Order:
    order_no: str          # format: ORD-YYYYMMDD-XXXX
    sample_id: str         # reference to Sample.id
    customer_name: str
    quantity: int          # must be positive
    created_at: datetime
    status: OrderStatus = field(default=OrderStatus.RESERVED)

    def __post_init__(self):
        validate_order_no(self.order_no)
        validate_positive_int(self.quantity, "quantity")
        if not isinstance(self.status, OrderStatus):
            raise TypeError(
                f"status must be an OrderStatus instance, got: {type(self.status)!r}"
            )

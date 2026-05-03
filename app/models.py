from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TradingResults(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String)
    exchange_product_name: Mapped[str] = mapped_column(String)
    oil_id: Mapped[str] = mapped_column(String)
    delivery_basis_id: Mapped[str] = mapped_column(String)
    delivery_basis_name: Mapped[str] = mapped_column(String)
    delivery_type_id: Mapped[str] = mapped_column(String)
    volume: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_on: Mapped[datetime] = mapped_column(DateTime)
    updated_on: Mapped[datetime] = mapped_column(DateTime)

    def to_dict(self):
        result = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[col.name] = value
        return result


from sqlalchemy import Column, Integer, String, Float, DateTime, Time, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base

# Enum for the override type
class OverrideTypeEnum(enum.Enum):
    date_time = "date_time"
    day_time = "day_time"
    time_only = "time_only"


class SportType(Base):
    __tablename__ = "sport_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    default_pricing_60 = Column(Float)  # Default price for 60 mins
    default_pricing_90 = Column(Float)  # Default price for 90 mins
    default_pricing_120 = Column(Float)  # Default price for 120 mins

    overrides = relationship("PricingOverride", back_populates="sport_type")


class PricingOverride(Base):
    __tablename__ = "pricing_overrides"

    id = Column(Integer, primary_key=True, index=True)
    sport_type_id = Column(Integer, index=True)
    override_type = Column(Enum(OverrideTypeEnum))  # date_time, day_time, time_only
    date = Column(DateTime, nullable=True)  # Applicable on a specific date (used for date_time type)
    start_time = Column(Time)  # Start time for the override
    end_time = Column(Time)  # End time for the override
    price_change = Column(Float)  # Price change (+/-)

    sport_type = relationship("SportType", back_populates="overrides")

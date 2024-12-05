from sqlalchemy.orm import Session
from datetime import datetime, time
from app.models import SportType, PricingOverride, OverrideTypeEnum


def get_sport_price(db: Session, sport_name: str, duration: int, date: datetime, time: datetime):
    sport = db.query(SportType).filter(SportType.name == sport_name).first()

    if not sport:
        return {"error": "Sport not found"}

    # Get the default price based on duration
    base_price = None
    if duration == 60:
        base_price = sport.default_pricing_60
    elif duration == 90:
        base_price = sport.default_pricing_90
    elif duration == 120:
        base_price = sport.default_pricing_120
    else:
        return {"error": "Invalid duration"}

    applicable_override = None

    # 1. Check Date and Time override first
    applicable_override = db.query(PricingOverride).filter(
        PricingOverride.sport_type_id == sport.id,
        PricingOverride.override_type == OverrideTypeEnum.date_time,
        PricingOverride.date == date.date(),
        PricingOverride.start_time <= time.time(),
        PricingOverride.end_time >= time.time()
    ).first()

    if applicable_override:
        return {"price": base_price + applicable_override.price_change}

    # 2. Check Day and Time override
    applicable_override = db.query(PricingOverride).filter(
        PricingOverride.sport_type_id == sport.id,
        PricingOverride.override_type == OverrideTypeEnum.day_time,
        PricingOverride.start_time <= time.time(),
        PricingOverride.end_time >= time.time(),
        date.weekday() in [5, 6]  # Saturday(5) and Sunday(6)
    ).first()

    if applicable_override:
        return {"price": base_price + applicable_override.price_change}

    # 3. Check Time-only override
    applicable_override = db.query(PricingOverride).filter(
        PricingOverride.sport_type_id == sport.id,
        PricingOverride.override_type == OverrideTypeEnum.time_only,
        PricingOverride.start_time <= time.time(),
        PricingOverride.end_time >= time.time()
    ).first()

    if applicable_override:
        return {"price": base_price + applicable_override.price_change}

    # 4. Default Pricing
    return {"price": base_price}


def create_override(
    db: Session,
    sport_name: str,
    override_type: OverrideTypeEnum,
    price_change: float,
    date: datetime = None,
    start_time: time = None,
    end_time: time = None
):
    sport = db.query(SportType).filter(SportType.name == sport_name).first()

    if not sport:
        return {"error": "Sport not found"}

    new_override = PricingOverride(
        sport_type_id=sport.id,
        override_type=override_type,
        date=date,
        start_time=start_time,
        end_time=end_time,
        price_change=price_change
    )

    db.add(new_override)
    db.commit()
    db.refresh(new_override)

    return {"message": "Override created successfully"}

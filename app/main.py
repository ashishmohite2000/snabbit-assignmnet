from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, time
from typing import Optional, List, Dict

# Setup FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default pricing for sports
default_prices = {
    "badminton": {
        60: 100,  # 60 minutes -> Rs. 100
        90: 150,  # 90 minutes -> Rs. 150
        120: 190  # 120 minutes -> Rs. 190
    }
}

# Pricing rules
pricing_overrides = [
    # Weekend pricing override: Saturdays and Sundays between 12 PM - 4 PM
    {"day_of_week": [5, 6], "time_range": (time(12, 0), time(16, 0)), "price_increase": 10},
    # Specific date pricing override: 05-01-2024 between 12 PM - 4 PM decrease Rs. 10
    {"date": "2024-01-05", "time_range": (time(12, 0), time(16, 0)), "price_decrease": 10},
    # Specific date pricing override: 05-01-2024 between 4 PM - 8 PM increase Rs. 20
    {"date": "2024-01-05", "time_range": (time(16, 0), time(20, 0)), "price_increase": 20},
]

@app.get("/price/{sport_name}")
async def get_price(sport_name: str, duration: int, date: str, time: str):
    try:
        # Parse date and time
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        time_obj = datetime.strptime(time, "%H:%M:%S").time()

        # Get the base price for the requested sport and duration
        base_price = default_prices.get(sport_name, {}).get(duration, None)
        if base_price is None:
            return {"error": "Invalid sport name or duration"}

        final_price = base_price

        # Apply overrides based on pricing rules
        for override in pricing_overrides:
            # Check for specific date override
            if "date" in override and override["date"] == date:
                start_time, end_time = override["time_range"]
                if start_time <= time_obj <= end_time:
                    if "price_increase" in override:
                        final_price += override["price_increase"]
                    elif "price_decrease" in override:
                        final_price -= override["price_decrease"]

            # Check for day of week override
            elif "day_of_week" in override and date_obj.weekday() in override["day_of_week"]:
                start_time, end_time = override["time_range"]
                if start_time <= time_obj <= end_time:
                    if "price_increase" in override:
                        final_price += override["price_increase"]

        return {
            "sport_name": sport_name,
            "date": date_obj.strftime("%Y-%m-%d"),
            "time": time_obj.strftime("%H:%M:%S"),
            "duration": duration,
            "final_price": final_price,
        }

    except ValueError:
        return {"error": "Invalid date or time format"}

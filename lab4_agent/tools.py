import json
from typing import Any

from langchain_core.tools import tool


# Mock DATA - dữ liệu giả lập hệ thống du lịch
# Lưu ý: giá cả có logic (ví dụ: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
FLIGHT_DB= {
    ("Hà Nội", "Đà Nẵng"):[
        {"airline": "Vietnam Airlines", "departure": "2024-07-01T08:00:00", "arrival": "2024-07-01T10:00:00", "price": 1_000_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-01T09:00:00", "arrival": "2024-07-01T11:00:00", "price": 800_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-01T10:00:00", "arrival": "2024-07-01T12:00:00", "price": 1_200_000, "class":"business"},
        {"airline": "Vietnam Airlines", "departure": "2024-07-02T08:00:00", "arrival": "2024-07-02T10:00:00", "price": 1_500_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-02T09:00:00", "arrival": "2024-07-02T11:00:00", "price": 1_200_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-02T10:00:00", "arrival": "2024-07-02T12:00:00", "price": 1_800_000, "class":"business"}
    ],
    ("Hà Nội", "TP HCM"):[
        {"airline": "Vietnam Airlines", "departure": "2024-07-01T08:00:00", "arrival": "2024-07-01T10:00:00", "price": 1_500_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-01T09:00:00", "arrival": "2024-07-01T11:00:00", "price": 1_200_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-01T10:00:00", "arrival": "2024-07-01T12:00:00", "price": 1_800_000, "class":"business"},
        {"airline": "Vietnam Airlines", "departure": "2024-07-02T08:00:00", "arrival": "2024-07-02T10:00:00", "price": 1_500_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-02T09:00:00", "arrival": "2024-07-02T11:00:00", "price": 1_200_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-02T10:00:00", "arrival": "2024-07-02T12:00:00", "price": 1_800_000, "class":"business"}
    ],
    ("Đà Nẵng", "TP HCM"):[
        {"airline": "Vietnam Airlines", "departure": "2024-07-01T08:00:00", "arrival": "2024-07-01T10:00:00", "price": 1_500_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-01T09:00:00", "arrival": "2024-07-01T11:00:00", "price": 1_200_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-01T10:00:00", "arrival": "2024-07-01T12:00:00", "price": 1_800_000, "class":"business"},
        {"airline": "Vietnam Airlines", "departure": "2024-07-02T08:00:00", "arrival": "2024-07-02T10:00:00", "price": 1_700_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-02T09:00:00", "arrival": "2024-07-02T11:00:00", "price": 1_500_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-02T10:00:00", "arrival": "2024-07-02T12:00:00", "price": 2_200_000, "class":"business"}
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "2024-07-01T08:00:00", "arrival": "2024-07-01T10:00:00", "price": 2_000_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-01T09:00:00", "arrival": "2024-07-01T11:00:00", "price": 1_800_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-01T10:00:00", "arrival": "2024-07-01T12:00:00", "price": 3_000_000, "class":"business"},
        {"airline": "Vietnam Airlines", "departure": "2024-07-02T08:00:00", "arrival": "2024-07-02T10:00:00", "price": 2_500_000, "class":"economy"},
        {"airline": "Vietjet Air", "departure": "2024-07-02T09:00:00", "arrival": "2024-07-02T11:00:00", "price": 2_000_000, "class":"economy"},
        {"airline": "Bamboo Airways", "departure": "2024-07-02T10:00:00", "arrival": "2024-07-02T12:00:00", "price": 3_500_000, "class":"business"}
    ]
}

ITINERARY_DB = {
    "Đà Nẵng": {
        "daytime": ["Bán đảo Sơn Trà", "Biển Mỹ Khê", "Ngũ Hành Sơn"],
        "night": ["Cầu Rồng", "Chợ đêm Sơn Trà", "Sky bar ven sông Hàn"],
        "food": ["Mì Quảng", "Bánh tráng cuốn thịt heo", "Hải sản ven biển"]
    },
    "TP HCM": {
        "daytime": ["Dinh Độc Lập", "Nhà thờ Đức Bà", "Bảo tàng Chứng tích Chiến tranh"],
        "night": ["Phố đi bộ Nguyễn Huệ", "Bùi Viện", "Du thuyền sông Sài Gòn"],
        "food": ["Cơm tấm", "Hủ tiếu", "Bánh mì Sài Gòn"]
    },
    "Phú Quốc": {
        "daytime": ["Bãi Sao", "Hòn Thơm", "Làng chài Hàm Ninh"],
        "night": ["Chợ đêm Dương Đông", "Sunset Sanato", "Bar bờ biển"],
        "food": ["Gỏi cá trích", "Bún quậy", "Nhum nướng"]
    },
    "Hà Nội": {
        "daytime": ["Văn Miếu", "Hồ Gươm", "Lăng Bác"],
        "night": ["Phố Tạ Hiện", "Chợ đêm phố cổ", "Cafe rooftop"],
        "food": ["Phở", "Bún chả", "Cà phê trứng"]
    }
}


def _format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


def _json_response(success: bool, message: str, data: Any) -> str:
    return json.dumps(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        ensure_ascii=False,
    )


def _normalize_price(raw: str) -> int:
    cleaned = raw.replace(".", "").replace("đ", "").replace(",", "").strip()
    return int(cleaned)

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Khách sạn A", "price_per_night": 50_000, "rating": 4.5},
        {"name": "Khách sạn B", "price_per_night": 30_000, "rating": 4.0},
        {"name": "Khách sạn C", "price_per_night": 100_000, "rating": 5.0}
    ],
    "TP HCM": [
        {"name": "Khách sạn D", "price_per_night": 70_000, "rating": 4.2},
        {"name": "Khách sạn E", "price_per_night": 40_000, "rating": 3.8},
        {"name": "Khách sạn F", "price_per_night": 150_000, "rating": 4.8}
    ],
    "Phú Quốc": [ 
        {"name": "Khách sạn G", "price_per_night": 80_000, "rating": 4.6},
        {"name": "Khách sạn H", "price_per_night": 60_000, "rating": 4.1},
        {"name": "Khách sạn I", "price_per_night": 200_000, "rating": 5.0}
    ],
    "Hà Nội": [
        {"name": "Khách sạn J", "price_per_night": 40_000, "rating": 4.0},
        {"name": "Khách sạn K", "price_per_night": 35_000, "rating": 3.5}
    ]
}

@tool
def search_flights(
    origin: str,
    destination: str,
    date: str = "",
    seat_class: str = "",
    max_price: int = 999_999_999,
    limit: int = 5,
) -> str:
    """Tìm kiếm chuyến bay theo điểm đi/đến, có thể lọc thêm theo ngày, hạng ghế và ngân sách."""
    key = (origin, destination)
    key_reverse = (destination, origin)

    if key in FLIGHT_DB:
        flights = FLIGHT_DB[key]
    elif key_reverse in FLIGHT_DB:
        flights = FLIGHT_DB[key_reverse]
    else:
        return _json_response(
            False,
            "Không tìm thấy chuyến bay giữa hai thành phố đã chọn.",
            [],
        )

    filtered = [
        f for f in flights
        if f["price"] <= max_price
        and (not date or f["departure"].startswith(date))
        and (not seat_class or f["class"].lower() == seat_class.lower())
    ]
    filtered.sort(key=lambda x: x["price"])

    output = []
    for flight in filtered[:max(1, limit)]:
        output.append(
            {
                "airline": flight["airline"],
                "departure": flight["departure"],
                "arrival": flight["arrival"],
                "class": flight["class"],
                "price": _format_money(flight["price"]),
            }
        )

    if not output:
        return _json_response(False, "Không có chuyến bay phù hợp bộ lọc.", [])

    return _json_response(True, "Đã tìm thấy chuyến bay phù hợp.", output)


@tool
def search_hotels(
    city: str,
    max_price_per_night: int = 99_999_999,
    min_rating: float = 0.0,
    sort_by: str = "rating_desc",
    limit: int = 5,
) -> str:
    """Tìm kiếm khách sạn theo thành phố, ngân sách, điểm đánh giá và cách sắp xếp."""
    if city in HOTELS_DB:
        hotels = HOTELS_DB[city]
        filtered_hotels = [
            hotel for hotel in hotels
            if hotel["price_per_night"] <= max_price_per_night and hotel["rating"] >= min_rating
        ]

        if sort_by == "price_asc":
            filtered_hotels.sort(key=lambda x: x["price_per_night"])
        elif sort_by == "price_desc":
            filtered_hotels.sort(key=lambda x: x["price_per_night"], reverse=True)
        else:
            filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

        output = []
        for hotel in filtered_hotels[:max(1, limit)]:
            output.append(
                {
                    "name": hotel["name"],
                    "price_per_night": _format_money(hotel["price_per_night"]),
                    "rating": hotel["rating"],
                }
            )

        if not output:
            return _json_response(False, "Không có khách sạn phù hợp bộ lọc.", [])

        return _json_response(True, "Đã tìm thấy khách sạn phù hợp.", output)
    else:
        return _json_response(False, f"Không tìm thấy khách sạn trong {city}.", [])

@tool
def calculate_budget(total_budget: int, expense: str) -> str:
    """Tính ngân sách còn lại sau khi trừ chi phí. Hỗ trợ định dạng tiền như 1.200.000đ."""
    try:
        expense_amount = _normalize_price(expense)
        remaining_budget = total_budget - expense_amount
        if remaining_budget < 0:
            return _json_response(
                False,
                "Ngân sách không đủ để chi trả khoản chi này.",
                {
                    "expense": _format_money(expense_amount),
                    "total_budget": _format_money(total_budget),
                    "remaining_budget": _format_money(remaining_budget),
                },
            )

        return _json_response(
            True,
            "Đã tính ngân sách thành công.",
            {
                "expense": _format_money(expense_amount),
                "total_budget": _format_money(total_budget),
                "remaining_budget": _format_money(remaining_budget),
            },
        )
    except ValueError:
        return _json_response(False, "Chi phí không hợp lệ. Vui lòng nhập số tiền hợp lệ.", {})


@tool
def estimate_trip_cost(
    origin: str,
    destination: str,
    nights: int,
    hotel_budget_per_night: int,
    seat_class: str = "economy",
    date: str = "",
) -> str:
    """Ước tính tổng chi phí chuyến đi dựa trên vé máy bay rẻ nhất và ngân sách khách sạn/đêm."""
    if nights <= 0:
        return _json_response(False, "Số đêm phải lớn hơn 0.", {})

    key = (origin, destination)
    key_reverse = (destination, origin)
    if key in FLIGHT_DB:
        flights = FLIGHT_DB[key]
    elif key_reverse in FLIGHT_DB:
        flights = FLIGHT_DB[key_reverse]
    else:
        return _json_response(False, "Không tìm thấy dữ liệu chuyến bay để ước tính.", {})

    candidate_flights = [
        f for f in flights
        if (not seat_class or f["class"].lower() == seat_class.lower())
        and (not date or f["departure"].startswith(date))
    ]
    if not candidate_flights:
        return _json_response(False, "Không có chuyến bay phù hợp để ước tính.", {})

    flight = min(candidate_flights, key=lambda x: x["price"])
    hotel_cost = hotel_budget_per_night * nights
    total = flight["price"] + hotel_cost

    return _json_response(
        True,
        "Đã ước tính chi phí chuyến đi.",
        {
            "origin": origin,
            "destination": destination,
            "nights": nights,
            "selected_flight": {
                "airline": flight["airline"],
                "departure": flight["departure"],
                "class": flight["class"],
                "price": _format_money(flight["price"]),
            },
            "hotel_estimated_cost": _format_money(hotel_cost),
            "total_estimated_cost": _format_money(total),
        },
    )


@tool
def suggest_itinerary(city: str, days: int = 3, budget_level: str = "medium") -> str:
    """Gợi ý lịch trình ngắn ngày theo thành phố và mức ngân sách (low/medium/high)."""
    if city not in ITINERARY_DB:
        return _json_response(False, f"Chưa có dữ liệu lịch trình cho {city}.", {})

    if days <= 0:
        return _json_response(False, "Số ngày phải lớn hơn 0.", {})

    city_data = ITINERARY_DB[city]
    activity_multiplier = {"low": 1, "medium": 2, "high": 3}
    max_items = activity_multiplier.get(budget_level.lower(), 2)

    itinerary = []
    for day in range(1, days + 1):
        itinerary.append(
            {
                "day": day,
                "morning": city_data["daytime"][day % len(city_data["daytime"])],
                "afternoon": city_data["daytime"][(day + 1) % len(city_data["daytime"])],
                "evening": city_data["night"][day % len(city_data["night"])],
                "food_suggestion": city_data["food"][:max_items],
            }
        )

    return _json_response(
        True,
        "Đã tạo gợi ý lịch trình.",
        {
            "city": city,
            "days": days,
            "budget_level": budget_level,
            "itinerary": itinerary,
        },
    )


import calendar
from datetime import datetime

from core.constants import (
    NORMAL_SHIFTS,
    HOLIDAY_ROTATION,
    THAI_MONTHS
)

def get_next_month():

    today = datetime.today()

    month = today.month + 1
    year = today.year

    if month > 12:
        month = 1
        year += 1

    return year, month

def build_schedule(employees):

    year, month = get_next_month()

    days_in_month = calendar.monthrange(
        year,
        month
    )[1]

    rows = []

    for day in range(
        1,
        days_in_month + 1
    ):

        row = {
            "date": day,
            "employees": []
        }

        holiday_person = None

        for emp in employees:

            if day in emp["holidays"]:
                holiday_person = emp["id"]
                break

        for emp in employees:

            if holiday_person is None:

                shift = NORMAL_SHIFTS[
                    emp["id"]
                ]

                status = "normal"

            else:

                shift = HOLIDAY_ROTATION[
                    holiday_person
                ][emp["id"]]

                status = (
                    "holiday"
                    if shift == "หยุด"
                    else "ot"
                )

            row["employees"].append({
                "name": emp["name"],
                "shift": shift,
                "status": status
            })

        rows.append(row)

    return {
        "year": year,
        "thai_year": year + 543,
        "month": month,
        "month_name":
            THAI_MONTHS[month],
        "days": rows
    }
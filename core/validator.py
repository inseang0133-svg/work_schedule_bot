import calendar
def validate_input(employees):
    return True
def validate_employees(
    employees,
    days_in_month
):

    if len(employees) != 3:
        raise ValueError(
            "กรุณาระบุพนักงานให้ครบ 3 คน"
        )

    all_holidays = []

    for emp in employees:

        holidays = emp["holidays"]

        if len(holidays) != 4:
            raise ValueError(
                f'{emp["name"]} มีวันหยุดไม่ครบ 4 วัน'
            )

        if len(set(holidays)) != 4:
            raise ValueError(
                f'{emp["name"]} มีวันหยุดซ้ำ'
            )

        if holidays != sorted(holidays):
            raise ValueError(
                f'{emp["name"]} กรุณาเรียงวันหยุดจากน้อยไปมาก'
            )

        for day in holidays:

            if day == 1:
                raise ValueError(
                    "ไม่อนุญาตให้หยุดวันที่ 1 ของเดือน"
                )

            if day == days_in_month:
                raise ValueError(
                    "ไม่อนุญาตให้หยุดวันสุดท้ายของเดือน"
                )

            if day > days_in_month:
                raise ValueError(
                    f"พบวันที่ไม่ถูกต้อง: {day}"
                )

            all_holidays.append(day)

    duplicate_days = {
        d
        for d in all_holidays
        if all_holidays.count(d) > 1
    }

    if duplicate_days:

        day = sorted(list(
            duplicate_days
        ))[0]

        raise ValueError(
            f"พบวันหยุดซ้ำกัน\n\n"
            f"วันที่ {day} มีพนักงานหยุดมากกว่า 1 คน\n\n"
            f"กรุณาตรวจสอบข้อมูลอีกครั้ง"
        )

    return True
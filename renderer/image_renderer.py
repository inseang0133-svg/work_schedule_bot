from PIL import Image, ImageDraw, ImageFont
import calendar
import os

# ==========================
# ขนาดภาพ PNG
# ==========================
IMAGE_WIDTH = 2200


# ระยะขอบ
MARGIN_LEFT = 40
MARGIN_TOP = 40
MARGIN_RIGHT = 40
MARGIN_BOTTOM = 40

# ==========================
# ขนาดตาราง
# ==========================
NO_COL_WIDTH = 80
NAME_COL_WIDTH = 180
DAY_COL_WIDTH = 250

HEADER_HEIGHT = 60
DATE_HEIGHT = 50
EMPLOYEE_ROW_HEIGHT = 60

WEEK_BLOCK_HEIGHT = (
    HEADER_HEIGHT
    + DATE_HEIGHT
    + EMPLOYEE_ROW_HEIGHT * 3
)

# ==========================
# สี
# ==========================

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

LIGHT_BLUE = (162, 195, 228)   # กะปกติ

DARK_BLUE = (18, 80, 145)     # OT

RED = (254, 0, 0)              # หยุด

# ความหนาเส้นตาราง
INNER_BORDER_WIDTH = 2
OUTER_BORDER_WIDTH = 3
# ==========================
# ฟอนต์
# ==========================
FONT_PATH = os.path.join(
    "fonts",
    "tahomabd.ttf"
)

TITLE_FONT_SIZE = 75
HEADER_FONT_SIZE = 35
CELL_FONT_SIZE = 35

title_font = ImageFont.truetype(
    FONT_PATH,
    TITLE_FONT_SIZE
)

header_font = ImageFont.truetype(
    FONT_PATH,
    HEADER_FONT_SIZE
)

cell_font = ImageFont.truetype(
    FONT_PATH,
    CELL_FONT_SIZE
)

# ==========================
# วันภาษาไทย
# ==========================
THAI_WEEKDAYS = [
    "จันทร์",
    "อังคาร",
    "พุธ",
    "พฤหัสบดี",
    "ศุกร์",
    "เสาร์",
    "อาทิตย์"
]


def create_canvas(schedule_data):

    weeks = len(
        get_weeks(
            schedule_data["year"],
            schedule_data["month"]
        )
    )

    image_height = (
        TABLE_START_Y
        + (weeks * WEEK_BLOCK_HEIGHT)
        + ((weeks - 1) * 20)
        + 100
    )

    image = Image.new(
        "RGB",
        (
            IMAGE_WIDTH,
            image_height
        ),
        WHITE
    )

    draw = ImageDraw.Draw(image)

    return image, draw


def draw_center_text(
    draw,
    text,
    font,
    left,
    top,
    width,
    height,
    fill=BLACK
):
    """
    วาดข้อความให้อยู่กึ่งกลางช่อง
    """

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = left + (width - text_width) / 2
    y = top + (height - text_height) / 2 - 4

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )


def draw_title(
    draw,
    month_name,
    thai_year
):

    title = (
        f"ตารางการทำงาน "
        f"เดือน{month_name}{thai_year}"
    )

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    text_width = bbox[2] - bbox[0]

    x = (
        IMAGE_WIDTH - text_width
    ) / 2

    y = 20

    draw.text(
        (x, y),
        title,
        font=title_font,
        fill=BLACK
    )
import math

TABLE_START_Y = 100


def get_weeks(year, month):
    """
    คืนค่า list ของสัปดาห์
    Monday = 0
    """
    cal = calendar.Calendar(firstweekday=0)

    return cal.monthdayscalendar(year, month)


def draw_rect(draw, x1, y1, x2, y2, width=1):
    draw.rectangle(
        [x1, y1, x2, y2],
        outline=BLACK,
        width=width
    )


def draw_week_block(
    draw,
    week,
    start_x,
    start_y,
    schedule_data
):
    """
    วาด 1 บล็อกของสัปดาห์
    """

    header_y = start_y

    # ======================
    # คอลัมน์พื้นฐาน
    # ======================

    name_x = start_x + NO_COL_WIDTH

    # ----------------------
    # หัวตาราง
    # ----------------------

    draw_rect(
        draw,
        start_x,
        header_y,
        start_x + NO_COL_WIDTH,
        header_y + HEADER_HEIGHT,
        width=INNER_BORDER_WIDTH
    )

    draw_center_text(
        draw,
        "ลำดับ",
        header_font,
        start_x,
        header_y,
        NO_COL_WIDTH,
        HEADER_HEIGHT
    )

    draw_rect(
        draw,
        name_x,
        header_y,
        name_x + NAME_COL_WIDTH,
        header_y + HEADER_HEIGHT,
        width=INNER_BORDER_WIDTH
    )

    draw_center_text(
        draw,
        "รายชื่อ",
        header_font,
        name_x,
        header_y,
        NAME_COL_WIDTH,
        HEADER_HEIGHT
    )

    # วันทั้ง 7 วัน
    for i in range(7):

        day_x = (
            name_x
            + NAME_COL_WIDTH
            + (DAY_COL_WIDTH * i)
        )

        draw_rect(
            draw,
            day_x,
            header_y,
            day_x + DAY_COL_WIDTH,
            header_y + HEADER_HEIGHT,
            width=INNER_BORDER_WIDTH
        )

        draw_center_text(
            draw,
            THAI_WEEKDAYS[i],
            header_font,
            day_x,
            header_y,
            DAY_COL_WIDTH,
            HEADER_HEIGHT
        )

    # ----------------------
    # แถววันที่
    # ----------------------

    date_y = header_y + HEADER_HEIGHT

    draw_rect(
        draw,
        start_x,
        date_y,
        start_x + NO_COL_WIDTH,
        date_y + DATE_HEIGHT,
        width=INNER_BORDER_WIDTH
    )

    draw_rect(
        draw,
        name_x,
        date_y,
        name_x + NAME_COL_WIDTH,
        date_y + DATE_HEIGHT,
        width=INNER_BORDER_WIDTH
    )

    for i in range(7):

        day_x = (
            name_x
            + NAME_COL_WIDTH
            + (DAY_COL_WIDTH * i)
        )

        draw_rect(
            draw,
            day_x,
            date_y,
            day_x + DAY_COL_WIDTH,
            date_y + DATE_HEIGHT,
            width=INNER_BORDER_WIDTH
        )

        day_number = week[i]

        if day_number != 0:

            full_date = (
                f"{day_number}/"
                f"{schedule_data['month']}/"
                f"{schedule_data['year']}"
            )

            draw_center_text(
                draw,
                full_date,
                cell_font,
                day_x,
                date_y,
                DAY_COL_WIDTH,
                DATE_HEIGHT
            )

    # ----------------------
    # รายชื่อพนักงาน
    # ----------------------

    employees = []

    first_day = schedule_data["days"][0]

    for index, emp in enumerate(
        first_day["employees"],
        start=1
    ):

        employees.append(
            (
                str(index),
                emp["name"]
            )
        )

    # ----------------------
    # 3 แถวพนักงาน
    # ----------------------

    for row_index, employee in enumerate(employees):

        row_y = (
            date_y
            + DATE_HEIGHT
            + (EMPLOYEE_ROW_HEIGHT * row_index)
        )

        emp_no, emp_name = employee

        # ลำดับ
        draw_rect(
            draw,
            start_x,
            row_y,
            start_x + NO_COL_WIDTH,
            row_y + EMPLOYEE_ROW_HEIGHT,
            width=INNER_BORDER_WIDTH
        )

        draw_center_text(
            draw,
            emp_no,
            cell_font,
            start_x,
            row_y,
            NO_COL_WIDTH,
            EMPLOYEE_ROW_HEIGHT
        )

        # รายชื่อ
        draw_rect(
            draw,
            name_x,
            row_y,
            name_x + NAME_COL_WIDTH,
            row_y + EMPLOYEE_ROW_HEIGHT,
            width=INNER_BORDER_WIDTH
        )

        draw_center_text(
            draw,
            emp_name,
            cell_font,
            name_x,
            row_y,
            NAME_COL_WIDTH,
            EMPLOYEE_ROW_HEIGHT
        )

        # ช่องวันทั้ง 7
        for i in range(7):

            day_x = (
                name_x
                + NAME_COL_WIDTH
                + (DAY_COL_WIDTH * i)
            )

            day_number = week[i]

            # ช่องว่างปลายเดือน
            if day_number == 0:

                draw.rectangle(
                    [
                        day_x,
                        row_y,
                        day_x + DAY_COL_WIDTH,
                        row_y + EMPLOYEE_ROW_HEIGHT
                    ],
                    fill=WHITE,
                    outline=BLACK,
                    width=INNER_BORDER_WIDTH
                )

                continue

            day_schedule = get_day_schedule(
                schedule_data,
                day_number
            )

            employee_schedule = (
                day_schedule["employees"][row_index]
            )

            draw_shift_cell(
                draw,
                day_x,
                row_y,
                DAY_COL_WIDTH,
                EMPLOYEE_ROW_HEIGHT,
                employee_schedule["shift"],
                employee_schedule["status"]
            )

    # ======================
    # กรอบนอกของสัปดาห์
    # ======================

    block_width = (
        NO_COL_WIDTH
        + NAME_COL_WIDTH
        + (DAY_COL_WIDTH * 7)
    )

    draw.rectangle(
        [
            start_x,
            start_y,
            start_x + block_width,
            start_y + WEEK_BLOCK_HEIGHT
        ],
        outline=BLACK,
        width=OUTER_BORDER_WIDTH
    )

def draw_month_layout(
    image,
    draw,
    schedule_data
):

    draw_title(
        draw,
        schedule_data["month_name"],
        schedule_data["thai_year"]
    )

    weeks = get_weeks(
        schedule_data["year"],
        schedule_data["month"]
    )

    start_x = MARGIN_LEFT

    current_y = TABLE_START_Y

    for week in weeks:

        draw_week_block(
            draw,
            week,
            start_x,
            current_y,
            schedule_data
        )

        current_y += (
            WEEK_BLOCK_HEIGHT
            + 20
        )

    return image
def draw_shift_cell(
    draw,
    x,
    y,
    width,
    height,
    shift,
    status
):

    if status == "holiday":
        fill = RED

    elif status == "ot":
        fill = DARK_BLUE

    else:
        fill = LIGHT_BLUE

    draw.rectangle(
        [
            x,
            y,
            x + width,
            y + height
        ],
        fill=fill,
        outline=BLACK,
        width=INNER_BORDER_WIDTH
    )

    draw_center_text(
        draw,
        shift,
        cell_font,
        x,
        y,
        width,
        height,
        fill=BLACK
    )
def get_day_schedule(
    schedule_data,
    day_number
):

    for day in schedule_data["days"]:

        if day["date"] == day_number:
            return day

    return None
import re

def parse_input(text: str):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    employees = []

    pattern = r"(\d+)\.(.+?)\s+([\d/]+)"

    for line in lines:

        match = re.match(pattern, line)

        if not match:
            raise ValueError(
                f"รูปแบบไม่ถูกต้อง: {line}"
            )

        employee_no = int(match.group(1))
        employee_name = match.group(2).strip()

        holidays = [
            int(x)
            for x in match.group(3).split("/")
        ]

        employees.append({
            "id": employee_no,
            "name": employee_name,
            "holidays": holidays
        })

    return employees
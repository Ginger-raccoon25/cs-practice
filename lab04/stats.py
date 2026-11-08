def parse_record(line: str) -> dict:
    """Строка «город;температура;дата» -> словарь. Негодная строка -> ValueError."""
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError(f"ожидались три поля через точку с запятой, получено {len(parts)}")

    city, temp, date = parts
    if not city.strip():
        raise ValueError("пустой город")
    if not date.strip():
        raise ValueError("пустая дата")

    try:
        temperature = float(temp)
    except ValueError:
        raise ValueError(f"температура не число: {temp!r}")

    return {"city": city.strip(), "temp": temperature, "date": date.strip()}


def read_valid(lines) -> list:
    """Разбирает строки журнала, пропуская пустые и негодные."""
    records = []
    for line in lines:
        if not line.strip():          # пустые строки — молча
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            continue                  # негодные — пропускаем, не роняем программу
    return records


def average_by_city(records: list) -> dict:
    """Средняя температура по каждому городу, округлённая до десятых."""
    total = {}
    count = {}
    for record in records:
        city = record["city"]
        total[city] = total.get(city, 0.0) + record["temp"]
        count[city] = count.get(city, 0) + 1
    return {city: round(total[city] / count[city], 1) for city in total}


def warmest_city(records: list) -> str:
    """Город с наибольшей средней температурой. При равенстве — первый по алфавиту."""
    averages = average_by_city(records)
    best = ""
    for city in sorted(averages):     # алфавитный порядок: при равенстве остаётся первый
        if best == "" or averages[city] > averages[best]:
            best = city
    return best


if __name__ == "__main__":
    # Мини-проверка: файл работает и сам по себе
    sample = [
        "Азов;24.5;2026-07-01",
        "мусор",
        "Азов;25.5;2026-07-02",
        "Таганрог;30;2026-07-01",
    ]
    records = read_valid(sample)
    assert parse_record("Азов;24.5;2026-07-01") == {
        "city": "Азов", "temp": 24.5, "date": "2026-07-01",
    }
    for bad in ("", "мусор", "Азов;н/д;2026-07-01", "А;Б;В;Г", "Азов;;2026-07-01"):
        try:
            parse_record(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"должна быть ValueError: {bad!r}")
    assert warmest_city(records) == "Таганрог"
    print("ok")

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def parse_event(line: str) -> dict:
    """Строка журнала -> словарь. Негодная строка -> ValueError."""
    parts = line.strip().split(" ", 2)  # не больше трёх частей
    if len(parts) != 3:
        raise ValueError("негодная строка: нет трёх частей")
    time, level, message = parts
    if level not in LEVELS or not message:
        raise ValueError("негодная строка: незнакомый или пустой уровень")
    return {"time": time, "level": level, "message": message}


def count_levels(lines) -> dict:
    counts = {}
    for line in lines:
        if not line.strip():          # пустые строки пропускаем
            continue
        try:
            event = parse_event(line)
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
        else:
            counts[event["level"]] = counts.get(event["level"], 0) + 1
    return counts


def top_errors(lines, n: int) -> list:
    counter = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue
        if event["level"] == "ERROR":
            counter[event["message"]] = counter.get(event["message"], 0) + 1
    ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return [[msg, cnt] for msg, cnt in ordered[:n]]


def format_report(counts: dict, errors: list) -> str:
    out = ["Отчёт по журналу", ""]
    for level in sorted(counts):      # sorted даёт алфавитный порядок
        out.append(f"{level}: {counts[level]}")
    out.append("")
    out.append("Частые ошибки:")
    for msg, cnt in errors:
        out.append(f"- {msg} — {cnt}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sample = [
        "2026-03-01T09:03:55 ERROR Не удалось открыть файл data.csv",
        "2026-03-01T09:04:01 INFO Служба запущена",
        "битая строка без уровня",
        "2026-03-01T09:05:00 FATAL Всё пропало",
        "",
    ]
    assert parse_event(sample[0]) == {
        "time": "2026-03-01T09:03:55",
        "level": "ERROR",
        "message": "Не удалось открыть файл data.csv",
    }
    for bad in (sample[2], sample[3]):
        try:
            parse_event(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("должна быть ValueError")
    assert count_levels(sample) == {"ERROR": 1, "INFO": 1, "BROKEN": 2}
    assert top_errors(sample, 5) == [["Не удалось открыть файл data.csv", 1]]
    assert format_report(count_levels(sample), top_errors(sample, 5)).endswith("\n")
    print("ok")

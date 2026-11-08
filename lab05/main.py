import os

from logstats import count_levels, top_errors, format_report


def main():
    path = input().strip()

    # Первый проход: считаем уровни.
    with open(path, encoding="utf-8") as log:
        counts = count_levels(log)

    total = sum(counts.values())          # все непустые строки
    error_total = counts.get("ERROR", 0)
    broken = counts.get("BROKEN", 0)

    print(total)
    print(error_total)
    print(broken)

    # Второй проход: файл дешевле открыть заново, чем держать в памяти.
    with open(path, encoding="utf-8") as log:
        errors = top_errors(log, 3)

    report = format_report(counts, errors)
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "report.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(report)


if __name__ == "__main__":
    main()

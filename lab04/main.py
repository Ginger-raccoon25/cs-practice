import sys

from stats import average_by_city, read_valid, warmest_city


def main():
    lines = sys.stdin.read().splitlines()
    records = read_valid(lines)
    total_lines = len(lines)

    # пустые строки не считаются ни корректными, ни испорченными
    empty = sum(1 for line in lines if not line.strip())
    skipped = total_lines - empty - len(records)

    print(len(records))
    print(skipped)
    print(average_by_city(records)[warmest_city(records)])


if __name__ == "__main__":
    main()

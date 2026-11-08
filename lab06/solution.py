def count_by_extension(paths: list[str]) -> dict[str, int]:
    counts = {}
    for p in paths:
        name = p.split("/")[-1]
        if "." in name:
            ext = name.rsplit(".", 1)[1].lower()
        else:
            ext = ""
        counts[ext] = counts.get(ext, 0) + 1
    return counts

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return min(paths, key=lambda p: (-p.count("/"), p))


def human_size(n_bytes: int) -> str:
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    for unit in units:
        if n_bytes < 1024 or unit == units[-1]:
            if unit == "Б":
                return f"{int(n_bytes)} {unit}"
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024


if __name__ == "__main__":
    paths = ["docs/report.PDF", "notes.txt", "docs/img/logo.png", "Makefile"]
    assert count_by_extension(paths) == {"pdf": 1, "txt": 1, "png": 1, "": 1}
    assert deepest_path(paths) == "docs/img/logo.png"
    assert deepest_path([]) == ""
    assert human_size(900) == "900 Б"
    assert human_size(1536) == "1.5 КБ"
    assert human_size(5 * 1024 * 1024) == "5.0 МБ"
    print("ok")

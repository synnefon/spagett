# Improved table printer with headers and alignment
def print_table(data):
    if not data:
        print("(empty)")
        return

    def format_row(row, widths):
        return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))

    if isinstance(data, dict):
        data = [data]

    if isinstance(data[0], dict):
        headers = list(data[0].keys())
        rows = [[str(row[h]) for h in headers] for row in data]
    else:
        headers = [f"col{i+1}" for i in range(len(data[0]))]
        rows = [list(map(str, item)) for item in data]

    widths = [
        max(len(str(h)), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)
    ]
    print()
    print(format_row(headers, widths))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(format_row(row, widths))
    print()

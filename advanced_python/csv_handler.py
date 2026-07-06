import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "interns.csv"
FIELDNAMES = ["intern_id", "name", "email", "domain", "duration"]


def ensure_csv(path=DEFAULT_CSV_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_record(record, path=DEFAULT_CSV_PATH):
    ensure_csv(path)
    with Path(path).open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(record)


def search_record(intern_id, path=DEFAULT_CSV_PATH):
    ensure_csv(path)
    with Path(path).open("r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["intern_id"] == intern_id:
                return row
    return None


def delete_record(intern_id, path=DEFAULT_CSV_PATH):
    ensure_csv(path)
    path = Path(path)
    with path.open("r", newline="") as file:
        rows = list(csv.DictReader(file))

    updated_rows = [row for row in rows if row["intern_id"] != intern_id]

    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated_rows)

    return len(updated_rows) != len(rows)

import os
import pandas as pd
from datetime import datetime

PATH = "data/rejections.csv"
BACKUP_DIR = "data/backups"


def _ensure_dirs():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def load_data():
    _ensure_dirs()
    if os.path.exists(PATH):
        df = pd.read_csv(PATH)
        if "ID" not in df.columns:
            df.insert(0, "ID", range(1, len(df) + 1))
        # Ensure Date column exists
        if "Date" in df.columns:
            try:
                df["Date"] = pd.to_datetime(df["Date"])
            except Exception:
                pass
        return df

    # empty dataframe schema
    return pd.DataFrame(
        columns=[
            "ID",
            "Product",
            "Age Group",
            "City",
            "Salesperson",
            "Reason",
            "Comments",
            "Date",
        ]
    )


def save_data(df):
    _ensure_dirs()
    # keep ID as first column
    cols = df.columns.tolist()
    if cols[0] != "ID" and "ID" in cols:
        cols.insert(0, cols.pop(cols.index("ID")))
    df.to_csv(PATH, index=False, columns=cols)


def generate_id(df):
    if df.empty:
        return 1
    if "ID" not in df.columns:
        return len(df) + 1
    try:
        return int(df["ID"].max()) + 1
    except Exception:
        return len(df) + 1


def detect_duplicates(df, record):
    # Simple duplicate detection: same Product, City, Salesperson, Reason, and similar Comments
    if df.empty:
        return pd.DataFrame()

    subset = ["Product", "City", "Salesperson", "Reason"]
    for k in subset:
        if k not in df.columns:
            return pd.DataFrame()

    mask = True
    for k in subset:
        mask = mask & (df[k].astype(str).str.lower() == str(record.get(k, "")).lower())

    candidates = df[mask]
    # fuzzy comments check: exact match or substring
    if len(candidates) > 0 and record.get("Comments"):
        candidates = candidates[candidates["Comments"].astype(str).str.contains(str(record.get("Comments", "")).strip(), case=False, na=False)]

    return candidates


def add_record(record, force=False):
    df = load_data()
    dups = detect_duplicates(df, record)
    if len(dups) > 0 and not force:
        return df, False, dups

    record_copy = record.copy()
    record_copy["Date"] = record_copy.get("Date") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_copy["ID"] = generate_id(df)
    new_df = pd.DataFrame([record_copy])
    df = pd.concat([df, new_df], ignore_index=True, sort=False)
    save_data(df)
    return df, True, None


def edit_record(record_id, updates):
    df = load_data()
    if "ID" not in df.columns:
        return df, False
    idx = df.index[df["ID"] == record_id]
    if len(idx) == 0:
        return df, False
    i = idx[0]
    for k, v in updates.items():
        if k in df.columns:
            df.at[i, k] = v
    save_data(df)
    return df, True


def delete_record(record_id):
    df = load_data()
    if "ID" not in df.columns:
        return df, False
    new_df = df[df["ID"] != record_id]
    if len(new_df) == len(df):
        return df, False
    save_data(new_df)
    return new_df, True


def backup_csv():
    _ensure_dirs()
    if not os.path.exists(PATH):
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(BACKUP_DIR, f"rejections_backup_{ts}.csv")
    with open(PATH, "rb") as r, open(dst, "wb") as w:
        w.write(r.read())
    return dst


def list_backups():
    _ensure_dirs()
    files = []
    for f in sorted(os.listdir(BACKUP_DIR), reverse=True):
        if f.endswith(".csv"):
            files.append(os.path.join(BACKUP_DIR, f))
    return files


def restore_backup(path_to_backup):
    _ensure_dirs()
    if not os.path.exists(path_to_backup):
        return False
    with open(path_to_backup, "rb") as r, open(PATH, "wb") as w:
        w.write(r.read())
    return True


def upload_csv_file(filelike, merge=True):
    # filelike: UploadedFile
    try:
        df_new = pd.read_csv(filelike)
    except Exception:
        return None, "invalid_csv"

    expected = ["Product", "Age Group", "City", "Salesperson", "Reason", "Comments"]
    # add Date/ID if missing
    for c in expected:
        if c not in df_new.columns:
            return None, "missing_columns"

    df_existing = load_data()
    # assign IDs to new rows
    start = generate_id(df_existing)
    df_new = df_new.copy()
    df_new["ID"] = range(start, start + len(df_new))
    if "Date" not in df_new.columns:
        df_new["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if merge:
        merged = pd.concat([df_existing, df_new], ignore_index=True, sort=False)
        save_data(merged)
        return merged, None

    save_data(df_new)
    return df_new, None

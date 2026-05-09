"""
Model (CSV): đọc/ghi dữ liệu điểm sinh viên bằng pandas.
Thống kê tính bằng numpy (vector hoá) + pandas (groupby).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLS = [
    "student_id",
    "full_name",
    "gender",
    "age",
    "course_code",
    "score",
    "credits",
    "notes",
]


class CsvModel:
    def __init__(self, csv_path: Path) -> None:
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists():
            self._write_df(self._empty_df())

    def _empty_df(self) -> pd.DataFrame:
        return pd.DataFrame({c: pd.Series(dtype="object") for c in REQUIRED_COLS})

    def _read_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path, encoding="utf-8-sig")
        for c in REQUIRED_COLS:
            if c not in df.columns:
                df[c] = "" if c != "age" else np.nan
        df = df[REQUIRED_COLS].copy()

        # Chuẩn hoá kiểu dữ liệu
        df["score"] = pd.to_numeric(df["score"], errors="coerce")
        df["credits"] = pd.to_numeric(df["credits"], errors="coerce")
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["gender"] = df["gender"].fillna("").astype(str)
        df["notes"] = df["notes"].fillna("").astype(str)
        df["student_id"] = df["student_id"].fillna("").astype(str)
        df["full_name"] = df["full_name"].fillna("").astype(str)
        df["course_code"] = df["course_code"].fillna("").astype(str)
        return df

    def _write_df(self, df: pd.DataFrame) -> None:
        df.to_csv(self.csv_path, index=False, encoding="utf-8-sig")

    # --- CRUD (mỗi dòng = 1 môn của 1 SV) ---
    def list_rows(self) -> list[dict]:
        df = self._read_df()
        df = df.reset_index(drop=True)
        df.insert(0, "row_id", df.index + 1)  # ID hiển thị 1..N
        return df.to_dict(orient="records")

    def add_row(self, row: dict) -> None:
        df = self._read_df()
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self._write_df(df[REQUIRED_COLS])

    def update_row(self, row_id: int, new_row: dict) -> None:
        df = self._read_df().reset_index(drop=True)
        idx = row_id - 1
        if idx < 0 or idx >= len(df):
            raise ValueError("Row ID không tồn tại.")
        for k in REQUIRED_COLS:
            df.at[idx, k] = new_row.get(k, df.at[idx, k])
        self._write_df(df[REQUIRED_COLS])

    def delete_rows(self, row_ids: list[int]) -> None:
        if not row_ids:
            return
        df = self._read_df().reset_index(drop=True)
        idxs = sorted({rid - 1 for rid in row_ids if rid > 0})
        mask = np.ones(len(df), dtype=bool)
        for i in idxs:
            if 0 <= i < len(df):
                mask[i] = False
        df2 = df.loc[mask].copy()
        self._write_df(df2[REQUIRED_COLS])

    # --- Import/Export ---
    def import_csv(self, other_csv: Path) -> int:
        other = pd.read_csv(other_csv, encoding="utf-8-sig")
        for c in REQUIRED_COLS:
            if c not in other.columns:
                other[c] = "" if c != "age" else np.nan
        other = other[REQUIRED_COLS].copy()
        df = self._read_df()
        df = pd.concat([df, other], ignore_index=True)
        self._write_df(df[REQUIRED_COLS])
        return len(other)

    def export_csv(self, out_csv: Path) -> None:
        df = self._read_df()
        df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    # --- Thống kê (NumPy + Pandas) ---
    def statistics(self) -> dict:
        df = self._read_df()
        if df.empty:
            return {
                "rows": 0,
                "students": 0,
                "mean_score": None,
                "mean_gpa": None,
                "gender": {},
                "notes_rows": 0,
                "total_credits": 0.0,
            }

        # Điểm trung bình tất cả dòng
        mean_score = float(np.nanmean(df["score"].to_numpy(dtype=np.float64)))
        total_credits = float(np.nansum(df["credits"].to_numpy(dtype=np.float64)))
        notes_rows = int(df["notes"].astype(str).str.strip().ne("").sum())

        # GPA theo SV: sum(score*credits)/sum(credits)
        gpas: list[float] = []
        for _, g in df.groupby("student_id"):
            sc = g["score"].to_numpy(dtype=np.float64)
            cr = g["credits"].to_numpy(dtype=np.float64)
            denom = np.nansum(cr)
            gpa = float(np.nansum(sc * cr) / denom) if denom > 0 else np.nan
            gpas.append(gpa)
        mean_gpa = float(np.nanmean(np.array(gpas))) if gpas else None

        students = int(df["student_id"].nunique())

        # Giới tính: lấy theo SV (dòng đầu tiên)
        gdf = df.copy()
        gdf["gender"] = gdf["gender"].fillna("").astype(str).replace("", "Chưa nhập")
        gdf = gdf.drop_duplicates("student_id")
        gender = gdf["gender"].value_counts().to_dict()

        return {
            "rows": int(len(df)),
            "students": students,
            "mean_score": mean_score,
            "mean_gpa": mean_gpa,
            "gender": gender,
            "notes_rows": notes_rows,
            "total_credits": total_credits,
        }


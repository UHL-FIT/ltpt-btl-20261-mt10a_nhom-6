"""
Controller (Python cơ bản): nối Model CSV ↔ View Tkinter.
"""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

from student_app_basic import __author__, __release_date__, __version__
from student_app_basic.model_csv import CsvModel
from student_app_basic.validators import validate_row
from student_app_basic.views_tk import AboutDialog, AnalysisDialog, MainView, AddDialog, EditDialog


class BasicController:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)
        self.csv_path = self.base_dir / "data" / "grades.csv"
        self.model = CsvModel(self.csv_path)

        self.view = MainView()
        self._wire()

    def _wire(self) -> None:
        self.view.on_add = self.add
        self.view.on_edit = self.edit
        self.view.on_delete = self.delete
        self.view.on_import = self.import_csv
        self.view.on_export = self.export_csv
        self.view.on_about = self.about
        self.view.on_search   = self.search
        self.view.on_reset    = self.reset
        self.view.on_analysis = self.show_analysis

    def run(self) -> None:
        self.refresh()
        self.view.mainloop()

    def refresh(self) -> None:
        rows = self.model.list_rows()
        self.view.populate(rows)
        self._update_stats()

    def _update_stats(self) -> None:
        s = self.model.statistics()
        gender = s.get("gender") or {}
        gender_text = ", ".join([f"{k}: {v}" for k, v in gender.items()]) if gender else "—"
        mean_score = s.get("mean_score")
        mean_gpa = s.get("mean_gpa")

        parts = [
            f"Số bản ghi: {s.get('rows', 0)}",
            f"Sĩ số: {s.get('students', 0)}",
            f"Điểm TB: {mean_score:.4f}" if mean_score is not None else "Điểm TB: —",
            f"GPA TB (trọng số TC): {mean_gpa:.4f}" if mean_gpa is not None else "GPA TB: —",
            f"Tổng TC: {s.get('total_credits', 0.0):.1f}",
            f"Giới tính: {gender_text}",
            f"Dòng có ghi chú: {s.get('notes_rows', 0)}",
        ]
        self.view.set_stats_text(" | ".join(parts))

    # --- CRUD ---
    def add(self) -> None:
        dlg = AddDialog(self.view)
        self.view.wait_window(dlg)
        if not dlg.result:
            return
        ok, msg, cleaned = validate_row(dlg.result)
        if not ok or cleaned is None:
            messagebox.showwarning("Dữ liệu không hợp lệ", msg, parent=self.view)
            return
        self.model.add_row(cleaned)
        self.refresh()

    def edit(self) -> None:
        ids = self.view.selected_ids()
        if not ids:
            messagebox.showwarning("Chưa chọn", "Mời bạn chọn 1 dòng để sửa.", parent=self.view)
            return
        if len(ids) > 1:
            messagebox.showwarning("Chọn quá nhiều", "Chỉ được chọn 1 dòng để sửa.", parent=self.view)
            return

        row_id = ids[0]
        rows = self.model.list_rows()
        current = next((r for r in rows if int(r["row_id"]) == row_id), None)
        if not current:
            messagebox.showerror("Lỗi", "Không tìm thấy dòng dữ liệu.", parent=self.view)
            return

        dlg = EditDialog(self.view, initial=current)
        self.view.wait_window(dlg)
        if not dlg.result:
            return
        ok, msg, cleaned = validate_row(dlg.result)
        if not ok or cleaned is None:
            messagebox.showwarning("Dữ liệu không hợp lệ", msg, parent=self.view)
            return
        self.model.update_row(row_id, cleaned)
        self.refresh()

    def delete(self) -> None:
        ids = self.view.selected_ids()
        if not ids:
            messagebox.showwarning("Chưa chọn", "Mời bạn chọn dòng để xoá.", parent=self.view)
            return
        if not messagebox.askyesno("Xác nhận", f"Xoá {len(ids)} dòng đã chọn?", parent=self.view):
            return
        self.model.delete_rows(ids)
        self.refresh()

    # --- CSV ---
    def import_csv(self) -> None:
        path = filedialog.askopenfilename(
            parent=self.view,
            title="Chọn file CSV để import",
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return
        try:
            n = self.model.import_csv(Path(path))
            self.refresh()
            messagebox.showinfo("Import", f"Đã import {n} dòng.", parent=self.view)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Lỗi import", str(e), parent=self.view)

    def export_csv(self) -> None:
        path = filedialog.asksaveasfilename(
            parent=self.view,
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return
        try:
            self.model.export_csv(Path(path))
            messagebox.showinfo("Export", f"Đã ghi file:\n{path}", parent=self.view)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Lỗi export", str(e), parent=self.view)

    # --- Search ---
    def search(self) -> None:
        q = (self.view.search_var.get() or "").strip().lower()
        rows = self.model.list_rows()
        if not q:
            self.view.populate(rows)
            return

        def match(r: dict) -> bool:
            blob = " ".join(
                str(r.get(k, "") or "")
                for k in ("student_id", "full_name", "gender", "course_code", "notes")
            ).lower()
            return q in blob

        filtered = [r for r in rows if match(r)]
        self.view.populate(filtered)

    def reset(self) -> None:
        self.view.search_var.set("")
        self.refresh()

    def about(self) -> None:
        AboutDialog(self.view, __version__, __author__, __release_date__)

    # --- Analysis ---
    def show_analysis(self) -> None:
        """Tính GPA có trọng số bằng numpy/pandas và mở AnalysisDialog."""
        import numpy as np
        import pandas as pd

        df = self.model._read_df()
        if df.empty:
            from tkinter import messagebox
            messagebox.showinfo("Phân tích", "Chưa có dữ liệu để phân tích.", parent=self.view)
            return

        # ─ Tính GPA từng SV bằng pandas vector hóa và numpy select ─
        # Tính tích score * credits cho mỗi dòng
        df["score_x_credits"] = df["score"].astype(float) * df["credits"].astype(float)
        
        # Nhóm theo sinh viên để tính tổng tín chỉ và tổng điểm
        grouped = df.groupby(["student_id", "full_name"], as_index=False).agg(
            total_credits=("credits", "sum"),
            total_score_x_credits=("score_x_credits", "sum")
        )
        
        # Lọc những sinh viên có tín chỉ > 0 để tránh chia cho 0
        grouped = grouped[grouped["total_credits"] > 0].copy()
        
        if grouped.empty:
            from tkinter import messagebox
            messagebox.showinfo("Phân tích", "Không tính được GPA (thiếu dữ liệu tín chỉ).", parent=self.view)
            return
            
        # Tính GPA
        grouped["gpa"] = grouped["total_score_x_credits"] / grouped["total_credits"]
        
        # Xếp loại bằng np.select theo yêu cầu
        conds = [
            grouped["gpa"] >= 9.0,
            grouped["gpa"] >= 8.0,
            grouped["gpa"] >= 6.5,
            grouped["gpa"] >= 5.0
        ]
        choices = ["Xuất sắc", "Giỏi", "Khá", "Trung bình"]
        grouped["rank"] = np.select(conds, choices, default="Yếu")
        
        # Sắp xếp để có Top 10
        grouped = grouped.sort_values("gpa", ascending=False)
        
        students_out = grouped[["student_id", "full_name", "gpa", "rank"]].to_dict(orient="records")

        gpa_arr = grouped["gpa"].to_numpy()
        stats = {
            "mean_gpa": float(np.mean(gpa_arr)),
            "max_gpa":  float(np.max(gpa_arr)),
            "min_gpa":  float(np.min(gpa_arr)),
            "std_gpa":  float(np.std(gpa_arr)),
        }

        # Phân bố
        dist = grouped["rank"].value_counts().to_dict()

        # Top 10
        top10 = students_out[:10]

        analysis_data = {
            "students": students_out,
            "stats":    stats,
            "dist":     dist,
            "top10":    top10,
        }
        AnalysisDialog(self.view, analysis_data)



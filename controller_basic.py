"""
Controller (Python cơ bản): nối Model CSV ↔ View Tkinter.
"""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

from __init__ import __author__, __release_date__, __version__
from model_csv import CsvModel
from validators import validate_row
from views_tk import (
    AboutDialog, AnalysisDialog, MainView,
    AddDialog, EditDialog, TranscriptDialog
)


class BasicController:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)
        self.csv_path = self.base_dir / "data" / "grades.csv"
        self.model = CsvModel(self.csv_path)

        self.view = MainView()
        self._wire()

    def _wire(self) -> None:
        self.view.on_add        = self.add
        self.view.on_edit       = self.edit
        self.view.on_delete     = self.delete
        self.view.on_import     = self.import_csv
        self.view.on_export     = self.export_csv
        self.view.on_about      = self.about
        self.view.on_search     = self.search
        self.view.on_reset      = self.reset
        self.view.on_analysis   = self.show_analysis
        self.view.on_transcript = self.show_transcript  # Bảng điểm cá nhân

    def run(self) -> None:
        self.refresh()
        self.view.mainloop()

    def refresh(self) -> None:
        rows = self.model.list_rows()
        self.view.populate(rows)
        self._update_stats()

    def _update_stats(self) -> None:
        s = self.model.statistics()

        # BẢO VỆ: Nếu model trả về None, tự động gán s thành dict trống để app không bị sập
        if s is None:
            s = {}

        gender = s.get("gender") or {}
        gender_text = ", ".join([f"{k}: {v}" for k, v in gender.items()]) if gender else "—"
        mean_score = s.get("mean_score")
        mean_gpa = s.get("mean_gpa")

        parts = [
            f"Số bản ghi: {s.get('rows', 0)}",
            f"Sĩ số: {s.get('students', 0)}",
            f"Điểm TB: {mean_score:.4f}" if mean_score is not None and str(mean_score).lower() != 'nan' else "Điểm TB: —",
            f"GPA TB (trọng số TC): {mean_gpa:.4f}" if mean_gpa is not None and str(mean_gpa).lower() != 'nan' else "GPA TB: —",
            f"Tổng TC: {s.get('total_credits', 0.0):.1f}" if s.get('total_credits') is not None else "Tổng TC: 0.0",
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
            title="Xuất dữ liệu học tập",
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx"), ("CSV (Comma delimited)", "*.csv")],
        )
        if not path:
            return
        try:
            self.model.export_csv(Path(path))
            messagebox.showinfo("Xuất dữ liệu", f"Đã xuất dữ liệu thành công ra file:\n{path}", parent=self.view)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Lỗi xuất dữ liệu", str(e), parent=self.view)

    # --- Search ---
    def search(self) -> None:
        q = (self.view.search_var.get() or "").strip().lower()

        # Lấy giá trị bộ lọc nhanh từ giao diện
        try:
            filter_mode = self.view.filter_var.get()
        except AttributeError:
            filter_mode = "Tất cả sinh viên"

        rows = self.model.list_rows()

        # 1. Áp dụng tìm kiếm bằng từ khóa
        if q:
            def match(r: dict) -> bool:
                blob = " ".join(
                    str(r.get(k, "") or "")
                    for k in ("student_id", "full_name", "gender", "course_code", "notes")
                ).lower()
                return q in blob
            filtered = [r for r in rows if match(r)]
        else:
            filtered = rows

        # 2. Áp dụng Bộ lọc nhanh
        if filter_mode == "Xét học bổng 🏅":
            filtered = [
                r for r in filtered
                if r.get("score") and str(r["score"]).strip() != ""
                and float(str(r["score"]).replace(",", ".")) >= 8.0
            ]
        elif filter_mode == "Cảnh báo học vụ ⚠️":
            filtered = [
                r for r in filtered
                if r.get("score") and str(r["score"]).strip() != ""
                and float(str(r["score"]).replace(",", ".")) < 5.0
            ]

        self.view.populate(filtered)

    def reset(self) -> None:
        self.view.search_var.set("")
        try:
            self.view.filter_var.set("Tất cả sinh viên")
            self.view.combobox_filter.set("Tất cả sinh viên")
        except AttributeError:
            pass
        self.refresh()

    def about(self) -> None:
        AboutDialog(self.view, __version__, __author__, __release_date__)

    # --- Analysis ---
    def show_analysis(self) -> None:
        """Tính kết quả xét học bổng bằng numpy/pandas và mở AnalysisDialog."""
        import numpy as np
        import pandas as pd

        df = self.model._read_df()
        if df.empty:
            messagebox.showinfo("Phân tích", "Chưa có dữ liệu để phân tích.", parent=self.view)
            return

        df["score_num"]       = pd.to_numeric(df["score"], errors="coerce")
        df["credits_num"]     = pd.to_numeric(df["credits"], errors="coerce")
        df["score_x_credits"] = df["score_num"] * df["credits_num"]

        def get_details(group):
            total_creds = group["credits_num"].sum()
            gpa = group["score_x_credits"].sum() / total_creds if total_creds > 0 else 0.0

            diem_min = group["score_num"].min()

            if gpa >= 9 and diem_min >= 7.5:
                hoc_bong = "Đạt loại Xuất sắc"
            elif gpa >= 8 and diem_min >= 6.5:
                hoc_bong = "Đạt loại Giỏi"
            else:
                hoc_bong = "Không đạt"

            ly_do_list = []
            if gpa < 8:
                ly_do_list.append("GPA chưa đạt điều kiện")
            if pd.notna(diem_min) and diem_min < 5:
                ly_do_list.append("Có môn <5")
            ly_do = ", ".join(ly_do_list) if ly_do_list else "Đạt điều kiện"

            if pd.notna(diem_min) and diem_min < 5:
                goi_y = "Học lại môn yếu"
            elif pd.notna(diem_min) and diem_min < 7:
                goi_y = "Cố gắng cải thiện điểm"
            else:
                goi_y = "Duy trì tốt"

            text = ", ".join(
                [f"{row['course_code']}:{row['score']}" for _, row in group.iterrows()]
            )
            mon_diem_text = text[:30] + "..." if len(text) > 30 else text
            full_mon_diem = "\n".join(
                [f"{row['course_code']}: {row['score']}" for _, row in group.iterrows()]
            )

            return pd.Series({
                "gpa":          gpa,
                "rank":         hoc_bong,
                "ly_do":        ly_do,
                "goi_y":        goi_y,
                "mon_diem":     mon_diem_text,
                "full_mon_diem": full_mon_diem,
            })

        # Tương thích pandas cũ (< 2.2) và mới (>= 2.2)
        try:
            grouped = (
                df.groupby(["student_id", "full_name"])
                .apply(get_details, include_groups=False)
                .reset_index()
            )
        except TypeError:
            grouped = (
                df.groupby(["student_id", "full_name"])
                .apply(get_details)
                .reset_index()
            )

        if grouped.empty:
            messagebox.showinfo("Phân tích", "Không tính được GPA (thiếu dữ liệu).", parent=self.view)
            return

        grouped = grouped.sort_values("gpa", ascending=False)
        students_out = grouped.to_dict(orient="records")

        gpa_arr = grouped["gpa"].to_numpy()
        stats = {
            "mean_gpa": float(np.mean(gpa_arr)) if len(gpa_arr) > 0 else 0.0,
            "max_gpa":  float(np.max(gpa_arr))  if len(gpa_arr) > 0 else 0.0,
            "min_gpa":  float(np.min(gpa_arr))  if len(gpa_arr) > 0 else 0.0,
            "std_gpa":  float(np.std(gpa_arr))  if len(gpa_arr) > 0 else 0.0,
        }

        dist     = grouped["rank"].value_counts().to_dict()
        top10    = [sv for sv in students_out if sv["rank"] in ["Đạt loại Xuất sắc", "Đạt loại Giỏi"]][:10]
        pie_data = self.model.get_pie_chart_data()  # Phân loại điểm số

        analysis_data = {
            "students": students_out,
            "stats":    stats,
            "dist":     dist,
            "top10":    top10,
            "pie_data": pie_data,
        }
        AnalysisDialog(self.view, analysis_data)

    # --- Bảng điểm cá nhân ---
    def show_transcript(self) -> None:
        """Hiển thị bảng điểm cá nhân với quy đổi điểm chữ & hệ 4 cho sinh viên được chọn."""
        ids = self.view.selected_ids()
        if not ids:
            messagebox.showwarning(
                "Chưa chọn",
                "Mời bạn chọn một dòng bất kỳ của sinh viên cần xem bảng điểm.",
                parent=self.view,
            )
            return

        row_id  = ids[0]
        rows    = self.model.list_rows()
        current = next((r for r in rows if int(r["row_id"]) == row_id), None)
        if not current:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu.", parent=self.view)
            return

        student_id = current.get("student_id")
        if not student_id:
            messagebox.showwarning(
                "Lỗi", "Dòng dữ liệu này không có Mã sinh viên hợp lệ.", parent=self.view
            )
            return

        # Lọc tất cả các dòng của sinh viên này
        student_rows = [r for r in rows if r.get("student_id") == student_id]

        student_info = {
            "student_id": student_id,
            "full_name":  current.get("full_name", ""),
            "gender":     current.get("gender", ""),
            "age":        current.get("age", ""),
        }

        courses       = []
        total_credits = 0.0
        sum_score_10  = 0.0
        sum_score_4   = 0.0

        for r in student_rows:
            try:
                score = float(str(r.get("score", 0)).replace(",", "."))
            except (ValueError, TypeError):
                score = 0.0
            try:
                credits = float(str(r.get("credits", 0)).replace(",", "."))
            except (ValueError, TypeError):
                credits = 0.0

            # Quy đổi điểm chữ & điểm hệ 4
            if score >= 8.5:
                letter, score_4, status = "A",  4.0, "Đạt"
            elif score >= 7.0:
                letter, score_4, status = "B",  3.0, "Đạt"
            elif score >= 5.5:
                letter, score_4, status = "C",  2.0, "Đạt"
            elif score >= 4.0:
                letter, score_4, status = "D",  1.0, "Đạt"
            else:
                letter, score_4, status = "F",  0.0, "Không đạt"

            courses.append({
                "course_code":  r.get("course_code", ""),
                "credits":      credits,
                "score_10":     score,
                "letter_grade": letter,
                "score_4":      score_4,
                "status":       status,
            })

            total_credits += credits
            sum_score_10  += score   * credits
            sum_score_4   += score_4 * credits

        gpa_10 = (sum_score_10 / total_credits) if total_credits > 0 else 0.0
        gpa_4  = (sum_score_4  / total_credits) if total_credits > 0 else 0.0

        if   gpa_4 >= 3.6: ranking = "Xuất sắc"
        elif gpa_4 >= 3.2: ranking = "Giỏi"
        elif gpa_4 >= 2.5: ranking = "Khá"
        elif gpa_4 >= 2.0: ranking = "Trung bình"
        else:              ranking = "Yếu"

        stats = {
            "total_credits": total_credits,
            "gpa_10":        gpa_10,
            "gpa_4":         gpa_4,
            "ranking":       ranking,
        }

        TranscriptDialog(self.view, student_info, courses, stats)

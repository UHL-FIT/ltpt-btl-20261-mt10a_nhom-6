"""
View (Tkinter): Main window + Dialogs.
Cấu trúc tinh gọn, đáp ứng yêu cầu dùng messagebox để báo lỗi.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox


class MainView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bài 6 — Quản lý Kết quả Học tập (MVC + CSV)")
        self.geometry("1100x600")
        self.minsize(900, 500)
        self._setup_styles()

        # callbacks (controller gán)
        self.on_add    = lambda: None
        self.on_edit   = lambda: None
        self.on_delete = lambda: None
        self.on_import = lambda: None
        self.on_export = lambda: None
        self.on_about  = lambda: None
        self.on_search = lambda: None
        self.on_reset  = lambda: None
        self.on_analysis = lambda: None

        self.search_var = tk.StringVar()
        self._build()

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
            
        bg_color = "#f4f6f9"
        text_color = "#2b2d42"
        self.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=4)
        style.configure("Add.TButton", foreground="#2a9d8f")
        style.configure("Edit.TButton", foreground="#4361ee")
        style.configure("Del.TButton", foreground="#e63946")
        style.configure("Action.TButton", foreground="#3f37c9")
        
        style.configure("Treeview", 
                        background="#ffffff",
                        foreground=text_color,
                        rowheight=25,
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#e0e1dd", 
                        foreground="#000000")
        style.map("Treeview", background=[("selected", "#4361ee")], foreground=[("selected", "#ffffff")])

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Toolbar
        top = ttk.Frame(self, padding=10)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(1, weight=1)

        btns = ttk.Frame(top)
        btns.grid(row=0, column=0, sticky="w")
        ttk.Button(btns, text="➕ Thêm",       style="Add.TButton", command=lambda: self.on_add()).pack(side="left", padx=2)
        ttk.Button(btns, text="✏️ Sửa",         style="Edit.TButton", command=lambda: self.on_edit()).pack(side="left", padx=2)
        ttk.Button(btns, text="🗑️ Xoá",         style="Del.TButton", command=lambda: self.on_delete()).pack(side="left", padx=2)
        ttk.Button(btns, text="📂 Import CSV",  style="Action.TButton", command=lambda: self.on_import()).pack(side="left", padx=(10, 2))
        ttk.Button(btns, text="💾 Export CSV",  style="Action.TButton", command=lambda: self.on_export()).pack(side="left", padx=2)
        ttk.Button(btns, text="📊 Thống kê",   style="Action.TButton", command=lambda: self.on_analysis()).pack(side="left", padx=(10, 2))
        ttk.Button(btns, text="ℹ️ About",        command=lambda: self.on_about()).pack(side="left", padx=2)

        search = ttk.Frame(top)
        search.grid(row=0, column=1, sticky="e")
        ttk.Label(search, text="Tìm kiếm:").pack(side="left", padx=2)
        ent = ttk.Entry(search, textvariable=self.search_var, width=25)
        ent.pack(side="left", padx=2)
        ent.bind("<Return>", lambda _e: self.on_search())
        ttk.Button(search, text="🔍 Tìm", command=lambda: self.on_search()).pack(side="left", padx=2)
        ttk.Button(search, text="Tất cả", command=lambda: self.on_reset()).pack(side="left", padx=2)

        # Table
        wrap = ttk.Frame(self, padding=(10, 0, 10, 10))
        wrap.grid(row=1, column=0, sticky="nsew")
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        cols = ("row_id", "student_id", "full_name", "gender", "age", "course_code", "score", "credits", "notes")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
        
        hdrs = {"row_id": "ID", "student_id": "Mã SV", "full_name": "Họ tên", "gender": "Giới tính", 
                "age": "Tuổi", "course_code": "Môn", "score": "Điểm", "credits": "TC", "notes": "Ghi chú"}
        ws = {"row_id": 40, "student_id": 80, "full_name": 160, "gender": 70, 
              "age": 50, "course_code": 80, "score": 60, "credits": 50, "notes": 250}
        
        for c in cols:
            self.tree.heading(c, text=hdrs[c])
            self.tree.column(c, width=ws[c], anchor="center" if c not in ("full_name", "notes") else "w")

        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Stats bar
        bottom = ttk.Frame(self, padding=(10, 0, 10, 5))
        bottom.grid(row=2, column=0, sticky="ew")
        self.stats_var = tk.StringVar(value="Sẵn sàng.")
        ttk.Label(bottom, textvariable=self.stats_var).pack(side="left")

    def set_stats_text(self, text: str) -> None:
        self.stats_var.set(text)

    def populate(self, rows: list[dict]) -> None:
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", iid=str(r["row_id"]), values=(
                r.get("row_id", ""), r.get("student_id", ""), r.get("full_name", ""),
                r.get("gender", ""), "" if str(r.get("age", "")).lower() == "nan" else r.get("age", ""),
                r.get("course_code", ""), "" if r.get("score", "") == "" else f"{float(r['score']):.2f}",
                "" if r.get("credits", "") == "" else f"{float(r['credits']):.1f}", r.get("notes", "")
            ))

    def selected_ids(self) -> list[int]:
        return [int(x) for x in self.tree.selection()]


class BaseRowDialog(tk.Toplevel):
    """Sub-window cơ sở cho Thêm/Sửa (dùng chung logic form, nhưng hiện messagebox khi lỗi)."""
    def __init__(self, master: tk.Tk, title: str, initial: dict | None = None) -> None:
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.initial = initial or {}
        self.result: dict | None = None

        self.vars = {k: tk.StringVar(value=str(self.initial.get(k, ""))) for k in (
            "student_id", "full_name", "gender", "age",
            "course_code", "score", "credits", "notes"
        )}

        self._build()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _build(self) -> None:
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)

        fields = [
            ("Mã sinh viên *", "student_id"), ("Họ và tên *", "full_name"),
            ("Giới tính", "gender"), ("Tuổi", "age"),
            ("Mã môn học *", "course_code"), ("Điểm (0-10) *", "score"),
            ("Số tín chỉ *", "credits"), ("Ghi chú", "notes")
        ]

        for i, (lbl, key) in enumerate(fields):
            ttk.Label(frm, text=lbl, font=("", 9, "bold")).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            if key == "gender":
                w = ttk.Combobox(frm, textvariable=self.vars[key], values=["Nam", "Nữ"], state="readonly", width=33)
            else:
                w = ttk.Entry(frm, textvariable=self.vars[key], width=35)
            w.grid(row=i, column=1, sticky="ew", pady=5, padx=5)

        btn_frm = ttk.Frame(frm)
        btn_frm.grid(row=len(fields), column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frm, text="✔ Lưu", command=self._ok).pack(side="left", padx=5)
        ttk.Button(btn_frm, text="✖ Huỷ", command=self._cancel).pack(side="left", padx=5)

    def _ok(self) -> None:
        # Validate theo yêu cầu đề bài -> HIỂN THỊ MESSAGEBOX
        v = {k: var.get().strip() for k, var in self.vars.items()}
        
        if not v["student_id"]:
            messagebox.showwarning("Lỗi", "Mời bạn nhập mã sinh viên.", parent=self)
            return
        if not v["full_name"]:
            messagebox.showwarning("Lỗi", "Mời bạn nhập họ tên.", parent=self)
            return
        if not v["course_code"]:
            messagebox.showwarning("Lỗi", "Mời bạn nhập mã môn học.", parent=self)
            return
        if not v["score"]:
            messagebox.showwarning("Lỗi", "Mời bạn nhập điểm.", parent=self)
            return
        if not v["credits"]:
            messagebox.showwarning("Lỗi", "Mời bạn nhập số tín chỉ.", parent=self)
            return

        try:
            float(v["score"].replace(",", "."))
        except ValueError:
            messagebox.showwarning("Lỗi", "Sai kiểu dữ liệu: Điểm phải là số.", parent=self)
            return
            
        try:
            float(v["credits"].replace(",", "."))
        except ValueError:
            messagebox.showwarning("Lỗi", "Sai kiểu dữ liệu: Tín chỉ phải là số.", parent=self)
            return

        if v["age"]:
            try:
                int(float(v["age"].replace(",", ".")))
            except ValueError:
                messagebox.showwarning("Lỗi", "Mời bạn nhập lại số tuổi.", parent=self)
                return

        self.result = v
        self.destroy()

    def _cancel(self) -> None:
        self.result = None
        self.destroy()


class AddDialog(BaseRowDialog):
    """Window thứ 2: Thêm thông tin"""
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, "Thêm thông tin mới")


class EditDialog(BaseRowDialog):
    """Window thứ 3: Sửa thông tin"""
    def __init__(self, master: tk.Tk, initial: dict) -> None:
        super().__init__(master, "Sửa thông tin sinh viên", initial)


class AboutDialog(tk.Toplevel):
    """Sub-window About."""
    def __init__(self, master: tk.Tk, version: str, author: str, date: str) -> None:
        super().__init__(master)
        self.title("About")
        self.resizable(False, False)
        frm = ttk.Frame(self, padding=20)
        frm.pack()
        ttk.Label(frm, text="Phân tích kết quả học tập (Bài 6)", font=("", 12, "bold")).pack(anchor="w", pady=2)
        ttk.Label(frm, text=f"Phiên bản: {version}").pack(anchor="w", pady=2)
        ttk.Label(frm, text=f"Tác giả: {author}").pack(anchor="w", pady=2)
        ttk.Label(frm, text=f"Ngày phát hành: {date}").pack(anchor="w", pady=2)
        ttk.Button(frm, text="Đóng", command=self.destroy).pack(anchor="e", pady=(10, 0))
        self.grab_set()


class AnalysisDialog(tk.Toplevel):
    """Sub-window thứ 4: Thống kê GPA (đáp ứng >3 windows)."""
    def __init__(self, master: tk.Tk, data: dict) -> None:
        super().__init__(master)
        self.title("📊 Thống kê Phân tích Kết quả Học tập")
        self.geometry("800x500")
        self.minsize(700, 400)
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Tab 1: Top 10 ---
        tab_top10 = ttk.Frame(notebook)
        notebook.add(tab_top10, text="🏆 Top 10 Xuất sắc")
        self._build_top10_tab(tab_top10, data.get("top10", []))
        
        # --- Tab 2: Danh sách ---
        tab_all = ttk.Frame(notebook)
        notebook.add(tab_all, text="📋 Tất cả Sinh viên")
        self._build_all_tab(tab_all, data.get("students", []))
        
        # --- Tab 3: Thống kê chung ---
        tab_stats = ttk.Frame(notebook)
        notebook.add(tab_stats, text="📈 Chỉ số & Phân bố")
        self._build_stats_tab(tab_stats, data.get("stats", {}), data.get("dist", {}))

    def _build_top10_tab(self, parent: ttk.Frame, top10: list[dict]) -> None:
        cols = ("id", "name", "gpa", "rank")
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        tree.heading("id", text="Mã SV")
        tree.heading("name", text="Họ tên")
        tree.heading("gpa", text="GPA")
        tree.heading("rank", text="Xếp loại")
        
        tree.column("id", width=100, anchor="center")
        tree.column("name", width=250)
        tree.column("gpa", width=100, anchor="center")
        tree.column("rank", width=150, anchor="center")

        for i, sv in enumerate(top10):
            prefix = ""
            if i == 0: prefix = "🥇 "
            elif i == 1: prefix = "🥈 "
            elif i == 2: prefix = "🥉 "
            
            tree.insert("", "end", values=(sv["student_id"], prefix + sv["full_name"], f"{sv['gpa']:.4f}", sv["rank"]))
            
        tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
    def _build_all_tab(self, parent: ttk.Frame, students: list[dict]) -> None:
        cols = ("id", "name", "gpa", "rank")
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        tree.heading("id", text="Mã SV")
        tree.heading("name", text="Họ tên")
        tree.heading("gpa", text="GPA")
        tree.heading("rank", text="Xếp loại")
        
        tree.column("id", width=80, anchor="center")
        tree.column("name", width=200)
        tree.column("gpa", width=80, anchor="center")
        tree.column("rank", width=100, anchor="center")

        for sv in students:
            tree.insert("", "end", values=(sv["student_id"], sv["full_name"], f"{sv['gpa']:.4f}", sv["rank"]))
        
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)
        tree.pack(side="left", fill="both", expand=True, pady=5)
        vsb.pack(side="right", fill="y", pady=5)

    def _build_stats_tab(self, parent: ttk.Frame, stats: dict, dist: dict) -> None:
        frm = ttk.Frame(parent, padding=20)
        frm.pack(fill="both", expand=True)
        
        ttk.Label(frm, text="Chỉ số thống kê GPA:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))
        ttk.Label(frm, text=f"• GPA trung bình: {stats.get('mean_gpa', 0):.4f}").grid(row=1, column=0, sticky="w", padx=15, pady=2)
        ttk.Label(frm, text=f"• GPA cao nhất: {stats.get('max_gpa', 0):.4f}").grid(row=2, column=0, sticky="w", padx=15, pady=2)
        ttk.Label(frm, text=f"• GPA thấp nhất: {stats.get('min_gpa', 0):.4f}").grid(row=3, column=0, sticky="w", padx=15, pady=2)
        ttk.Label(frm, text=f"• Độ lệch chuẩn: {stats.get('std_gpa', 0):.4f}").grid(row=4, column=0, sticky="w", padx=15, pady=2)

        ttk.Label(frm, text="Phân bố xếp loại:", font=("Segoe UI", 12, "bold")).grid(row=5, column=0, sticky="w", pady=(20, 10))
        row_idx = 6
        for rank, count in dist.items():
            ttk.Label(frm, text=f"• {rank}: {count} sinh viên").grid(row=row_idx, column=0, sticky="w", padx=15, pady=2)
            row_idx += 1

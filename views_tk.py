"""
View (CustomTkinter): Main window + Dialogs.
Đã nâng cấp lên giao diện Flat Design hiện đại.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cài đặt giao diện mặc định cho CustomTkinter
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MainView(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bài 6 — Quản lý Kết quả Học tập (MVC + CSV)")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Các thuộc tính callback (controller gán)
        self.on_add    = lambda: None
        self.on_edit   = lambda: None
        self.on_delete = lambda: None
        self.on_import = lambda: None
        self.on_export = lambda: None
        self.on_about  = lambda: None
        self.on_search = lambda: None
        self.on_reset  = lambda: None
        self.on_analysis   = lambda: None
        self.on_transcript = lambda: None  # Bảng điểm cá nhân

        self.search_var = tk.StringVar()
        self.filter_var = ctk.StringVar(value="Tất cả sinh viên") # Bộ lọc nhanh
        self.stats_var = ctk.StringVar(value="Sẵn sàng.")
        
        # Cấu hình grid tổng: 1 cột sidebar (weight 0), 1 cột main frame (weight 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._setup_styles()
        self._build_sidebar()
        self._build_main()

    def _setup_styles(self) -> None:
        """Cấu hình style cho các widget ttk (như Treeview) để đồng bộ với Flat Design"""
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
            
        # Style cho Treeview
        style.configure("Treeview", 
                        background="#ffffff",
                        foreground="#0f172a",
                        rowheight=32, # Độ cao hàng 32px theo yêu cầu
                        fieldbackground="#ffffff",
                        bordercolor="#e2e8f0",
                        borderwidth=0,
                        font=("Segoe UI", 10))
        
        # Style cho tiêu đề cột Treeview phẳng nhã nhặn
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#f1f5f9", 
                        foreground="#0f172a",
                        relief="flat",
                        padding=5)
        
        style.map("Treeview", 
                  background=[("selected", "#3b82f6")], 
                  foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading",
                  background=[("active", "#e2e8f0")])

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """Sự kiện chuyển đổi chế độ Sáng/Tối"""
        ctk.set_appearance_mode(new_appearance_mode)
        
        style = ttk.Style(self)
        if new_appearance_mode == "Dark":
            style.configure("Treeview", background="#2b2b2b", foreground="#f8fafc", rowheight=32, fieldbackground="#2b2b2b", bordercolor="#3f3f46", borderwidth=0, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#3f3f46", foreground="#f8fafc", relief="flat", padding=5)
            style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
            style.map("Treeview.Heading", background=[("active", "#52525b")])
        else:
            style.configure("Treeview", background="#ffffff", foreground="#0f172a", rowheight=32, fieldbackground="#ffffff", bordercolor="#e2e8f0", borderwidth=0, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f1f5f9", foreground="#0f172a", relief="flat", padding=5)
            style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
            style.map("Treeview.Heading", background=[("active", "#e2e8f0")])

    def _build_sidebar(self) -> None:
        """Xây dựng thanh Menu điều hướng bên trái (Sidebar Frame)"""
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#0f172a")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Đẩy menu sáng/tối xuống dưới cùng

        # Tiêu đề ứng dụng
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📊 STUDENT\nANALYTICS", 
                                       font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
                                       text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))

        # Các nút điều hướng
        self.btn_ds_diem = ctk.CTkButton(self.sidebar_frame, text="📋 Danh sách điểm", 
                                         corner_radius=8, height=40,
                                         fg_color="#1e293b", hover_color="#334155",
                                         font=ctk.CTkFont("Segoe UI", 14), anchor="w")
        self.btn_ds_diem.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_do_thi = ctk.CTkButton(self.sidebar_frame, text="📈 Đồ thị phân tích", 
                                        corner_radius=8, height=40,
                                        fg_color="transparent", hover_color="#334155",
                                        font=ctk.CTkFont("Segoe UI", 14), anchor="w",
                                        command=lambda: self.on_analysis())
        self.btn_do_thi.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_about = ctk.CTkButton(self.sidebar_frame, text="ℹ️ Về phần mềm", 
                                        corner_radius=8, height=40,
                                        fg_color="transparent", hover_color="#334155",
                                        font=ctk.CTkFont("Segoe UI", 14), anchor="w",
                                        command=lambda: self.on_about())
        self.btn_about.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Menu thả xuống chọn chế độ Light/Dark Mode
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Chế độ màn hình:", text_color="#94a3b8", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                             command=self.change_appearance_mode_event,
                                                             fg_color="#1e293b", button_color=("#334155", "#e2e8f0"), button_hover_color=("#475569", "#cbd5e1"))
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="ew")

    def _build_main(self) -> None:
        """Xây dựng vùng hiển thị nội dung chính bên phải (Main Frame)"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#f8fafc", "#1e1e1e"))
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1) # Dành không gian mở rộng cho bảng
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Tiêu đề trang
        self.title_label = ctk.CTkLabel(self.main_frame, text="Quản lý Danh sách Điểm", 
                                        font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                                        text_color=("#0f172a", "#f8fafc"))
        self.title_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")

        # Khung Card màu trắng chứa Bộ lọc và Tìm kiếm
        self.filter_card = ctk.CTkFrame(self.main_frame, fg_color=("#ffffff", "#2b2b2b"), corner_radius=12, 
                                        border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        self.filter_card.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.filter_card.grid_columnconfigure(3, weight=1) # Đẩy tìm kiếm sang phải

        # Bộ lọc nhanh (Thêm theo yêu cầu)
        ctk.CTkLabel(self.filter_card, text="Bộ lọc nhanh:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=("#475569", "#cbd5e1")).grid(row=0, column=0, padx=(20, 10), pady=15)
        self.combobox_filter = ctk.CTkComboBox(self.filter_card, values=["Tất cả sinh viên", "Xét học bổng 🏅", "Cảnh báo học vụ ⚠️"],
                                               variable=self.filter_var, width=180,
                                               fg_color=("#f8fafc", "#1e1e1e"), border_color=("#cbd5e1", "#52525b"), button_color=("#e2e8f0", "#3f3f46"), button_hover_color=("#cbd5e1", "#52525b"),
                                               command=lambda _: self.on_search())
        self.combobox_filter.grid(row=0, column=1, padx=10, pady=15)
        
        # Ô nhập liệu Tìm kiếm
        self.search_entry = ctk.CTkEntry(self.filter_card, placeholder_text="Nhập từ khóa...", 
                                         textvariable=self.search_var, width=250, border_color=("#cbd5e1", "#52525b"))
        self.search_entry.grid(row=0, column=3, padx=(10, 10), pady=15, sticky="e")
        self.search_entry.bind("<Return>", lambda _e: self.on_search())
        
        # Các nút tìm kiếm
        self.btn_search = ctk.CTkButton(self.filter_card, text="🔍 Tìm", width=80, 
                                        fg_color="#3b82f6", hover_color="#2563eb", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                                        command=lambda: self.on_search())
        self.btn_search.grid(row=0, column=4, padx=5, pady=15, sticky="e")
        
        self.btn_reset = ctk.CTkButton(self.filter_card, text="🔄 Đặt lại", width=80, 
                                        fg_color=("#64748b", "#94a3b8"), hover_color="#475569", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                                        command=lambda: self.on_reset())
        self.btn_reset.grid(row=0, column=5, padx=(5, 20), pady=15, sticky="e")

        # Vùng Bảng dữ liệu và Nút thao tác
        self.table_card = ctk.CTkFrame(self.main_frame, fg_color=("#ffffff", "#2b2b2b"), corner_radius=12,
                                        border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        self.table_card.grid(row=2, column=0, padx=30, pady=(10, 10), sticky="nsew")
        self.table_card.grid_rowconfigure(1, weight=1)
        self.table_card.grid_columnconfigure(0, weight=1)

        # Các nút hành động (bo góc nhẹ 8px)
        self.action_frame = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.action_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        
        # Thêm mới (Xanh dương)
        ctk.CTkButton(self.action_frame, text="➕ Thêm mới", corner_radius=8,
                      fg_color="#3b82f6", hover_color="#2563eb", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_add()).pack(side="left", padx=(0, 10))
        # Sửa (Xám)
        ctk.CTkButton(self.action_frame, text="✏️ Sửa", corner_radius=8,
                      fg_color=("#64748b", "#94a3b8"), hover_color="#475569", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_edit()).pack(side="left", padx=10)
        # Xóa (Đỏ)
        ctk.CTkButton(self.action_frame, text="🗑️ Xóa", corner_radius=8,
                      fg_color="#ef4444", hover_color="#dc2626", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_delete()).pack(side="left", padx=10)
        # Bảng điểm cá nhân (Cam)
        ctk.CTkButton(self.action_frame, text="📜 Bảng điểm", corner_radius=8,
                      fg_color="#f97316", hover_color="#ea580c", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_transcript()).pack(side="left", padx=10)
        
        # Nhóm hành động Import / Export bên phải
        # Xuất Excel/CSV (Xanh lá)
        ctk.CTkButton(self.action_frame, text="💾 Xuất Excel/CSV", corner_radius=8,
                      fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_export()).pack(side="right", padx=(10, 0))
        # Import CSV
        ctk.CTkButton(self.action_frame, text="📂 Nhập CSV", corner_radius=8,
                      fg_color="#8b5cf6", hover_color="#7c3aed", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      command=lambda: self.on_import()).pack(side="right", padx=10)

        # Bảng Treeview
        self.tree_scroll = ttk.Scrollbar(self.table_card, orient="vertical")
        self.tree_scroll.grid(row=1, column=1, sticky="ns", padx=(0, 2), pady=2)
        
        cols = ("row_id", "student_id", "full_name", "gender", "age", "course_code", "score", "credits", "notes")
        self.tree = ttk.Treeview(self.table_card, columns=cols, show="headings", selectmode="extended")
        
        hdrs = {"row_id": "ID", "student_id": "Mã SV", "full_name": "Họ tên", "gender": "Giới tính", 
                "age": "Tuổi", "course_code": "Môn", "score": "Điểm", "credits": "TC", "notes": "Ghi chú"}
        ws = {"row_id": 40, "student_id": 80, "full_name": 160, "gender": 70, 
              "age": 50, "course_code": 80, "score": 60, "credits": 50, "notes": 250}
        
        for c in cols:
            self.tree.heading(c, text=hdrs[c])
            self.tree.column(c, width=ws[c], anchor="center" if c not in ("full_name", "notes") else "w")
            
        self.tree.configure(yscroll=self.tree_scroll.set)
        self.tree_scroll.configure(command=self.tree.yview)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        # Thanh trạng thái (Stats bar) dưới cùng
        self.stats_label = ctk.CTkLabel(self.main_frame, textvariable=self.stats_var, text_color=("#64748b", "#94a3b8"), font=ctk.CTkFont("Segoe UI", 11, slant="italic"))
        self.stats_label.grid(row=3, column=0, sticky="w", padx=30, pady=(0, 10))

    def set_stats_text(self, text: str) -> None:
        """Cập nhật thanh trạng thái"""
        self.stats_var.set(text)

    def populate(self, rows: list[dict]) -> None:
        """Đổ dữ liệu vào bảng Treeview"""
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", "end", iid=str(r["row_id"]), values=(
                r.get("row_id", ""), r.get("student_id", ""), r.get("full_name", ""),
                r.get("gender", ""), "" if str(r.get("age", "")).lower() == "nan" else r.get("age", ""),
                r.get("course_code", ""), "" if r.get("score", "") == "" else f"{float(r['score']):.2f}",
                "" if r.get("credits", "") == "" else f"{float(r['credits']):.1f}", r.get("notes", "")
            ))

    def selected_ids(self) -> list[int]:
        """Lấy danh sách ID các hàng đang chọn"""
        return [int(x) for x in self.tree.selection()]


class BaseRowDialog(ctk.CTkToplevel):
    """Sub-window cơ sở cho Thêm/Sửa bằng CustomTkinter"""
    def __init__(self, master: ctk.CTk, title: str, initial: dict | None = None) -> None:
        super().__init__(master)
        self.title(title)
        self.geometry("500x550")
        self.resizable(False, False)
        
        # Đảm bảo cửa sổ nổi lên trên cùng
        self.transient(master)
        
        self.initial = initial or {}
        self.result: dict | None = None

        self.vars = {}
        for k in ("student_id", "full_name", "gender", "age", "course_code", "score", "credits", "notes"):
            val = self.initial.get(k, "")
            if k == "age" and val is not None and str(val).lower() != "nan" and val != "":
                try:
                    val = str(int(float(val)))
                except (ValueError, TypeError):
                    pass
            self.vars[k] = ctk.StringVar(value=str(val) if val is not None else "")

        self._build()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Khung chính
        frm = ctk.CTkFrame(self, corner_radius=10, fg_color=("#ffffff", "#2b2b2b"))
        frm.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frm.grid_columnconfigure(1, weight=1)

        fields = [
            ("Mã sinh viên *", "student_id"), ("Họ và tên *", "full_name"),
            ("Giới tính", "gender"), ("Tuổi", "age"),
            ("Mã môn học *", "course_code"), ("Điểm (0-10) *", "score"),
            ("Số tín chỉ *", "credits"), ("Ghi chú", "notes")
        ]

        for i, (lbl, key) in enumerate(fields):
            ctk.CTkLabel(frm, text=lbl, font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=("#0f172a", "#f8fafc")).grid(row=i, column=0, sticky="w", pady=8, padx=15)
            if key == "gender":
                w = ctk.CTkComboBox(frm, variable=self.vars[key], values=["Nam", "Nữ"], state="readonly", width=250,
                                    border_color=("#cbd5e1", "#52525b"), button_color=("#e2e8f0", "#3f3f46"))
            else:
                w = ctk.CTkEntry(frm, textvariable=self.vars[key], width=250, border_color=("#cbd5e1", "#52525b"))
            w.grid(row=i, column=1, sticky="ew", pady=8, padx=15)

        btn_frm = ctk.CTkFrame(frm, fg_color="transparent")
        btn_frm.grid(row=len(fields), column=0, columnspan=2, pady=(20, 10))
        
        ctk.CTkButton(btn_frm, text="✔ Lưu", command=self._ok, fg_color="#3b82f6", hover_color="#2563eb", font=ctk.CTkFont("Segoe UI", 12, "bold"), width=100).pack(side="left", padx=10)
        ctk.CTkButton(btn_frm, text="✖ Huỷ", command=self._cancel, fg_color=("#64748b", "#94a3b8"), hover_color="#475569", font=ctk.CTkFont("Segoe UI", 12, "bold"), width=100).pack(side="left", padx=10)

    def _ok(self) -> None:
        """Validate dữ liệu trước khi lưu"""
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
    """Sub-window: Thêm thông tin mới"""
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master, "Thêm thông tin mới")


class EditDialog(BaseRowDialog):
    """Sub-window: Sửa thông tin"""
    def __init__(self, master: ctk.CTk, initial: dict) -> None:
        super().__init__(master, "Sửa thông tin sinh viên", initial)


class AboutDialog(ctk.CTkToplevel):
    """Sub-window About"""
    def __init__(self, master: ctk.CTk, version: str, author: str, date: str) -> None:
        super().__init__(master)
        self.title("Về phần mềm")
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(master)
        
        frm = ctk.CTkFrame(self, corner_radius=10, fg_color=("#ffffff", "#2b2b2b"))
        frm.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frm, text="Phân tích kết quả học tập (Bài 6)", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=("#0f172a", "#f8fafc")).pack(pady=(15, 10))
        ctk.CTkLabel(frm, text=f"Phiên bản: {version}", font=ctk.CTkFont("Segoe UI", 12), text_color=("#475569", "#cbd5e1")).pack(pady=5)
        ctk.CTkLabel(frm, text=f"Tác giả: {author}", font=ctk.CTkFont("Segoe UI", 12), text_color=("#475569", "#cbd5e1")).pack(pady=5)
        ctk.CTkLabel(frm, text=f"Ngày phát hành: {date}", font=ctk.CTkFont("Segoe UI", 12), text_color=("#475569", "#cbd5e1")).pack(pady=5)
        
        ctk.CTkButton(frm, text="Đóng", command=self.destroy, fg_color="#3b82f6", hover_color="#2563eb", font=ctk.CTkFont("Segoe UI", 12, "bold"), width=100).pack(pady=(15, 0))
        self.grab_set()


class AnalysisDialog(ctk.CTkToplevel):
    """Sub-window: Thống kê và Phân tích"""
    def __init__(self, master: ctk.CTk, data: dict) -> None:
        super().__init__(master)
        self.title("📊 Thống kê Phân tích Kết quả Học tập")
        self.geometry("1100x650")
        self.minsize(1000, 500)
        self.transient(master)
        self.data = data
        
        # Tabs
        self.tabview = ctk.CTkTabview(self, fg_color=("#f8fafc", "#1e1e1e"), text_color=("#0f172a", "#f8fafc"), 
                                      segmented_button_selected_color="#3b82f6", 
                                      segmented_button_selected_hover_color="#2563eb")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        self.tabview.add("🏆 Top 10 Xuất sắc")
        self.tabview.add("📋 Tất cả Sinh viên")
        self.tabview.add("📈 Chỉ số & Phân bố")
        
        self._build_top10_tab(self.tabview.tab("🏆 Top 10 Xuất sắc"), data.get("top10", []))
        self._build_all_tab(self.tabview.tab("📋 Tất cả Sinh viên"), data.get("students", []))
        self._build_stats_tab(self.tabview.tab("📈 Chỉ số & Phân bố"), data.get("stats", {}), data.get("dist", {}), data.get("pie_data", {}))

        # Khung chứa nút xuất báo cáo ở dưới cùng (được gộp từ xuat_file_txt.py)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 15))
        ctk.CTkButton(btn_frame, text="💾 Xuất báo cáo (TXT)", command=self._export_report, 
                      fg_color="#10b981", hover_color="#059669", 
                      font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(side="right")

    def _build_top10_tab(self, parent, top10: list[dict]) -> None:
        cols = ("id", "name", "mon_diem", "gpa", "rank", "ly_do", "goi_y")
        
        tree_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="Treeview")
        tree.heading("id", text="Mã SV")
        tree.heading("name", text="Họ tên")
        tree.heading("mon_diem", text="Môn & Điểm")
        tree.heading("gpa", text="GPA")
        tree.heading("rank", text="Học bổng")
        tree.heading("ly_do", text="Lý do")
        tree.heading("goi_y", text="Gợi ý")
        
        tree.column("id", width=80, anchor="center")
        tree.column("name", width=150)
        tree.column("mon_diem", width=250)
        tree.column("gpa", width=60, anchor="center")
        tree.column("rank", width=120, anchor="center")
        tree.column("ly_do", width=150)
        tree.column("goi_y", width=120)

        for i, sv in enumerate(top10):
            prefix = ""
            if i == 0: prefix = "🥇 "
            elif i == 1: prefix = "🥈 "
            elif i == 2: prefix = "🥉 "
            
            tree.insert("", "end", values=(
                sv["student_id"], 
                prefix + sv["full_name"],
                sv.get("mon_diem", ""),
                f"{sv['gpa']:.2f}", 
                sv["rank"],
                sv.get("ly_do", ""),
                sv.get("goi_y", "")
            ))
            
        tree.pack(side="left", fill="both", expand=True)

        def show_full(event):
            item = tree.selection()
            if not item: return
            sv_id = tree.item(item, "values")[0]
            for sv in top10:
                if str(sv["student_id"]) == str(sv_id):
                    messagebox.showinfo(f"Môn của {sv['full_name']}", sv.get("full_mon_diem", ""))
                    break
        tree.bind("<Double-1>", show_full)
        
    def _build_all_tab(self, parent, students: list[dict]) -> None:
        cols = ("id", "name", "mon_diem", "gpa", "rank", "ly_do", "goi_y")
        
        tree_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="Treeview", yscrollcommand=tree_scroll.set)
        tree_scroll.configure(command=tree.yview)
        
        tree.heading("id", text="Mã SV")
        tree.heading("name", text="Họ tên")
        tree.heading("mon_diem", text="Môn & Điểm")
        tree.heading("gpa", text="GPA")
        tree.heading("rank", text="Học bổng")
        tree.heading("ly_do", text="Lý do")
        tree.heading("goi_y", text="Gợi ý")
        
        tree.column("id", width=80, anchor="center")
        tree.column("name", width=150)
        tree.column("mon_diem", width=250)
        tree.column("gpa", width=60, anchor="center")
        tree.column("rank", width=120, anchor="center")
        tree.column("ly_do", width=150)
        tree.column("goi_y", width=120)

        for sv in students:
            tree.insert("", "end", values=(
                sv["student_id"], 
                sv["full_name"], 
                sv.get("mon_diem", ""),
                f"{sv['gpa']:.2f}", 
                sv["rank"],
                sv.get("ly_do", ""),
                sv.get("goi_y", "")
            ))
        
        tree.pack(side="left", fill="both", expand=True)

        def show_full(event):
            item = tree.selection()
            if not item: return
            sv_id = tree.item(item, "values")[0]
            for sv in students:
                if str(sv["student_id"]) == str(sv_id):
                    messagebox.showinfo(f"Môn của {sv['full_name']}", sv.get("full_mon_diem", ""))
                    break
        tree.bind("<Double-1>", show_full)

    def _build_stats_tab(self, parent, stats: dict, dist: dict, pie_data: dict) -> None:
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        frm_text = ctk.CTkFrame(parent, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        frm_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(frm_text, text="Chỉ số thống kê GPA", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=("#0f172a", "#f8fafc")).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        mgpa = stats.get('mean_gpa')
        maxg = stats.get('max_gpa')
        ming = stats.get('min_gpa')
        stdg = stats.get('std_gpa')
        
        stats_data = [
            (f"• GPA trung bình: {f'{mgpa:.4f}' if mgpa is not None else 'N/A'}"),
            (f"• GPA cao nhất: {f'{maxg:.4f}' if maxg is not None else 'N/A'}"),
            (f"• GPA thấp nhất: {f'{ming:.4f}' if ming is not None else 'N/A'}"),
            (f"• Độ lệch chuẩn: {f'{stdg:.4f}' if stdg is not None else 'N/A'}")
        ]
        
        for i, text in enumerate(stats_data):
            ctk.CTkLabel(frm_text, text=text, font=ctk.CTkFont("Segoe UI", 13), text_color=("#334155", "#e2e8f0")).grid(row=i+1, column=0, sticky="w", padx=30, pady=5)
            
        ctk.CTkLabel(frm_text, text="Phân bố xếp loại", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=("#0f172a", "#f8fafc")).grid(row=5, column=0, sticky="w", padx=20, pady=(20, 10))
        row_idx = 6
        for rank, count in dist.items():
            ctk.CTkLabel(frm_text, text=f"• {rank}: {count} sinh viên", font=ctk.CTkFont("Segoe UI", 13), text_color=("#334155", "#e2e8f0")).grid(row=row_idx, column=0, sticky="w", padx=30, pady=5)
            row_idx += 1

        # Phải: Biểu đồ
        frm_chart = ctk.CTkFrame(parent, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        frm_chart.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        labels = [k for k, v in dist.items() if v > 0]
        values = [v for v in dist.values() if v > 0]

        fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=90)
        fig.patch.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')
        ax.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')
        
        color_map = {
            "Đạt loại Xuất sắc": "#1b4332", "Đạt loại Giỏi": "#2ecc71", 
            "Không đạt": "#e63946",
            "Xuất sắc": "#1b4332", "Giỏi": "#2ecc71", 
            "Khá": "#f39c12", "Trung bình": "#f1c40f", 
            "Yếu": "#e63946", "Kém": "#9b2226"
        }
        colors = [color_map.get(lbl, "#bdc3c7") for lbl in labels]

        if values:
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colors,
                wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2) 
            )
            plt.setp(autotexts, size=9, weight="bold", color="white")
            plt.setp(texts, size=10, color="#334155")
            ax.set_title("Tỉ lệ xếp loại học lực", fontdict={"fontname": "Segoe UI", "fontsize": 12, "weight": "bold", "color": "#0f172a" if ctk.get_appearance_mode() == "Light" else "#f8fafc"})
        else:
            ax.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center', color="#64748b")
        
        ax.axis('equal')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frm_chart)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def _export_report(self) -> None:
        """Xuất báo cáo dạng file văn bản (.txt) được gộp từ xuat_file_txt.py"""
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            parent=self, title="Lưu báo cáo thống kê", defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("BÁO CÁO THỐNG KÊ KẾT QUẢ HỌC TẬP\n")
                    f.write("="*40 + "\n\n")
                    
                    stats = self.data.get("stats", {})
                    f.write("1. CHỈ SỐ THỐNG KÊ:\n")
                    f.write(f"- GPA trung bình: {stats.get('mean_gpa', 0):.4f}\n")
                    f.write(f"- GPA cao nhất: {stats.get('max_gpa', 0):.4f}\n")
                    f.write(f"- GPA thấp nhất: {stats.get('min_gpa', 0):.4f}\n")
                    f.write(f"- Độ lệch chuẩn: {stats.get('std_gpa', 0):.4f}\n\n")
                    
                    dist = self.data.get("dist", {})
                    f.write("2. PHÂN BỐ XẾP LOẠI:\n")
                    for rank, count in dist.items():
                        f.write(f"- {rank}: {count} sinh viên\n")
                    f.write("\n")
                    
                    top10 = self.data.get("top10", [])
                    f.write("3. TOP 10 SINH VIÊN XUẤT SẮC NHẤT:\n")
                    for i, sv in enumerate(top10, 1):
                        f.write(f"{i}. {sv['student_id']} - {sv['full_name']} - GPA: {sv['gpa']:.4f} - Xếp loại: {sv['rank']}\n")
                        
                messagebox.showinfo("Thành công", "Xuất báo cáo thành công!", parent=self)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Xuất báo cáo thất bại: {e}", parent=self)


class TranscriptDialog(ctk.CTkToplevel):
    """Cửa sổ Bảng điểm cá nhân: hiển thị điểm hệ 10, điểm chữ, hệ 4 và xếp loại."""
    def __init__(self, master: ctk.CTk, student_info: dict, courses: list, stats: dict) -> None:
        super().__init__(master)
        self.title(f"🎓 Bảng điểm cá nhân — {student_info.get('full_name', 'Sinh viên')}")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.transient(master)
        self.grab_set()

        main_frm = ctk.CTkFrame(self, fg_color=("#f8fafc", "#1e1e1e"), corner_radius=0)
        main_frm.pack(fill="both", expand=True)

        # Header — thông tin sinh viên
        hdr = ctk.CTkFrame(main_frm, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10,
                           border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        hdr.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(hdr, text="BẢNG ĐIỂM KẾT QUẢ HỌC TẬP",
                     font=ctk.CTkFont("Segoe UI", 20, "bold"),
                     text_color=("#0f172a", "#f8fafc")).pack(pady=(15, 5))

        info_frm = ctk.CTkFrame(hdr, fg_color="transparent")
        info_frm.pack(fill="x", padx=30, pady=(5, 15))
        info_frm.grid_columnconfigure(0, weight=1)
        info_frm.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(info_frm, text=f"Họ và tên : {student_info.get('full_name', '')}",
                     font=ctk.CTkFont("Segoe UI", 13)).grid(row=0, column=0, sticky="w", pady=2)
        ctk.CTkLabel(info_frm, text=f"Mã SV     : {student_info.get('student_id', '')}",
                     font=ctk.CTkFont("Segoe UI", 13)).grid(row=1, column=0, sticky="w", pady=2)
        ctk.CTkLabel(info_frm, text=f"Giới tính : {student_info.get('gender', '')}",
                     font=ctk.CTkFont("Segoe UI", 13)).grid(row=0, column=1, sticky="w", pady=2)
        ctk.CTkLabel(info_frm, text=f"Tuổi      : {student_info.get('age', '')}",
                     font=ctk.CTkFont("Segoe UI", 13)).grid(row=1, column=1, sticky="w", pady=2)

        # Bảng môn học
        tbl_frm = ctk.CTkFrame(main_frm, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10,
                               border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        tbl_frm.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        sb = ttk.Scrollbar(tbl_frm, orient="vertical")
        sb.pack(side="right", fill="y", padx=(0, 2), pady=2)

        cols = ("stt", "course_code", "credits", "score_10", "letter_grade", "score_4", "status")
        tree = ttk.Treeview(tbl_frm, columns=cols, show="headings",
                            style="Treeview", yscrollcommand=sb.set)
        sb.configure(command=tree.yview)

        hdrs = {"stt": "STT", "course_code": "Mã môn học", "credits": "Số TC",
                "score_10": "Điểm hệ 10", "letter_grade": "Điểm chữ",
                "score_4": "Điểm hệ 4", "status": "Trạng thái"}
        ws   = {"stt": 50, "course_code": 160, "credits": 80,
                "score_10": 110, "letter_grade": 90, "score_4": 110, "status": 110}
        for c in cols:
            tree.heading(c, text=hdrs[c])
            tree.column(c, width=ws[c], anchor="center")

        for idx, crs in enumerate(courses, 1):
            tree.insert("", "end", values=(
                idx,
                crs["course_code"],
                f"{crs['credits']:.1f}",
                f"{crs['score_10']:.2f}",
                crs["letter_grade"],
                f"{crs['score_4']:.2f}",
                crs["status"],
            ))
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Footer — tổng kết
        ftr = ctk.CTkFrame(main_frm, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10,
                           border_width=1, border_color=("#e2e8f0", "#3f3f46"))
        ftr.pack(fill="x", padx=20, pady=(0, 20))
        stat_row = ctk.CTkFrame(ftr, fg_color="transparent")
        stat_row.pack(pady=15, padx=20, fill="x")

        stat_items = [
            ("Tổng TC tích lũy",       f"{stats['total_credits']:.1f}"),
            ("TB chung (Hệ 10)",        f"{stats['gpa_10']:.2f}"),
            ("TB chung (Hệ 4)",         f"{stats['gpa_4']:.2f}"),
            ("Xếp loại học lực",        stats["ranking"]),
        ]
        for i, (lbl, val) in enumerate(stat_items):
            stat_row.grid_columnconfigure(i, weight=1)
            box = ctk.CTkFrame(stat_row, fg_color="transparent")
            box.grid(row=0, column=i)
            ctk.CTkLabel(box, text=lbl, font=ctk.CTkFont("Segoe UI", 11),
                         text_color=("#64748b", "#94a3b8")).pack()
            color = "#3b82f6"
            if lbl == "Xếp loại học lực":
                if val in ("Xuất sắc", "Giỏi"):  color = "#10b981"
                elif val in ("Yếu", "Kém"):       color = "#ef4444"
                elif val == "Trung bình":          color = "#f59e0b"
            ctk.CTkLabel(box, text=val, font=ctk.CTkFont("Segoe UI", 18, "bold"),
                         text_color=color).pack()


class PieChartWindow:
    """Cửa sổ hiển thị biểu đồ tròn dự phòng (nếu controller dùng trực tiếp)"""
    def __init__(self, parent, data_thong_ke: dict):
        self.top = ctk.CTkToplevel(parent)
        self.top.title("Biểu đồ tròn thống kê học lực")
        self.top.geometry("650x550")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        frm = ctk.CTkFrame(self.top, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10)
        frm.pack(fill="both", expand=True, padx=20, pady=20)

        labels = [key for key, value in data_thong_ke.items() if value > 0]
        values = [value for value in data_thong_ke.values() if value > 0]

        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')
        ax.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')
        fig.suptitle('TỈ LỆ PHẦN TRĂM XẾP LOẠI HỌC LỰC', fontsize=13, fontweight='bold', y=0.95, color="#0f172a" if ctk.get_appearance_mode() == "Light" else "#f8fafc")

        color_map = {
            'Yếu/Kém (<5)': '#ef4444',         
            'Trung bình/Khá (5->8)': '#f59e0b', 
            'Giỏi/Xuất sắc (>=8)': '#10b981'    
        }
        colors = [color_map.get(label, "#94a3b8") for label in labels]

        if values:
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colors,
                wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2) 
            )
            plt.setp(autotexts, size=11, weight="bold", color="white")
            plt.setp(texts, size=10, color="#334155")
            ax.legend(wedges, labels, title="Xếp loại", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        else:
            ax.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center', fontsize=12, color="#64748b")

        ax.axis('equal')  
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frm)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ctk.CTkButton(frm, text="Đóng cửa sổ", command=self.top.destroy, 
                      fg_color=("#64748b", "#94a3b8"), hover_color="#475569", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=10)

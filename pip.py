import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ================== DATA ==================
data = pd.DataFrame(columns=["ten", "mon", "diem"])


# ================== LOGIC ==================
def tinh_ket_qua():
    global data

    if data.empty:
        messagebox.showwarning("Lỗi", "Chưa có dữ liệu!")
        return

    # GPA
    gpa_sv = data.groupby("ten")["diem"].mean().reset_index()
    gpa_sv.rename(columns={"diem": "gpa"}, inplace=True)

    # Xét học bổng
    def xet_hoc_bong(ten):
        sv = data[data["ten"] == ten]
        gpa = sv["diem"].mean()
        diem_min = sv["diem"].min()

        if gpa >= 9 and diem_min >= 7.5:
            return "Đạt loại Xuất sắc"
        elif gpa >= 8 and diem_min >= 6.5:
            return "Đạt loại Giỏi"
        else:
            return "Không đạt"

    # Lý do
    def giai_thich(ten):
        sv = data[data["ten"] == ten]
        gpa = sv["diem"].mean()
        diem_min = sv["diem"].min()

        ly_do = []

        if gpa < 8:
            ly_do.append("GPA chưa đạt điều kiện")
        if diem_min < 5:
            ly_do.append("Có môn <5")

        if not ly_do:
            return "Đạt điều kiện"
        return ", ".join(ly_do)

    # Gợi ý
    def goi_y(ten):
        sv = data[data["ten"] == ten]
        diem_min = sv["diem"].min()

        if diem_min < 5:
            return "Học lại môn yếu"
        elif diem_min < 7:
            return "Cố gắng cải thiện điểm"
        else:
            return "Duy trì tốt"
    
    # Môn & Đểm
    def mon_diem(ten):
        sv = data[data["ten"] == ten]
        text = ", ".join([f"{row['mon']}:{row['diem']}" for _, row in sv.iterrows()])
        return text[:30] + "..." if len(text) > 30 else text

    # Áp dụng
    gpa_sv["hoc_bong"] = gpa_sv["ten"].apply(xet_hoc_bong)
    gpa_sv["mon_diem"] = gpa_sv["ten"].apply(mon_diem)
    gpa_sv["ly_do"] = gpa_sv["ten"].apply(giai_thich)
    gpa_sv["goi_y"] = gpa_sv["ten"].apply(goi_y)

    # Thống kê
    so_dat = (gpa_sv["hoc_bong"] != "Không đạt").sum()
    so_khong_dat = (gpa_sv["hoc_bong"] == "Không đạt").sum()

    label_thong_ke.config(
        text=f"Đạt học bổng: {so_dat} | Không đạt: {so_khong_dat}"
    )

    # Hiển thị
    tree.delete(*tree.get_children())

    for _, row in gpa_sv.iterrows():
        tree.insert("", "end", values=(
            row["ten"],
            row["mon_diem"],
            f"{row['gpa']:.2f}",
            row["hoc_bong"],
            row["ly_do"],
            row["goi_y"]
        ))
        # ================== DOUBLE CLICK XEM FULL ==================
def show_full(event):
    item = tree.selection()
    if not item:
        return

    values = tree.item(item, "values")
    ten = values[0]

    sv = data[data["ten"] == ten]
    full = "\n".join([f"{row['mon']}: {row['diem']}" for _, row in sv.iterrows()])

    messagebox.showinfo(f"Môn của {ten}", full)


# ================== ADD DATA ==================
def them_du_lieu():
    global data

    ten = entry_ten.get().strip()
    mon = entry_mon.get().strip()
    diem = entry_diem.get().strip()

    if not ten or not mon or not diem:
        messagebox.showwarning("Lỗi", "Nhập đầy đủ thông tin!")
        return

    try:
        diem = float(diem)
    except:
        messagebox.showwarning("Lỗi", "Điểm phải là số!")
        return

    data.loc[len(data)] = [ten, mon, diem]

    entry_ten.delete(0, tk.END)
    entry_mon.delete(0, tk.END)
    entry_diem.delete(0, tk.END)

    messagebox.showinfo("OK", "Đã thêm!")


# ================== UI ==================
root = tk.Tk()
root.title("Hệ thống xét học bổng")
root.geometry("900x500")

# Input
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)

ttk.Label(frame_input, text="Tên").grid(row=0, column=0)
entry_ten = ttk.Entry(frame_input)
entry_ten.grid(row=0, column=1)

ttk.Label(frame_input, text="Môn").grid(row=1, column=0)
entry_mon = ttk.Entry(frame_input)
entry_mon.grid(row=1, column=1)

ttk.Label(frame_input, text="Điểm").grid(row=2, column=0)
entry_diem = ttk.Entry(frame_input)
entry_diem.grid(row=2, column=1)

ttk.Button(frame_input, text="Thêm", command=them_du_lieu).grid(row=3, columnspan=2, pady=5)

# Button phân tích
ttk.Button(root, text="🎓 Xét học bổng", command=tinh_ket_qua).pack(pady=10)

# Thống kê
label_thong_ke = ttk.Label(root, text="Đạt học bổng: 0 | Không đạt: 0")
label_thong_ke.pack()

# Table
columns = ("ten", "mon_diem", "gpa", "hoc_bong", "ly_do", "goi_y")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("ten", text="Tên")
tree.heading("mon_diem", text="Môn & Điểm")
tree.heading("gpa", text="GPA")
tree.heading("hoc_bong", text="Học bổng")
tree.heading("ly_do", text="Lý do")
tree.heading("goi_y", text="Gợi ý")
tree.column("mon_diem", width=250)
tree.pack(fill="both", expand=True)
tree.bind("<Double-1>", show_full)

# RUN
root.mainloop()
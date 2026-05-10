import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def xu_ly_du_lieu():
    # 1. Lấy dữ liệu từ ô nhập bằng phương thức .get()
    mssv = o_nhap_ma_sv.get()
    ho_ten = o_nhap_ho_ten.get()

    # 2. Ràng buộc dữ liệu: Kiểm tra MSSV phải là số (thử thách)
    if mssv != "" and not mssv.isdigit():
        nhan_ket_qua.config(text="MSSV phải là số! Vui lòng kiểm tra lại.", fg="red")
        messagebox.showerror("Lỗi nhập liệu", "MSSV không hợp lệ! MSSV chỉ được chứa chữ số.")
        return

    # 3. In ra Terminal để lập trình viên kiểm tra + thời gian hiện tại (thử thách)
    thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{thoi_gian}] Dữ liệu nhận được: MSSV: {mssv} - Họ tên: {ho_ten}")

    # 4. Cập nhật trực tiếp lên giao diện (Label kết quả)
    if ho_ten != "":
        nhan_ket_qua.config(text=f"Chào sinh viên: {ho_ten} ({mssv})", fg="blue")
        # Xóa trắng ô nhập sau khi xác nhận thành công (thử thách)
        o_nhap_ma_sv.delete(0, tk.END)
        o_nhap_ho_ten.delete(0, tk.END)
    else:
        nhan_ket_qua.config(text="Vui lòng không để trống thông tin!", fg="red")


root = tk.Tk()
root.title("Quản lý Sinh viên - UHL")
root.geometry("400x350")
root.columnconfigure(1, weight=1)

# --- PHẦN GIAO DIỆN (Giữ nguyên từ Lộ trình 3) ---
tk.Label(root, text="Mã sinh viên:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
o_nhap_ma_sv = tk.Entry(root)
o_nhap_ma_sv.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Họ và tên:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
o_nhap_ho_ten = tk.Entry(root)
o_nhap_ho_ten.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Nút bấm có tham số 'command' kết nối tới hàm xử lý
nut_xac_nhan = tk.Button(root, text="Xác nhận điểm danh", command=xu_ly_du_lieu)
nut_xac_nhan.grid(row=2, column=0, columnspan=2, pady=10)

# Nhãn hiển thị kết quả ngay trên giao diện
nhan_ket_qua = tk.Label(root, text="Chưa có dữ liệu", font=("Arial", 10, "italic"))
nhan_ket_qua.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()

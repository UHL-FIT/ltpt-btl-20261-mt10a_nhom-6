import tkinter as tk

# 1. Khởi tạo cửa sổ gốc
root = tk.Tk()
root.title("Ứng dụng đầu tiên - UHL")
root.geometry("400x200")

# 2. Tạo thành phần hiển thị văn bản (Label)
nhan_chao = tk.Label(root, text="Chào mừng sinh viên Đại học Hạ Long!")
nhan_chao.pack(pady=50)  # Đưa nhãn vào cửa sổ và tạo khoảng cách lề

# 3. Duy trì cửa sổ (Vòng lặp chính)
root.mainloop()

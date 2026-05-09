# 📊 Phần mềm Quản lý & Phân tích Kết quả Học tập
**Bài tập lớn môn học - Nhóm 6 (MT10A)**

## 📝 Giới thiệu
Dự án là một ứng dụng Desktop được viết bằng Python giúp lưu trữ, quản lý và phân tích kết quả học tập của sinh viên. Ứng dụng được thiết kế theo mô hình kiến trúc **MVC (Model - View - Controller)** giúp code rõ ràng, dễ bảo trì, kết hợp với giao diện trực quan và hệ thống lưu trữ tệp tin.

## 👥 Thành viên nhóm 6
1. Lê Huy Phúc
2. Nguyễn Minh Giang
3. Hoàng Tiến Tâm
4. Lục Văn Hải

## 🛠️ Công nghệ & Kiến trúc sử dụng
- **Ngôn ngữ:** Python 3.x
- **Giao diện (GUI):** Thư viện `Tkinter` (tích hợp sẵn trong Python)
- **Cơ sở dữ liệu:** Lưu trữ cục bộ bằng tệp tin `.csv`
- **Mô hình kiến trúc:** MVC (Model - View - Controller)

## ✨ Tính năng chính của ứng dụng
- **Quản lý dữ liệu:** Thêm, sửa, xóa, và cập nhật thông tin sinh viên, điểm số.
- **Xác thực dữ liệu:** Kiểm tra tính hợp lệ của dữ liệu đầu vào (tuổi, giới tính, định dạng điểm) thông qua module `validators.py`.
- **Phân tích kết quả:** [Bạn ghi thêm các tính năng lọc ở đây, ví dụ: Tính điểm trung bình, lọc danh sách sinh viên Giỏi/Khá/Yếu, thống kê tỷ lệ...]
- **Giao diện trực quan:** Bảng hiển thị dữ liệu rõ ràng, dễ thao tác.

## 📁 Cấu trúc thư mục
```text
📦 ltpt-btl-20261-mt10a_nhom-6
 ┣ 📂 controllers       # Xử lý logic điều hướng giữa View và Model
 ┣ 📂 models            # Chứa các hàm xử lý dữ liệu và giao tiếp với file CSV
 ┣ 📂 views             # Chứa mã nguồn xây dựng giao diện Tkinter
 ┣ 📂 data              # Thư mục lưu trữ tệp dữ liệu CSV
 ┣ 📜 main.py           # File gốc dùng để khởi chạy toàn bộ chương trình
 ┣ 📜 validators.py     # Module kiểm tra dữ liệu đầu vào
 ┗ 📜 README.md         # File tài liệu giới thiệu dự án

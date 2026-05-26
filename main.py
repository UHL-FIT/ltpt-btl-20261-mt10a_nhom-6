import sys
from pathlib import Path

# Thêm thư mục cha vào sys.path để Python nhận diện được package 'student_app_basic'
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from controller_basic import BasicController

def main():
    # Khởi tạo Controller với thư mục hiện tại làm thư mục gốc (nơi chứa data/grades.csv)
    app = BasicController(current_dir)
    app.run()

if __name__ == "__main__":
    main()

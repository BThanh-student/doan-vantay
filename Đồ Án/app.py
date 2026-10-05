import serial
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Giả lập database: ID vân tay tương ứng với Tên học sinh
# Bạn có thể thêm đủ danh sách nhóm vào đây
DATABASE = {
    "1": {"name": "Phạm Văn Việt Anh", "class": "12A4"},
    "2": {"name": "Đinh Duy Bảo", "class": "12A4"},
    "3": {"name": "Nguyễn Kiên Cường", "class": "12A4"},
    "4": {"name": "Nguyễn Xuân Cường", "class": "12A4"},
    "5": {"name": "Đỗ Hữu Duy", "class": "12A4"},
    "6": {"name": "Cao Thị Mỹ Duyên", "class": "12A4"},
    "7": {"name": "Hoàng Ánh Dương", "class": "12A4"},
    "8": {"name": "Đoàn Tiến Đạt", "class": "12A4"},
    "9": {"name": "Đỗ Tuấn Đạt", "class": "12A4"},
    "10": {"name": "Hoàng Gia Ngọc Đức", "class": "12A4"},
    "11": {"name": "Hoàng Gia Giang", "class": "12A4"},
    "12": {"name": "Phạm Thu Ngân Hà", "class": "12A4"},
    "13": {"name": "Nguyễn Xuân Hùng", "class": "12A4"},
    "14": {"name": "Đỗ Quang Hưng", "class": "12A4"},
    "15": {"name": "Ngô Thị Lan Hương", "class": "12A4"},
    "16": {"name": "Đinh Xuân Khánh", "class": "12A4"},
    "17": {"name": "Nguyễn Ngọc Khánh", "class": "12A4"},
    "18": {"name": "Bùi Hồng Hoàng Linh", "class": "12A4"},
    "19": {"name": "Đinh Xuân Hồng Minh", "class": "12A4"},
    "20": {"name": "Đoàn Trà My", "class": "12A4"},
    "21": {"name": "Đoàn Toàn Nam", "class": "12A4"},
    "22": {"name": "Phạm Minh Nam", "class": "12A4"},
    "23": {"name": "Trần Hải Nam", "class": "12A4"},
    "24": {"name": "Phạm Thị Kim Ngân", "class": "12A4"},
    "25": {"name": "Lưu Gia Như", "class": "12A4"},
    "26": {"name": "Đinh Minh Phương", "class": "12A4"},
    "27": {"name": "Ngô Thị Phương", "class": "12A4"},
    "28": {"name": "Phạm Bảo Anh Quyết", "class": "12A4"},
    "29": {"name": "Vũ Thành Tâm", "class": "12A4"},
    "30": {"name": "Đoàn Mạnh Tân", "class": "12A4"},
    "31": {"name": "Bùi Trọng Thanh", "class": "12A4"},
    "32": {"name": "Lê Hoàng Minh Thư", "class": "12A4"},
    "33": {"name": "Nguyễn Thị Thùy Trang", "class": "12A4"},
    "34": {"name": "Hoàng Gia Việt", "class": "12A4"}
}

current_student = {"name": "", "class": "", "id": ""}

def read_arduino():
    global current_student
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        print("Đã kết nối Arduino thành công!")

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Gốc từ Arduino: {line}") # Xem dòng này ở Terminal

                if "#" in line:
                    try:
                        # BƯỚC QUAN TRỌNG: Lọc lấy con số duy nhất
                        import re
                        numbers = re.findall(r'\d+', line) # Tìm tất cả các cụm số
                        if numbers:
                            f_id = str(int(numbers[0])) # Lấy số đầu tiên, ép sang int rồi về str để mất số 0 thừa
                            
                            print(f"ID sau khi lọc sạch: '{f_id}'") # Kiểm tra xem có dấu cách ko

                            if f_id in DATABASE:
                                current_student = {
                                    "name": DATABASE[f_id]["name"],
                                    "class": DATABASE[f_id]["class"],
                                    "id": f_id
                                }
                                print(f"==> KHỚP: {current_student['name']}")
                            else:
                                print(f"==> LỖI: ID {f_id} chưa có trong DATABASE")
                                current_student = {"name": "ID " + f_id + " chưa nạp tên", "class": "???", "id": f_id}
                    except Exception as e:
                        print(f"Lỗi xử lý ID: {e}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    global current_student
    # Tạo một bản sao để gửi đi
    data_to_send = current_student.copy()
    
    # Reset biến tạm về rỗng sau khi đã gửi dữ liệu cho Web
    # Việc này giúp Web không bị điền lặp dữ liệu cũ
    current_student = {"name": "", "class": "", "id": ""}
    
    return jsonify(data_to_send)
if __name__ == '__main__':
    t = threading.Thread(target=read_arduino, daemon=True)
    t.start()

    app.run(debug=False, host='0.0.0.0', port=5000)
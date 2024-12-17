from flask import Flask, render_template, jsonify
from sense_emu import SenseHat
import time

# Khởi tạo Sense HAT
cam_bien = SenseHat()

app = Flask(__name__)

# Đọc dữ liệu cảm biến từ Sense HAT
def doc_du_lieu_cam_bien():
    nhiet_do = cam_bien.get_temperature()
    do_am = cam_bien.get_humidity()
    trang_thai_joystick = cam_bien.stick.get_events()
    
    # Ghi nhận trạng thái joystick (nếu có sự kiện)
    su_kien = []
    for sk in trang_thai_joystick:
        if sk.action == "pressed":
            su_kien.append(f"Joystick {sk.direction} nhấn")
    
    return {
        "nhiet_do": round(nhiet_do, 1),
        "do_am": round(do_am, 1),
        "joystick": su_kien if su_kien else ["Không có sự kiện"]
    }

# Route trang chủ
@app.route("/")
def index():
    return render_template("index.html")

# API trả về dữ liệu cảm biến dưới dạng JSON
@app.route("/api/data")
def api_data():
    data = doc_du_lieu_cam_bien()
    return jsonify(data)

# Chạy chương trình hiển thị tên trên LED
@app.route("/led")
def hien_thi_led():
    cam_bien.clear()
    cam_bien.show_message("HOA", text_colour=[255, 0, 0], back_colour=[0, 0, 0], scroll_speed=0.1)
    return "Đã hiển thị chữ 'HOA' trên LED!"

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(debug=True)
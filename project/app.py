from flask import Flask, request, jsonify, render_template, redirect, url_for
import ctypes
import os
import csv

app = Flask(__name__)

# C 라이브러리 로드 (DLL 파일로 경로 변경)
lib_path = os.path.join(os.path.dirname(__file__), r'login_lib\x64\Debug\login_lib.dll')
login_lib = ctypes.CDLL(lib_path)

# C 함수의 반환 타입 및 매개변수 설정
login_lib.login.restype = ctypes.c_bool
login_lib.login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/sign_up.html')
def signup_page():
    return render_template('sign_up.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data['id'].encode('utf-8')
    user_password = data['password'].encode('utf-8')

    # C 라이브러리의 login 함수 호출
    is_logged_in = login_lib.login(user_id, user_password)

    if is_logged_in:
        return jsonify({"success": True})  # 로그인 성공
    else:
        return jsonify({"success": False})  # 로그인 실패

# 메인 페이지 라우트
@app.route('/main')
def main_page():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

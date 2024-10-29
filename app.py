from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import ctypes
import os
import zipfile
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 세션 관리를 위한 비밀 키
app.secret_key = '1111'

# 폴더 설정
UPLOAD_FOLDER = 'static/uploads'  # 업로드된 파일을 저장할 폴더
USER_INFO_FOLDER = 'static/users'  # 사용자 정보 txt 파일을 저장할 폴더
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USER_INFO_FOLDER'] = USER_INFO_FOLDER

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(USER_INFO_FOLDER):
    os.makedirs(USER_INFO_FOLDER)

# C_function DLL 로드 (로그인, 회원가입, 중복 확인 기능 처리)
c_function_lib_path = os.path.join(os.path.dirname(__file__), r'C_function\x64\Debug\C_function.dll')
c_function = ctypes.CDLL(c_function_lib_path)

# 로그인 함수
c_function.login.restype = ctypes.c_int
c_function.login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

# 회원가입 요청 함수
c_function.signup_request.restype = ctypes.c_bool
c_function.signup_request.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# 아이디 중복 확인 함수
c_function.duplicate_check.restype = ctypes.c_bool
c_function.duplicate_check.argtypes = [ctypes.c_char_p]

# 회원가입 수락 함수
c_function.signup_accept.restype = ctypes.c_bool
c_function.signup_accept.argtypes = [ctypes.c_char_p]

# 관리자 계정 정보
ADMIN_USERNAME = "admin"

# 관리자 페이지에 표시할 회원가입 데이터
signup_data = []

# 라우트

# 로그인 화면 (기본)
@app.route('/')
def login_page():
    return render_template('login.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data['id'].encode('utf-8')
    user_password = data['password'].encode('utf-8')

    # C DLL 로그인 함수 호출
    login_rst = c_function.login(user_id, user_password)

    # login_rst는 0(실패), 1(일반 사용자), 2(관리자)의 정수값을 가짐
    if login_rst == 2:
        session['admin'] = True
        return jsonify({"success": True, "redirect": "/admin"})
    elif login_rst == 1:
        return jsonify({"success": True, "redirect": "/main"})
    else: # login_rst == 0
        return jsonify({"success": False})

# 회원가입 화면
@app.route('/sign_up.html', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        try:
            # 폼에서 사용자 데이터 추출
            user_id = request.form['id']
            user_password = request.form['password']
            user_role = request.form['role']
            user_name = request.form['name']
            user_birthday = request.form['birthday']
            user_gender = request.form['gender']
            
            # 업로드된 파일 저장
            uploaded_files = []
            for file in request.files.getlist('files'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(file_path)

            # C DLL 회원가입 함수 호출하여 txt 파일 생성 처리
            result = c_function.signup_request(
                user_id.encode('utf-8'), 
                user_password.encode('utf-8'), 
                user_role.encode('utf-8'),
                user_name.encode('utf-8'), 
                user_birthday.encode('utf-8'),
                user_gender.encode('utf-8')
            )

            # ZIP 파일 생성
            zip_filename = f"{user_id}_files.zip"
            zip_path = os.path.join(USER_INFO_FOLDER, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                # C 함수로 생성된 txt 파일과 업로드된 파일을 zip에 추가
                txt_file_path = os.path.join(USER_INFO_FOLDER, f"{user_id}_info.txt")
                zipf.write(txt_file_path, os.path.basename(txt_file_path))
                for file_path in uploaded_files:
                    zipf.write(file_path, os.path.basename(file_path))

            # 관리자 페이지에 표시할 회원가입 데이터 저장
            signup_data.append({
                'id': user_id,
                'apply_date': time.strftime("%Y.%m.%d"),
                'role': user_role,
                'zip_path': zip_path
            })

            if result:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        
        except Exception as e:
            print(f"오류 발생: {e}")
            return jsonify({"success": False, "message": f"서버 오류: {str(e)}"})

    return render_template('sign_up.html')

# 아이디 중복 확인 버튼
@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.json
    user_id = data['id'].encode('utf-8')

    # C DLL 중복 확인 함수 호출
    is_duplicate = c_function.duplicate_check(user_id)
    return jsonify({"is_duplicate": is_duplicate})


@app.route('/download_zip/<user_id>')
def download_zip(user_id):
    user_zip_path = None
    for signup in signup_data:
        if signup['id'] == user_id:
            user_zip_path = signup['zip_path']
            break

    if user_zip_path and os.path.exists(user_zip_path):
        return send_file(user_zip_path, as_attachment=True, download_name=f"{user_id}_files.zip", mimetype='application/zip')
    return "파일을 찾을 수 없습니다.", 404

# admin 화면
@app.route('/admin')
def admin_page():
    if 'admin' not in session:
        return redirect(url_for('login_page'))
    return render_template('admin.html', signup_data=signup_data)

# main 화면
@app.route('/main')
def main_mento_page():
    return render_template('main.html')

# 회원가입 승인 라우트
@app.route('/accept_signup/<user_id>', methods=['POST'])
def accept_signup(user_id):
    # 회원가입 승인 C 함수 호출하여 user.csv에 데이터 전송
    result = c_function.signup_accept(user_id.encode('utf-8'))
    
    if result:
        # 사용자 정보 파일 삭제
        txt_file_path = os.path.join(USER_INFO_FOLDER, f"{user_id}_info.txt")
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)

        # signup_data 리스트에서 사용자 제거
        global signup_data
        signup_data = [signup for signup in signup_data if signup['id'] != user_id]

        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
# admin 로그아웃
@app.route('/logout')
def logout():
    session.pop('admin', None)  # 세션에서 관리자 정보 제거
    return redirect(url_for('login_page'))  # 로그인 페이지로 리다이렉트

if __name__ == '__main__':
    app.run(debug=True)

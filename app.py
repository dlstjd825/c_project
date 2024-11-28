# 필요한 라이브러리 import
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import ctypes
import os
import zipfile
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'dkssud!dlrjs!vmfaldxlavmfzhemdla~' # 세션 암호화 위한 키

UPLOAD_FOLDER = 'c_project/static/uploads' # 회원가입에서 업로드한 파일 관리
USER_INFO_FOLDER = 'c_project/static/users' # admin에게 전달할 사용자 정보 폴더

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['USER_INFO_FOLDER'] = USER_INFO_FOLDER

# 폴더들이 없다면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(USER_INFO_FOLDER):
    os.makedirs(USER_INFO_FOLDER)

# C에서 구현한 함수를 사용하기 위해 dll파일 불러옴
c_function = ctypes.CDLL(os.path.join(os.path.dirname(__file__), r'C_function\x64\Debug\C_function.dll'))

# 로그인 함수
c_function.login.restype = ctypes.c_int
c_function.login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

# 회원가입 요청 함수
c_function.signup_request.restype = ctypes.c_bool
c_function.signup_request.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# 아이디 중복확인 함수
c_function.duplicate_check.restype = ctypes.c_bool
c_function.duplicate_check.argtypes = [ctypes.c_char_p]

# 회원가입 수락 함수
c_function.signup_accept.restype = ctypes.c_bool
c_function.signup_accept.argtypes = [ctypes.c_char_p]

# 회원가입 거절 함수
c_function.signup_reject.restype = ctypes.c_bool
c_function.signup_reject.argtypes = [ctypes.c_char_p]

# delete_user 함수 설정
c_function.delete_user.restype = ctypes.c_bool
c_function.delete_user.argtypes = [ctypes.c_char_p]

#추가
# change_id 함수 설정
c_function.change_id.restype = ctypes.c_bool
c_function.change_id.argtypes = [ctypes.c_char_p]

# change_password 함수 설정
c_function.change_password.restype = ctypes.c_bool
c_function.change_password.argtypes = [ctypes.c_char_p]

# admin페이지에서 보여줄 내용 (회원가입 대기자) 저장하는 리스트
signup_data = []

# 로그인 페이지 -> 실행되면 login.html 실행
@app.route('/')
def login_page():
    return render_template('login.html')

# 로그인 시도 받으면 처리하는 라우트
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data['id'].encode('utf-8')
    user_password = data['password'].encode('utf-8')
    
    # login_rst > 2: admin, 1: 일반 사용자, 0: 오류, -1: 승인 대기중, -2: 거절
    login_rst = c_function.login(user_id, user_password)
    # login_rst = 1
    
    if login_rst == 2:
        session['admin'] = True
        return jsonify({"success": True, "redirect": "/admin"}) # admin페이지로 이동
    elif login_rst == 1:
        session['user_id'] = user_id  # 세션에 user_id 저장#추가한거임
        session['user_password'] = user_password
        return jsonify({"success": True, "redirect": "/main"}) # main페이지로 이동
    elif login_rst == -1:
        return jsonify({"success": False, "message": "관리자 승인 대기중입니다."})
    elif login_rst == -2:
        session['rejected_user'] = data['id']
        return jsonify({"success": False, "message": "회원가입이 거절되었습니다."})

    return jsonify({"success": False, "message": "아이디 또는 비밀번호가 잘못되었습니다."})

# 회원가입 처리하는 라우트
@app.route('/sign_up.html', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('sign_up.html')
    
    try:
        # 사용자 정보 저장
        user_id = request.form['id']
        user_password = request.form['password']
        user_status = 'pending' # 회원가입 진행 상태 나타내는 정보. 기본적으로 pendig : 대기중
        user_role = request.form['role'] # mento 또는 mentee
        user_name = request.form['name']
        user_birthday = request.form['birthday']
        user_gender = request.form['gender']

        uploaded_files = [] # 업로드된 파일 모으는 리스트
        for file in request.files.getlist('files'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(file_path)

        # 회원가입 대기 상태로 전환
        result = c_function.signup_request(
            user_id.encode('utf-8'), 
            user_password.encode('utf-8'), 
            user_status.encode('utf-8'),
            user_role.encode('utf-8'),
            user_name.encode('utf-8'), 
            user_birthday.encode('utf-8'),
            user_gender.encode('utf-8')
        )

        # 사용자가 업로드한 파일을 압축 => admin페이지에서 다운받아서 확인 가능
        zip_filename = f"{user_id}_files.zip"
        zip_path = os.path.join(USER_INFO_FOLDER, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            txt_file_path = os.path.join(USER_INFO_FOLDER, f"{user_id}_info.txt")
            zipf.write(txt_file_path, os.path.basename(txt_file_path))
            for file_path in uploaded_files:
                zipf.write(file_path, os.path.basename(file_path))

        signup_data.append({
            'id': user_id,
            'apply_date': time.strftime("%Y.%m.%d"),
            'role': user_role,
            'zip_path': zip_path
        })
        return jsonify({"success": result})
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"success": False, "message": f"서버 오류: {str(e)}"})

# 회원가입 수락하는 라우트
@app.route('/signup_accept/<user_id>', methods=['POST'])
def accept_signup(user_id):
    # signup_fuction은 status를 approved로 변경. 성공하면 true, 실패하면 false
    result = c_function.signup_accept(user_id.encode('utf-8'))
    if result:
        global signup_data
        # 회원가입 대기자 명단에서 회원가입 수락된 사람 제거
        signup_data = [x for x in signup_data if x['id'] != user_id]
        return jsonify({"success": True})
    return jsonify({"success": False})

# 회원가입 거절하는 라우트
@app.route('/signup_reject/<user_id>', methods=['POST'])
def reject_signup(user_id):
    # status를 rejected로 변경
    result = c_function.signup_reject(user_id.encode('utf-8'))
    if result:
        global signup_data
        # 회원가입 대기자 명단에서 회원가입 거절된 사람 제거
        signup_data = [signup for signup in signup_data if signup['id'] != user_id]
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/delete_rejected_user', methods=['POST'])
def confirm_rejection():
    # 세션에서 거절된 사용자 ID를 가져옴
    user_id = session.pop('rejected_user', None)
    
    if user_id:
        # delete_user 함수로 사용자의 모든 정보 삭제
        result = c_function.delete_user(user_id.encode('utf-8'))  # 해당 ID에 대한 정보 삭제
        if result:
            return jsonify({"success": True})
    
    return jsonify({"success": False})

# 아이디 중복 확인 라우트
@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    user_id = request.json['id'].encode('utf-8')
    is_duplicate = c_function.duplicate_check(user_id)
    return jsonify({"is_duplicate": is_duplicate})

# admin페이지에서 사용자 정보, 제출 서류를 모은 zip파일 다운받는 라우트
@app.route('/download_zip/<user_id>')
def download_zip(user_id):
    user_zip_path = None
    for x in signup_data:
        if x['id'] == user_id:
            user_zip_path = x['zip_path']
            break  # 첫 번째로 조건을 만족하는 항목을 찾으면 루프 종료

    if user_zip_path and os.path.exists(user_zip_path):
        return send_file(user_zip_path, as_attachment=True, download_name=f"{user_id}_files.zip", mimetype='application/zip')
    return "파일을 찾을 수 없습니다.", 404

# admin페이지 라우트
@app.route('/admin')
def admin_page():
    signup_data.clear()  # 기존 데이터를 초기화
    
    # CSV 파일에서 대기열 사용자 데이터 읽기
    try:
        with open('static/user.csv', 'r', encoding='UTF-8') as file:
            for line in file:
                user_info = line.strip().split(',')
                if len(user_info) < 7:
                    continue
                
                id, pw, status, role, name, birthday, gender = user_info
                
                # 'pending' 상태인 사용자만 대기열에 추가
                if status == 'pending':
                    signup_data.append({
                        'id': id,
                        'apply_date': time.strftime("%Y.%m.%d"), 
                        'role': role,
                        'zip_path': f'static/users/{id}_files.zip'  # 파일 경로 설정
                    })
    except FileNotFoundError:
        print("user.csv 파일을 찾을 수 없습니다.")

    return render_template('admin.html', signup_data=signup_data)

# 메인화면 라우트 => 추후 메인화면과 연결 필요
@app.route('/main')
def main_page():
    return render_template('main.html')


# 마이페이지 라우트
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


# 프로필 수정 처리 라우트
@app.route('/change_profile', methods=['POST'])
def change_profile():
    # 여기서 프로필 수정 처리 코드 작성
    return redirect(url_for('mypage'))


@app.route('/change_id', methods=['POST'])
def change_id():
    data = request.json
    new_id = data.get('new_id')  # JSON 데이터에서 new_id 가져오기
    old_id = session.get('user_id')  # 세션에서 user_id 가져오기

    # 검증
    if not old_id:
        return jsonify({"success": False, "message": "Session user_id is missing"})
    if not new_id or not isinstance(new_id, str):
        return jsonify({"success": False, "message": "Invalid new ID"})

    # ID 변경 로직 호출
    result = c_function.change_id(old_id, new_id.encode('utf-8')) # 세션에서 가져온애들은 이미 인코드 했기 때문에 다시 하면 안됨. new_id만 해주기

    if result:
        session['user_id'] = new_id
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Failed to change ID"})


@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    user_id = session.get('user_id')  # 세션에서 user_id 가져오기
  # JSON 데이터에서 id 가져오기
    old_password = session.get('user_password')  # JSON 데이터에서 oldPassword 가져오기 아니고 마찬가지로 user_password세션에서 가져와야 함.
    new_password = data.get('newPassword')  # JSON 데이터에서 newPassword 가져오기

    # 검증
    if not user_id or not old_password or not new_password:
        return jsonify({"success": False, "message": "Invalid input"})

    # 비밀번호 변경 로직 호출
    result = c_function.change_password(user_id, old_password, new_password.encode('utf-8'))

    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Failed to change password"})



# admin페이지 로그아웃 라우트
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)



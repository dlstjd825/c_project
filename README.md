# 수정내역
엔터치는 방법 : 엔터치고싶은곳에서 공백 두 번 이상 입력하고 엔터치기 또는 `<br>` 태그 사용  
양식 복붙해서 써주세용~ㅎ  
가장 최근 수정 내역 위에다가 작성합시다

***
수정일 : 2024-11-29
수정인 : 우재연
- user interface 완료
- class_detail.html, community_detail.html

***
수정일 : 2024-11-29
수정인 : 정세은
- (이름)부분에 로그인한 user_id 반영되도록 하는 것 기능 구현 완료

***
수정일 : 2024-11-28
수정인 : 정세은
- 사이드바 마이페이지 누르면 마이페이지html로, 클래스 누르면 클래스html로 넘어가도록 함.
- 아이디 변경, 비밀번호 변경 구현 완료.
- 남은 것: 크게 보면 클래스 마이페이지로 끌어오는 것, (이름)부분에 로그인한 user_id 반영되도록 하는 것(하는중)

- 추가:
- 친절한 코드 빌드 방법 설명
- 
- 위의 코드를 실행하면 실행하고 있는 폴더와 동일한 폴더에 static 파일 하나가 생성됨.
- 새로 생성되는 static파일 속에는 빈 upload랑 user폴더가 있는데, 그 두 개 폴더 안에다가 넣지 말고 그냥 새로 생성된 static 폴더 안에다가 user.csv파일을 복붙해서 넣어야함.
- user.csv는 원래있던 static 파일 속에 넣어놨음. 경로로 설명하면 c_project/static/user.csv

- user.csv 파일을 옮긴 이후엔 sln 파일 빌드해서 파일 경로들 싹 바꿔줘야하는데, vscode에선 실행하는 법 모르겠고, visualstudio들어가서 c_project/C_function/C_fuction.sln 열면 안에 c파일들 있는거 보일거임.
- ctrl shift b 누르면 dll파일 다시 생성되서 경로 본인 컴퓨터로 바뀔거임.

- 다시 vscode로 넘어가서 app.py 실행하면 됨.

- 더해서 c언어 기능 작업하는 사람 있다면, c언어 파일 하나 수정할 때마다 vs가서 빌드 다시 해줘야 바뀐거 적용됨.
- 폴더명 바꾸더라도 다시 빌드해줘서 경로 바꿔줘야함.



***
수정일 : 2024-11-12
수정인 : 정인성
- 웹 실행에 불필요한 파일 제거 후 업로드
- 전제 html파일을 html, css, js파일로 분리

***
수정일 : 2024-11-10
수정인 : 정인성
- sign_up.html 파일 html, css, js로 분리
- C_function 파일에서 웹 실행에 불필요한 파일 제거

***
수정일 : 2024-11-09
수정인 : 정인성
- 웬만한거 다 구현 끗~

***
수정일 : 2024-11-06
수정인 : 정세은
- 마이페이지 UI 완료, 기능 구현 어려운 부분은 수정 필요
  
***
수정일 : 2024-11-04
수정인 : 정인성
- 90% 완료
- 회원가입 신청 버튼 오류 수정완료
- admin페이지에서 거절버튼 만들기
- 웹 다시 실행해도 admin페이지에 정보 남아있게 만들기
- 사람 많아질거 대비해서 로그인 할 때 해시나 이분탐색 쓰면 괜찮을듯,,

***
수정일 : 2024-10-29
수정인 : 우재연
- 70% 완료
- 커뮤니티, 클래스 구현 완료
- 클래스 및 커뮤니티 게시물 추가 관련 수정 필요 백엔드와 논의 후 방향 잡을 듯

***
수정일 : 2024-10-29
수정인 : 정인성
- 80% 완료
- 회원가입 신청 버튼 안 눌리는거 수정해야함 개같은거

***
수정일 : 2024-10-26  
수정인 : 정인성  
- 로그인 c로 구현 완료
- 로그인 <-> 회원가입 전환 다시 구현해야함

***
수정일 : 2024-10-05  
수정인 : 정인성  
- 로그인, 회원가입 ui 구현 완료  
- 로그인에서 회원가입으로, 회원가입에서 로그인으로 넘어가기 구현 완료  
- 회원가입에서 파일 업로드 구현 완료








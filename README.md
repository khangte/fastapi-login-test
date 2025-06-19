# FastAPI 회원가입 구현

## 개발환경 구성 
### 시스템 환경
- 가상화 플랫폼: VirtualBox + Ubuntu 22.04 Server
- 메모리: 8GB
- 프로세서: 4개 이상(pycharm, vscode 사용 때문)
- 비디오메모리: 16MB
- 모니터개수: 1개
- 저장소 메모리: 16~25GB
- 네트워크: NAT + 포트포워딩
### 백엔드
- 프레임워크: FastAPI
- 서버 실행: Uvicorn
- 개발 환경: PyCharm
### 프론트엔드
- 프레임워크: Svelte
- UI 라이브러리: Bootstrap 5.3.6
- 개발환경: Visual Studio Code
### 데이터베이스 
- RDBMS: MySQL 
- 구동 방식: Docker Container
- 데이터 유지: Docker Volume

---

## 파일 구조
```
login-test/
├── domain/
│   ├── common/
│   │   └── enums.py
│   └── user/
│       ├── user_crud.py
│       ├── user_router.py
│       └── user_schema.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Error.svelte
│   │   │   └── Navigation.svelte
│   │   ├── lib/
│   │   │   ├── api.js
│   │   │   └── store.js
│   │   ├── routes/
│   │   │   ├── auth
│   │   │   │   └── VerifyPassword.svelte
│   │   │   ├── user_update
│   │   │   │   ├── UpdatePassword.svelte
│   │   │   │   └── UpdateUser.svelte
│   │   │   ├── Home.svelte
│   │   │   ├── UserCreate.svelte
│   │   │   ├── UserDelete.svelte
│   │   │   ├── UserLogin.svelte
│   │   │   └── UserProfile.svelte
│   │   ├── app.css
│   │   ├── App.svelte
│   │   ├── main.js
│   │   └── vite-env.d.ts
│   ├── .env
│   ├── .gitignore
│   ├── index.html
│   ├── jsconfig.json
│   ├── package-lock.json
│   └── package.json
│
├── migrations/
│   ├── versions/
│   └── env.py
│
├── .env
├── alembic.ini
├── database.py
├── main.py
├── models.py
├── README.md
└── requirements.txt
```

---

## 개발환경 설정

### uv 가상환경
- 가상환경 생성
```
$ uv venv --python 3.11
```
- 가상환경 활성화
```bash
$ source .venv/bin/activate 
```

### Svelte 설치 (frontend 생성 전)
```bash
$ npm create vite@latest frontend -- --template svelte
$ cd frontend
$ npm install
```
- jsconfig.json 타입스크립트 사용 안함 => false로 변경
```json
파일명: /frontend/jsconfig.json
{
  (...생락...)
  "checkJs": false
  (...생락...)
}
```

### 데이터베이스 마이그레이션 (Alembic) 

1. Alembic 초기화
```bash
alembic init migrations
```
2. 설정 파일 수정
- ```alembic.ini```수정
- ```migrations/env.py```수정
```python
 from models
 target_metadata = models.Base.metadata
```
3. 변경사항 감지하고 마이그레이션 파일 생성
```bash
alembic revision --autogenerate
```
4. DB에 적용
```bash
alembic upgrade head
```

---

## MySQL 서버 구성
- Docker + Volume
- Windows Docker Desktop 환경
 
✅ **1. Docker Volume 생성** (Windows PowerShell에서 실행 가능)
```bash
docker volume create mysql-volume
```

✅ **2. MySQL 컨테이너 실행** (Windows Docker Desktop 기준)
```bash
- 컨테이너 처음 생성 시
docker run -d ^
  --name my-mysql ^
  -e MYSQL_ROOT_PASSWORD=1234 ^
  -e MYSQL_DATABASE=testdb ^
  -p 3306:3306 ^
  -v mysql-volume:/var/lib/mysql ^
  --restart unless-stopped ^
  mysql:8.0

- 기존 컨테이너 실행 시
docker start my-mysql
```

🔸 `--restart unless-stopped`: Windows 재시작 후 Docker Desktop이 다시 실행되면 컨테이너도 자동 실행됨  
🔸 `-v mysql-volume:/var/lib/mysql`: MySQL 데이터를 Docker Volume에 저장하여 컨테이너를 재생성해도 데이터 보존  
🔸 `MYSQL_DATABASE=testdb`: 초기 데이터베이스 자동 생성

✅ **3. MySQL 컨테이너 상태 확인**
```bash
docker ps
```
 
✅ **4. PowerShell에서 현재 IP 확인 (ifconfig는 Linux 명령어입니다)**
```powershell
ipconfig
```

🔍 `이더넷 어댑터`, `Wi-Fi`, 또는 `vEthernet (Default Switch)` 중  
**IPv4 주소** 항목에서 `192.168.x.x` 또는 `10.x.x.x` 와 같은 IP를 찾습니다.
```
예시: 
이더넷 어댑터 이더넷 2:
   IPv4 주소 . . . . . . . . . : 192.0.0.0
```

✅ **5. Ubuntu (WSL or VirtualBox)에서 MySQL 접속**
```bash
예시: 
mysql -h 192.168.0.101 -P 3306 -u root -p
```
비밀번호: 1234

📌 Ubuntu에서 `localhost → Docker(MySQL)`에 접근하려면 Docker가 `3306` 포트를 로컬에 노출하고 있어야 합니다.  
위 `-p 3306:3306` 설정으로 자동 처리됩니다.

✅ **6. FastAPI의 `SQLALCHEMY_DATABASE_URL` 설정**
```python
예시:
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@192.168.0.101:3306/testdb"
```
📌 `localhost`로 접속이 되지 않을 경우 반드시 위처럼 **Windows의 실제 IP 주소를 지정**해야 합니다.

---

## 실행코드

### 개발중
1. 백엔드 실행 (FastAPI)
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
2. 프론트엔드 실행 (Svelte + Vite 개발 서버)
```bash
$ cd frontend
$ npm run dev
```
3. 개발 서버 접속 ```URL: **localhost:5173**```

---

### 배포용
1. 프론트엔드 빌드
```bash
$ cd frontend
$ npm run build
```
2. 프론트엔드 정적 파일 서빙 설정
```python
# main.py 에 추가
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
origins=["http://localhost:8000", # 배포 서버]
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))
@app.get("/") # / 경로로 접속하면 frontend/dist/index.html 파일을 읽어서 서비스 한다.
def index():
   return FileResponse("frontend/dist/index.html")
```
3. 백엔드 실행 (FastAPI)
```bash
$ uvicorn main:app --host 0.0.0.0 --port 8000
```
4. FastAPI 서버 접속 ```URL: **localhost:8000**```

---

## MySQL 서버 사용 방법(Docker 사용 X)
1.mysql 설치
```bash
$ sudo apt update
$ sudo apt install mysql-server
```

2. mysql 서버 실행 상태 확인
```bash
$ sudo service mysql status
```
 
3. MySQL 로그인
```bash
$ mysql -u root -p
```

※ 에러 메시지
```bash
ERROR 1698 (28000): Access denied for user 'root'@'localhost'
=> root 유저가 패스워드 인증이 아닌 
"auth_socket" 방식으로만 로그인이 가능하도록 설정되어 있기 때문!
```
- 해결방법
```bash
$ sudo mysql
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';
> FLUSH PRIVILEGES;
```

- MySQL은 서버 기반 DB이기 때문에, DB가 서버 내에 직접 있어야함.
- 즉, 미리 CREATE DATABASE를 해서 DB를 생성해야됨.
```sql
CREATE DATABASE login_test 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

---
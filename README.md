# sgcc-web-study

## 프로젝트 구조

### 폴더 구조

`src/lib/components`에 스벨트 컴포넌트들을 담는다. `Memo.svelte`가 이 폴더 안에 있다.

이 `Memo.svelte`를 `src/routes/+page.svelte`에서 불러와서 사용한다.

- `/service`: FastAPI 백엔드 & 서버용 스크립트
    - gunicorn.socket: systemd용 소켓 파일
        - FastAPI용 소켓 정의
    - gunicorn.service: systemd용 서비스 스크립트
        - Uvicorn을 통한 FastAPI용 소켓 활성화 및 main.py 실행 스크립트
    - main.py: FastAPI 백엔드 코드
        - MariaDB로 구현한 데이터베이스와 연결 및 초기 설정
        - 애플리케이션 생명주기 및 리소스 초기화
        - FastAPI 앱 인스턴스 생성 및 애플리케이션 생명주기 연결
        - API Endpoint 정의 
        

### `Memo.svelte` 구조

- `memoText`: 현재 작성하고 있는 마크다운 평문을 담는 변수이다.

- `savedMemoText`: 저장된 마크다운 평문을 담는 변수이다. (메모를 저장하면 `memoText`에 담긴 변수가 `savedMemoText`에 대입되어 저장된다.)

- `markdownRenderedMemoText`: 마크다운 평문(`memoText`)이 HTML 태그로 바뀐 변수이다.

- `isModalOpen`: 메모를 클릭했을 때 모달 창(메모를 수정하는 창)이 열렸는지 아닌지를 저장하는 변수이다.

- `marked.use()` 메소드로 코드 하이라이팅, 깃허브 마크다운 문법, 줄바꿈 등을 설정한다.

- `{@html markdownRenderedMemoText}`을 이용해 `markdownRenderedMemoText`을 실제 HTML 태그로 렌더링한다.

- `updateMarkdownRenderedMemoText()` 함수를 이용하여 마크다운 평문(`memoText`)가 바뀔 때마다 오른쪽 화면(`markdownRenderedMemoText`)을 재렌더링한다.

- 닫기 버튼은 `closeModal` 함수를 호출해 모달 창을 닫고, 저장 버튼은 `saveMemo` 함수를 호출해 `memoText`에 담긴 변수를 `savedMemoText`에 대입하고 창을 닫는다.

--- 

## Manual Deployment Steps

### 1. SvelteKit 애플리케이션 빌드하기

```bash
cd directory-to-repository
npm run build
```

### 2. 애플리케이션 서비스 설치 및 시작 (아치 리눅스 기준)

```bash
# Copy service file
sudo cp service/sgcc-memo-app.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable sgcc-memo-app
sudo systemctl start sgcc-memo-app

# Check status
sudo systemctl status sgcc-memo-app
```

### 3. Nginx 설정 수정하기

```bash
# Backup existing config
sudo cp /etc/nginx/sites-available/memo-demo.com /etc/nginx/sites-available/memo-demo.com.backup

# Copy new config
sudo cp service/memo-demo.com.fixed /etc/nginx/sites-available/memo-demo.com

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 4. 배포 확인

```bash
# Check SvelteKit app
curl http://163.239.88.120:3000/

# Check nginx proxy
curl http://163.239.88.120/

# Check API access
curl http://163.239.88.120/memos/
```

## 서비스 관리

```bash
# Start the service
sudo systemctl start sgcc-memo-app

# Stop the service
sudo systemctl stop sgcc-memo-app

# Restart the service
sudo systemctl restart sgcc-memo-app

# Check service status
sudo systemctl status sgcc-memo-app

# View logs
sudo journalctl -u sgcc-memo-app -f
```

## Troubleshooting

### 서비스가 실행 중인지 확인하기:
```bash
# Check if SvelteKit app is on port 3000
lsof -i :3000

# Check if FastAPI is on port 8000
lsof -i :8000

# Check nginx status
sudo systemctl status nginx
```

### 로그 보기:
```bash
# SvelteKit app logs
sudo journalctl -u sgcc-memo-app -f

# Nginx access logs
sudo tail -f /var/log/nginx/sgcc-memo-demo.access.log

# Nginx error logs
sudo tail -f /var/log/nginx/sgcc-memo-demo.error.log
```

### 흔하게 등장하는 문제 해결:

1. **Port already in use**: 해당 포트를 사용하고 있는 프로세스를 강제로 종료시킴.
   ```bash
   pkill -f "node build/index.js"
   ```

2. **Permission denied**: 파일 권한 확인
   ```bash
   ls -la /home/rvnnt/sgcc-web-study/build/
   ```

3. **API not accessible**: FastAPI 백엔드 프로그램이 실행 중인지 확인
   ```bash
   # Start FastAPI if needed
   cd /home/rvnnt/sgcc-memo-demo
   python main.py
   ```

## Architecture

- **Nginx** (Port 80) → Reverse proxy
  - `/memos/` → FastAPI backend (Port 8000)
  - All other routes → SvelteKit app (Port 3000)
- **SvelteKit App** (Port 3000) → Node.js server with SSR
- **FastAPI Backend** (Port 8000) → Memo API and database

## Files Modified

- `service/nginx.conf` → Fixed nginx configuration
- `service/sgcc-memo-app.service` → Systemd service
- `src/lib/api.ts` → API base URL for SSR/client
- `svelte.config.js` → Changed to adapter-node
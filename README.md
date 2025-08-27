# sgcc-web-study

2025년 1학기 SGCC 웹 스터디의 프로젝트로, 동아리 서버 위에서 작동하는 메모 앱을 만들었습니다.

## 프로젝트 구조

- `/src/lib/`: 라이브러리
    - `types.ts`: 자료형 정의
    - `api.ts`: 클라이언트 계층 API
        - 생성, 읽기, 갱신, 삭제 인터페이스
        - 메모 탐색 기능
        - 오류 처리
    - `utils.ts`: 유틸리티 함수
        - `debounce()`: 기능 개선을 위한 유틸리티 함수
    - `markdown.ts`: 마크다운 처리 엔진
        - Github Flavored Markdown 사용
        - 하이라이트 기능
        - `DOMPurify`를 통한 XSS 공격 방지
    - `markdown.css`: 마크다운 스타일링
        - 폰트 및 헤더
        - 코드 블록
        - 링크, 인용구, 표 등 인터랙티브 요소
        - 리스트
        - 텍스트 색상
    - `/component`: 컴포넌트 라이브러리
        - `MemoCard.svelte`: 개별 메모 관련 코드
            - 메모 카드 표시 및 상태 관리
            - 바로 옆에서 미리보기가 가능한 마크다운 편집기
            - 편집 내용의 실시간 업데이트
            - 생성, 읽기, 갱신, 삭제 버튼
            - 반응형 디자인
        - `MemoPlus.svelte`: 메모 생성 관련 코드
            - 새로운 메모 생성을 위한 "+" 버튼
            - 메모 인터페이스
            - 메모의 제목과 컨텐츠가 적혀있는지 확인
            - 홈페이지에서 메모 미리보기
        - `MarkdownEditor.svelte`: 메모 편집기
            - 실시간 미리보기
            - 편집 인터페이스
            - 홈페이지에서 메모 미리보기
- `/src/routes`: 라우팅
    - `+layout.svelte`: 글로벌 레이아웃
        - CSS 불러오기
        - 내부 라우팅 설정
    - `+page.server.ts`: SSR 데이터 로딩
        - SSR 데이터 가져오기
        - 오류 처리
        - 타입 에러 예방
    - `+page.svelte`: 메인 페이지
        - 메모 정렬 기능
        - 그리드 형태로 메모 배치
        - ID에 따른 색깔 지정
        - 요소 통합
- `/service`: FastAPI 백엔드 & 서버용 스크립트
    - `gunicorn.socket`: systemd용 소켓 파일
        - FastAPI용 소켓 정의
    - `gunicorn.service`: systemd용 서비스 스크립트
        - Uvicorn을 통한 FastAPI용 소켓 활성화 및 `main.py` 실행 스크립트
    - `main.py`: FastAPI 백엔드 코드
        - MariaDB로 구현한 데이터베이스와 연결 및 초기 설정
        - 애플리케이션 생명주기 및 리소스 초기화
        - FastAPI 앱 인스턴스 생성 및 애플리케이션 생명주기 연결
        - API Endpoint 정의 
    - `memo-demo.com`, `nginx.conf`: nginx 서버 설정 파일
        - 웹 서버의 전체적인 동작 방식 정의
        - HTTP 트래픽 처리
        - 프론트엔드 & 백엔드 서비스와의 연결 정의
        - `gzip` 압축 활성화를 통해 네트워크 트래픽 감소 및 클라이언트의 로딩 속도 개선
    - `sgcc-memo-app.service`: systemd용 서버 스크립트 파일
        - 언제든지 서버에 접속했을 때 서비스를 이용할 수 있도록 재시작 및 환경 변수 설정.
        

### 메모 기능 구조

- `memoText`: 현재 작성하고 있는 마크다운 평문을 담는 변수이다.

- `savedMemoText`: 저장된 마크다운 평문을 담는 변수이다. (메모를 저장하면 `memoText`에 담긴 변수가 `savedMemoText`에 대입되어 저장된다.)

- `markdownRenderedMemoText`: 마크다운 평문(`memoText`)이 HTML 태그로 바뀐 변수이다.

- `isModalOpen`: 메모를 클릭했을 때 모달 창(메모를 수정하는 창)이 열렸는지 아닌지를 저장하는 변수이다.

- `marked.use()` 메소드로 코드 하이라이팅, 깃허브 마크다운 문법, 줄바꿈 등을 설정한다.

- `{@html markdownRenderedMemoText}`을 이용해 `markdownRenderedMemoText`을 실제 HTML 태그로 렌더링한다.

- `updateMarkdownRenderedMemoText()` 함수를 이용하여 마크다운 평문(`memoText`)가 바뀔 때마다 오른쪽 화면(`markdownRenderedMemoText`)을 재렌더링한다.

- 닫기 버튼은 `closeModal` 함수를 호출해 모달 창을 닫고, 저장 버튼은 `saveMemo` 함수를 호출해 `memoText`에 담긴 변수를 `savedMemoText`에 대입하고 창을 닫는다.

### API

| 기능 유형         | Method & Endpoint                                         | 설명                        |
|-----------------------|-----------------------------------------------------------|------------------------------------|
| **Create**            | `POST /memos/`                                            | 새 메모 생성                    |
| **List**              | `GET /memos/`                                             | 모든 메모 가져오기         |
| **Get**               | `GET /memos/123`                                          | ID로 특정 메모 가져오기                  |
| **Update**            | `PUT /memos/123`                                          | 메모 업데이트              |
| **Delete**            | `DELETE /memos/123`                                       | 메모 삭제                        |
| **Search (text)**     | `GET /memos/search/?q=keyword`                            | 텍스트로 검색                        |
| **Search (keywords)** | `GET /memos/list-by-keywords/?keywords=work+todo`         | 키워드로 검색               |
| **Filter (tags)**     | `GET /memos/list-by-tags/?tags=urgent,work`               | 태그로 필터링                      |
| **Filter (priority)** | `GET /memos/list-by-priority/?priority=3`                 | 우선순위로 필터링               |
| **Filter (category)** | `GET /memos/list-by-category/?category=work`              | 카테고리로 필터링                    |
| **Favorites**         | `GET /memos/list-favorites/`                              | 즐겨찾기에 등록된 메모만 가져오기                     |
| **Archived**          | `GET /memos/list-archived/`                               | 저장된 메모만 가져오기                      |
| **Recent**            | `GET /memos/list-recent/?days=30&order_by=updated`        | 최근 편집된 메모부터 가져오기                    |
| **Date Range**        | `GET /memos/list-by-date/?start_date=2024-01-01`          | 생성일자로 특정 메모 가져오기               |


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
sudo cp service/memo-demo.com /etc/nginx/sites-available/memo-demo.com

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

- **Nginx** (80번 포트) → 리버스 프록시
  - `/memos/` → FastAPI 백엔드 (8000번 포트)
  - 그 외 → SvelteKit 프론트엔드 (3000번 포트)
- **SvelteKit App** (3000번 포트) → Node.js 서버 (SSR 적용)
- **FastAPI Backend** (8000번 포트) → API 및 데이터베이스
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
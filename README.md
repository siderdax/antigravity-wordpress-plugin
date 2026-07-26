# Antigravity WordPress Plugin

Google Antigravity 에이전트를 위한 WordPress.com REST API 제어 및 스킬 플러그인입니다.

## 📁 디렉토리 구조
```text
antigravity-wordpress-plugin/
├── plugin.json                              # Antigravity 플러그인 매니페스트
├── README.md
├── scripts/
│   └── wp_cli.py                            # Python 기반 WordPress CLI 유틸리티
└── skills/
    └── wordpress-management/
        └── SKILL.md                         # Antigravity 스킬 가이드 문서
```

## 🛠️ 설치 및 설정 방법 (Antigravity CLI)

### 1. 전역 플러그인 경로 복사
개발 폴더의 수정 및 삭제 영향 없이 독립적으로 동작하도록 Antigravity CLI 전역 플러그인 디렉터리에 복사합니다:

```bash
mkdir -p ~/.gemini/antigravity-cli/plugins/wordpress-plugin
rsync -av ~/Projects/antigravity-wordpress-plugin/ ~/.gemini/antigravity-cli/plugins/wordpress-plugin/
```

### 2. Antigravity CLI 플러그인 등록
`agy plugin install` 명령어로 복사된 플러그인을 Antigravity CLI에 등록합니다:

```bash
agy plugin install ~/.gemini/antigravity-cli/plugins/wordpress-plugin
```

설치 상태 확인:
```bash
agy plugin list
```

### 3. 환경 변수 (인증 정보) 설정
`~/.gemini/antigravity-cli/.env` 또는 `~/.gemini/antigravity-cli/plugins/wordpress-plugin/.env` 파일에 WordPress API 인증 정보를 설정합니다:

```env
WORDPRESS_SITE_ID="165329412"
WORDPRESS_SITE_URL="steelcup.home.blog"
WORDPRESS_ACCESS_TOKEN="<YOUR_WORDPRESS_ACCESS_TOKEN>"
WORDPRESS_CLIENT_ID="144537"
```

---

## 🔑 시크릿 (인증 정보) 발급 및 확인 방법

WordPress.com REST API 연동에 필요한 정보들을 발급받는 방법입니다.

### 1. Client ID 및 Client Secret 발급
1. [WordPress.com Developer Applications](https://developer.wordpress.com/apps/) 관리 페이지에 접속합니다.
2. **Create New Application** 버튼을 클릭합니다.
3. 앱 이름, 설명, **Redirect URL** (예: `http://localhost`)을 작성 후 앱을 등록합니다.
4. 앱이 생성되면 부여된 **Client ID**를 확인합니다.

### 2. Access Token (액세스 토큰) 발급
* **OAuth2 인증 절차**:
  1. 웹 브라우저에서 인증 URL에 접속하여 응답 코드를 획득합니다:
     ```text
     https://public-api.wordpress.com/oauth2/authorize?client_id=<YOUR_CLIENT_ID>&redirect_uri=<YOUR_REDIRECT_URI>&response_type=code
     ```
  2. 사용자 승인 후 리다이렉트된 URL의 `code=` 파라미터 값을 복사합니다.
  3. `https://public-api.wordpress.com/oauth2/token` 주소로 `POST` 요청을 보낸 후 `access_token`을 발급받습니다.
* **개발자 콘솔 / 테스트 용도**:
  * [WordPress.com Developer Console](https://developer.wordpress.com/docs/api/console/) 또는 API 테스트 도구(Postman 등)에서 OAuth2 인증을 진행하여 테스트용 `access_token`을 빠르게 발급받을 수 있습니다.

### 3. Site ID 확인 방법
* **API 호출로 확인**: `access_token` 발급 후 다음 curl 명령어로 본인의 블로그 ID를 조회할 수 있습니다:
  ```bash
  curl -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" https://public-api.wordpress.com/rest/v1.1/me/sites
  ```
  응답 결과 JSON의 `ID` 항목(예: `165329412`)을 확인합니다.
* **도메인 사용**: WordPress.com REST API는 숫자 `SITE_ID` 외에도 `steelcup.home.blog`와 같은 도메인 주소를 사이트 식별자로 사용할 수 있습니다.

---

## 🚀 사용법

### CLI 유틸리티 사용 (직접 실행)
```bash
# 최근 포스트 목록 조회
python3 ~/.gemini/antigravity-cli/plugins/wordpress-plugin/scripts/wp_cli.py posts list -n 5

# 새 글 발행
python3 ~/.gemini/antigravity-cli/plugins/wordpress-plugin/scripts/wp_cli.py posts create \
  --title "포스트 제목" \
  --content "<h1>내용</h1><p>포스트 내용...</p>" \
  --categories "Development" \
  --tags "Python, CLI"

# 카테고리/태그 목록 확인
python3 ~/.gemini/antigravity-cli/plugins/wordpress-plugin/scripts/wp_cli.py categories list
python3 ~/.gemini/antigravity-cli/plugins/wordpress-plugin/scripts/wp_cli.py tags list
```

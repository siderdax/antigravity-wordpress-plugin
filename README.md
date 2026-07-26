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

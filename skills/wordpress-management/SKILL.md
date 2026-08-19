---
name: "wordpress-management"
description: "WordPress.com REST API management skill for Antigravity Agent using Python CLI script"
---

# Antigravity WordPress Management Skill

이 스킬은 WordPress.com 블로그(`steelcup.home.blog`)의 포스트 작성, 수정, 삭제, 카테고리 및 태그 관리를 Antigravity 에이전트에서 원활하게 수행할 수 있도록 지원합니다.

---

## 1. 전용 Python CLI 실행 스크립트 위치

* **CLI 경로**: `~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py`
* **인증 정보**: `~/.hermes/.env` 파일의 `WORDPRESS_ACCESS_TOKEN` 및 `WORDPRESS_SITE_ID` 사용

---

## 2. 주요 CLI 명령법 및 사용 가이드

### A. 최근 포스트 목록 조회
```bash
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts list -n 5
```

### B. 특정 포스트 상세 조회
```bash
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts get <POST_ID>
```

### C. 새 포스트 작성 (발행 또는 임시저장)
```bash
# 발행(Publish)
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts create \
  --title "포스트 제목" \
  --content "<h1>내용</h1><p>포스트 내용...</p>" \
  --categories "Development" \
  --tags "JavaScript, Web" \
  --status publish

# 임시저장(Draft)
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts create \
  --title "임시 저장글" \
  --content "Draft content..." \
  --status draft
```

### D. 기존 포스트 수정
```bash
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts update <POST_ID> \
  --title "수정된 제목" \
  --tags "Linux, CLI"
```

### E. 포스트 삭제
```bash
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts delete <POST_ID>
```

### F. 카테고리 및 태그 조회 / 정리
```bash
# 카테고리 목록 조회
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py categories list

# 태그 목록 조회
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py tags list

# 미사용(Count 0) 태그 일괄 정리
python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py tags cleanup
```

---

## 3. 표준 블로그 카테고리 참고

* `Development`: 개발, 언어(JS/TS, Python), 프론트엔드/백엔드, API
* `OS & Environment`: Linux, Windows, 라즈베리 파이 OS, CLI 환경
* `Network & Security`: 네트워크, Nginx, VPN, 보안, Auth
* `Infra & DevOps`: Docker, Grafana, 모니터링, 데브옵스
* `Embedded & Hardware`: 임베디드, ROS, MQTT, 하드웨어
* `Review & Tips`: 소프트웨어/기기 리뷰, 생산성 팁

---

## 4. OAuth2 토큰 갱신 절차 (`HTTP 400: invalid_token` 발생 시)

1. **사용자 승인 링크 제공**:
   - URL: `https://public-api.wordpress.com/oauth2/authorize?client_id=144537&redirect_uri=https://steelcup.home.blog/&response_type=code`
   - 사용자에게 승인 후 이동한 주소(`https://steelcup.home.blog/?code=<code>`) 전달 요청

2. **Access Token 교환**:
   - `POST https://public-api.wordpress.com/oauth2/token`
   - Data: `client_id=144537`, `client_secret=...`, `redirect_uri=https://steelcup.home.blog/`, `grant_type=authorization_code`, `code=<code>`

3. **.env 파일 업데이트**:
   - `C:\Users\USER\Projects\antigravity-wordpress-plugin\.env` 및 `C:\Users\USER\.gemini\config\plugins\wordpress-plugin\.env` 내 `WORDPRESS_ACCESS_TOKEN` 신규 토큰으로 갱신

---

## 5. 포스팅 작성 문체 및 서식 규칙 (필수 준수)

1. **이모지 사용 금지**:
   - 포스트 제목, 본문, 소제목 전체에서 이모지(😀, 🚀, 📌, ⚠️ 등)를 절대 사용하지 않는다.

2. **결론, 요약, 정리 및 교훈 섹션 작성 금지**:
   - 포스팅 끝 또는 본문에 "결론", "요약", "마무리", "총평", "정리", "교훈" 등의 별도 세션을 작성하지 않는다.

3. **기본 문체 (본문 전체)**:
   - 일반 본문 설명 문장은 `~다` 어미로 끝낸다 (`~한다`, `~다`, `~가 있다`).

4. **부연 설명 문장 명사 종결 규칙**:
   - **하위 내용(코드, 목록 항목 등)을 설명하거나 상단 이미지/코드를 설명하는 짧은 부연 설명 문장만** 반드시 **명사**로 종결한다.
   - **예시 구분**:
     - *일반 본문 설명 문장*: `리눅스에서 이전 디렉터리로 이동할 때는 cd 명령어를 사용한다.`
     - *하위/이미지/코드 부연 설명 문장*: `하단 코드 내용은 데이터를 클리어하는 코드.` / `상위 경로로 이동하기 위한 커맨드.` / `역방향 대화형 검색을 실행하는 단축키.`




---
name: "wordpress-management"
description: "WordPress.com REST API management skill for Antigravity Agent using Python CLI script"
---

# Antigravity WordPress Management Skill

이 스킬은 WordPress.com 블로그(`steelcup.home.blog`)의 포스트 작성, 수정, 삭제, 카테고리 및 태그 관리를 Antigravity 에이전트에서 원활하게 수행할 수 있도록 지원합니다.

---

## 1. 전용 Python CLI 실행 스크립트 위치

* **CLI 경로**: `~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py`
* **인증 정보**: `~/.hermes/.env` 파일의 `WORDPRESS_ACCESS_TOKEN`, `WORDPRESS_CLIENT_ID`, `WORDPRESS_CLIENT_SECRET`, `WORDPRESS_REDIRECT_URI` 사용

---

## 1.1 토큰 만료 시 재인증 및 갱신 프로세스

API 호출 중 `invalid_token` (토큰 만료 또는 오류)이 발생하면 즉시 사용자에게 아래 재인증 링크를 제시하고, 사용자가 전달한 `code` 값으로 토큰을 자동 교환함:

1. **사용자 재인증 링크**:
   [https://public-api.wordpress.com/oauth2/authorize?client_id=144537&redirect_uri=https://steelcup.home.blog/&response_type=code](https://public-api.wordpress.com/oauth2/authorize?client_id=144537&redirect_uri=https://steelcup.home.blog/&response_type=code)
2. **토큰 자동 교환 명령**:
   ```bash
   python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py token --code <AUTHORIZATION_CODE>
   ```

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

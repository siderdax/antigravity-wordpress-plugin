---
name: "wordpress-blog-post-writer"
description: "WordPress 블로그 포스팅 작성 시 사용자 전용 어조(이모지 미사용, 기술 문서형 종결어미, 명사형 단답어미) 및 사전 구성 확인 -> 초안 검토 -> 안전한 Draft/Publish 단계로 발행하는 스킬"
---

# WordPress Blog Post Writer Skill

이 스킬은 WordPress 블로그(`steelcup.home.blog`)용 포스트를 작성할 때 사용자의 개별적인 글쓰기 스타일과 워드프레스 블록 규격을 준수하며, 사전 구성안 확인, 초안 검토, 그리고 실수 방지를 위한 안전한 Draft/Publish 단계를 거쳐 글을 저장 및 발행하는 지침을 정의함.

---

## 1. 스타일 및 문체 작성 규칙 (Writing Style Rules)

### A. 이모지 전면 금지 (No Emojis)
- 글 제목, 본문, 헤딩, 리스트, 표 등 포스트 전체에서 이모지를 절대로 사용하지 않음.

### B. 어조 및 종결 어미 (Tone & Sentence Endings)
- **메인 본문 서술어**: `~한다` 형태의 평서체(한다체) 사용. 구어체(`~해요`, `~입니다`)는 전면 금지함.
- **부연 설명 및 목록 항목**: `~함`, `~임` 형태의 음슴체 사용.
- **작은 설명 및 표/캡션/인자 비고 (명사형 종결)**:
  - 캡션, 인자 설명, 표 비고, 이미지/코드의 간략한 설명은 명사로 끝맺음.
  - *예시*:
    - `<이미지>: 특정 설정을 변경했을 때 나오는 화면` ("화면"으로 종결)
    - `listenport`: 외부에서 접속할 때 사용할 포트 번호 ("번호"로 종결)
    - `connectaddress`: WSL 터미널에서 `hostname -I`로 확인한 IP 주소 ("주소"로 종결)
    - 표 비고 및 변화량: `로그 상세 모니터링` ("모니터링"으로 종결), `97.7 MB 회수` ("회수"로 종결)

### C. 레이아웃 및 서식 구조
- **제목 번호링**: 목차 및 주요 단락 구분 시 `1.`, `1.1`, `2.` 등의 번호 체계 활용.
- **비교 분석 표**: 개념 비교나 특성 정리는 마크다운 표(`table`) 또는 HTML `<table>` 활용.
- **코드 및 디렉토리 구조**:
  - 디렉토리 트리는 `code` 블록 사용.
  - 명령어 및 스크립트는 적절한 언어 하이라이팅 적용.
- **구분선**: 단락 및 주요 섹션 전환 시 구분선(`<hr class="wp-block-separator" />` 또는 `---`) 활용.

---

## 2. 포스팅 작성 및 저장/발행 단계별 프로세스 (Workflow)

### Step 1. 사전 구성 항목 제시 및 동의 확인
- 초안 작성 전 포스트의 **목차 및 구성 항목(단락 구조)**을 먼저 정리하여 사용자에게 제시함.
- **"이 구성대로 포스트를 작성할지"** 사용자에게 확인 요청.

### Step 2. 초안 작성 및 검토 공유
- 동의받은 구성안을 바탕으로 글 규칙을 준수하여 초안 작성.
- 작성된 초안을 대화 메시지 또는 아티팩트(Artifact) 형태로 제시하여 **사용자에게 검토 요청**.

### Step 3. 안전한 Draft / Publish 분리 단계 (안전 장치)
- **A. "임시 저장해줘" / "드래프트로 올려줘" 요청 시**:
  - 사용자 질문 없이 즉시 `--status draft`로 임시 저장 실행.
- **B. "바로 포스팅해줘" / "발행해줘" 요청 시**:
  - **실수 방지 안전장치**: 아직 임시 저장(Draft)이 되지 않은 상태라면, 바로 발행하기 전에 **"임시 저장(Draft)으로 먼저 보관할지, 아니면 즉시 공개 발행(Publish)까지 진행할지"** 사용자에게 확인 질문을 수행함.
  - 임시 저장이 이미 완료되었거나 사용자가 공개 발행을 재확인한 경우 `--status publish` (또는 기존 draft글 status update) 진행.

---

## 3. 표준 포스팅 구성 항목 예시 (Template)

1. **개요 및 배경**: 다루고자 하는 기술/도구의 개념 및 문제 상황 정리
2. **원인 및 비교 분석**: 발생 원인 분석 및 기존 방식 vs 대안/개선 방식 비교
3. **구조/아키텍처**: 파일/디렉토리 구조 트리 및 메타데이터 정의
4. **단계별 실전 가이드**: Step-by-Step 구축 방법 및 코드 예시
5. **트러블슈팅 및 유의사항**: 실행 권한, 절대 경로 사용, 환경 변수 등 주의사항
6. **정리**: 포스트 핵심 요약 및 마무리

---

## 4. WordPress CLI 연동 명령

1. **카테고리/태그 조회**:
   ```bash
   python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py categories list
   python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py tags list
   ```
2. **임시 저장 (Draft)**:
   ```bash
   python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts create \
     --title "포스트 제목" \
     --content "Gutenberg HTML 내용..." \
     --categories "Development" \
     --tags "Antigravity, Python, CLI" \
     --status draft
   ```
3. **공개 발행 (Publish)**:
   ```bash
   python3 ~/Projects/antigravity-wordpress-plugin/scripts/wp_cli.py posts create \
     --title "포스트 제목" \
     --content "Gutenberg HTML 내용..." \
     --categories "Development" \
     --tags "Antigravity, Python, CLI" \
     --status publish
   ```

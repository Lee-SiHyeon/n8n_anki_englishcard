# 🎴 YouTube to Anki - Phrasal Verb Cards

YouTube 영상에서 자동으로 구동사(Phrasal Verbs)를 추출하여 Anki 플래시카드를 생성하는 n8n 워크플로우입니다.

![workflow](https://img.shields.io/badge/n8n-workflow-orange)
![license](https://img.shields.io/badge/license-MIT-blue)

## ✨ 주요 기능

- 🎬 **YouTube 자막 추출**: 영상 URL에서 자동으로 자막을 가져옴
- 🤖 **AI 구동사 필터링**: Gemini AI가 실용적인 구동사 문장을 선별
- 🔊 **Google TTS 음성**: 각 문장의 원어민 발음 오디오 생성
- 🎯 **구동사 하이라이트**: 문장에서 구동사를 자동으로 강조 표시
- 📚 **풍부한 학습 정보**:
  - 한국어 번역
  - 직역 vs 관용적 의미
  - 핵심 이미지 (particle의 의미)
  - 사용법 노트
  - **대체 표현/동의어**
  - **격식체 표현**
  - **추가 예문 2개**

## 📋 필수 요구사항

### 소프트웨어
- [n8n](https://n8n.io/) (v1.0 이상)
- [Anki](https://apps.ankiweb.net/) + [AnkiConnect](https://ankiweb.net/shared/info/2055492159) 플러그인
- Python 3.8+

### API 키 (무료)
- **Gemini API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 발급
- **Google Cloud TTS API Key**: [Google Cloud Console](https://console.cloud.google.com/)에서 발급

### Python 패키지
```bash
pip install spacy lemminflect flask youtube-transcript-api
python -m spacy download en_core_web_sm
```

## 🚀 설치 방법

### 1. Anki 설정
1. Anki 설치 후 [AnkiConnect](https://ankiweb.net/shared/info/2055492159) 애드온 설치
2. "YouTube English" 덱 생성 (또는 워크플로우에서 덱 이름 변경)

### 2. Python 서버 실행
```bash
# Lemma 서버 (동사 활용형 처리)
python lemma_server.py
```

또는 Windows에서:
```bash
start_lemma_server.bat
```

### 3. n8n 워크플로우 가져오기
1. n8n 열기
2. "Import from file" 선택
3. `workflow_export.json` 가져오기
4. API 키 설정 (코드 노드에서 직접 수정):
   - `YOUR_GEMINI_API_KEY` → 실제 Gemini API 키
   - `YOUR_GOOGLE_TTS_API_KEY` → 실제 Google TTS API 키

### 4. 워크플로우 활성화
1. n8n에서 워크플로우 열기
2. "Active" 토글 켜기

## 📖 사용 방법

### Webhook으로 실행
```bash
curl -X POST http://localhost:5678/webhook/youtube-english \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### Python으로 실행
```python
import requests

response = requests.post(
    'http://localhost:5678/webhook/youtube-english',
    json={'youtube_url': 'https://www.youtube.com/watch?v=VIDEO_ID'}
)
print(response.json())
```

## 📁 프로젝트 구조

```
├── workflow_export.json     # n8n 워크플로우 (메인)
├── lemma_server.py          # 동사 원형/활용형 서버 (Python)
├── start_lemma_server.bat   # Lemma 서버 실행 스크립트 (Windows)
└── README.md
```

## 🎴 생성되는 카드 예시

### 앞면 (Front)
```
문장: "I need to look into the budget for next month."
[오디오 재생 버튼]

LOOK + into = look into

📺 YouTube (0:05)
```

### 뒷면 (Back)
```
🔤 look into

📖 한국어:
다음 달 예산을 조사해 봐야겠어요.

🔍 의미 변화:
직역: 안을 들여다보다
➜ 관용: 조사하다, 검토하다

💡 핵심 이미지:
INTO의 핵심 이미지: 안쪽 깊숙이 시선을 보내는 동작

📝 사용법:
문제나 상황의 원인을 파악하기 위해 자세히 살펴볼 때 사용.

🔄 대체 표현:
investigate, examine, check out

👔 격식체:
investigate

✏️ 추가 예문:
• The police are looking into the cause of the accident.
• We are looking into new ways to reduce costs.
```

## ⚙️ 커스터마이징

### 덱 이름 변경
워크플로우의 "Process All Sentences" 노드에서:
```javascript
deckName: "YouTube English"  // 원하는 덱 이름으로 변경
```

### 선별 기준 변경
"Parse & Group Sentences" 노드의 Gemini 프롬프트를 수정하여 필터링 기준 조정 가능

## 🐛 문제 해결

### AnkiConnect 연결 오류
- Anki가 실행 중인지 확인
- AnkiConnect 애드온이 설치되어 있는지 확인
- 포트 8765가 열려 있는지 확인

### 자막 추출 실패
- 영상에 자막이 있는지 확인 (자동 생성 자막 포함)

### 하이라이트가 안 됨
- lemma_server.py가 실행 중인지 확인 (포트 8768)
- 영상 자막의 문장과 Gemini가 반환한 문장이 다를 수 있음 (Gemini 오류)

## 📄 라이선스

MIT License

## 🙏 기여

Pull Request와 Issue는 언제나 환영합니다!

---

Made with ❤️ for English learners

import requests
import json

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MzcyYzk4Yy1kODM0LTQ0NzMtODU4YS1jYjBjZjUyMmUzMWEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY2OTA0ODM3fQ.QW61lHVmTkUFEBYl1YxuqdW1xxVLh7Tr-E6-3-oniVw'
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# 기존 워크플로우 복제
r = requests.get('http://localhost:5678/api/v1/workflows/MD6PXu5l3rXpEFGA', headers=headers)
wf = r.json()

wf['name'] = 'Confusing English - 헷갈리는 표현'

for node in wf['nodes']:
    if 'Parse' in node['name'] and 'Group' in node['name']:
        new_code = '''// 헷갈리는 영어 표현 비교 카드 생성
const inputData = $input.first().json;
const videoId = inputData.videoId || "confusing";

// 헷갈리는 표현 카테고리
const confusingTopics = [
  // 단어 비교
  { type: "word", korean: "약속", words: ["promise", "appointment", "plan", "schedule"] },
  { type: "word", korean: "화장실", words: ["bathroom", "restroom", "toilet", "washroom"] },
  { type: "word", korean: "빌리다", words: ["borrow", "lend", "rent", "lease"] },
  { type: "word", korean: "듣다", words: ["hear", "listen"] },
  { type: "word", korean: "보다", words: ["see", "look", "watch"] },
  { type: "word", korean: "말하다", words: ["say", "tell", "speak", "talk"] },
  { type: "word", korean: "여행", words: ["travel", "trip", "journey", "tour"] },
  { type: "word", korean: "고치다", words: ["fix", "repair", "correct", "revise"] },
  { type: "word", korean: "만들다", words: ["make", "create", "produce", "build"] },
  { type: "word", korean: "얻다", words: ["get", "obtain", "acquire", "gain"] },
  
  // 문법 비교
  { type: "grammar", topic: "should have p.p vs could have p.p vs might have p.p", context: "과거 후회/추측" },
  { type: "grammar", topic: "will vs be going to", context: "미래 표현" },
  { type: "grammar", topic: "used to vs would vs be used to", context: "과거 습관" },
  { type: "grammar", topic: "must vs have to vs should", context: "의무 표현" },
  { type: "grammar", topic: "some vs any", context: "불특정 표현" },
  { type: "grammar", topic: "few vs a few vs little vs a little", context: "수량 표현" },
  { type: "grammar", topic: "since vs for", context: "시간 표현" },
  { type: "grammar", topic: "already vs yet vs still", context: "완료 시제" },
  { type: "grammar", topic: "although vs despite vs in spite of", context: "양보 표현" },
  { type: "grammar", topic: "so vs such", context: "강조 표현" },
];

// 랜덤 5개 선택
const selected = confusingTopics.sort(() => Math.random() - 0.5).slice(0, 5);

const prompt = `You are an expert English teacher who helps Korean speakers understand CONFUSING English expressions.

## Your Task
Explain the differences between similar English words/grammar that Korean speakers often confuse.

## Topics to Explain:
${selected.map((item, i) => {
  if (item.type === "word") {
    return `${i + 1}. [WORD] Korean "${item.korean}" → ${item.words.join(" vs ")}`;
  } else {
    return `${i + 1}. [GRAMMAR] ${item.topic} (${item.context})`;
  }
}).join("\\n")}

## Response Format (JSON array only):
[{
  "type": "word",
  "korean_meaning": "약속",
  "comparisons": [
    {
      "word": "promise",
      "definition": "A declaration that you will do something",
      "korean_def": "반드시 하겠다는 맹세/약속",
      "example": "I promise I'll call you tomorrow.",
      "example_korean": "내일 꼭 전화할게.",
      "usage_note": "주로 사람에게 하는 '맹세' 느낌의 약속"
    },
    {
      "word": "appointment",
      "definition": "A scheduled meeting with someone",
      "korean_def": "예약된 만남 (병원, 미용실 등)",
      "example": "I have a doctor's appointment at 3pm.",
      "example_korean": "3시에 병원 예약이 있어.",
      "usage_note": "공식적/전문적인 예약 (의사, 변호사 등)"
    }
  ],
  "common_mistakes": [
    {
      "wrong": "I have a promise with my friend.",
      "correct": "I have plans with my friend. / I'm meeting my friend.",
      "explanation": "친구와의 약속은 promise가 아니라 plans 또는 meeting"
    }
  ],
  "quick_tip": "promise = 맹세, appointment = 예약, plans = 일정/친구와의 약속"
},
{
  "type": "grammar",
  "topic": "should have p.p vs could have p.p vs might have p.p",
  "context": "과거에 대한 후회/추측",
  "comparisons": [
    {
      "pattern": "should have + p.p",
      "meaning": "~했어야 했는데 (후회)",
      "example": "I should have studied harder.",
      "example_korean": "더 열심히 공부했어야 했는데.",
      "nuance": "과거에 하지 않은 것에 대한 후회"
    },
    {
      "pattern": "could have + p.p",
      "meaning": "~할 수 있었는데 (가능성)",
      "example": "I could have helped you.",
      "example_korean": "내가 도와줄 수 있었는데.",
      "nuance": "과거에 가능했지만 하지 않은 것"
    },
    {
      "pattern": "might have + p.p",
      "meaning": "~했을지도 모른다 (추측)",
      "example": "He might have forgotten.",
      "example_korean": "그가 잊어버렸을지도 몰라.",
      "nuance": "과거 사실에 대한 불확실한 추측"
    }
  ],
  "quick_tip": "should = 후회, could = 가능성, might = 추측"
}]

Generate 5 detailed comparison cards.`;

return [{
  json: {
    prompt: prompt,
    topics: selected,
    videoId: videoId
  }
}];
'''
        node['parameters']['jsCode'] = new_code
        print(f"✅ Parse & Group Sentences 수정 완료")

    if 'Filter Practical' in node['name']:
        new_filter_code = '''// Gemini API로 헷갈리는 표현 비교 생성
const inputData = $input.first().json;
const prompt = inputData.prompt;
const videoId = inputData.videoId || "confusing";

const GEMINI_KEY = "YOUR_GEMINI_API_KEY";

const response = await this.helpers.httpRequest({
  method: "POST",
  url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`,
  headers: { "Content-Type": "application/json" },
  body: {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.7,
      maxOutputTokens: 5000,
    }
  },
  json: true
});

let comparisonCards = [];
try {
  const text = response.candidates[0].content.parts[0].text;
  const jsonMatch = text.match(/\\[\\s*\\{[\\s\\S]*\\}\\s*\\]/);
  if (jsonMatch) {
    comparisonCards = JSON.parse(jsonMatch[0]);
  }
} catch (e) {
  throw new Error("Failed to parse Gemini response: " + e.message);
}

return [{
  json: {
    comparisonCards: comparisonCards,
    videoId: videoId,
    count: comparisonCards.length
  }
}];
'''
        node['parameters']['jsCode'] = new_filter_code
        print(f"✅ Filter 노드 수정 완료")

    if 'Process All' in node['name']:
        new_process_code = '''// 헷갈리는 표현 비교 Anki 카드 생성
const inputData = $input.first().json;
const comparisonCards = inputData.comparisonCards || [];
const videoId = inputData.videoId || "confusing";

if (comparisonCards.length === 0) {
  return [{ json: { error: "No comparison cards", videoId } }];
}

const results = [];
const GOOGLE_TTS_KEY = "YOUR_GOOGLE_TTS_API_KEY";

for (let i = 0; i < comparisonCards.length; i++) {
  const card = comparisonCards[i];
  
  try {
    // 첫 번째 예문으로 TTS 생성
    let firstExample = "";
    if (card.type === "word" && card.comparisons?.[0]?.example) {
      firstExample = card.comparisons[0].example;
    } else if (card.type === "grammar" && card.comparisons?.[0]?.example) {
      firstExample = card.comparisons[0].example;
    }
    
    let audioTag = "";
    if (firstExample) {
      const ttsResponse = await this.helpers.httpRequest({
        method: "POST",
        url: `https://texttospeech.googleapis.com/v1/text:synthesize?key=${GOOGLE_TTS_KEY}`,
        headers: { "Content-Type": "application/json" },
        body: {
          input: { text: firstExample },
          voice: { languageCode: "en-US", name: "en-US-Neural2-J" },
          audioConfig: { audioEncoding: "MP3", speakingRate: 0.9 }
        },
        json: true
      });
      
      if (ttsResponse.audioContent) {
        const audioFileName = `confusing_${videoId}_${i + 1}.mp3`;
        await this.helpers.httpRequest({
          method: "POST",
          url: "http://127.0.0.1:8765",
          headers: { "Content-Type": "application/json" },
          body: {
            action: "storeMediaFile",
            version: 6,
            params: { filename: audioFileName, data: ttsResponse.audioContent }
          },
          json: true
        });
        audioTag = `[sound:${audioFileName}]`;
      }
    }
    
    // Front - 질문 형식
    let frontContent = "";
    if (card.type === "word") {
      frontContent = `
        <div style="background:#e3f2fd;padding:20px;border-radius:10px;">
          <div style="font-size:24px;text-align:center;margin-bottom:15px;">
            🤔 <b>"${card.korean_meaning}"</b>을 영어로?
          </div>
          <div style="text-align:center;color:#666;">
            ${card.comparisons.map(c => `<span style="background:#fff;padding:5px 15px;border-radius:20px;margin:5px;display:inline-block;">${c.word}</span>`).join(" ")}
          </div>
          <div style="text-align:center;color:#888;margin-top:15px;font-size:14px;">
            차이점이 뭘까요?
          </div>
        </div>
      `;
    } else {
      frontContent = `
        <div style="background:#fff3e0;padding:20px;border-radius:10px;">
          <div style="font-size:20px;text-align:center;margin-bottom:10px;">
            📚 <b>${card.topic}</b>
          </div>
          <div style="text-align:center;color:#666;font-size:14px;">
            ${card.context}
          </div>
          <div style="text-align:center;color:#888;margin-top:15px;font-size:14px;">
            각각 언제 사용할까요?
          </div>
        </div>
      `;
    }
    
    const front = `<div style="font-size:18px;line-height:1.8;color:#333;padding:10px;">${frontContent}</div>`;
    
    // Back - 상세 비교
    let comparisonsHtml = "";
    if (card.type === "word") {
      comparisonsHtml = card.comparisons.map((comp, idx) => `
        <div style="background:#f5f5f5;padding:12px;border-radius:8px;margin-bottom:10px;border-left:4px solid #1976d2;color:#333;">
          <div style="font-size:18px;font-weight:bold;color:#1976d2;">${comp.word}</div>
          <div style="font-size:13px;color:#666;margin:5px 0;">${comp.definition}</div>
          <div style="font-size:13px;color:#333;margin:5px 0;">→ ${comp.korean_def}</div>
          <div style="background:#e8f5e9;padding:8px;border-radius:5px;margin-top:8px;">
            ${idx === 0 ? audioTag : ""}
            <div style="color:#2e7d32;">"${comp.example}"</div>
            <div style="color:#666;font-size:12px;">${comp.example_korean}</div>
          </div>
          <div style="font-size:12px;color:#888;margin-top:5px;">💡 ${comp.usage_note}</div>
        </div>
      `).join("");
    } else {
      comparisonsHtml = card.comparisons.map((comp, idx) => `
        <div style="background:#f5f5f5;padding:12px;border-radius:8px;margin-bottom:10px;border-left:4px solid #7b1fa2;color:#333;">
          <div style="font-size:16px;font-weight:bold;color:#7b1fa2;">${comp.pattern}</div>
          <div style="font-size:14px;color:#333;margin:5px 0;">→ ${comp.meaning}</div>
          <div style="background:#f3e5f5;padding:8px;border-radius:5px;margin-top:8px;">
            ${idx === 0 ? audioTag : ""}
            <div style="color:#6a1b9a;">"${comp.example}"</div>
            <div style="color:#666;font-size:12px;">${comp.example_korean}</div>
          </div>
          <div style="font-size:12px;color:#888;margin-top:5px;">🎯 ${comp.nuance}</div>
        </div>
      `).join("");
    }
    
    // 흔한 실수
    let mistakesHtml = "";
    if (card.common_mistakes && card.common_mistakes.length > 0) {
      mistakesHtml = `
        <div style="margin-top:15px;">
          <b>🚫 흔한 실수:</b>
          ${card.common_mistakes.map(m => `
            <div style="background:#ffebee;padding:10px;border-radius:8px;margin-top:8px;color:#333;">
              <div style="color:#c62828;">❌ ${m.wrong}</div>
              <div style="color:#2e7d32;margin-top:5px;">✅ ${m.correct}</div>
              <div style="font-size:12px;color:#666;margin-top:3px;">${m.explanation}</div>
            </div>
          `).join("")}
        </div>
      `;
    }
    
    const back = `
<div style="font-size:16px;line-height:1.8;color:#333;">
  <div style="background:#fff8e1;padding:10px;border-radius:8px;margin-bottom:15px;color:#333;">
    <b>📝 Quick Tip:</b> ${card.quick_tip}
  </div>
  
  ${comparisonsHtml}
  ${mistakesHtml}
</div>
`;
    
    // Anki에 추가
    const addNoteResponse = await this.helpers.httpRequest({
      method: "POST",
      url: "http://127.0.0.1:8765",
      headers: { "Content-Type": "application/json" },
      body: {
        action: "addNote",
        version: 6,
        params: {
          note: {
            deckName: "Confusing English",
            modelName: "Basic",
            fields: { Front: front, Back: back },
            options: { allowDuplicate: false },
            tags: ["confusing", card.type, `batch-${videoId}`]
          }
        }
      },
      json: true
    });
    
    results.push({
      success: true,
      type: card.type,
      topic: card.type === "word" ? card.korean_meaning : card.topic,
      noteId: addNoteResponse.result
    });
    
  } catch (e) {
    results.push({ success: false, error: e.message });
  }
}

return [{
  json: {
    totalCards: comparisonCards.length,
    successCount: results.filter(r => r.success).length,
    results: results,
    videoId: videoId
  }
}];
'''
        node['parameters']['jsCode'] = new_process_code
        print(f"✅ Process All Sentences 수정 완료")

# Webhook 경로 변경
for node in wf['nodes']:
    if node['name'] == 'Webhook':
        node['parameters']['path'] = 'confusing-english'
        print(f"✅ Webhook 경로 변경: /confusing-english")

# 새 워크플로우 생성
new_wf = {
    "name": wf['name'],
    "nodes": wf['nodes'],
    "connections": wf['connections'],
    "settings": wf.get('settings', {}),
}

r = requests.post(
    "http://localhost:5678/api/v1/workflows",
    headers=headers,
    json=new_wf
)

if r.status_code == 200:
    result = r.json()
    print(f"\n✅ 새 워크플로우 생성 완료!")
    print(f"   이름: {result['name']}")
    print(f"   ID: {result['id']}")
else:
    print(f"\n❌ 생성 실패: {r.status_code}")
    print(r.text[:500])

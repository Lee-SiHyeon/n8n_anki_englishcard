import requests
import json

api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MzcyYzk4Yy1kODM0LTQ0NzMtODU4YS1jYjBjZjUyMmUzMWEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY2OTA0ODM3fQ.QW61lHVmTkUFEBYl1YxuqdW1xxVLh7Tr-E6-3-oniVw'
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# 기존 워크플로우 복제해서 새로 만들기
r = requests.get('http://localhost:5678/api/v1/workflows/MD6PXu5l3rXpEFGA', headers=headers)
wf = r.json()

# 워크플로우 이름 변경
wf['name'] = 'Assertive English - 상황 대처 표현'

# Parse & Group Sentences 노드의 프롬프트 변경
for node in wf['nodes']:
    if 'Parse' in node['name'] and 'Group' in node['name']:
        # 새로운 프롬프트로 교체 - AI가 상황을 생성하고 표현을 가르침
        new_code = '''// AI Agent가 상황을 생성하고 대처 표현을 가르치는 카드 생성
const inputData = $input.first().json;
const videoId = inputData.videoId || "assertive";

// AI Agent에게 상황 생성 요청을 위한 프롬프트
const situations = [
  "complaining about a defective product",
  "asking for a refund",
  "disagreeing politely in a meeting",
  "questioning unclear instructions",
  "negotiating a better price",
  "expressing disappointment professionally",
  "requesting urgent help",
  "pushing back on unreasonable demands",
  "clarifying misunderstandings",
  "following up on unanswered emails"
];

// 랜덤하게 5개 상황 선택
const selectedSituations = situations.sort(() => Math.random() - 0.5).slice(0, 5);

const prompt = `You are an expert English communication coach specializing in ASSERTIVE and PROFESSIONAL expressions.

## Your Task
Generate practical English expressions for handling difficult situations confidently.

## Situations to Cover:
${selectedSituations.map((s, i) => `${i + 1}. ${s}`).join("\\n")}

## For EACH situation, provide:
1. A realistic scenario description
2. 2-3 key expressions natives actually use
3. What NOT to say (common mistakes by non-native speakers)

## Response Format (JSON array only):
[{
  "situation_type": "complaining",
  "scenario": "You bought a laptop online but it arrived with a cracked screen.",
  "expressions": [
    {
      "expression": "I'd like to speak with someone about an issue with my order.",
      "korean": "주문 관련 문제에 대해 담당자와 이야기하고 싶습니다.",
      "tone": "polite but firm",
      "usage_context": "Opening line when calling customer service"
    },
    {
      "expression": "This isn't acceptable. I expect a full refund or replacement.",
      "korean": "이건 받아들일 수 없습니다. 전액 환불이나 교환을 원합니다.",
      "tone": "assertive",
      "usage_context": "When the first response isn't satisfactory"
    }
  ],
  "avoid_saying": [
    {
      "wrong": "I'm sorry to bother you, but...",
      "why_wrong": "Apologizing weakens your position when YOU are the wronged party",
      "better": "I need your help resolving an issue."
    }
  ],
  "cultural_note": "In Western business culture, being direct is expected and respected. Excessive politeness can be seen as weakness."
}]

Generate 5 complete situation cards with varied scenarios.`;

return [{
  json: {
    prompt: prompt,
    situations: selectedSituations,
    videoId: videoId
  }
}];
'''
        node['parameters']['jsCode'] = new_code
        print(f"✅ Parse & Group Sentences 프롬프트 변경 완료")

    # Filter 노드도 수정 - Gemini 호출 방식 유지하되 응답 파싱 변경
    if 'Filter Practical' in node['name']:
        new_filter_code = '''// Gemini API로 상황별 표현 생성
const inputData = $input.first().json;
const prompt = inputData.prompt;
const videoId = inputData.videoId || "assertive";

const GEMINI_KEY = "YOUR_GEMINI_API_KEY";

const response = await this.helpers.httpRequest({
  method: "POST",
  url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`,
  headers: { "Content-Type": "application/json" },
  body: {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.8,
      maxOutputTokens: 4000,
    }
  },
  json: true
});

let situationCards = [];
try {
  const text = response.candidates[0].content.parts[0].text;
  const jsonMatch = text.match(/\\[\\s*\\{[\\s\\S]*\\}\\s*\\]/);
  if (jsonMatch) {
    situationCards = JSON.parse(jsonMatch[0]);
  }
} catch (e) {
  throw new Error("Failed to parse Gemini response: " + e.message);
}

return [{
  json: {
    situationCards: situationCards,
    videoId: videoId,
    count: situationCards.length
  }
}];
'''
        node['parameters']['jsCode'] = new_filter_code
        print(f"✅ Filter 노드 수정 완료")

    # Process All Sentences 노드 수정 - 카드 생성 방식 변경
    if 'Process All' in node['name']:
        new_process_code = '''// 상황 대처 표현 Anki 카드 생성
const inputData = $input.first().json;
const situationCards = inputData.situationCards || [];
const videoId = inputData.videoId || "assertive";

if (situationCards.length === 0) {
  return [{ json: { error: "No situation cards", videoId } }];
}

const results = [];
const GOOGLE_TTS_KEY = "YOUR_GOOGLE_TTS_API_KEY";

for (let i = 0; i < situationCards.length; i++) {
  const card = situationCards[i];
  
  try {
    // 첫 번째 표현으로 TTS 생성
    const mainExpression = card.expressions[0]?.expression || "";
    
    let audioTag = "";
    if (mainExpression) {
      const ttsResponse = await this.helpers.httpRequest({
        method: "POST",
        url: `https://texttospeech.googleapis.com/v1/text:synthesize?key=${GOOGLE_TTS_KEY}`,
        headers: { "Content-Type": "application/json" },
        body: {
          input: { text: mainExpression },
          voice: { languageCode: "en-US", name: "en-US-Neural2-J" },
          audioConfig: { audioEncoding: "MP3", speakingRate: 0.9 }
        },
        json: true
      });
      
      if (ttsResponse.audioContent) {
        const audioFileName = `assertive_${videoId}_${i + 1}.mp3`;
        await this.helpers.httpRequest({
          method: "POST",
          url: "http://127.0.0.1:8765",
          headers: { "Content-Type": "application/json" },
          body: {
            action: "storeMediaFile",
            version: 6,
            params: {
              filename: audioFileName,
              data: ttsResponse.audioContent
            }
          },
          json: true
        });
        audioTag = `[sound:${audioFileName}]`;
      }
    }
    
    // Front 카드 - 상황 설명
    const front = `
<div style="font-size:18px;line-height:1.8;color:#333;padding:15px;">
  <div style="background:#ffebee;padding:15px;border-radius:10px;margin-bottom:15px;">
    <b style="color:#c62828;font-size:20px;">🎭 상황</b><br><br>
    ${card.scenario}
  </div>
  <div style="text-align:center;color:#666;font-size:14px;">
    이 상황에서 어떻게 말할까요?
  </div>
</div>
`;
    
    // Back 카드 - 표현들 + 피해야 할 표현
    let expressionsHtml = card.expressions.map((exp, idx) => `
      <div style="background:#e8f5e9;padding:12px;border-radius:8px;margin-bottom:10px;color:#333;">
        <div style="font-size:16px;margin-bottom:5px;">
          ${idx === 0 ? audioTag : ""}
          <b>"${exp.expression}"</b>
        </div>
        <div style="color:#666;font-size:14px;">→ ${exp.korean}</div>
        <div style="margin-top:5px;">
          <span style="background:#2e7d32;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">${exp.tone}</span>
          <span style="color:#888;font-size:12px;margin-left:8px;">${exp.usage_context}</span>
        </div>
      </div>
    `).join("");
    
    let avoidHtml = card.avoid_saying ? card.avoid_saying.map(avoid => `
      <div style="background:#ffebee;padding:10px;border-radius:8px;margin-bottom:8px;color:#333;">
        <div style="color:#c62828;"><b>❌ "${avoid.wrong}"</b></div>
        <div style="font-size:13px;color:#666;">→ ${avoid.why_wrong}</div>
        <div style="color:#2e7d32;font-size:13px;margin-top:5px;">✅ Better: "${avoid.better}"</div>
      </div>
    `).join("") : "";
    
    const back = `
<div style="font-size:16px;line-height:1.8;color:#333;">
  <div style="background:#fff3e0;padding:12px;border-radius:8px;margin-bottom:12px;color:#333;">
    <b style="color:#e65100;">💪 ${card.situation_type.toUpperCase()}</b>
  </div>
  
  <div style="margin-bottom:15px;">
    <b>✨ 이렇게 말하세요:</b>
  </div>
  ${expressionsHtml}
  
  ${avoidHtml ? `
  <div style="margin-top:15px;margin-bottom:10px;">
    <b>🚫 피해야 할 표현:</b>
  </div>
  ${avoidHtml}
  ` : ""}
  
  ${card.cultural_note ? `
  <div style="background:#e3f2fd;padding:10px;border-radius:8px;margin-top:15px;color:#333;">
    <b>💡 문화 팁:</b><br>
    ${card.cultural_note}
  </div>
  ` : ""}
</div>
`;
    
    // Anki에 카드 추가
    const addNoteResponse = await this.helpers.httpRequest({
      method: "POST",
      url: "http://127.0.0.1:8765",
      headers: { "Content-Type": "application/json" },
      body: {
        action: "addNote",
        version: 6,
        params: {
          note: {
            deckName: "Assertive English",
            modelName: "Basic",
            fields: { Front: front, Back: back },
            options: { allowDuplicate: false },
            tags: ["assertive", "situation", card.situation_type, `batch-${videoId}`]
          }
        }
      },
      json: true
    });
    
    results.push({
      success: true,
      situation: card.situation_type,
      noteId: addNoteResponse.result
    });
    
  } catch (e) {
    results.push({
      success: false,
      situation: card.situation_type,
      error: e.message
    });
  }
}

return [{
  json: {
    totalCards: situationCards.length,
    successCount: results.filter(r => r.success).length,
    results: results,
    videoId: videoId
  }
}];
'''
        node['parameters']['jsCode'] = new_process_code
        print(f"✅ Process All Sentences 노드 수정 완료")

# Webhook 경로 변경
for node in wf['nodes']:
    if node['name'] == 'Webhook':
        node['parameters']['path'] = 'assertive-english'
        print(f"✅ Webhook 경로 변경: /assertive-english")

# 새 워크플로우로 저장 (새 ID로)
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

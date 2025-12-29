// YouTube Transcript를 문장 단위로 파싱 (짧은 문장으로 분리)
const transcriptResponse = $input.first().json;

if (!transcriptResponse.success || !transcriptResponse.transcript) {
  throw new Error("Failed to get transcript: " + JSON.stringify(transcriptResponse));
}

const transcriptItems = transcriptResponse.transcript;
const videoId = transcriptResponse.videoId || "";

// 설정: 문장 길이 제한
const MAX_WORDS = 15;  // 최대 단어 수
const MAX_TIME_GAP = 2.5;  // 최대 시간 간격 (초)

// 문장으로 합치기 (짧게 유지)
const sentences = [];
let currentSentence = "";
let currentStart = 0;
let lastEnd = 0;

function countWords(text) {
  return text.trim().split(/\s+/).filter(w => w.length > 0).length;
}

function saveSentence(text, start) {
  const trimmed = text.trim();
  if (trimmed && countWords(trimmed) >= 3) {  // 최소 3단어 이상
    sentences.push({
      index: sentences.length,
      text: trimmed,
      start: start
    });
  }
}

for (const item of transcriptItems) {
  const text = item.text.replace(/\n/g, " ").trim();
  const itemStart = item.start;
  const itemDuration = item.duration || 2;
  const itemEnd = itemStart + itemDuration;
  
  // 시간 간격이 크면 새 문장 시작
  const timeGap = currentSentence ? (itemStart - lastEnd) : 0;
  
  if (currentSentence && timeGap > MAX_TIME_GAP) {
    saveSentence(currentSentence, currentStart);
    currentSentence = "";
  }
  
  // 문장 시작
  if (!currentSentence) {
    currentStart = itemStart;
  }
  
  // 텍스트 추가
  currentSentence += " " + text;
  lastEnd = itemEnd;
  
  // 마침표로 끝나면 문장 종료
  if (text.match(/[.!?]$/)) {
    saveSentence(currentSentence, currentStart);
    currentSentence = "";
    continue;
  }
  
  // 단어 수가 초과하면 자연스러운 끊김 찾기
  const wordCount = countWords(currentSentence);
  if (wordCount >= MAX_WORDS) {
    // 자연스러운 끊김 패턴 (접속사, 콤마 등)
    const breakPatterns = [
      /,\s*(and|but|or|so|because|when|if|that|which|who|where|while|although|however)\s/gi,
      /,\s/g,
      /\s(and|but|or|so)\s/gi
    ];
    
    let broken = false;
    for (const pattern of breakPatterns) {
      const matches = [...currentSentence.matchAll(pattern)];
      if (matches.length > 0) {
        // 마지막 매치 지점에서 자르기
        const lastMatch = matches[matches.length - 1];
        const breakPoint = lastMatch.index + lastMatch[0].indexOf(lastMatch[0].trim());
        
        if (breakPoint > currentSentence.length * 0.4) {  // 40% 이후에서만 자르기
          const firstPart = currentSentence.substring(0, breakPoint).trim();
          const secondPart = currentSentence.substring(breakPoint).trim();
          
          saveSentence(firstPart, currentStart);
          currentSentence = secondPart;
          currentStart = itemStart;  // 대략적인 시작 시간
          broken = true;
          break;
        }
      }
    }
    
    // 자연스러운 끊김이 없으면 그냥 저장
    if (!broken && wordCount >= MAX_WORDS + 5) {
      saveSentence(currentSentence, currentStart);
      currentSentence = "";
    }
  }
}

// 남은 문장 저장
if (currentSentence.trim()) {
  saveSentence(currentSentence, currentStart);
}

// Gemini에 인덱스와 함께 전달
const indexedSentences = sentences.map(s => `[${s.index}] ${s.text}`);

const prompt = `You are an expert English teacher specializing in PHRASAL VERBS that native speakers use daily.

## Your Task
From the transcript below, find sentences containing PHRASAL VERBS that are:
1. Commonly used by native English speakers in everyday conversation
2. Essential for natural-sounding English
3. Practical and useful for learners

## What is a Phrasal Verb?
A phrasal verb = BASE VERB + PARTICLE(s) (preposition/adverb)
Examples: "give up", "look after", "come up with", "run out of"

## Selection Criteria
✅ INCLUDE:
- High-frequency phrasal verbs natives use daily
- Natural conversational expressions
- Idiomatically meaningful (meaning changes from literal)
- Useful in multiple contexts

❌ EXCLUDE:
- "subscribe", "click", "like this video" (YouTube spam)
- Overly technical or rare phrasal verbs
- Simple verb + preposition that aren't true phrasal verbs

## Important
- Each sentence has an INDEX in brackets like [0], [1], [2]
- You MUST return the EXACT index number
- Select 10-15 best examples

## Response Format (JSON array only):
[{
  "sentence_index": 5,
  "original": "exact sentence from transcript (without the [5] prefix)",
  "korean": "자연스러운 한국어 번역",
  "base_verb": "GET",
  "phrasal_verb": "get up",
  "particle": "up",
  "literal_meaning": "위로 얻다/가져가다",
  "idiomatic_meaning": "일어나다, 기상하다 (관용적 의미)",
  "core_image": "UP의 핵심 이미지: 완전히 위로 올라오는 동작",
  "usage_note": "아침에 잠에서 깨어 일어날 때 가장 자주 사용. 'What time do you usually get up?'",
  "alternatives": ["wake up", "rise", "get out of bed"],
  "formal_equivalent": "arise (formal)",
  "example_sentences": [
    "I usually get up at 7 AM.",
    "She got up early to catch the flight."
  ]
}]

## Field Descriptions:
- alternatives: 2-3개의 동의어 또는 대체 표현 (구동사 또는 단일 동사)
- formal_equivalent: 격식체에서 사용하는 동등한 표현 (있는 경우)
- example_sentences: 해당 구동사를 사용한 추가 예문 2개

## Numbered Sentences from Transcript:
\${indexedSentences.join("\n")}`;

return [{
  json: {
    prompt: prompt,
    sentences: sentences,
    videoId: videoId
  }
}];
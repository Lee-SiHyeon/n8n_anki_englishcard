#!/usr/bin/env python3
"""
동사 Lemmatization + Inflection 서버
- spaCy로 원형 추출
- lemminflect로 모든 활용형 생성
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import spacy
from lemminflect import getInflection, getAllInflections

# spaCy 로드
print("🔄 spaCy 모델 로딩 중...")
nlp = spacy.load("en_core_web_sm")
print("✅ spaCy 모델 로드 완료")

class LemmaHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 로그 출력 최소화
        pass
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            verb = data.get("verb", "").strip().lower()
            
            if not verb:
                self.send_error(400, "verb required")
                return
            
            # spaCy로 원형 추출
            doc = nlp(verb)
            lemma = doc[0].lemma_ if doc else verb
            
            # lemminflect로 모든 활용형 생성
            patterns = set([verb, lemma])
            
            # 모든 동사 활용형 가져오기
            all_forms = getAllInflections(lemma, upos="VERB")
            for tag, forms in all_forms.items():
                for form in forms:
                    patterns.add(form.lower())
            
            # 추가 패턴 (일부 불규칙 동사 보완)
            irregular_extras = {
                'be': ['am', 'is', 'are', 'was', 'were', 'been', 'being'],
                'go': ['went', 'gone', 'goes', 'going'],
                'have': ['has', 'had', 'having'],
                'do': ['does', 'did', 'done', 'doing'],
            }
            if lemma in irregular_extras:
                for form in irregular_extras[lemma]:
                    patterns.add(form)
            
            result = {
                "verb": verb,
                "lemma": lemma,
                "patterns": sorted(list(patterns))
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8768):
    server = HTTPServer(('127.0.0.1', port), LemmaHandler)
    print(f"🚀 Lemma 서버 시작: http://127.0.0.1:{port}")
    print("   POST /  body: {\"verb\": \"arose\"}")
    print("   Response: {\"verb\": \"arose\", \"lemma\": \"arise\", \"patterns\": [...]}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()

import difflib
from datetime import datetime

class TradutorIA:
    # ... (mantenha todo o existente) ...
    
    def analisar_traducao(self, original, traduzido):
        """Gera um diff entre os textos para feedback"""
        diff = list(difflib.ndiff(original.split(), traduzido.split()))
        changes = [word for word in diff if word.startswith('+ ') or word.startswith('- ')]
        return changes
    
    def salvar_feedback(self, usuario, original, traduzido, sugestao):
        """Armazena feedbacks em JSON"""
        feedback = {
            "data": datetime.now().isoformat(),
            "usuario": usuario,
            "original": original,
            "traduzido": traduzido,
            "sugestao": sugestao
        }
        
        with open('feedback.json', 'a', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False)
            f.write('\n')
    
    def carregar_feedback(self):
        """Carrega todos os feedbacks"""
        if os.path.exists('feedback.json'):
            with open('feedback.json', 'r', encoding='utf-8') as f:
                return [json.loads(line) for line in f if line.strip()]
        return []
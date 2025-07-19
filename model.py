import re
import json
import os
from collections import defaultdict

class TradutorIA:
    def __init__(self):
        self.memory_file = "memory.json"
        self.carregar_memoria()
        
    def carregar_memoria(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.substituicoes = data.get("substituicoes", {})
                self.erros_comuns = data.get("erros_comuns", defaultdict(int))
        else:
            self.substituicoes = {
                # Artigos e pronomes
                "o": "ê", "a": "ê", "os": "es", "as": "es",
                "um": "ume", "uma": "ume", "uns": "umes", "umas": "umes",
                "ele": "elu", "ela": "elu", "dele": "delu", "dela": "delu",
                "aquele": "aquelu", "aquela": "aquelu",
                
                # Substantivos biformes (com flexão de gênero)
                "menino": "menine", "menina": "menine",
                "garoto": "garote", "garota": "garote",
                "vovô": "vovôe", "vovó": "vovôe",
                "pai": "pae", "mãe": "pae",
                "paternidade": "naternidade", "maternidade": "naternidade",
                "ator": "atore", "atriz": "atore",  # Caso especial
                
                # Adjetivos
                "bonito": "bonite", "bonita": "bonite",
                "todos": "todes", "todas": "todes"
            }
            self.erros_comuns = defaultdict(int)
            self.salvar_memoria()

    def salvar_memoria(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump({
                "substituicoes": self.substituicoes,
                "erros_comuns": dict(self.erros_comuns)
            }, f, ensure_ascii=False, indent=2)

    def aprender(self, correcao):
        try:
            original, neutro = [p.strip() for p in correcao.split(">", 1)]
            self.substituicoes[original.lower()] = neutro.lower()
            self.salvar_memoria()
            return True
        except:
            return False

    def registrar_erro(self, palavra):
        self.erros_comuns[palavra.lower()] += 1
        self.salvar_memoria()

    def traduzir_palavra(self, palavra):
        # Verifica se é uma contração
        if '-' in palavra:
            partes = palavra.split('-')
            return '-'.join([self.traduzir_palavra(p) for p in partes])
            
        original = palavra.lower()
        
        # 1. Verifica substituições específicas na memória
        if original in self.substituicoes:
            return self.substituicoes[original]
            
        # 2. Regras para palavras biformes (com flexão de gênero)
        # Padrão: terminações com 'o'/'a' precedidas por consoante
        if re.search(r'[^aeiouãõâôêáéíóú]o$', original):
            return palavra[:-1] + 'e'
        elif re.search(r'[^aeiouãõâôêáéíóú]a$', original):
            return palavra[:-1] + 'e'
            
        # 3. Para plural (os/as)
        if original.endswith('os'):
            return palavra[:-2] + 'es'
        elif original.endswith('as'):
            return palavra[:-2] + 'es'
            
        # 4. Casos especiais (como "filho" -> "filhe")
        if original in ['filho', 'filha']:
            return 'filhe'
            
        # 5. Mantém a palavra original se não precisar de neutralização
        return palavra

    def prever(self, texto):
        # Preserva pontuação e espaçamento
        palavras = re.findall(r"(\w+|\W+)", texto)
        resultado = []
        
        for palavra in palavras:
            if palavra.strip():  # Se for palavra (não apenas espaços/pontuação)
                trad = self.traduzir_palavra(palavra)
                # Preserva capitalização
                if palavra.istitle():
                    trad = trad.capitalize()
                elif palavra.isupper():
                    trad = trad.upper()
                resultado.append(trad)
            else:
                resultado.append(palavra)
        
        return ''.join(resultado)

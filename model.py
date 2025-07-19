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
                "o": "ê", "a": "ê", "os": "es", "as": "es",
                "ele": "elu", "ela": "elu", "dele": "delu", "dela": "delu",
                "menino": "menine", "menina": "menine",
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

    def prever(self, texto):
        palavras = texto.split()
        resultado = []
        
        for palavra in palavras:
            original = palavra.lower()
            
            # Verifica contrações
            if '-' in palavra:
                partes = [self.prever(p) for p in palavra.split('-')]
                resultado.append('-'.join(partes))
                continue
                
            # Verifica substituições conhecidas
            if original in self.substituicoes:
                resultado.append(self.substituicoes[original])
                continue
                
            # Aplica regras gerais
            modificada = palavra
            if original.endswith('o'):
                modificada = palavra[:-1] + 'e'
            elif original.endswith('a'):
                modificada = palavra[:-1] + 'e'
            elif original.endswith('os'):
                modificada = palavra[:-2] + 'es'
            elif original.endswith('as'):
                modificada = palavra[:-2] + 'es'
                
            resultado.append(modificada)
        
        return ' '.join(resultado)
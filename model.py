import re
import json
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from random import choice
from datetime import datetime

class GerenciadorConteudo:
    def __init__(self):
        self.pasta_estudos = "estudos"
        os.makedirs(self.pasta_estudos, exist_ok=True)
        
    def adicionar_material(self, titulo, conteudo, tags=""):
        """Adiciona novo material sem alterar o código"""
        arquivo = f"{self.pasta_estudos}/{titulo.lower().replace(' ', '_')}.txt"
        metadata = {
            "tags": tags.split(","),
            "data": datetime.now().strftime("%Y-%m-%d")
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(f"METADATA: {json.dumps(metadata)}\n")
            f.write(conteudo)
        return True

    def buscar_material(self, termo):
        """Busca conteúdo nos materiais cadastrados"""
        resultados = []
        for arquivo in os.listdir(self.pasta_estudos):
            if arquivo.endswith('.txt'):
                with open(f"{self.pasta_estudos}/{arquivo}", 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    metadata = json.loads(linhas[0].replace("METADATA: ", ""))
                    conteudo = "".join(linhas[1:])
                    
                    if (termo.lower() in conteudo.lower() or 
                        termo.lower() in metadata['tags'] or
                        termo.lower() in arquivo.lower()):
                        
                        resultados.append({
                            "titulo": arquivo[:-4].replace('_', ' '),
                            "trecho": conteudo[:200] + "...",
                            "tags": metadata['tags'],
                            "data": metadata['data']
                        })
        return resultados

    def listar_materiais(self):
        """Lista todos os materiais disponíveis"""
        return self.buscar_material("")

# model.py
class GerenciadorConteudo:
    def adicionar_material(self, titulo, conteudo, tags="", imagens=None):
        arquivo = f"{self.pasta_estudos}/{titulo.lower().replace(' ', '_')}.json"
        
        dados = {
            "metadata": {
                "tags": tags.split(","),
                "data": datetime.now().strftime("%Y-%m-%d"),
                "imagens": imagens or []
            },
            "conteudo": conteudo
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f)

class TradutorIA:
    def __init__(self):
        # Cria a pasta config se não existir
        os.makedirs("config", exist_ok=True)
        
        self.memory_file = "config/memory.json"
        self.excecoes_file = "config/excecoes.json"
        self.palavras_com_genero_file = "config/palavras_com_genero.json"
        self.carregar_dados()
        
    def carregar_dados(self):
        # Carrega substituições padrão e aprendidas
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.substituicoes = data.get("substituicoes", {})
                    self.erros_comuns = data.get("erros_comuns", defaultdict(int))
            else:
                self.substituicoes = {
                    # Pronomes
                    "ele": "elu", "ela": "elu", "dele": "delu", "dela": "delu",
                    "aquele": "aquelu", "aquela": "aquelu",
                    
                    # Substantivos biformes
                    "menino": "menine", "menina": "menine",
                    "garoto": "garote", "garota": "garote",
                    "ator": "atore", "atriz": "atore",
                    
                    # Adjetivos
                    "bonito": "bonite", "bonita": "bonite",
                    "todos": "todes", "todas": "todes"
                }
                self.erros_comuns = defaultdict(int)
                self.salvar_memoria()
        except Exception as e:
            print(f"Erro ao carregar memory.json: {e}")
            self.substituicoes = {}

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
                "pai": "nae", "mãe": "nae",
                "paternidade": "naternidade", "maternidade": "naternidade",
                "ator": "atore", "atriz": "atore",  # Caso especial
                
                # Adjetivos
                "bonito": "bonite", "bonita": "bonite",
                "todos": "todes", "todas": "todes"
            }
            self.erros_comuns = defaultdict(int)

        # Carrega exceções que não devem ser traduzidas
        try:
            if os.path.exists(self.excecoes_file):
                with open(self.excecoes_file, 'r', encoding='utf-8') as f:
                    self.excecoes = set(json.load(f))
            else:
                self.excecoes = {"vida", "algo", "água", "fogo", "ar", "terra"}
                with open(self.excecoes_file, 'w', encoding='utf-8') as f:
                    json.dump(list(self.excecoes), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao carregar excecoes.json: {e}")
            self.excecoes = set()

        # Carrega palavras com flexão de gênero
        try:
            if os.path.exists(self.palavras_com_genero_file):
                with open(self.palavras_com_genero_file, 'r', encoding='utf-8') as f:
                    self.palavras_com_genero = set(json.load(f))
            else:
                self.palavras_com_genero = {
                    "menino", "menina", "garoto", "garota", 
                    "ator", "atriz", "professor", "professora",
                    "aluno", "aluna", "amigo", "amiga",
                    "namorado", "namorada", "filho", "filha",
                    "neto", "neta", "primo", "prima",
                    "irmão", "irmã", "sobrinho", "sobrinha"
                }
                with open(self.palavras_com_genero_file, 'w', encoding='utf-8') as f:
                    json.dump(list(self.palavras_com_genero), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao carregar palavras_com_genero.json: {e}")
            self.palavras_com_genero = set()

    def salvar_memoria(self):
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "substituicoes": self.substituicoes,
                    "erros_comuns": dict(self.erros_comuns)
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar memory.json: {e}")

    def aprender(self, correcao):
        try:
            original, neutro = [p.strip() for p in correcao.split(">", 1)]
            
            if original.lower() in self.excecoes:
                return False
                
            self.substituicoes[original.lower()] = neutro.lower()
            
            # Se for palavra com gênero, adiciona ao conjunto
            if any(original.lower().endswith(sufixo) for sufixo in ['o', 'a', 'os', 'as']):
                self.palavras_com_genero.add(original.lower())
                with open(self.palavras_com_genero_file, 'w', encoding='utf-8') as f:
                    json.dump(list(self.palavras_com_genero), f, ensure_ascii=False, indent=2)
            
            self.salvar_memoria()
            return True
        except Exception as e:
            print(f"Erro ao aprender: {e}")
            return False

    def tem_flexao_genero(self, palavra):
        """Versão melhorada para identificar gênero"""
        palavra = palavra.lower().strip()
    
        # Carrega exceções de palavras sem gênero
        if palavra in self.excecoes:
            return False
        
        # Verifica padrões linguísticos
        padrao = re.compile(r'(?<![aeiouáéíóúãõâêô])[oa]s?$')
        return (palavra in self.palavras_com_genero or 
               (bool(padrao.search(palavra)) and len(palavra) > 3))

    def traduzir_palavra(self, palavra, proxima_palavra=None):
        original = palavra.lower()
        
        # Não traduz exceções
        if original in self.excecoes:
            return palavra
            
        # Verifica contrações
        if '-' in palavra:
            partes = palavra.split('-')
            return '-'.join([self.traduzir_palavra(p) for p in partes])
            
        # Verifica substituições conhecidas
        if original in self.substituicoes:
            return self.substituicoes[original]
            
        # Regra para artigos (só traduz se a próxima palavra tiver flexão de gênero)
        if original in ['o', 'a', 'os', 'as']:
            if proxima_palavra and self.tem_flexao_genero(proxima_palavra):
                return 'ê' if original in ['o', 'a'] else 'es'
            return palavra
            
        # Regras para palavras biformes
        if re.search(r'[^aeiouãõâôêáéíóú]o$', original):
            return palavra[:-1] + 'e'
        elif re.search(r'[^aeiouãõâôêáéíóú]a$', original):
            return palavra[:-1] + 'e'
        elif original.endswith('os'):
            return palavra[:-2] + 'es'
        elif original.endswith('as'):
            return palavra[:-2] + 'es'
            
        return palavra

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
<<<<<<< HEAD
        tokens = re.findall(r"(\w+|\W+)", texto)
        resultado = []
        
        for i, token in enumerate(tokens):
            if token.strip():
                proxima = tokens[i+1].strip() if i+1 < len(tokens) else None
                trad = self.traduzir_palavra(token, proxima)
                
                if token.istitle():
                    trad = trad.capitalize()
                elif token.isupper():
                    trad = trad.upper()
                    
                resultado.append(trad)
            else:
                resultado.append(token)
        
        return ''.join(resultado)

    def adicionar_excecao(self, palavra):
        self.excecoes.add(palavra.lower())
        try:
            with open(self.excecoes_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.excecoes), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar excecoes: {e}")
            return False

class Chatbot:
    def __init__(self, tradutor):
        self.tradutor = tradutor
        self.historico = []
        self.contexto = {
            "ultimo_topico": None,
            "aguardando_acao": None,
            "dados_para_aprender": None
        }
        
        self.personalidade = {
            "nome": "Lune",
            "emoji": "🌈",
            "pronomes": "elu/delu",
            "saudacoes": {
                "manha": "**BOM DIA!** ☀️ Prontu para aprender sobre linguagem inclusiva?",
                "tarde": "**BOA TARDE!** 🌤 Vamos estudar juntes?",
                "noite": "**BOA NOITE!** 🌙 Hora de praticar gênero neutro!"
            },
            "despedidas": [
                "Até mais! Lembre-se: a linguagem inclusiva transforma o mundo!",
                "Foi um prazer ajudar! Volte sempre que precisar :)",
                "Tchauzinhu! Se precisar de algo, é só chamar!"
            ]
        }
        
        self.carregar_conhecimento()
        self.respostas_rapidas = {
            "oi": self.responder_saudacao,
            "olá": self.responder_saudacao,
            "ola": self.responder_saudacao,
            "bom dia": self.responder_saudacao,
            "boa tarde": self.responder_saudacao,
            "boa noite": self.responder_saudacao,
            "tchau": self.responder_despedida,
            "adeus": self.responder_despedida,
            "vlw": self.responder_despedida
        }
    
    def carregar_conhecimento(self):
        try:
            with open('conhecimento_lune.json', 'r', encoding='utf-8') as f:
                self.conhecimento = json.load(f)
        except:
            self.conhecimento = {
                "pronomes": {
                    "titulo": "PRONOMES NEUTROS",
                    "conteudo": "• Ele/Ela → **ELU**\n• Dele/Dela → **DELU**\n• Aquele/Aquela → **AQUELU**",
                    "exemplos": ["Elu é incrível", "Isso é delu", "Aquelu pessoa"]
                },
                "artigos": {
                    "titulo": "ARTIGOS NEUTROS",
                    "conteudo": "• O/A → **Ê**\n• Os/As → **ES**",
                    "exemplos": ["Ê estudante", "Es professoris"]
                }
            }
    
    def salvar_conhecimento(self):
        with open('conhecimento_lune.json', 'w', encoding='utf-8') as f:
            json.dump(self.conhecimento, f, ensure_ascii=False, indent=2)
    
    def obter_saudacao(self):
        hora = datetime.now().hour
        if 5 <= hora < 12:
            return self.personalidade['saudacoes']['manha']
        elif 12 <= hora < 18:
            return self.personalidade['saudacoes']['tarde']
        else:
            return self.personalidade['saudacoes']['noite']
    
    def responder_saudacao(self):
        return f"{self.obter_saudacao()} {self.personalidade['emoji']}\n\n" \
               f"Me chamo **{self.personalidade['nome']}**, e uso pronomes {self.personalidade['pronomes']}!\n" \
               "Como posso te ajudar hoje com linguagem neutra?"
    
    def responder_despedida(self):
        return f"{choice(self.personalidade['despedidas'])} {self.personalidade['emoji']}"
    
    def pesquisar_online(self, query):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://www.google.com/search?q={query}+linguagem+neutra"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            resultados = []
            for g in soup.find_all('div', class_='g')[:3]:
                titulo = g.find('h3').text if g.find('h3') else "Sem título"
                link = g.find('a')['href'] if g.find('a') else "#"
                desc = g.find('div', class_='IsZvec').text if g.find('div', class_='IsZvec') else "Sem descrição"
                resultados.append(f"• **{titulo}**\n  {link}\n  _{desc[:150]}..._")
            
            return "\n\n".join(resultados) if resultados else "Não encontrei informações sobre isso."
        except:
            return "Não consegui acessar a internet no momento."

    def processar_mensagem(self, mensagem):
        mensagem = mensagem.lower().strip()
        self.historico.append(mensagem)
        
        # Respostas rápidas pré-definidas
        if mensagem in self.respostas_rapidas:
            return self.respostas_rapidas[mensagem]()
        
        # Modo de aprendizado
        if self.contexto["dados_para_aprender"]:
            resposta = self.finalizar_aprendizado(mensagem)
            self.contexto["dados_para_aprender"] = None
            return resposta
        
        # Comandos com contexto
        if self.contexto["aguardando_acao"] == "traducao":
            self.contexto["aguardando_acao"] = None
            traducao = self.tradutor.prever(mensagem)
            return self.formatar_resposta(
                "TRADUÇÃO PRONTA",
                traducao,
                tipo="traducao"
            )
        
        # Comandos específicos
        if any(p in mensagem for p in ["traduzir", "traduza"]):
            self.contexto["aguardando_acao"] = "traducao"
            return "**Digite o texto que deseja traduzir:** ✍️"
            
        if "pronome" in mensagem:
            return self.responder_tema("pronomes")
            
        if "artigo" in mensagem:
            return self.responder_tema("artigos")
            
        if mensagem.startswith("pesquisar "):
            return self.pesquisar_online(mensagem[9:])
            
        if mensagem.startswith("aprenda "):
            self.contexto["dados_para_aprender"] = mensagem[8:]
            return "Ótimo! Qual deve ser a resposta para isso?"
        
        # Resposta inteligente padrão
        return self.gerar_resposta_inteligente(mensagem)
    
    def finalizar_aprendizado(self, resposta):
        pergunta = self.contexto["dados_para_aprender"]
        self.conhecimento[pergunta.lower()] = resposta
        self.salvar_conhecimento()
        return f"✅ **Aprendido!** Agora quando alguém perguntar '{pergunta}', eu responderei:\n\n{resposta}"
    
    def responder_tema(self, tema):
        if tema in self.conhecimento:
            dados = self.conhecimento[tema]
            return self.formatar_resposta(
                dados["titulo"],
                dados["conteudo"],
                exemplos=dados.get("exemplos", []),
                tipo="explicacao"
            )
        return "Ainda não sei sobre isso. Quer me ensinar? Diga 'aprenda {tema} = {resposta}'"
    
    def formatar_resposta(self, titulo, conteudo, exemplos=None, tipo="info"):
        resposta = f"**{titulo.upper()}**\n\n{conteudo}"
        
        if exemplos:
            resposta += "\n\n💡 **EXEMPLOS:**\n" + "\n".join(f"• {ex}" for ex in exemplos)
        
        if tipo == "traducao":
            resposta = f"✍️ {resposta}\n\n_Deseja corrigir algo? Me ensine com 'aprenda [original] = [correção]'_"
        elif tipo == "explicacao":
            resposta = f"📚 {resposta}\n\n_Quer pesquisar mais sobre isso? Digite 'pesquisar [tema]'_"
        
        return resposta
    
    def gerar_resposta_inteligente(self, mensagem):
        # Verifica se já sabe a resposta
        if mensagem.lower() in self.conhecimento:
            return self.conhecimento[mensagem.lower()]
        
        # Sugere aprendizado ou pesquisa
        return (
            f"🤔 **Não tenho certeza sobre isso.**\n\n"
            f"Você pode:\n"
            f"1. Me ensinar com 'aprenda {mensagem} = [resposta]'\n"
            f"2. Pesquisar online com 'pesquisar {mensagem}'\n"
            f"3. Pedir ajuda sobre 'pronomes' ou 'artigos'"
        )
        
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

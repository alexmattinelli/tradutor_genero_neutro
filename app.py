from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from model import TradutorIA
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

app = Flask(__name__)
tradutor_instance = TradutorIA()  # Renomeado para evitar conflito

# Configuração do ChatBot
def criar_chatbot():
    chatbot = ChatBot(
        'Lune',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Desculpe, não entendi. Poderia reformular?',
                'maximum_similarity_threshold': 0.90
            }
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ]
    )
    
    conversas = [
        ("qual seu nome", 
         "Me chamo Lune! Sou sue assistente para traduções neutras. Uso pronomes elu/delu :)"),
        ("como você funciona",
         "Funciono através de:\n\n"
         "- Análise de texto com foco em neutralidade\n"
         "- Sugestões de termos inclusivos\n"
         "- Respeito aos pronomes neutros"),
        ("linguagem neutra",
         "É uma forma de comunicação que:\n\n"
         "✓ Evita assumir gêneros\n"
         "✓ Usa termos como 'pessoas' em vez de 'homens/mulheres'\n"
         "✓ Prioriza 'elu/delu' ou estruturas sem pronomes")
    ]
    
    trainer = ListTrainer(chatbot)
    for pergunta, resposta in conversas:
        trainer.train([pergunta, resposta])
    
    return chatbot

# Inicialização do chatbot
try:
    chatbot_instance = criar_chatbot()  # Renomeado para evitar conflito
except Exception as e:
    print(f"Erro ao iniciar chatbot: {str(e)}")
    chatbot_instance = None

# Sistema de Rotas
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tradutor", methods=["GET", "POST"])
def tradutor_route():  # Renomeado para evitar conflito
    if request.method == "POST":
        if "correcao" in request.form:
            correcao = request.form["correcao"]
            if tradutor_instance.aprender(correcao):
                return redirect(url_for('tradutor_route', sucesso=True))
        
        texto = request.form.get("texto", "")
        if texto:
            traducao = tradutor_instance.prever(texto)
            return render_template("tradutor.html", traducao=traducao, texto_original=texto)
    
    return render_template("tradutor.html")

@app.route("/chatbot")
def chatbot_route():  # Renomeado para evitar conflito
    return render_template("chatbot.html")

@app.route("/api/chatbot", methods=["POST"])
def chatbot_api():
    mensagem = request.json.get("mensagem", "").strip().lower()
    
    # Respostas prioritárias
    respostas_imediatas = {
        "oi": "Olá! 🌈 Sou Lune, especialista em linguagem neutra!",
        "boa tarde": f"{chatbot_instance.obter_saudacao()} Como posso ajudar?",
        "ei lune": "Estou aqui! ✨ Pergunte sobre pronomes neutros, traduções ou diga 'ajuda'"
    }
    
    if mensagem in respostas_imediatas:
        return jsonify({"resposta": respostas_imediatas[mensagem]})
    
    # Lógica inteligente
    try:
        if "pronome" in mensagem:
            return jsonify({"resposta": chatbot_instance.responder_tema("pronomes")})
        elif "artigo" in mensagem:
            return jsonify({"resposta": chatbot_instance.responder_tema("artigos")})
        else:
            # Integração com tradutor
            traducao = tradutor_instance.prever(mensagem)
            return jsonify({
                "resposta": f"🔍 Tradução neutra:\n{traducao}\n\nDiga 'exemplos' para ver frases similares"
            })
    except Exception as e:
        return jsonify({"resposta": "Algo deu errado, mas vou aprender! 🌱"})
@app.route("/estudos")
def estudos():
    return render_template("estudos.html")

# Dados de login (em produção, use banco de dados com senhas hasheadas!)
usuarios_admin = {
    "admin": "senha123"  # Troque isso antes de colocar em produção
}

@app.route('/', methods=['GET', 'POST'])
def index():
    traducao = None
    texto_original = ""
    
    if request.method == 'POST' and 'texto' in request.form:
        texto_original = request.form['texto']
        # Aqui você colocaria sua lógica real de tradução
        traducao = f"[TRADUÇÃO DE TESTE] {texto_original}"
        
    return render_template('tradutor.html', 
                         traducao=traducao,
                         texto_original=texto_original)

@app.route('/admin')
def admin():
    if not session.get('admin_logado'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if usuario in usuarios_admin and senha == usuarios_admin[usuario]:
            session['admin_logado'] = True
            return redirect(url_for('admin'))
    
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Admin</title>
            <style>
                body { font-family: Arial; max-width: 400px; margin: 50px auto; }
                input, button { padding: 8px; margin: 5px 0; width: 100%; }
            </style>
        </head>
        <body>
            <h2>Área de Login</h2>
            <form method="post">
                <input type="text" name="usuario" placeholder="Usuário" required>
                <input type="password" name="senha" placeholder="Senha" required>
                <button type="submit">Entrar</button>
            </form>
        </body>
        </html>
    '''

@app.route('/logout')
def logout():
    session.pop('admin_logado', None)
    return redirect(url_for('index'))

@app.route('/upload_imagem', methods=['POST'])
def upload_imagem():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo"})
    
    arquivo = request.files['file']
    if arquivo.filename == '':
        return jsonify({"erro": "Nome vazio"})
    
    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join('static/imagens', filename))
        return jsonify({"sucesso": True, "caminho": f"/static/imagens/{filename}"})

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_servidor(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template, request, redirect, url_for, abort
from model import TradutorIA

app = Flask(__name__)
tradutor = TradutorIA()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Processar correção
        if "correcao" in request.form:
            correcao = request.form["correcao"]
            if tradutor.aprender(correcao):
                return redirect(url_for('home', sucesso=True))
        
        # Processar tradução
        texto = request.form.get("texto", "")
        if texto:
            traducao = tradutor.prever(texto)
            return render_template("index.html", traducao=traducao, texto_original=texto)
    
    return render_template("index.html")

@app.route("/estudos")
def estudos():
    return render_template("estudos.html")

# ======================================
# TRATAMENTO DE ERROS
# ======================================

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    """
    Página personalizada para erro 404 - Página não encontrada
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_servidor(error):
    """
    Página personalizada para erro 500 - Erro interno do servidor
    """
    return render_template('500.html'), 500

# ======================================
# ROTAS DE TESTE (OPCIONAL - PODE REMOVER DEPOIS)
# ======================================

@app.route("/teste-404")
def teste_404():
    """Rota para testar o erro 404"""
    abort(404)

@app.route("/teste-500")
def teste_500():
    """Rota para testar o erro 500"""
    abort(500)

# ======================================
# INICIALIZAÇÃO DO APLICATIVO
# ======================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
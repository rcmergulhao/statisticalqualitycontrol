from flask import Flask, request, render_template_string
from scipy.stats import binom

app = Flask(__name__)

def encontrar_plano_amostral(TAMANHO_LOTE, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX):
    for tamanho_amostra in range(1, TAMANHO_LOTE + 1):
        for aceitacao_maxima in range(tamanho_amostra + 1):
            risco_fornecedor = 1 - binom.cdf(aceitacao_maxima, tamanho_amostra, NQA)
            risco_consumidor = binom.cdf(aceitacao_maxima, tamanho_amostra, PTDL)
            if risco_fornecedor <= RISCO_FORNECEDOR_MAX and risco_consumidor <= RISCO_CONSUMIDOR_MAX:
                return tamanho_amostra, aceitacao_maxima, risco_fornecedor, risco_consumidor
    return None, None, None, None

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Plano Amostral</title>
</head>
<body>
    <h1>Calculadora de Plano Amostral</h1>
    <form method="post">
        <label for="tamanho_lote">Tamanho do Lote:</label>
        <input type="number" id="tamanho_lote" name="tamanho_lote" value="10000" required><br><br>
        
        <label for="nqa">NQA:</label>
        <input type="number" step="0.01" id="nqa" name="nqa" value="0.015" required><br><br>
        
        <label for="ptdl">PTDL:</label>
        <input type="number" step="0.01" id="ptdl" name="ptdl" value="0.05" required><br><br>
        
        <label for="risco_fornecedor_max">Risco Fornec. Máx:</label>
        <input type="number" step="0.001" id="risco_fornecedor_max" name="risco_fornecedor_max" value="0.1" required><br><br>
        
        <label for="risco_consumidor_max">Risco Cons. Máx:</label>
        <input type="number" step="0.001" id="risco_consumidor_max" name="risco_consumidor_max" value="0.075" required><br><br>
        
        <button type="submit">Calcular Plano Amostral</button>
    </form>

    {% if result %}
        <h2>Resultado:</h2>
        {% if result is string %}
            <p>{{ result }}</p>
        {% else %}
            <p>Tamanho da amostra: {{ result.tamanho_amostra }}</p>
            <p>Índice de aceitação máxima: {{ result.aceitacao_maxima }}</p>
            <p>Risco do fornecedor: {{ result.risco_fornecedor }}</p>
            <p>Risco do consumidor: {{ result.risco_consumidor }}</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        tamanho_lote = int(request.form['tamanho_lote'])
        nqa = float(request.form['nqa'])
        ptdl = float(request.form['ptdl'])
        risco_fornecedor_max = float(request.form['risco_fornecedor_max'])
        risco_consumidor_max = float(request.form['risco_consumidor_max'])

        tamanho_amostra, aceitacao_maxima, risco_fornecedor, risco_consumidor = encontrar_plano_amostral(
            tamanho_lote, nqa, ptdl, risco_fornecedor_max, risco_consumidor_max
        )

        if tamanho_amostra is not None:
            result = {
                'tamanho_amostra': tamanho_amostra,
                'aceitacao_maxima': aceitacao_maxima,
                'risco_fornecedor': round(risco_fornecedor, 3),
                'risco_consumidor': round(risco_consumidor, 3)
            }
        else:
            result = 'Nenhum plano amostral encontrado com os parâmetros fornecidos.'
    return render_template_string(template, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

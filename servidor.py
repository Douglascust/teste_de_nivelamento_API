from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from ftfy import fix_text
import unicodedata

app = Flask(__name__)
CORS(app)

@app.route('/operadoras')
def buscar_operadoras():
    try:
        pagina = request.args.get('pagina')
        termo_busca = request.args.get('termo', '').lower()
        print(f"Página: {pagina}, Termo de busca: {termo_busca}")
        df = pd.read_csv('Relatorio_cadop.csv', encoding='utf-8', sep=';')

        # Tratar valores NaN
        df = df.fillna('')

        # Remover caracteres não ASCII
        df = df.replace(r'[^\x00-\x7F]+', '', regex=True)

        # Substituir caracteres especiais por espaços
        df = df.replace(r'[^\w\s]+', ' ', regex=True)

        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, float) else x)
            df[col] = df[col].apply(fix_text)
            df[col] = df[col].apply(lambda x: unicodedata.normalize('NFKD', str(x)).encode('ascii', 'ignore').decode('utf-8'))

        colunas_desejadas = [
            "Registro_ANS", "CNPJ", "Razao_Social", "Modalidade",
            "Logradouro", "Numero", "Bairro", "Cidade", "UF", "CEP",
            "DDD", "Telefone", "Fax", "Endereco_eletronico", "Representante",
            "Cargo_Representante", "Regiao_de_Comercializacao", "Data_Registro_ANS"
        ]
        df = df[colunas_desejadas]
        dados = df.to_dict(orient='records')

        if termo_busca:
            dados = [d for d in dados if termo_busca in str(d).lower()]

        if pagina:
            pagina = int(pagina)
            registros_por_pagina = 10
            inicio = (pagina - 1) * registros_por_pagina
            fim = inicio + registros_por_pagina
            dados = dados[inicio:fim]

        print(f"Colunas do DataFrame: {df.columns}")
        print(f"Dados paginados: {dados}")

        return jsonify(dados)
    except FileNotFoundError as e:
        print(f"Erro ao ler arquivo: {e}")
        return jsonify({'error': 'Arquivo Relatorio_cadop.csv não encontrado.'}), 404
    except pd.errors.ParserError as e:
        print(f"Erro ao analisar o arquivo CSV: {e}")
        return jsonify({'error': 'Erro ao analisar o arquivo CSV.'}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({'error': f'Erro inesperado: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from flask import Flask, render_template, redirect, request
from database.banco import salvar_monitor_config
import sqlite3
import subprocess


app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "web" / "templates"),
    static_folder=str(BASE_DIR / "web" / "static")
)


BANCO = BASE_DIR / "database" / "monitor.db"


def conectar():

    conn = sqlite3.connect(BANCO)

    conn.row_factory = sqlite3.Row

    return conn


@app.route("/executar", methods=["POST"])
def executar():

    conn = conectar()

    status = conn.execute("""
        SELECT status
        FROM status_monitor
        WHERE id = 1
    """).fetchone()

    conn.close()

    if status and status[0] == "Executando":

        return """
        <script>
            alert('O monitor já está em execução!');
            window.location.href='/';
        </script>
        """

    config = {

        "email": "",

        "cidade": request.form.get("cidade", ""),

        "tipo": request.form.get("tipo", ""),

        "finalidade": request.form.get("negocio", ""),

        "bairro": request.form.get("bairro", ""),

        "valor_maximo": request.form.get("valor_max", ""),

        "quartos": request.form.get("quartos", ""),

        "vagas": "",

        "imobiliaria": ""

    }

    salvar_monitor_config(config)

    subprocess.Popen(
        [
            sys.executable,
            str(BASE_DIR / "main.py")
        ]
    )

    return """
    <script>
        alert('Monitor iniciado!');
        window.location.href='/';
    </script>
    """


@app.route("/")
def index():

    conn = conectar()


    total_imoveis = conn.execute("""
        SELECT COUNT(*)
        FROM imoveis
    """).fetchone()[0]


    total_execucoes = conn.execute("""
        SELECT COUNT(*)
        FROM execucoes
    """).fetchone()[0]


    ultima_execucao = conn.execute("""
        SELECT
            data_execucao,
            coletados,
            aprovados,
            novos
        FROM execucoes
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()


    total_novos = 0

    if ultima_execucao:

        total_novos = ultima_execucao[3]


    status_monitor = conn.execute("""
        SELECT
            status,
            mensagem,
            inicio,
            fim
        FROM status_monitor
        WHERE id = 1
    """).fetchone()


    historico = conn.execute("""
        SELECT
            data_execucao,
            coletados,
            aprovados,
            novos
        FROM execucoes
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()



    # =========================
    # FILTROS DE PESQUISA
    # =========================

    filtros = []
    parametros_filtros = []


    categoria = request.args.get("categoria")
    cidade = request.args.get("cidade")
    negocio = request.args.get("negocio")
    tipo = request.args.get("tipo")
    bairro = request.args.get("bairro")

    if not bairro or bairro == "None":
        bairro = None

    valor_min = request.args.get("valor_min")
    valor_max = request.args.get("valor_max")
    quartos = request.args.get("quartos")
    ordenar = request.args.get("ordenar", "recentes")

    print("ORDENAÇÃO RECEBIDA:", ordenar)


    
    if categoria:

        if categoria == "Residencial":

            filtros.append(
                """
                tipo_imovel IN (
                    'Casa',
                    'Apartamento',
                    'Kitnet'
                )
                """
            )


        elif categoria == "Comercial":

            filtros.append(
                """
                tipo_imovel IN (
                    'Loja',
                    'Sala',
                    'Galpão'
                )
                """
            )

    if cidade:
    
        # Atualmente todos os imóveis coletados são de Governador Valadares
        # A cidade não precisa filtrar a coluna localizacao
        pass    

    if negocio:

        filtros.append(
            "tipo_negocio = ?"
        )

        parametros_filtros.append(
            negocio
        )
    

    if tipo:

        filtros.append(
            "tipo_imovel = ?"
        )

        parametros_filtros.append(
            tipo
        )
        

    if bairro:

        filtros.append(
            "localizacao LIKE ?"
        )

        parametros_filtros.append(
            f"%{bairro}%"
        )

    if valor_min:

        filtros.append(
            """
            CAST(
                REPLACE(
                    REPLACE(valor,'R$ ',''),
                    ',','.'
                )
                AS REAL
            ) >= ?
            """
        )

        parametros_filtros.append(
            float(valor_min.replace(",", "."))
        )

    if valor_max:

        filtros.append(
            """
            CAST(
                REPLACE(
                    REPLACE(valor,'R$ ',''),
                    ',','.'
                )
                AS REAL
            ) <= ?
            """
        )

        parametros_filtros.append(
            float(valor_max.replace(",", "."))
        )

    if quartos:

        filtros.append(
            "CAST(quartos AS INTEGER) >= ?"
        )

        parametros_filtros.append(
            quartos
        )


    # =========================
    # CONSULTA PADRÃO
    # =========================

    sql = """

    SELECT
        codigo,
        origem,
        titulo,
        valor,
        localizacao,
        quartos,
        vagas,
        area,
        data_cadastro,
        link,
        imagem

    FROM imoveis

    WHERE 1=1

    """

    parametros = []


    if filtros:

        sql += " AND " + " AND ".join(filtros)


    parametros.extend(
        parametros_filtros
    )


    if ordenar == "menor_valor":

        sql += """

        ORDER BY
        CAST(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(valor,'Valor:',''),
                        'R$',''),
                    ' ', ''),
                '.', ''),
            ',', '.')
            AS REAL
        ) ASC

        """


    elif ordenar == "maior_valor":

        sql += """

        ORDER BY
        CAST(
                REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(valor,'Valor:',''),
                        'R$',''),
                    ' ', ''),
                '.', ''),
            ',', '.')
            AS REAL
        ) DESC

        """

    elif ordenar == "imobiliaria":

        sql += """
        ORDER BY origem ASC
        """
    elif ordenar == "bairro":

        sql += """
        ORDER BY localizacao ASC
        """

    else:

        sql += """

        ORDER BY data_cadastro DESC

        """


    sql += """

    LIMIT 50

    """

    print("\nSQL:")
    print(sql)

    print("\nPARÂMETROS:")
    print(parametros)


    if any([
        categoria,
        cidade,
        negocio,
        tipo,
        bairro,
        valor_min,
        valor_max,
        quartos
    ]):

        ultimos_imoveis = conn.execute(
            sql,
            parametros
        ).fetchall()

        print("TOTAL ENCONTRADO:", len(ultimos_imoveis))

        for item in ultimos_imoveis:
            print(dict(item))

    else:

        ultimos_imoveis = []


    conn.close()


    return render_template(
        "index.html",
        imoveis=ultimos_imoveis,
        total_imoveis=total_imoveis,
        total_execucoes=total_execucoes,
        total_novos=total_novos,
        ultima_execucao=ultima_execucao,
        status_monitor=status_monitor,
        historico=historico,
        categoria=categoria,
        cidade=cidade,
        negocio=negocio,
        tipo=tipo,
        bairro=bairro,
        valor_min=valor_min,
        valor_max=valor_max,
        quartos=quartos,
        ordenar=ordenar
)

@app.route("/historico")
def historico():

    conn = conectar()


    historico = conn.execute("""
        SELECT
            data_execucao,
            coletados,
            aprovados,
            novos

        FROM execucoes

        ORDER BY id DESC

    """).fetchall()


    conn.close()


    return render_template(
        "historico.html",
        historico=historico
    )



@app.route("/abrir/<origem>/<codigo>")
def abrir_imovel(origem, codigo):

    conn = conectar()


    imovel = conn.execute("""
        SELECT *
        FROM imoveis
        WHERE origem = ?
        AND codigo = ?
    """, (origem, codigo)).fetchone()


    conn.close()



    if not imovel:

        return "Imóvel não encontrado", 404



    return redirect(imovel[9])



@app.route("/imovel/<origem>/<codigo>")
def detalhes_imovel(origem, codigo):

    conn = conectar()


    imovel = conn.execute("""
        SELECT *
        FROM imoveis
        WHERE origem = ?
        AND codigo = ?
    """, (origem, codigo)).fetchone()


    conn.close()



    if not imovel:

        return f"Não encontrado: {origem} - {codigo}", 404



    return render_template(
        "detalhes.html",
        imovel=imovel
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def calcular_valor(bolsa, num_modalidades, desconto):
    if bolsa == 1:
        return 0
    desconto = desconto or 0
    if num_modalidades == 2:
        return 300 - desconto
    else:
        return 200 - desconto


@app.route('/atletas')
def listar_atletas():
    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute("""SELECT atletas.*, categorias.nome AS nome_categoria
                    FROM atletas
                    JOIN categorias ON atletas.categoria_id = categorias.id""")
    atletas = cursor.fetchall()
    
    conexao.close()

    return render_template('atletas.html', atletas=atletas)

@app.route('/atletas/<int:id>')
def ficha_atleta(id):
    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    
    cursor = conexao.cursor()
    cursor.execute("""SELECT atletas.* , categorias.nome AS nome_categoria
                    FROM atletas
                    JOIN categorias ON atletas.categoria_id = categorias.id
                    WHERE atletas.id = ?""", (id,))

    atleta = cursor.fetchone()

    cursor.execute("""SELECT modalidades.nome FROM relacao_atletas
                    JOIN modalidades ON relacao_atletas.modalidade_id = modalidades.id
                    WHERE relacao_atletas.atleta_id = ?""", (id,))
    modalidades = cursor.fetchall()
    
    num_modalidades = len(modalidades)

    valor = calcular_valor(atleta['bolsa'], num_modalidades, atleta['desconto'])

    cursor.execute("""SELECT * FROM pagamentos
                    WHERE atleta_id = ?
                    ORDER BY mes_referencia DESC""", (id,))
    relatorio_pagamentos = cursor.fetchall()


    
    
    conexao.close()
    return render_template('ficha_atleta.html', atleta=atleta, modalidades = modalidades, valor = valor, relatorio_pagamentos = relatorio_pagamentos)

@app.route('/atletas/<int:id>/alterar_status', methods = ['POST'])
def alterar_status_atleta(id):
    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
        
    cursor = conexao.cursor()

    cursor.execute("SELECT status FROM atletas WHERE id = ?", (id,))
    atleta = cursor.fetchone()

    novo_status = 'inativo' if atleta['status'] == 'ativo' else 'ativo'


    cursor.execute("UPDATE atletas SET  status = ? WHERE id = ?", (novo_status, id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for('ficha_atleta', id=id))


@app.route('/atletas/<int:id>/editar', methods = ['GET', 'POST'])
def editar_atleta(id):
    if request.method == 'POST':
        conexao = sqlite3.connect('banco.db')
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        cpf_atleta = request.form['cpf_atleta']
        pai = request.form['pai']
        mae = request.form['mae']
        cpf_responsavel = request.form['cpf_responsavel']
        endereco = request.form['endereco']
        whats = request.form['whats']
        escola = request.form['escola']
        categoria_id = request.form['categoria_id']
        desconto = float(request.form.get('desconto') or '0')
        
        bolsa = 1 if request.form.get('bolsa') else 0
        equipe = 1 if request.form.get('equipe') else 0
        modalidades = request.form.getlist('modalidades')

        cursor.execute("""UPDATE atletas
                        SET nome = ?, data_nascimento = ?, cpf_atleta = ?, pai = ?, mae = ?, 
                        cpf_responsavel = ?, endereco = ?, whats = ?, escola = ?, categoria_id = ?,
                        bolsa = ?, desconto = ?, equipe = ? 
                        WHERE id = ?""", (nome, data_nascimento, cpf_atleta, pai, mae, cpf_responsavel, endereco, whats, escola, categoria_id, bolsa, desconto, equipe, id,))
        cursor.execute(""" DELETE FROM relacao_atletas
                        WHERE atleta_id = ?""", (id,))

        for modalidades_id in modalidades:
            cursor.execute("""INSERT INTO relacao_atletas
                            (atleta_id, modalidade_id) VALUES (?, ?)""", (id, modalidades_id))   
        conexao.commit()
        conexao.close()
        return redirect(url_for('ficha_atleta', id=id))

    else:
        conexao = sqlite3.connect('banco.db')
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("""SELECT atletas.*, categorias.nome AS nome_categoria
                    FROM atletas
                    JOIN categorias ON atletas.categoria_id = categorias.id
                    WHERE atletas.id = ?""", (id,))
        atleta = cursor.fetchone()

        cursor.execute("""SELECT modalidades.nome, relacao_atletas.modalidade_id FROM relacao_atletas
                        JOIN modalidades ON modalidades.id = relacao_atletas.modalidade_id
                        WHERE relacao_atletas.atleta_id = ?""", (id,))
        modalidades = cursor.fetchall()
        conexao.close()
        return render_template('editar_atleta.html', atleta=atleta, modalidades=modalidades)




@app.route('/atletas/novo', methods = ['GET', 'POST'])
def novo_atleta():
    
    if request.method == 'POST':
        conexao = sqlite3.connect('banco.db')
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        

        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        cpf_atleta = request.form['cpf_atleta']
        pai = request.form['pai']
        mae = request.form['mae']
        cpf_responsavel = request.form['cpf_responsavel']
        endereco = request.form['endereco']
        whats = request.form['whats']
        escola = request.form['escola']
        categoria_id = request.form['categoria_id']
        desconto = float(request.form.get('desconto') or '0')
        bolsa = 1 if request.form.get('bolsa') else 0
        equipe = 1 if request.form.get('equipe') else 0
        status = 'ativo'

        modalidades = request.form.getlist('modalidades')

        cursor.execute("""INSERT INTO atletas
                        (nome, data_nascimento, cpf_atleta, pai, mae, cpf_responsavel, endereco, whats, escola, categoria_id, bolsa, desconto, equipe, status)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?)""",
                        (nome, data_nascimento, cpf_atleta, pai, mae, cpf_responsavel, endereco, whats, escola, categoria_id, bolsa, desconto, equipe, status))
        atleta_id = cursor.lastrowid
        for modalidades_id in modalidades:
            cursor.execute(""" INSERT INTO relacao_atletas
                                (atleta_id, modalidade_id) VALUES(?,?)""",
                                (atleta_id, modalidades_id))

        cursor.execute("""SELECT * FROM relacao_atletas 
                        WHERE atleta_id = ?""", (atleta_id,))
        modalidades = cursor.fetchall()
        num_modalidades = len(modalidades)

        mes_referencia = datetime.now().strftime('%Y-%m')

        valor = calcular_valor(bolsa, num_modalidades, desconto)

        cursor.execute("""INSERT INTO pagamentos
                        (atleta_id, mes_referencia, tipo, valor, status)
                        VALUES(?, ?, ?, ?, ?)""",
                       (atleta_id, mes_referencia, 'mensalidade', valor, 'pendente'))
        cursor.execute("""INSERT INTO pagamentos
                        (atleta_id, mes_referencia, tipo, valor, status)
                        VALUES(?, ?, ?, ?, ?)""",
                       (atleta_id, mes_referencia, 'matricula', 100, 'pendente'))

        conexao.commit()
        conexao.close()
        return redirect(url_for('listar_atletas'))
    else:
        return render_template('novo_atleta.html')

@app.route('/pagamentos')
def pagamentos():

    mes = request.args.get('mes')
    ano = request.args.get('ano')
    categoria_id = request.args.get('categoria_id')

    sql = """SELECT pagamentos.*, atletas.nome
            FROM pagamentos 
            JOIN atletas ON pagamentos.atleta_id = atletas.id"""

    where = []
    params = []

    if mes and ano:
        mes_referencia = f'{ano}-{mes.zfill(2)}'
        where.append("pagamentos.mes_referencia = ?")
        params.append(mes_referencia)

    if categoria_id:
        where.append("atletas.categoria_id = ?")
        params.append(categoria_id)

    if where:
        sql += " WHERE " + " AND ".join(where)

    sql += " ORDER BY mes_referencia DESC"

    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute(sql, params)
    lista_pagamentos = cursor.fetchall()

    sql_total = "SELECT SUM(valor) FROM pagamentos JOIN atletas ON pagamentos.atleta_id = atletas.id"

    if where:
        sql_total += " WHERE " + " AND ".join(where)
        cursor.execute(sql_total + " AND pagamentos.status = 'pago'", params)
    else:
        cursor.execute(sql_total + " WHERE pagamentos.status = 'pago'")
    total_recebido = cursor.fetchone()[0] or 0
    
    if where:
        cursor.execute(sql_total + " AND pagamentos.status = 'pendente'", params)
    else:
        cursor.execute(sql_total + " WHERE pagamentos.status = 'pendente'")
    total_pendente = cursor.fetchone()[0] or 0

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    conexao.close()

    return render_template('pagamentos.html', lista_pagamentos = lista_pagamentos, total_recebido = total_recebido, total_pendente = total_pendente, mes = mes, ano = ano, categoria_id = categoria_id, categorias = categorias)
        

@app.route('/pagamentos/<int:id>/pagar', methods = ['POST'])
def marcar_pago(id):

    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("UPDATE pagamentos SET status = 'pago' WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for('pagamentos'))

@app.route('/pagamentos/gerar', methods = ['POST'])
def gerar_cobranca():
    conexao = sqlite3.connect('banco.db')
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()


    mes = request.form['mes']
    ano = request.form['ano']
    mes_referencia = f'{ano}-{mes.zfill(2)}'

    cursor.execute("SELECT * FROM atletas WHERE status = 'ativo'")
    atletas = cursor.fetchall()

    for atleta in atletas:
        cursor.execute("""SELECT * FROM relacao_atletas 
                        WHERE atleta_id = ?""", (atleta['id'],))
        modalidades = cursor.fetchall()
        num_modalidades = len(modalidades)

        valor = calcular_valor(atleta['bolsa'], num_modalidades, atleta['desconto']) 

        cursor.execute("""SELECT id FROM pagamentos
                        WHERE atleta_id = ? AND mes_referencia = ? AND tipo = 'mensalidade'""", (atleta['id'], mes_referencia))
        ja_existe = cursor.fetchone()

        if not ja_existe:
            cursor.execute("""INSERT INTO pagamentos 
                            (atleta_id, mes_referencia, tipo, valor, status )
                            VALUES (?, ?, ?, ? ,? )""",
                            (atleta['id'], mes_referencia, 'mensalidade', valor, 'pendente'))

    conexao.commit()
    conexao.close()

    return redirect(url_for('pagamentos'))  
    

if __name__ == '__main__':
    app.run(debug=True)

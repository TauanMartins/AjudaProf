from checar_sessao import *


class Professor:
    def __init__(self, app):

        def verify_password(senha_crip, senha):
            return check_password_hash(senha_crip, senha)

        # abaixo é feito a primeira solicitação do login que caíra no GET
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele fará um request = post em /login_p novamente e
        # entrará na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_p', methods=['POST', 'GET'])
        def login_professor():
            if request.method == "POST":
                # pega oq o prof digitou no usuario e senha
                usuario_p = request.form['usuario_p']
                senha_p = request.form['senha_p']

                # abre o banco de dados
                mysql = db.SQL()

                # puxa do banco de dados info(usuario e senha) do usuário q
                # logou, isso puxará a senha para a validação
                comando = "SELECT matricula_professor AS usuario, senha_professor as senha_crip," \
                          "nme_professor as nome FROM tb_professor WHERE matricula_professor=%s;"
                cs = mysql.consultar(comando, [usuario_p])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n existir, vai entrar
                # na primeira condiçao onde retornará dados invalidos e requisitara outro login
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_p')
                elif not (verify_password(dados[1], senha_p)):
                    return redirect('/login_p')

                # se existirem dados validos o programa retora o elif
                # abaixo, permitindo o usuario entrar no menu principal
                elif verify_password(dados[1], senha_p):
                    session.permanent = True
                    session['user_p'] = usuario_p
                    return redirect('/menu_principal_prof')

            # abaixo um comando get
            else:
                # if abaixo valida se o usuário ja estava logada na maquina
                # permitindo uma entrada mais rápida.
                if "user_p" in session:
                    return redirect('/menu_principal_prof')
                return render_template('login_p.html')

        @app.route('/menu_principal_prof', methods=['POST', 'GET'])
        @checar_sessao_professor
        def menu_principal_prof():
            mural_msg = ''
            ocorrencias_msg = ''
            if request.method == "GET":
                # chama o banco
                mysql = db.SQL()
                # mostra o nome do usuário
                comando = "SELECT idt_professor, nme_professor FROM tb_professor WHERE matricula_professor=%s;"
                cs = mysql.consultar(comando, [session['user_p']])
                dados = cs.fetchone()

                # consultar todas as mensagens
                comando1 = "SELECT mural_mensagem, data_mensagem FROM tb_mural join ta_mural_professor " \
                           "join ta_mural_aluno join tb_responsavel join tb_aluno join tb_professor on cod_ta_ma_aluno=idt_aluno and " \
                           "cod_ta_ma_mural=idt_mural and cod_ta_mp_professor=idt_professor and cod_ta_mp_mural=idt_mural;"
                cs1 = mysql.consultar(comando1, ())

                # formando o select para jogar no menu principal
                for [mural_mensagem, data_mensagem] in cs1:
                    mural_msg += f"""<tr style="height: 39px;">
                                        <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">{data_mensagem}</td>
                                        <td class="u-border-1 u-border-grey-75 u-table-cell">{mural_mensagem}</td>
                                        </tr>"""

                # consultar todas as ocorrencias
                comando2 = "SELECT * FROM tb_ocorrencia WHERE cod_ocorrencia_prof=%s;"
                cs2 = mysql.consultar(comando2, [dados[0]])

                # formando o select para jogar no menu principal
                for [idt_ocorrencia, ocorrencia_msg, cod_ocorrencia_aluno, cod_ocorrencia_prof] in cs2:
                    ocorrencias_msg += f"""<tr style="height: 39px;">
                                    <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">data</td>
                                    <td class="u-border-1 u-border-grey-75 u-table-cell">{cod_ocorrencia_aluno}</td>
                                    <td class="u-border-1 u-border-grey-75 u-table-cell">{ocorrencia_msg}</td>
                                  </tr>"""
                return render_template('menu_principal_prof.html', mural_msg=mural_msg, ocorrencias_msg=ocorrencias_msg, nome=dados[1])
            elif request.method == "POST" and request.form.get('mensagem') is not None:
                # puxa do banco de dados a mensagem que foi digitada para o mural
                mural = request.form['mensagem']
                data = request.form['data']
                # abre o banco de dados p postagem a mensagem no banco
                mysql = db.SQL()
                comando = "INSERT INTO tb_mural(mural_mensagem, data_mensagem, cod_mural_professor," \
                          " cod_mural_aluno, cod_mural_resp) VALUES(%s, %s, %s, %s, %s);"
                cs = mysql.executar(comando, [mural, data, 6, 8, 1234567890])
                mysql.cnx.commit()
                return mural_msg
            elif request.method == "POST" and request.form.get("ocorrencia") is not None:
                print("terceira cond")
                # puxa do banco de dados a mensagem que foi digitada para o mural
                ocorrencia = request.form['ocorrencia']
                data = request.form['data']
                matricula = request.form['matricula']
                # abre o banco de dados p postagem a mensagem no banco
                mysql = db.SQL()

                comando0 = "SELECT idt_professor FROM tb_professor WHERE matricula_professor=%s;"
                cs0 = mysql.consultar(comando0, [(session["user_p"])])
                dados = cs0.fetchone()

                comando1 = "SELECT idt_aluno FROM tb_aluno WHERE matricula_aluno=%s;"
                cs1 = mysql.consultar(comando1, [matricula])
                dados1 = cs1.fetchone()

                comando2 = "INSERT INTO tb_ocorrencia(ocorrencia_msg, cod_ocorrencia_aluno, cod_ocorrencia_prof) VALUES(%s, %s, %s);"
                cs = mysql.executar(comando2, [ocorrencia, dados1[0], dados[0]])
                mysql.cnx.commit()
                return mural_msg

        @app.route('/inserir_aula', methods=["POST", "GET"])
        @checar_sessao_professor
        def inserir_aula():
            disc = ""
            # metodo get para renderizar pagina com caixas p inserção da aula
            if request.method == "GET":
                # abre o banco para puxar o idt da disciplina e fazer um select com todas as informações
                mysql = db.SQL()
                comando = "SELECT idt_disciplina, nme_disciplina, cod_disciplina_serie FROM tb_professor join tb_disciplina on " \
                          "cod_disciplina_professor=idt_professor and matricula_professor=%s order by cod_disciplina_serie;"
                cs = mysql.consultar(comando, [(session["user_p"])])

                # são tratadas as informaçoes para por em um select
                disc += '<select id="disciplina" class="u-border-1 u-border-grey-30 u-input u-input-rectangle">'
                for [idt_disciplina, nme_disciplina, serie] in cs:
                    disc += f"""<option value="{idt_disciplina}" >{nme_disciplina} - {serie}º Ano</option> """
                disc += "</select>"
                return render_template('inserir_aula.html', disciplina=disc)

            # metodo post para inserir a tabela aula e a relacao dos alunos e a aula
            elif request.method == "POST":
                # comandos para puxar dados que o professor digitou
                disciplina = request.form["disciplina"]
                conteudo = request.form["conteudo"]
                data = request.form["data"]
                bimestre = request.form["bimestre"]

                # abre o banco e abre uma transação para inserção da aula e relação
                mysql = db.SQL()
                mysql.cnx.start_transaction()

                # insere a aula com os dados digitados
                comando0 = "INSERT INTO tb_aula(dt_aula, conteudo_aula, cod_aula_disciplina, " \
                           "cod_aula_bimestre) values(%s, %s, %s, %s);"
                mysql.executar(comando0, [data, conteudo, disciplina, bimestre])

                # pega o último idt criado
                idt_aula = mysql.cs.lastrowid

                # mostra a serie daquela disciplina
                comando1 = "SELECT cod_disciplina_serie from tb_disciplina where idt_disciplina=%s"
                cs = mysql.consultar(comando1, [disciplina])
                serie = cs.fetchone()

                # mostra os alunos daquela disciplina/serie
                comando = "SELECT idt_aluno, nme_aluno FROM tb_aluno JOIN ta_bimestre_turma JOIN tb_disciplina " \
                          "ON cod_aluno_serie=cod_ta_serie_turma WHERE cod_ta_bimestre=%s " \
                          "AND cod_ta_serie_turma=%s AND idt_disciplina=%s;"
                cs = mysql.consultar(comando, ([bimestre, serie[0], disciplina]))

                # comando para inserir a relação
                comando2 = "INSERT INTO ta_aula_aluno(cod_ta_aula, cod_ta_aluno) VALUES"
                for [idt_aluno, nme_aluno] in cs:
                    comando2 += f"({idt_aula}, {idt_aluno}),"
                # comandos para retirar a última vírgula e coloca um ; pra nao haver conflito
                comando2 = comando2[:-1]
                comando2 += ";"

                # comandos para executar comandos anteriores de inserir no banco
                mysql.executar(comando2, [])
                mysql.cnx.commit()
                return "ok"

        @app.route('/alterar_notas', methods=["POST", "GET"])
        @checar_sessao_professor
        def alterar_notas():
            sel = ''

            # metodo get p renderizar pagina de alteracao de notas
            if request.method == "GET":
                return render_template('alterar_notas.html')

            # metodo post entra quase na mesma hora que o get, ao entrar na pagina
            # é pedido os alunos do sexto ano diretamente.
            elif request.method == "POST" and request.form.get("serie") is not None:
                # é pedido a serie e o bimestre bem como a matricula do professor
                idtSerie = request.form['serie']
                bimestre = request.form['bimestre']

                # abre o banco consultar o idt único daquela disciplina.
                # ex: matemática do 6 ano difere-se de matemática do 7 ano
                # possuem idts diferentes.
                banco = db.SQL()
                comando1 = "select idt_disciplina, nme_disciplina from tb_disciplina " \
                           "join tb_professor join tb_turma on " \
                           "idt_professor=cod_disciplina_professor and " \
                           "cod_disciplina_serie=idt_serie_turma where " \
                           "matricula_professor=%s and cod_disciplina_serie=%s;"
                cs1 = banco.consultar(comando1, [(session["user_p"]), idtSerie])
                dados1 = cs1.fetchone()

                # se o professor não tiver uma turma é retornado um sel vazio,
                # esse sel mostraria todos os alunos daquela disciplina.
                if dados1 is None:
                    return sel

                # caso o professor tenha uma turma não entrará no if acima,
                # continuando o código abaixo, que puxa todos os alunos daquela
                # serie, disciplina e bimestre especificados.
                comando = "SELECT idt_aluno, nme_aluno, n1, n2, n3, rec, idt_notas," \
                          "cod_avaliacao_serie, peso_avaliacao FROM tb_aluno JOIN tb_notas " \
                          "JOIN tb_avaliacao JOIN ta_bimestre_turma JOIN tb_disciplina " \
                          "ON cod_aluno_serie=cod_ta_serie_turma AND cod_notas_aluno=idt_aluno " \
                          "AND cod_notas_avaliacao=idt_avaliacao AND " \
                          "cod_avaliacao_bimestre=cod_ta_bimestre AND " \
                          "cod_avaliacao_serie=cod_ta_serie_turma AND " \
                          "cod_avaliacao_disciplina=idt_disciplina WHERE cod_ta_bimestre=%s " \
                          "AND cod_ta_serie_turma=%s AND idt_disciplina=%s ORDER BY nme_aluno;"
                cs = banco.consultar(comando, ([bimestre, idtSerie, dados1[0]]))

                # abaixo é mostrado o começo da tabela
                sel += f"""
                              <tr style="height: 26px;">
                            <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">Alunos</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 1 de {dados1[1]}</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 2 de {dados1[1]}</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 3 de {dados1[1]}</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Média</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Rec</td>
                            <td class="u-border-1 u-border-grey-75 u-table-cell">Alterar</td>
                          </tr>"""

                # comando do banco de dados retornou todos os alunos, abaixo são tratados
                # cada aluno para ser mostrado na tela a tabela com todos os alunos.
                for [idt_aluno, nme_aluno, n1, n2, n3, rec, idt_notas, cod_avaliacao_serie,
                     peso_avaliacao] in cs:
                    if (n1 or n2 or n3) != 0:
                        media_calc = (((n1 * peso_avaliacao) + (n2 * peso_avaliacao) + (n3 * peso_avaliacao)) /
                                      (peso_avaliacao + peso_avaliacao + peso_avaliacao))
                    else:
                        media_calc = 0
                    sel += f"""<tr style="height: 26px;">
                                        <td class="u-border-2 u-border-grey-dark-1
                                        u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                                        <input type="hidden" name='idt_aluno'
                                        id="idt_aluno_{idt_notas}" value="{idt_aluno}"/>
                                        <input type="hidden" name='serie2'
                                        id="serie_{idt_notas}" value="{cod_avaliacao_serie}"/>
                                        <input type="hidden" name='media' id="media_{idt_notas}"
                                        value="{media_calc:.2f}"/><td class="u-border-1
                                        u-border-grey-75 u-table-cell"><input style="width:110px;"
                                        type="number" name='n1' id="n1_{idt_notas}" value="{n1}"/></td>
                                        <td class="u-border-1 u-border-grey-75 u-table-cell">
                                        <input style="width:110px;" type="number" name='n2'
                                        id="n2_{idt_notas}" value="{n2}"/></td><td class="u-border-1
                                        u-border-grey-75 u-table-cell"><input style="width:110px;"
                                        type="number" name='n3' id="n3_{idt_notas}" value="{n3}"/></td>
                                        <td class="u-border-1 u-border-grey-75 u-table-cell">{media_calc:.2f}</td>
                                        <td class="u-border-1 u-border-grey-75 u-table-cell">{rec}</td>
                                        <td class="u-border-1 u-border-grey-75 u-table-cell">
                                        <button onclick="alterar({idt_notas})">Alterar</button></td></tr>"""

                return sel

            # comando abaixo é para caso o professor mude a nota de um aluno.
            elif request.method == "POST":
                # são pedidos todos os dados necessários para inclusão das notas.
                idt_notas = int(request.form['idt_nota'])
                idt_aluno = request.form['idt_aluno']
                media_calc = float(request.form['media_calc'])
                n1 = float(request.form['n1'])
                n2 = float(request.form['n2'])
                n3 = float(request.form['n3'])

                # banco é aberto e é mostrado o boletim(idt) daquele aluno específico
                # para inserir as notas nele.
                mysql = db.SQL()
                comando = "SELECT idt_avaliacao FROM tb_aluno JOIN tb_notas " \
                          "JOIN tb_avaliacao JOIN ta_bimestre_turma JOIN " \
                          "tb_disciplina ON cod_aluno_serie=cod_ta_serie_turma " \
                          "AND cod_notas_aluno=idt_aluno AND cod_notas_avaliacao=idt_avaliacao " \
                          "AND cod_avaliacao_bimestre=cod_ta_bimestre AND " \
                          "cod_avaliacao_serie=cod_ta_serie_turma AND " \
                          "cod_avaliacao_disciplina=idt_disciplina WHERE idt_notas=%s;"
                cs0 = mysql.consultar(comando, [idt_notas])
                idt_av = cs0.fetchone()

                # comando abaixo faz o update das notas do boletim de acordo com
                # todos os dados requisitados.
                comando = "UPDATE tb_notas SET n1=%s, n2=%s, n3=%s, media=%s WHERE " \
                          "cod_notas_avaliacao=%s AND cod_notas_aluno=%s AND idt_notas=%s;"
                mysql.executar(comando, [n1, n2, n3, media_calc, int(idt_av[0]), idt_aluno, idt_notas])
                mysql.cnx.commit()

                return sel

        @app.route('/alterar_presenca', methods=['POST', "GET"])
        @checar_sessao_professor
        def alterar_presenca():
            # metodo get renderiza o html de alterar atividades e presença
            sel = ""
            if request.method == 'GET':
                return render_template('alterar_presenca.html')

            # metodo post entra logo em seguida, puxando dados que o professor digitou
            # para mostrar alunos e suas presenças p alteraçao
            elif request.method == "POST" and request.form.get('serie'):
                # comando p puxar dados
                idtSerie = request.form['serie']
                bimestre = request.form['bimestre']
                data = request.form['date']

                # banco é aberto para puxar idt da série
                banco = db.SQL()
                comando1 = "select idt_disciplina, nme_disciplina from tb_disciplina " \
                           "join tb_professor join tb_turma on " \
                           "idt_professor=cod_disciplina_professor and " \
                           "cod_disciplina_serie=idt_serie_turma where " \
                           "matricula_professor=%s and cod_disciplina_serie=%s;"
                cs1 = banco.consultar(comando1, [(session["user_p"]), idtSerie])
                dados1 = cs1.fetchone()

                # se o professor não tiver uma turma é retornado nada na tela
                if dados1 is None:
                    return sel

                # comando para mostrar todos os alunos e suas presencas
                comando = "SELECT idt_aluno, nme_aluno, presen_aula, conteudo_aula, idt_aula FROM tb_aluno " \
                          "JOIN ta_aula_aluno JOIN tb_aula JOIN ta_bimestre_turma JOIN tb_disciplina " \
                          "ON idt_aluno=cod_ta_aluno AND idt_aula=cod_ta_aula AND " \
                          "cod_ta_serie_turma=cod_disciplina_serie AND cod_aula_disciplina=idt_disciplina " \
                          "AND cod_aula_bimestre=cod_ta_bimestre WHERE tb_aula.cod_aula_bimestre=%s " \
                          "AND cod_ta_serie_turma=%s AND idt_disciplina=%s and dt_aula=%s ORDER BY nme_aluno;"
                cs = banco.consultar(comando, ([bimestre, idtSerie, dados1[0], data]))

                # a partir daqui é tratado todos os alunos para mostrar na tela
                sel += """<tr style="height: 26px;">
                                <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">Alunos</td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">Presença</td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">Alterar</td>
                              </tr>"""
                for [idt_aluno, nme_aluno, presen_aula, conteudo_aula, idt_aula] in cs:
                    sel += f"""<tr style="height: 26px;">
                                <input type="hidden" name='serie' id="serie2" value="{idtSerie}"/>
                                <input type="hidden" name='idt_aula_aluno_{idt_aluno}'
                                 id="idt_aula" value="{idt_aula}"/>
                                <input type="hidden" name='idt_aluno' id="idt_aluno_{idt_aluno}" value="{idt_aluno}"/>
                                <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">{nme_aluno}</td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">{presen_aula}</td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">
                                <select onchange=alterar({idt_aluno}) id="presenca_{idt_aluno}" name="presenca">
                                        <option value="{presen_aula}">Alterar</option>
                                        <option value="Presente">Presente</option>
                                        <option value="Falta">Falta</option></td></tr>"""

                return sel
            # metodo post para puxar dados para alteracao
            elif request.method == "POST":
                # comandos para alteracao da presenca dos alunos
                idt_aluno = int(request.form["idt_aluno"])
                idt_aula = request.form["idt_aula"]
                presenca = (request.form["presenca"])

                # abre o banco para alterar os dados do aluno em relacao aos dados requisitados
                mysql = db.SQL()
                comando = "UPDATE ta_aula_aluno SET presen_aula=%s WHERE cod_ta_aluno=%s AND cod_ta_aula=%s;"
                mysql.executar(comando, ([presenca, idt_aluno, idt_aula]))
                mysql.cnx.commit()
                return sel

        @app.route('/editar_perfil_p', methods=['POST', "GET"])
        @checar_sessao_professor
        def editar_perfil_p():
            # comando get para renderizar o html de editar perfil do prof
            if request.method == "GET":
                # abre o banco de dados para mostrar todos os dados p alterar
                mysql = db.SQL()
                comando = "SELECT * FROM tb_professor WHERE matricula_professor=%s;"
                cs = mysql.consultar(comando, [session['user_p']])
                dados = cs.fetchone()
                return render_template('editar_perfil_professor.html',
                                       nome=dados[1], nasc=dados[4], matricula=dados[3], sangue=dados[5])

            elif request.method == "POST":
                # metodo post para alteração dos dados, abaixo é puxado todos
                # os dados alterados do professor e faz o update no banco
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                data = request.form["data"]
                sangue = request.form["sangue"]

                # abre o banco para fazer o update
                mysql = db.SQL()
                comando = "UPDATE tb_professor SET nme_professor=%s, matricula_professor=%s, " \
                          "nasc_professor=%s, sangue_professor=%s WHERE matricula_professor=%s;"
                mysql.executar(comando, [nme, matricula, data, sangue, session['user_p']])
                mysql.cnx.commit()
                return 'ok'

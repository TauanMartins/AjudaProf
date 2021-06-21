from flask import Flask, render_template, request, redirect, session
import bd
from checker_prof import check_logged_in_p
from checker_aluno import check_logged_in_a
from checker_resp import check_logged_in_r
from checker_dir import check_logged_in_d
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash


class AjudaProf:

    def __init__(self):

        def verify_password(senha_crip, senha):
            return check_password_hash(senha_crip, senha)

        @app.route('/')
        def primeira_tela():
            session.pop('user_p', None)
            session.pop('user_a', None)
            session.pop('user_r', None)
            session.pop('user_d', None)
            return render_template('Primeira_TelaNN//primeira_tela.html')

        # rotas do prof começam aqui
        # abaixo é feito a primeira solicitação do login que caíra no ultimo else
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele dá um request = post em /login_p novamente
        # entra na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_p', methods=['POST', 'GET'])
        def login_professor():
            if request.method == "POST":
                # pega oq o prof digitou no usuario e senha
                usuario_p = request.form['usuario_p']
                senha_p = request.form['senha_p']

                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "SELECT matricula_professor AS usuario, senha_professor as senha_crip," \
                          "nme_professor as nome FROM tb_professor WHERE matricula_professor=%s;"
                cs = mysql.consultar(comando, [usuario_p])
                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                print(cs)
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_p')
                elif not (verify_password(dados[1], senha_p)):
                    return redirect('/login_p')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                elif verify_password(dados[1], senha_p):
                    session.permanent = True
                    session['user_p'] = usuario_p
                    return redirect('/menu_principal_prof')
            else:
                if "user_p" in session:
                    return redirect('/menu_principal_prof')
                return render_template('Primeira_TelaNN//login_p.html')

        @app.route('/menu_principal_prof', methods=['POST', 'GET'])
        @check_logged_in_p
        def menu_principal_prof():
            # chamar o banco
            mysql = bd.SQL()
            comando = "SELECT nme_professor FROM tb_professor WHERE matricula_professor=%s;"
            cs = mysql.consultar(comando, [session['user_p']])
            dados = cs.fetchone()
            mural_msg = ''
            ocorrencias_msg = ''

            mysql = bd.SQL()
            # consultar todas as mensagens
            comando = "SELECT * FROM tb_msg;"
            # cs = mysql.consultar(comando, ())

            mysql = bd.SQL()
            # consultar todas as mensagens
            comando = "SELECT * FROM tb_ocorrencia;"
            # cs = mysql.consultar(comando, ())

            # printar tudo na tela
            # for msg in csT:
            #  mural_msg += f"""<tr style="height: 56px;"><td class="u-border-1 u-border-grey-dark-1 u-table-cell">{msg}</td></tr>"""

            # for msg in csT:
            #  ocorrencias_msg += f"""<tr style="height: 56px;"><td class="u-border-1 u-border-grey-dark-1 u-table-cell">{msg}</td></tr>"""

            if request.method == "POST":
                mural = request.form['muralmsg']
                # abre o banco de dados
                mysql = bd.SQL()
                # posta a mensagem no banco
                comando = "INSERT INTO tb_msg(msg) VALUES(%s);"
                # cs = mysql.consultar(comando, [mural])
                return "ok"
            return render_template('Primeira_TelaNN//menu_principal_prof.html', mural_msg=mural_msg,
                                   ocorrencias_msg=ocorrencias_msg, nome=dados[0])

        @app.route('/alterar_notas', methods=["POST", "GET"])
        @check_logged_in_p
        def alterar_notas():
            sel = ''
            if request.method == "GET":
                return render_template('Primeira_TelaNN//alterar_notas.html')
            elif request.method == "POST" and request.form.get("idtSerie") is None:
                print("terceira cond")
                idtSerie = request.form['serie']
                bimestre = request.form['bimestre']
                banco = bd.SQL()
                comando1 = "select idt_disciplina from tb_disciplina join tb_professor on idt_professor=cod_professor WHERE matricula_professor=%s;"
                cs1 = banco.consultar(comando1, [(session["user_p"])])
                dados1 = cs1.fetchone()
                mysql = bd.SQL()
                comando = "SELECT idt_aluno, nme_aluno as Nome, n1, n2, n3, media, rec FROM tb_aluno JOIN tb_notas JOIN tb_turma JOIN tb_avaliacao " \
                          "JOIN tb_disciplina JOIN ta_bimestre_turma JOIN tb_bimestre ON tb_aluno.idt_aluno=tb_notas.cod_aluno AND " \
                          "tb_aluno.cod_turma=tb_turma.idt_serie_turma AND tb_avaliacao.idt_avaliacao=tb_notas.cod_avaliacao AND " \
                          "tb_disciplina.idt_disciplina=tb_avaliacao.cod_disciplina AND tb_turma.idt_serie_turma=ta_bimestre_turma.cod_serie_turma " \
                          "AND tb_bimestre.idtb_bimestre=ta_bimestre_turma.cod_bimestre WHERE idtb_bimestre=%s AND idt_serie_turma=%s AND idt_disciplina=%s;"
                cs = mysql.consultar(comando, ([bimestre, idtSerie, dados1[0]]))

                dados = cs
                if dados is None:
                    dados = ["Avaliação", 0]

                sel += f"""
                      <tr style="height: 26px;">
                        <td class="u-border-1 u-border-grey-75 u-first-column u-table-cell">Alunos</td>
                        <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 1</td>
                        <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 2</td>
                        <td class="u-border-1 u-border-grey-75 u-table-cell">Avaliação 3</td>
                        <td class="u-border-1 u-border-grey-75 u-table-cell">Média</td>
                        <td class="u-border-1 u-border-grey-75 u-table-cell">Rec</td>
                      </tr>"""
                notas = " $('.n1').val},  $('.n2').val},  $('.n3').val}"
                for [idt_aluno, nme_aluno, n1, n2, n3, media, rec] in cs:
                    sel += f"""<tr style="height: 26px;">
                                <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell"><input style="width:110px;" type="number" name='n1' id="{idt_aluno}" value="{n1}"/></td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell"><input style="width:110px;" type="number" name='n2' id="{idt_aluno}" value="{n2}"/></td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell"><input style="width:110px;" type="number" name='n1' id="{idt_aluno}" value="{n3}"/></td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">{media}</td>
                                <td class="u-border-1 u-border-grey-75 u-table-cell">{rec} onload=(armazenar({idt_aluno, nme_aluno,notas, media, rec})</td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get("n1") is not None:
                sel = print("terceira cond")
                return sel

        @app.route('/alterar_presenca', methods=['POST', "GET"])
        @check_logged_in_p
        def alterar_presenca():
            # renderiza o html de alterar atividades e presença
            return render_template('Primeira_TelaNN//alterar_presenca.html')

        @app.route('/editar_perfil_p', methods=['POST', "GET"])
        @check_logged_in_p
        def editar_perfil_p():
            # renderiza o html de editar perfil do prof
            if request.method == "GET":
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_professor JOIN tb_disciplina ON cod_professor=idt_professor WHERE matricula_professor=%s;"
                cs = mysql.consultar(comando, [session['user_p']])
                dados = cs.fetchone()

                return render_template('Primeira_TelaNN//editar_perfil_professor.html', nome=dados[1], nasc=dados[4],
                                       matricula=dados[3], sangue=dados[5])

            elif request.method == "POST":
                print("post")
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                data = request.form["data"]
                sangue = request.form["sangue"]
                print(nme, matricula, data, sangue)
                mysql = bd.SQL()
                comando = "UPDATE tb_professor SET nme_professor=%s, matricula_professor=%s, nasc_professor=%s, sangue_professor=%s WHERE matricula_professor=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, data, sangue, session['user_p']])
                return 'ok'

        # rotas do prof acabam aqui
        # rotas do aluno começam aqui
        # abaixo é feito a primeira solicitação do login que caíra no ultimo else
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele dá um request = post em /login_p novamente
        # entra na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_a', methods=["POST", "GET"])
        def login_aluno():

            if request.method == "POST":
                # pega oq o aluno digitou no usuario e senha
                usuario_a = request.form['usuario_a']
                senha_a = request.form['senha_a']

                # abre o banco de dados
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "SELECT matricula_aluno AS usuario, senha_aluno AS senha, nme_aluno" \
                          " as nome FROM tb_aluno WHERE matricula_aluno=%s;"
                cs = mysql.consultar(comando, [usuario_a])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()

                if dados is None:
                    return redirect('/login_a')
                if not (verify_password(dados[1], senha_a)):
                    return redirect('/login_a')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                elif verify_password(dados[1], senha_a):
                    session.permanent = True
                    session['user_a'] = usuario_a
                    return redirect('/menu_principal_aluno')
            else:
                if "user_a" in session:
                    return redirect('/menu_principal_aluno')
                return render_template('Primeira_TelaNN//login_a.html')

        @app.route('/menu_principal_aluno', methods=['POST', 'GET'])
        @check_logged_in_a
        def menu_principal_aluno():
            return render_template('Primeira_TelaNN//menu_principal_aluno.html')

        @app.route('/ver_notas', methods=['POST', 'GET'])
        @check_logged_in_a
        def notas():
            return render_template("Primeira_TelaNN//ver_notas.html")

        @app.route('/ver_presenca_e_atividades', methods=['POST', 'GET'])
        @check_logged_in_a
        def presenca_e_atividades():
            # renderiza o html atividades e presença
            return render_template("Primeira_TelaNN//visualizar_presenca.html")

        @app.route('/editar_perfil_a', methods=['POST', 'GET'])
        @check_logged_in_a
        def editar_perfil_a():
            # renderiza o html de editar perfil+
            if request.method == "GET":
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON idt_serie_turma=cod_turma WHERE matricula_aluno=%s;"
                cs = mysql.consultar(comando, [session['user_a']])
                dados = cs.fetchone()

                return render_template('Primeira_TelaNN//editar_perfil_aluno.html', nome=dados[1], nasc=dados[4],
                                       mao=dados[5],
                                       matricula=dados[3], sangue=dados[6], serie=dados[9])

            elif request.method == "POST":
                mao = request.form["mao"]
                sangue = request.form["sangue"]
                mysql = bd.SQL()
                comando = "UPDATE tb_aluno SET mao_aluno=%s,sangue_aluno=%s WHERE matricula_aluno=%s;"
                cs2 = mysql.executar(comando, [mao, sangue, session['user_a']])
                return 'ok'

        @app.route('/esqueci_senha', methods=['POST', 'GET'])
        def esqueci_senha():
            # renderiza o html de esqueci a senha POS(login)
            return render_template('Primeira_TelaNN//esqueci_senha.html')

        @app.route('/primeiro_acesso', methods=['POST', 'GET'])
        def primeiro_acesso():
            if request.method == "POST":
                # pega oq o aluno digitou no usuario e senha
                nome = str(request.form['nome'])
                sangue = str(request.form['sangue'])
                mao = str(request.form['mao'])
                data = request.form['data']
                senha = generate_password_hash(request.form['senha'])
                nme_r = str(request.form['nme_r'])
                cpf = (request.form['cpf'])
                print(nome, sangue, mao, data, senha)
                # abre o banco de dados
                mysql1 = bd.SQL()
                comando = "INSERT INTO tb_responsavel(cpf_responsavel, nme_responsavel) " \
                          "VALUES(%s, %s);"
                cs = mysql1.executar(comando, [cpf, nme_r])
                mysql2 = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_aluno(nme_aluno, senha_aluno, " \
                          "nasc_aluno, mao_aluno, sangue_aluno, cod_responsavel) " \
                          "VALUES(%s, %s, %s, %s, %s, %s);"
                cs = mysql2.executar(comando, [nome, senha, data, mao, sangue, cpf])

                if cs:
                    msg = 'Cadastrou'
                    return redirect("/login_a")
            return render_template('Primeira_TelaNN//primeiro_acesso.html')

        # rotas do aluno acabam aqui
        # rotas do responsavel começam aqui

        @app.route('/login_r', methods=['POST', 'GET'])
        def login_responsaveis():
            if request.method == 'POST':
                # pega oq o prof digitou no usuario e senha
                usuario_r = request.form['usuario_r']

                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = f"SELECT cpf_responsavel AS cpf, nme_responsavel as nome " \
                          f"FROM tb_responsavel WHERE cpf_responsavel=%s;"
                cs = mysql.consultar(comando, [usuario_r])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()

                if dados is None:
                    return redirect('/login_r')
                # abaixo haverá a validação: comparando oq o usuario digitou e oq está no banco de dados
                if dados[0] == usuario_r:
                    session.permanent = True
                    session['user_r'] = usuario_r
                    return redirect('/menu_principal_resp')
                elif dados[0] != usuario_r:
                    return redirect('/login_r')
            else:
                if "user_r" in session:
                    return redirect('/menu_principal_resp')
                return render_template('Primeira_TelaNN//login_r.html')

        @app.route('/menu_principal_resp', methods=['POST', 'GET'])
        @check_logged_in_r
        def menu_principal_resp():
            return render_template('teste_de_login.html')

        # rotas do responsavel acabam aqui
        # rotas da diretoria começam aqui
        @app.route('/login_d', methods=['POST', 'GET'])
        def login_d():
            if request.method == "POST":
                # pega oq o aluno digitou no usuario e senha
                usuario_d = int(request.form['usuario_d'])
                senha_d = request.form['senha_d']

                # abre o banco de dados
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "SELECT matricula_diretoria AS usuario, senha_diretoria AS senha" \
                          " FROM tb_diretoria WHERE matricula_diretoria=%s;"
                cs = mysql.consultar(comando, [usuario_d])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_d')
                if not (dados[1] == senha_d):
                    return redirect('/login_d')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                elif (dados[1] == senha_d):
                    session.permanent = True
                    session['user_d'] = usuario_d
                    return redirect('/menu_principal_dir')
            else:
                if "user_d" in session:
                    return redirect('/menu_principal_dir')
                return render_template('Primeira_TelaNN//login_d.html')

        @app.route('/menu_principal_dir', methods=['POST', 'GET'])
        @check_logged_in_d
        def menu_principal_dir():
            return render_template('Primeira_TelaNN//menu_dir.html')

        @app.route('/incluir_prof', methods=['POST', 'GET'])
        @check_logged_in_d
        def incluir_prof():
            sel = ''
            if request.method == 'GET':
                return render_template('Primeira_TelaNN//incluir_prof.html')
            elif request.method == 'POST':
                nme_professor = request.form['nme_professor']
                senha_professor = generate_password_hash(request.form['senha_professor'])
                matricula_professor = request.form['matricula_professor']
                nasc_professor = request.form['date']
                sangue_professor = request.form['sangue_professor']
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_professor(nme_professor, senha_professor, " \
                          "matricula_professor," \
                          "nasc_professor, sangue_professor)" \
                          " values(%s, %s, %s, %s, %s);"

                mysql.executar(comando, [nme_professor, senha_professor, matricula_professor,
                                         nasc_professor, sangue_professor])
                return "ok"
            return render_template('Primeira_TelaNN//incluir_prof.html')

        @app.route('/alterar_prof', methods=['POST', 'GET'])
        @check_logged_in_d
        def alterar_prof():
            sel = ''
            if request.method == "GET":
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_professor join tb_disciplina on cod_professor=idt_professor ORDER BY nme_professor;"
                cs = mysql.consultar(comando, ())

                for [idt_professor, nme_professor, senha_professor, matricula_professor, nasc_professor,
                     sangue_professor,
                     idt_disciplina, nme_disciplina, cod_disciplina_turma, cod_professor] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_professor}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">********</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_professor}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_professor} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_professor} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_disciplina}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{cod_disciplina_turma}º Ano</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_professor}" onclick="especificar({idt_professor})" >Alterar</button></td></tr>"""
                return render_template('Primeira_TelaNN//alterar_prof.html', prof=sel)
            elif request.method == "POST" and request.form.get('matricula') is None:
                idtProfessor = request.form['idt']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_professor join tb_disciplina on cod_professor=idt_professor WHERE idt_professor=%s;"
                cs = mysql.consultar(comando, [int(idtProfessor)])

                for [idt_professor, nme_professor, senha_professor, matricula_professor, nasc_professor,
                     sangue_professor,
                     idt_disciplina, nme_disciplina, cod_disciplina_turma, cod_professor] in cs:
                    selectSangue = f"""<select id="sangue" name="sangue" type="text">
                                        <option value="{sangue_professor}">Sangue</option>
                                      <option value="A+">A+</option>
                                      <option value="A-">A-</option>
                                      <option value="B+">B+</option>
                                      <option value="B-">B-</option>
                                      <option value="AB+">AB+</option>
                                      <option value="AB-">AB-</option>
                                      <option value="O+">O+</option>
                                      <option value="O-">O-</option> """
                    sel += f"""<tr style="height: 43px;">
                        <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell"><input style="width:110px;" id="nome" name="nome" type="text" value="{nme_professor}"/></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;" placeholder="Senha" name="senha" id='senha' type="text" minlength='6' maxlength="8" required="required" value="{senha_professor}"/></td>
                        <td class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;" name="matricula" id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_professor}"/></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:143px;" name="data" id='data' type="date" value="{nasc_professor}" /></td> 
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSangue}</select></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_disciplina}</td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{cod_disciplina_turma}º Série/Ano</td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt' id='idt' value="{idtProfessor}" onclick="alterar({idtProfessor})">Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is not None:
                idtProfessor = request.form['idt']
                nme = request.form["nome"]
                senha = generate_password_hash(request.form["senha"])
                matricula = request.form["matricula"]
                data = request.form["data"]
                sangue = request.form["sangue"]
                mysql = bd.SQL()
                comando = "UPDATE tb_professor SET nme_professor=%s, matricula_professor=%s, senha_professor=%s, nasc_professor=%s, sangue_professor=%s WHERE idt_professor=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, senha, data, sangue, idtProfessor])
                return "alterou"

        @app.route('/matricular_aluno', methods=['POST', 'GET'])
        @check_logged_in_d
        def matricular_aluno():
            sel = ''
            # condição a seguir para caso aperto o botão
            # de mostrar alunos, mostre todos para a matrícula
            if request.method == "POST" and request.form.get('idt') is None:
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno join tb_responsavel on cod_responsavel=cpf_responsavel WHERE matricula_aluno is NULL;"
                cs = mysql.consultar(comando, ())
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno, cod_turma,
                     cod_responsavel,
                     cpf_responsavel, nme_responsavel] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td> 
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_responsavel}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >Matricular</button></td></tr>"""
                return sel
            # condição para que mostre o aluno escolhido para a matrícula
            # podendo assim editar informações erradas e matricular
            elif request.method == "POST" and request.form.get('serie') is None:
                idtAluno = request.form["idt"]
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno join tb_responsavel on cod_responsavel=cpf_responsavel WHERE idt_aluno=%s;"
                cs = mysql.consultar(comando, ([idtAluno]))
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno, cod_turma,
                     cod_responsavel,
                     cpf_responsavel, nme_responsavel] in cs:
                    selectSerie = f"""<select name="serie" id="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle"  autofocus="autofocus">
                                                                                          <option value="0">Série</option>
                                                                                          <option value="6">6º ano</option>
                                                                                          <option value="7">7º ano</option>
                                                                                          <option value="8">8º ano</option>
                                                                                          <option value="9">9º ano</option>
                                                                                          <option value="1">1º ano</option>
                                                                                          <option value="2">2º ano</option>
                                                                                          <option value="3">3º ano</option>
                                                                                        """
                    selectTurma = f"""<select id="turma" name="turma" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                                            <optionvalue="A">Turma</option>
                                                                                          <option value="A">A</option>"""
                    sel += f"""<tr style="height: 43px;">
                                                <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell"><input id="nome" name="nome" type="text" value="{nme_aluno}"/><br></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="matricula" id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_aluno}"/></td>
                                                <td class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="data" id='data' type="date" value="{nasc_aluno}" /></td> 
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSerie} /></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectTurma} /></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_responsavel}</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt' id='idt' value="{idtAluno}" onclick="matricular({idtAluno})" >Matricular</button></td></tr>"""
                return sel
            # condição para matricular o aluno e jogar no banco de dados
            elif request.method == "POST" and request.form.get('serie') is not None:
                idtAluno = request.form['idt']
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                serie = request.form["serie"]

                mysql = bd.SQL()
                comando2 = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, cod_turma=%s WHERE idt_aluno=%s;"
                cs2 = mysql.executar(comando2, [nme, matricula, serie, idtAluno])
                return "ok"
            return render_template('Primeira_TelaNN//matricular_aluno.html', aluno=sel)

        @app.route('/alterar_aluno', methods=['POST', 'GET'])
        @check_logged_in_d
        def alterar_aluno():
            sel = ''
            if request.method == "POST" and request.form.get('idt') is None:
                idtSerie = request.form['select']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON idt_serie_turma=cod_turma AND idt_serie_turma=%s ORDER BY nme_aluno;"
                cs = mysql.consultar(comando, ([idtSerie]))

                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno, cod_turma,
                     cod_responsavel,
                     idt_serie_turma, turma] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_aluno}</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{idt_serie_turma}º ano </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{turma} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is None:
                idtAluno = request.form['idt']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON idt_serie_turma=cod_turma WHERE idt_aluno=%s;"
                cs = mysql.consultar(comando, [int(idtAluno)])

                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno, cod_turma,
                     cod_responsavel, idt_serie_turma, turma] in cs:
                    selectSerie = f"""<select name="serie" id="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle"  autofocus="autofocus">
                                                                      <option value="{idt_serie_turma}">Série/Ano</option>
                                                                      <option value="6">6º ano</option>
                                                                      <option value="7">7º ano</option>
                                                                      <option value="8">8º ano</option>
                                                                      <option value="9">9º ano</option>
                                                                      <option value="1">1º ano</option>
                                                                      <option value="2">2º ano</option>
                                                                      <option value="3">3º ano</option>
                                                                    """
                    selectSangue = f"""<select id="sangue" name="sangue" type="text" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                        <option value="{sangue_aluno}">Sangue</option>
                                                                      <option value="A+">A+</option>
                                                                      <option value="A-">A-</option>
                                                                      <option value="B+">B+</option>
                                                                      <option value="B-">B-</option>
                                                                      <option value="AB+">AB+</option>
                                                                      <option value="AB-">AB-</option>
                                                                      <option value="O+">O+</option>
                                                                      <option value="O-">O-</option> """
                    selectTurma = f"""<select id="turma" name="turma" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                        <optionvalue="{turma}">Turma</option>
                                                                      <option value="A">A</option>
                                                                      <option value="B">B</option>
                                                                      <option value="C">C</option>"""
                    selectMao = f"""<select id="select-ab6a" name="mao" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                                        <option value="{mao_aluno}">Mão</option>
                                                                                      <option value="destro">Destro</option>
                                                                                      <option value="canhoto">Canhoto</option>
                                                                                      <option value="ambidestro">Ambidestro</option>"""
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell"><input id="nome" name="nome" type="text" value="{nme_aluno}"/><br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="matricula" id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_aluno}"/></td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="data" id='data' type="date" value="{nasc_aluno}" /></td> 
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSerie} /></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectTurma} /></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectMao}/></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSangue}/></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt' id='idt' value="{idtAluno}" onclick="alterar({idt_aluno})" >Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is not None:
                idtAluno = request.form['idt']
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                serie = request.form["serie"]
                turma = request.form["turma"]
                data = request.form["data"]
                mao = request.form["mao"]
                sangue = request.form["sangue"]

                mysql = bd.SQL()
                comando = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, nasc_aluno=%s, mao_aluno=%s, sangue_aluno=%s, cod_turma=%s WHERE idt_aluno=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, data, mao, sangue, serie, idtAluno])
            return render_template('Primeira_TelaNN//alterar_aluno.html', aluno=sel)

        @app.route('/incluir_disc', methods=['POST', 'GET'])
        @check_logged_in_d
        def incluir_disc():
            sel = ''
            sel2 = ''
            if request.method == 'GET':
                mysql = bd.SQL()
                comando = "SELECT idt_professor, nme_professor FROM tb_professor ORDER BY nme_professor;"
                cs = mysql.consultar(comando, ())
                sel = f"""<select id="select-20fa" name="nme_professor" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                    <option value="{0}">Professor</option>"""
                for [idt_professor, nme_professor] in cs:
                    sel += f"""<option value="{idt_professor}">{nme_professor}</option> """
                sel += "</select>"

                mysql2 = bd.SQL()
                comando2 = "SELECT idt_serie_turma FROM tb_turma ORDER BY idt_serie_turma;"
                cs2 = mysql2.consultar(comando2, ())
                sel2 = f"""<select id="select-20fa" name="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                                    <option value="{0}">Série/Ano</option>"""
                for [idt_serie_turma] in cs2:
                    sel2 += f"""<option value="{idt_serie_turma}">{idt_serie_turma}º Ano</option> """
                sel2 += "</select>"

                return render_template('Primeira_TelaNN//incluir_disc.html', nme_professor=sel, idt_serie=sel2)
            if request.method == 'POST':
                nme_disciplina = request.form['disciplina']
                idt_professor = request.form['nme_professor']
                idt_serie = request.form['serie']
                print(nme_disciplina, idt_professor, idt_serie)
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_disciplina(nme_disciplina, cod_disciplina_turma, cod_professor) values(%s, %s, %s);"

                mysql.executar(comando, [nme_disciplina, idt_serie, idt_professor])
                return "ok"
            return render_template('Primeira_TelaNN//incluir_disc.html')

        @app.route('/incluir_avaliacao', methods=['POST', 'GET'])
        @check_logged_in_d
        def incluir_avaliacao():
            sel = ''
            sel2 = ''
            if request.method == 'GET':
                # id
                mysql = bd.SQL()
                comando = "SELECT idt_disciplina, nme_disciplina FROM tb_disciplina ORDER BY nme_disciplina;"

                cs = mysql.consultar(comando, ())
                sel = f"""<select id="select-20fa" name="idt_disciplina" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                            <option value="{0}">Disciplina</option>"""
                for [idt_disciplina, nme_disciplina] in cs:
                    sel += f"""<option value="{idt_disciplina}">{nme_disciplina}</option> """
                sel += "</select>"

                mysql2 = bd.SQL()
                comando2 = "SELECT idt_serie_turma FROM tb_turma ORDER BY idt_serie_turma;"
                cs2 = mysql2.consultar(comando2, ())
                sel2 = f"""<select id="select-20fa" name="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                                            <option value="{0}">Série/Ano</option>"""
                for [idt_serie_turma] in cs2:
                    sel2 += f"""<option value="{idt_serie_turma}">{idt_serie_turma}º Ano</option> """
                sel2 += "</select>"

                return render_template('Primeira_TelaNN//incluir_avaliacao.html', nme_disciplina=sel, idt_serie=sel2)
            if request.method == 'POST':
                dt_avaliacao = request.form['date']
                idt_disciplina = int(request.form['idt_disciplina'])
                idt_serie = int(request.form['serie'])
                print(dt_avaliacao, idt_disciplina, idt_serie)
                mysql1 = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando1 = "INSERT INTO tb_avaliacao(dt_avaliacao, cod_disciplina, cod_avaliacao_turma) values(%s, %s, %s);"
                mysql1.executar(comando1, [dt_avaliacao, idt_disciplina, idt_serie])

                mysql2 = bd.SQL()
                comando2 = "SELECT idt_avaliacao FROM tb_avaliacao WHERE dt_avaliacao=%s AND cod_disciplina=%s AND cod_avaliacao_turma=%s;"
                cs = mysql2.consultar(comando2, [dt_avaliacao, idt_disciplina, idt_serie])
                dados = cs.fetchone()
                print(dados[0])
                mysql3 = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando3 = "select idt_aluno from tb_aluno join tb_turma on tb_aluno.cod_turma=tb_turma.idt_serie_turma where idt_serie_turma=%s;"
                alunos = mysql3.consultar(comando3, [(dados[0])])

                mysql4 = bd.SQL()
                comando4 = "INSERT INTO tb_notas(cod_aluno, cod_avaliacao) VALUES"
                for [idt_aluno] in alunos:
                    comando4 += f"({idt_aluno}, {dados[0]}),"
                comando4 = comando4[:-1]
                comando4 += ";"
                print(comando4)


                mysql4.executar(comando4, [])
                return "ok"


app = Flask(__name__)
app.secret_key = "SenhaSecreta"
app.permanent_session_lifetime = timedelta(minutes=60)
AjudaProf()
if __name__ == '__main__':
    app.run(debug=True)

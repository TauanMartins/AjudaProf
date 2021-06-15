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
                cs = mysql.consultar(comando, [int(usuario_p)])
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
            mural_msg = ''
            ocorrencias_msg = ''

            mysql = bd.SQL()
            # consultar todas as mensagens
            comando = "SELECT * FROM tb_msg;"
            # cs = mysql.consultar(comando, ())
            csT = ["Oi", "Teste2", "Professora mandando", "Diretora mandando", "Opa ai sim", "Desse jeito"]
            if csT is None:
                msg = "Nenhuma mensagem"

            mysql = bd.SQL()
            # consultar todas as mensagens
            comando = "SELECT * FROM tb_ocorrencia;"
            # cs = mysql.consultar(comando, ())
            csT = ["Oi", "Teste2", "Professora mandando", "Diretora mandando", "Opa ai sim", "Desse jeito"]
            if csT is None:
                msg = "Nenhuma mensagem"

            # printar tudo na tela
            for msg in csT:
                mural_msg += f"""<tr style="height: 56px;"><td class="u-border-1 u-border-grey-dark-1 u-table-cell">{msg}</td></tr>"""

            for msg in csT:
                ocorrencias_msg += f"""<tr style="height: 56px;"><td class="u-border-1 u-border-grey-dark-1 u-table-cell">{msg}</td></tr>"""

            if request.method == "POST":
                mural = request.form['muralmsg']
                # abre o banco de dados
                mysql = bd.SQL()
                # posta a mensagem no banco
                comando = "INSERT INTO tb_msg(msg) VALUES(%s);"
                # cs = mysql.consultar(comando, [mural])
                return "ok"
            return render_template('Primeira_TelaNN//menu_principal_prof.html', mural_msg=mural_msg,
                                   ocorrencias_msg=ocorrencias_msg)

        @app.route('/alterar_notas', methods=["POST", "GET"])
        @check_logged_in_p
        def alterar_notas():
            return render_template('Primeira_TelaNN//alterar_notas.html')

        @app.route('/alterar_presenca', methods=['POST', "GET"])
        @check_logged_in_p
        def alterar_presenca():
            # renderiza o html de alterar atividades e presença
            return 'entrou'

        @app.route('/editar_perfil_p')
        @check_logged_in_p
        def editar_perfil_p():
            # renderiza o html de editar perfil do prof
            pass

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
                usuario_a = int(request.form['usuario_a'])
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
            return render_template('teste_de_login.html')

        @app.route('/ver_notas', methods=['POST', 'GET'])
        @check_logged_in_a
        def notas():
            return render_template("Primeira_TelaNN//ver_notas.html")

        @app.route('/ver_presenca_e_atividades', methods=['POST', 'GET'])
        @check_logged_in_a
        def presenca_e_atividades():
            # renderiza o html atividades e presença
            pass

        @app.route('/editar_perfil_a', methods=['POST', 'GET'])
        @check_logged_in_a
        def editar_perfil_a():
            # renderiza o html de editar perfil
            pass

        @app.route('/esqueci_senha', methods=['POST', 'GET'])
        def esqueci_senha():
            # renderiza o html de esqueci a senha POS(login)
            pass

        @app.route('/primeiro_acesso', methods=['POST', 'GET'])
        def primeiro_acesso():
            if request.method == "POST":
                # pega oq o aluno digitou no usuario e senha
                nome = str(request.form['nome'])
                matricula = int(request.form['matricula'])
                sangue = str(request.form['sangue'])
                mao = str(request.form['mao'])
                data = request.form['data']
                senha = generate_password_hash(request.form['senha'])
                if request.form['senha'] != request.form['senha1']:
                    print("senhas n compatíveis")
                    return redirect("/login_a")
                print(nome, matricula, sangue, mao, data, senha)
                # abre o banco de dados
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_aluno(nme_aluno, senha_aluno, " \
                          "matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno) " \
                          "VALUES(%s, %s, %s, %s, %s, %s);"
                cs = mysql.executar(comando, [nome, senha, matricula, data, mao, sangue])
                if cs:
                    return redirect("/login_a")
            return render_template('Primeira_TelaNN//primeiro_acesso.html')

        # rotas do aluno acabam aqui
        # rotas do responsavel começam aqui

        @app.route('/login_r', methods=['POST', 'GET'])
        def login_responsaveis():
            if request.method == 'POST':
                # pega oq o prof digitou no usuario e senha
                usuario_r = int(request.form['usuario_r'])

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
                if not (verify_password(dados[1], senha_d)):
                    return redirect('/login_d')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                elif verify_password(dados[1], senha_d):
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
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_disciplina ORDER BY nme_disciplina;"
                cs = mysql.consultar(comando, ())
                sel = f"""<select id="select-20fa" name="disc_professor" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                        <option value="{0}">Disciplina</option>"""
                for [idt_disciplina, nme_disciplina] in cs:
                    sel += f"""<option value="{idt_disciplina}">{nme_disciplina}</option> """
                sel += "</select>"
                return render_template('Primeira_TelaNN//incluir_prof.html', disciplina=sel)
            elif request.method == 'POST':
                nme_professor = request.form['nme_professor']
                senha_professor = generate_password_hash(request.form['senha_professor'])
                matricula_professor = int(request.form['matricula_professor'])
                nasc_professor = request.form['date']
                sangue_professor = request.form['sangue_professor']
                disc_professor = request.form['disc_professor']
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_professor(nme_professor, senha_professor, " \
                          "matricula_professor," \
                          "nasc_professor, sangue_professor, cod_disciplina)" \
                          " values(%s, %s, %s, %s, %s, %s);"

                mysql.executar(comando, [nme_professor, senha_professor, matricula_professor,
                                         nasc_professor, sangue_professor, disc_professor])
            return render_template('Primeira_TelaNN//incluir_prof.html')

        @app.route('/alterar_prof', methods=['POST', 'GET'])
        @check_logged_in_d
        def alterar_prof():
            sel = ''
            if request.method == "GET":
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_professor join tb_disciplina on cod_disciplina=idt_disciplina ORDER BY nme_professor;"
                cs = mysql.consultar(comando, ())

                for [idt_professor, nme_professor, senha_professor, matricula_professor, nasc_professor,
                     sangue_professor, cod_displina,
                     idt_disciplina, nme_disciplina] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_professor}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">********</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_professor}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_professor} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_professor} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_disciplina}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_professor}" onclick="especificar({idt_professor})" >Alterar</button></td></tr>"""
                return render_template('Primeira_TelaNN//alterar_prof.html', prof=sel)
            elif request.method == "POST" and request.form.get('matricula') is None:
                idtProfessor = request.form['idt']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_professor join tb_disciplina on cod_disciplina=idt_disciplina WHERE idt_professor=%s;"
                mysql2 = bd.SQL()
                cs = mysql.consultar(comando, [int(idtProfessor)])
                comando2 = "select * from tb_disciplina;"
                cs2 = mysql2.consultar(comando2, ())

                for [idt_professor, nme_professor, senha_professor, matricula_professor, nasc_professor,
                     sangue_professor, cod_displina, idt_disciplina, nme_disciplina] in cs:
                    selectDisciplina = f"""<select id="disciplina" name="disciplina" >
                                            <option value="{idt_disciplina}">Disciplina</option>"""
                    for [idt_disciplina, nme_disciplina] in cs2:
                        selectDisciplina += f"""<option value="{idt_disciplina}">{nme_disciplina}</option> """
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
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;" name="senha" id='senha' type="text" minlength='10' maxlength="10" required="required" value="********"/></td>
                        <td class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;" name="matricula" id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_professor}"/></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:143px;" name="data" id='data' type="date" value="{nasc_professor}" /></td> 
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSangue}</select></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectDisciplina} </select></td>
                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt' id='idt' value="{idtProfessor}" onclick="alterar({idtProfessor})">Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is not None:
                idtProfessor = request.form['idt']
                nme = request.form["nome"]
                senha = generate_password_hash(request.form["senha"])
                matricula = request.form["matricula"]
                disciplina = request.form["disciplina"]
                data = request.form["data"]
                sangue = request.form["sangue"]
                mysql = bd.SQL()
                comando = "UPDATE tb_professor SET nme_professor=%s, matricula_professor=%s, senha_professor=%s, cod_disciplina=%s, nasc_professor=%s, sangue_professor=%s WHERE idt_professor=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, senha, disciplina, data, sangue, idtProfessor])
                return "alterou"

        @app.route('/matricular_aluno', methods=['POST', 'GET'])
        @check_logged_in_d
        def matricular_aluno():
            sel = ''
            # condição a seguir para caso aperto o botão
            # de mostrar alunos, mostre todos para a matrícula
            if request.method == "POST" and request.form.get('idt') is None:
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno WHERE serie_aluno is NULL;"

                cs = mysql.consultar(comando, ())

                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, serie_aluno, turma_aluno,
                     mao_aluno, sangue_aluno] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_aluno}</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td> 
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{serie_aluno}º ano </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{turma_aluno} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >Matricular</button></td></tr>"""
                return sel
            # condição para que mostre o aluno escolhido para a matrícula
            # podendo assim editar informações erradas e matricular
            elif request.method == "POST" and request.form.get('serie') is None:
                idtAluno = request.form["idt"]
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno WHERE idt_aluno=%s ORDER BY nme_aluno;"
                cs = mysql.consultar(comando, [idtAluno])
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, serie_aluno, turma_aluno,
                     mao_aluno, sangue_aluno] in cs:
                    selectSerie = f"""<select name="serie" id="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle"  autofocus="autofocus">
                                                                                          <option value="{serie_aluno}">Série</option>
                                                                                          <option value="6">6º ano</option>
                                                                                          <option value="7">7º ano</option>
                                                                                          <option value="8">8º ano</option>
                                                                                          <option value="9">9º ano</option>
                                                                                          <option value="1">1º ano</option>
                                                                                          <option value="2">2º ano</option>
                                                                                          <option value="3">3º ano</option>
                                                                                        """
                    selectTurma = f"""<select id="turma" name="turma" class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                                            <optionvalue="{turma_aluno}">Turma</option>
                                                                                          <option value="A">A</option>
                                                                                          <option value="B">B</option>
                                                                                          <option value="C">C</option>"""
                    sel += f"""<tr style="height: 43px;">
                                                <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell"><input id="nome" name="nome" type="text" value="{nme_aluno}"/><br></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="matricula" id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_aluno}"/></td>
                                                <td class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="data" id='data' type="date" value="{nasc_aluno}" /></td> 
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSerie} /></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectTurma} /></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt' id='idt' value="{idtAluno}" onclick="matricular({idtAluno})" >Matricular</button></td></tr>"""
                return sel
            # condição para matricular o aluno e jogar no banco de dados
            elif request.method == "POST" and request.form.get('serie') is not None:
                idtAluno = request.form['idt']
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                serie = request.form["serie"]
                turma = request.form["turma"]
                data = request.form["data"]
                mysql = bd.SQL()
                comando = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, serie_aluno=%s, turma_aluno=%s WHERE idt_aluno=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, serie, turma, idtAluno])
                # insert na tabela boletim
                return "ok"
            return render_template('Primeira_TelaNN//matricular_aluno.html', aluno=sel)

        @app.route('/alterar_aluno', methods=['POST', 'GET'])
        @check_logged_in_d
        def alterar_aluno():
            sel = ''
            if request.method == "POST" and request.form.get('idt') is None:
                idtSerie = request.form['select']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno WHERE serie_aluno=%s ORDER BY serie_aluno;"
                cs = mysql.consultar(comando, [int(idtSerie)])

                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, serie_aluno, turma_aluno,
                     mao_aluno, sangue_aluno] in cs:
                    sel += f"""<tr style="height: 43px;">
                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_aluno}</td>
                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{serie_aluno}º ano </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{turma_aluno} </td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt" name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is None:
                idtAluno = request.form['idt']
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno WHERE idt_aluno=%s;"
                cs = mysql.consultar(comando, [int(idtAluno)])

                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, serie_aluno, turma_aluno,
                     mao_aluno, sangue_aluno] in cs:
                    selectSerie = f"""<select name="serie" id="serie" class="u-border-1 u-border-grey-30 u-input u-input-rectangle"  autofocus="autofocus">
                                                                      <option value="{serie_aluno}">Série/Ano</option>
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
                                                                        <optionvalue="{turma_aluno}">Turma</option>
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
                comando = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, serie_aluno=%s, turma_aluno=%s, nasc_aluno=%s, mao_aluno=%s, sangue_aluno=%s WHERE idt_aluno=%s;"
                cs2 = mysql.executar(comando, [nme, matricula, serie, turma, data, mao, sangue, idtAluno])
            return render_template('Primeira_TelaNN//alterar_aluno.html', aluno=sel)

        @app.route('/incluir_disc', methods=['POST', 'GET'])
        @check_logged_in_d
        def incluir_disc():
            if request.method == 'POST':
                nme_disciplina = request.form['disciplina']
                mysql = bd.SQL()
                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = "INSERT INTO tb_disciplina(nme_disciplina) values(%s);"

                mysql.executar(comando, [nme_disciplina])
            return render_template('Primeira_TelaNN//incluir_disc.html')


app = Flask(__name__)
app.secret_key = "SenhaSecreta"
app.permanent_session_lifetime = timedelta(minutes=60)
AjudaProf()
if __name__ == '__main__':
    app.run(debug=True)
